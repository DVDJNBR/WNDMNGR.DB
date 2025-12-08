"""
ETL Step 6: Load data to Azure SQL Database from GitHub Actions
- Truncates existing tables in correct order (respects FK constraints)
- Loads GOLD CSV files from Azure Blob Storage
- Validates data integrity (Silver-Gold reconciliation, UUIDs, FKs)
- Tracks ingestion version with validation results
"""

import os
import sys
import time
import json
import pyodbc
import pandas as pd
from io import BytesIO
from pathlib import Path
from loguru import logger
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from typing import cast

# Load environment variables
load_dotenv()

# Configuration
AZURE_SQL_CONNECTION_STRING = os.getenv('AZURE_SQL_CONNECTION_STRING')
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = 'windmanager-data'
BLOB_PREFIX = 'gold/'

# GitHub Actions context (optional)
GITHUB_ACTOR = os.getenv('GITHUB_ACTOR', 'local-user')
GITHUB_SHA = os.getenv('GITHUB_SHA', None)

# Validate required environment variables
if not AZURE_SQL_CONNECTION_STRING:
    logger.error("Missing AZURE_SQL_CONNECTION_STRING environment variable")
    sys.exit(1)
if not AZURE_STORAGE_CONNECTION_STRING:
    logger.error("Missing AZURE_STORAGE_CONNECTION_STRING environment variable")
    sys.exit(1)

# Tables to load (order matters for FK constraints)
# CRITICAL: Reference tables MUST be loaded BEFORE tables that reference them
TABLES = [
    # 1. Reference tables (no dependencies)
    ('farm_types.csv', 'farm_types'),
    ('company_roles.csv', 'company_roles'),
    ('person_roles.csv', 'person_roles'),

    # 2. Entity tables (reference farm_types)
    ('persons.csv', 'persons'),
    ('companies.csv', 'companies'),
    ('farms.csv', 'farms'),

    # 3. Relationship tables (reference persons, companies, farms, roles)
    ('farm_referents.csv', 'farm_referents'),
    ('farm_company_roles.csv', 'farm_company_roles'),

    # 4. Look-up tables (reference farms)
    ('farm_administrations.csv', 'farm_administrations'),
    ('farm_environmental_installations.csv', 'farm_environmental_installations'),
    ('farm_locations.csv', 'farm_locations'),
    ('farm_om_contracts.csv', 'farm_om_contracts'),
    ('farm_tcma_contracts.csv', 'farm_tcma_contracts'),
    ('farm_turbine_details.csv', 'farm_turbine_details'),
    # Note: farm_financial_guarantees excluded due to poor data quality

    # 5. Grid infrastructure (reference farms)
    ('substations.csv', 'substations'),

    # 6. Wind turbine generators (reference farms and substations)
    ('wind_turbine_generators.csv', 'wind_turbine_generators'),
]


def get_next_version_number(cursor):
    """Get the next version number for ingestion"""
    cursor.execute("SELECT ISNULL(MAX(version_number), 0) + 1 FROM ingestion_versions")
    return cursor.fetchone()[0]


def create_ingestion_version(cursor, conn, version_number, triggered_by, commit_sha):
    """Create a new ingestion version record"""
    cursor.execute("""
        INSERT INTO ingestion_versions (
            version_number, ingestion_source, triggered_by, commit_sha, status
        ) VALUES (?, 'github-actions', ?, ?, 'in_progress')
    """, version_number, triggered_by, commit_sha)
    conn.commit()
    cursor.execute("SELECT id FROM ingestion_versions WHERE version_number = ?", version_number)
    return cursor.fetchone()[0]


def update_ingestion_version(cursor, conn, version_id, **kwargs):
    """Update ingestion version with results"""
    set_clauses = []
    values = []
    for key, value in kwargs.items():
        set_clauses.append(f"{key} = ?")
        values.append(value)

    query = f"UPDATE ingestion_versions SET {', '.join(set_clauses)} WHERE id = ?"
    values.append(version_id)
    cursor.execute(query, *values)
    conn.commit()


def truncate_tables(cursor, conn):
    """Truncate all data tables in reverse order (respects FK constraints)"""
    logger.info("Truncating existing tables...")

    for csv_file, table_name in reversed(TABLES):
        try:
            cursor.execute(f"DELETE FROM {table_name}")
            row_count = cursor.rowcount
            logger.info(f"  ✓ Cleared {table_name} ({row_count} rows deleted)")
        except Exception as e:
            logger.warning(f"  ⚠ Could not clear {table_name}: {e}")

    conn.commit()
    logger.success("All tables cleared")


def download_csv_from_blob(blob_service_client, csv_file):
    """Download CSV file from Azure Blob Storage"""
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    blob_client = container_client.get_blob_client(f"{BLOB_PREFIX}{csv_file}")

    try:
        blob_data = blob_client.download_blob()
        csv_content = blob_data.readall()
        return pd.read_csv(BytesIO(csv_content), encoding='utf-8')
    except Exception as e:
        logger.error(f"Failed to download {csv_file}: {e}")
        return None


def load_table(cursor, conn, df, table_name):
    """Load dataframe into SQL table"""
    # Remove 'id' column if present (IDENTITY columns managed by SQL Server)
    if 'id' in df.columns:
        df = df.drop(columns=['id'])

    # Replace NaN with None (NULL) - must use replace for proper conversion
    df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None})
    # Also convert remaining NaN values
    df = df.where(pd.notna(df), None)

    # Insert rows
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['?'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    inserted = 0
    for _, row in df.iterrows():
        try:
            # Convert row values to list and replace any remaining NaN
            values = [None if pd.isna(v) else v for v in row.values]
            cursor.execute(insert_query, *values)
            inserted += 1
        except Exception as e:
            logger.error(f"Failed to insert row into {table_name}: {e}")
            logger.debug(f"Row data: {row.to_dict()}")

    conn.commit()
    return inserted


def validate_silver_gold_reconciliation(blob_service_client):
    """Validate that Silver and Gold row counts match for key tables"""
    logger.info("Validating Silver-Gold reconciliation...")

    validation_errors = []

    # Tables to check (Silver filename -> expected Gold filename)
    reconciliation_tables = {
        'silver/database_sheet.csv': 'gold/farms.csv',  # 1:1 mapping
        'silver/dbwtg_sheet.csv': 'gold/wind_turbine_generators.csv',  # 1:1 mapping
        'silver/dbgrid_sheet.csv': 'gold/substations.csv',  # 1:1 mapping
    }

    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    for silver_file, gold_file in reconciliation_tables.items():
        try:
            # Download and count rows
            silver_blob = container_client.get_blob_client(silver_file)
            silver_df = pd.read_csv(BytesIO(silver_blob.download_blob().readall()))
            silver_count = len(silver_df)

            gold_blob = container_client.get_blob_client(gold_file)
            gold_df = pd.read_csv(BytesIO(gold_blob.download_blob().readall()))
            gold_count = len(gold_df)

            if silver_count != gold_count:
                error = f"{silver_file} ({silver_count} rows) != {gold_file} ({gold_count} rows)"
                validation_errors.append(error)
                logger.warning(f"  ⚠ {error}")
            else:
                logger.success(f"  ✓ {silver_file} ({silver_count}) == {gold_file} ({gold_count})")

        except Exception as e:
            error = f"Failed to validate {silver_file} -> {gold_file}: {e}"
            validation_errors.append(error)
            logger.error(f"  ✗ {error}")

    return len(validation_errors) == 0, validation_errors


def validate_uuid_integrity(cursor):
    """Validate that all UUIDs are valid and unique"""
    logger.info("Validating UUID integrity...")

    validation_errors = []

    # Tables with UUIDs
    uuid_tables = {
        'persons': 'uuid',
        'companies': 'uuid',
        'farms': 'uuid',
        'substations': 'uuid',
        'wind_turbine_generators': 'uuid',
    }

    for table, uuid_col in uuid_tables.items():
        try:
            # Check for NULL UUIDs
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {uuid_col} IS NULL")
            null_count = cursor.fetchone()[0]
            if null_count > 0:
                error = f"{table}.{uuid_col}: {null_count} NULL values"
                validation_errors.append(error)
                logger.warning(f"  ⚠ {error}")

            # Check for duplicate UUIDs
            cursor.execute(f"""
                SELECT {uuid_col}, COUNT(*) as cnt
                FROM {table}
                GROUP BY {uuid_col}
                HAVING COUNT(*) > 1
            """)
            duplicates = cursor.fetchall()
            if duplicates:
                error = f"{table}.{uuid_col}: {len(duplicates)} duplicate UUIDs"
                validation_errors.append(error)
                logger.warning(f"  ⚠ {error}")

            if null_count == 0 and not duplicates:
                logger.success(f"  ✓ {table}.{uuid_col} is valid")

        except Exception as e:
            error = f"Failed to validate {table}.{uuid_col}: {e}"
            validation_errors.append(error)
            logger.error(f"  ✗ {error}")

    return len(validation_errors) == 0, validation_errors


def validate_foreign_keys(cursor):
    """Validate foreign key relationships"""
    logger.info("Validating foreign key relationships...")

    validation_errors = []

    # Key FK relationships to check
    fk_checks = [
        ('farm_referents', 'farm_uuid', 'farms', 'uuid'),
        ('farm_referents', 'person_uuid', 'persons', 'uuid'),
        ('farm_company_roles', 'farm_uuid', 'farms', 'uuid'),
        ('farm_company_roles', 'company_uuid', 'companies', 'uuid'),
        ('wind_turbine_generators', 'farm_uuid', 'farms', 'uuid'),
        ('wind_turbine_generators', 'substation_uuid', 'substations', 'uuid'),
        ('substations', 'farm_uuid', 'farms', 'uuid'),
    ]

    for child_table, child_col, parent_table, parent_col in fk_checks:
        try:
            # Find orphaned records
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM {child_table} c
                WHERE c.{child_col} IS NOT NULL
                AND NOT EXISTS (
                    SELECT 1 FROM {parent_table} p WHERE p.{parent_col} = c.{child_col}
                )
            """)
            orphan_count = cursor.fetchone()[0]

            if orphan_count > 0:
                error = f"{child_table}.{child_col} -> {parent_table}.{parent_col}: {orphan_count} orphaned records"
                validation_errors.append(error)
                logger.warning(f"  ⚠ {error}")
            else:
                logger.success(f"  ✓ {child_table}.{child_col} -> {parent_table}.{parent_col}")

        except Exception as e:
            error = f"Failed to validate FK {child_table}.{child_col}: {e}"
            validation_errors.append(error)
            logger.error(f"  ✗ {error}")

    return len(validation_errors) == 0, validation_errors


def validate_required_fields(cursor):
    """Validate that required fields are populated"""
    logger.info("Validating required fields...")

    validation_errors = []

    # Critical fields that should not be NULL
    required_fields = [
        ('persons', 'first_name'),
        ('persons', 'last_name'),
        ('companies', 'name'),
        ('farms', 'spv'),
        ('farms', 'project'),
        ('farms', 'code'),
        ('wind_turbine_generators', 'serial_number'),
        ('wind_turbine_generators', 'farm_uuid'),
    ]

    for table, field in required_fields:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {field} IS NULL OR {field} = ''")
            null_count = cursor.fetchone()[0]

            if null_count > 0:
                error = f"{table}.{field}: {null_count} NULL/empty values"
                validation_errors.append(error)
                logger.warning(f"  ⚠ {error}")
            else:
                logger.success(f"  ✓ {table}.{field} is populated")

        except Exception as e:
            error = f"Failed to validate {table}.{field}: {e}"
            validation_errors.append(error)
            logger.error(f"  ✗ {error}")

    return len(validation_errors) == 0, validation_errors


def connect_with_retry(connection_string, max_retries=3, retry_delay=30):
    """Connect to Azure SQL with retry logic for cold starts"""
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Connection attempt {attempt}/{max_retries}...")
            conn = pyodbc.connect(connection_string, timeout=60)
            logger.success("✓ Connected to Azure SQL Database")
            return conn
        except Exception as e:
            if attempt < max_retries:
                logger.warning(f"⚠ Connection failed: {e}")
                logger.info(f"Retrying in {retry_delay} seconds (Azure SQL may be in cold start)...")
                time.sleep(retry_delay)
            else:
                logger.error(f"✗ Failed to connect after {max_retries} attempts: {e}")
                raise
    # This line should never be reached due to the raise above
    raise RuntimeError("Connection retry logic failed unexpectedly")


def main():
    """Main ingestion process"""
    start_time = time.time()

    logger.info("=" * 80)
    logger.info("ETL STEP 6: LOAD DATA TO AZURE SQL (GITHUB ACTIONS)")
    logger.info("=" * 80)

    # Connect to Azure SQL with retry logic
    logger.info("Connecting to Azure SQL Database...")
    try:
        conn = connect_with_retry(AZURE_SQL_CONNECTION_STRING)
        cursor = conn.cursor()
    except Exception as e:
        logger.error(f"✗ Failed to connect to database: {e}")
        sys.exit(1)

    # Get next version number and create ingestion record
    version_number = get_next_version_number(cursor)
    version_id = create_ingestion_version(cursor, conn, version_number, GITHUB_ACTOR, GITHUB_SHA)
    logger.info(f"Starting ingestion version {version_number} (ID: {version_id})")

    try:
        # Step 1: Truncate existing tables
        truncate_tables(cursor, conn)

        # Step 2: Connect to Azure Blob Storage
        logger.info("Connecting to Azure Blob Storage...")
        blob_service_client = BlobServiceClient.from_connection_string(cast(str, AZURE_STORAGE_CONNECTION_STRING))
        logger.success("✓ Connected to Azure Blob Storage")

        # Step 3: Load all tables
        logger.info("Loading GOLD data into Azure SQL...")
        total_rows = 0
        tables_loaded = 0

        for csv_file, table_name in TABLES:
            logger.info(f"Loading {csv_file} -> {table_name}...")

            # Download CSV from blob
            df = download_csv_from_blob(blob_service_client, csv_file)

            if df is None:
                logger.warning(f"  ⚠ Skipped {csv_file} (not found or failed to download)")
                continue

            # Load into database
            rows_inserted = load_table(cursor, conn, df, table_name)
            total_rows += rows_inserted
            tables_loaded += 1

            logger.success(f"  ✓ {table_name}: {rows_inserted} rows inserted")

        logger.success(f"Loaded {tables_loaded} tables with {total_rows} total rows")

        # Step 4: Run validation tests
        logger.info("=" * 80)
        logger.info("Running validation tests...")
        logger.info("=" * 80)

        all_validation_errors = []

        # Test 1: Silver-Gold reconciliation
        test_silver_gold, errors = validate_silver_gold_reconciliation(blob_service_client)
        all_validation_errors.extend(errors)

        # Test 2: UUID integrity
        test_uuid, errors = validate_uuid_integrity(cursor)
        all_validation_errors.extend(errors)

        # Test 3: Foreign key relationships
        test_fk, errors = validate_foreign_keys(cursor)
        all_validation_errors.extend(errors)

        # Test 4: Required fields
        test_required, errors = validate_required_fields(cursor)
        all_validation_errors.extend(errors)

        # Overall validation result
        validation_passed = test_silver_gold and test_uuid and test_fk and test_required

        if validation_passed:
            logger.success("✓ All validation tests passed!")
        else:
            logger.warning(f"⚠ Validation completed with {len(all_validation_errors)} errors")

        # Step 5: Update ingestion version with results
        execution_time = int(time.time() - start_time)

        update_ingestion_version(
            cursor, conn, version_id,
            status='completed',
            tables_affected=tables_loaded,
            total_rows_inserted=total_rows,
            execution_time_seconds=execution_time,
            validation_passed=1 if validation_passed else 0,
            test_silver_gold_reconciliation=1 if test_silver_gold else 0,
            test_uuid_integrity=1 if test_uuid else 0,
            test_foreign_keys=1 if test_fk else 0,
            test_required_fields=1 if test_required else 0,
            validation_errors=json.dumps(all_validation_errors) if all_validation_errors else None
        )

        logger.info("=" * 80)
        logger.success(f"✓ Ingestion version {version_number} completed successfully")
        logger.info(f"Tables loaded: {tables_loaded}")
        logger.info(f"Total rows: {total_rows}")
        logger.info(f"Execution time: {execution_time}s")
        logger.info(f"Validation: {'PASSED' if validation_passed else 'FAILED'}")
        logger.info("=" * 80)

    except Exception as e:
        # Update ingestion version with error
        execution_time = int(time.time() - start_time)
        error_message = str(e)

        update_ingestion_version(
            cursor, conn, version_id,
            status='failed',
            execution_time_seconds=execution_time,
            error_message=error_message
        )

        logger.error(f"✗ Ingestion failed: {e}")
        sys.exit(1)

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()

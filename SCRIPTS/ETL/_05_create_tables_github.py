"""
Create SQL tables in Azure SQL Database from SQL files
Executed by GitHub Actions workflow
"""

import os
import sys
import time
import pyodbc
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
AZURE_SQL_CONNECTION_STRING = os.getenv('AZURE_SQL_CONNECTION_STRING')
FORCE_RECREATE = os.getenv('FORCE_RECREATE', 'false').lower() == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')

# Validate required environment variables
if not AZURE_SQL_CONNECTION_STRING:
    logger.error("Missing AZURE_SQL_CONNECTION_STRING environment variable")
    sys.exit(1)

# Base directory (repository root)
BASE_DIR = Path(__file__).parent.parent.parent

# SQL scripts directory
TABLES_DIR = BASE_DIR / 'TABLES'

# Order of execution (respects dependencies)
SQL_SCRIPT_CATEGORIES = [
    '01_REFERENCES',      # Reference tables (farm_types, roles, etc.)
    '01_METADATA',        # Metadata tables (ingestion_versions)
    '02_ENTITIES',        # Core entities (persons, companies, farms, etc.)
    '03_RELATIONSHIPS',   # Junction tables (farm_referents, farm_company_roles)
    '04_LOOK_UPS',        # Lookup tables (administrations, locations, contracts, etc.)
    '05_FOREIGN_KEYS',    # Foreign key constraints
]


def execute_sql_script(cursor, conn, sql_file):
    """Execute a SQL script file"""
    logger.info(f"Executing {sql_file.name}...")

    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Split by GO statements (SQL Server batch separator)
        batches = [batch.strip() for batch in sql_content.split('GO') if batch.strip()]

        for i, batch in enumerate(batches, 1):
            # Skip comments-only batches
            if not batch or batch.startswith('--'):
                continue

            try:
                cursor.execute(batch)
                conn.commit()
            except pyodbc.Error as e:
                # Check if error is "object already exists"
                if 'already an object' in str(e) or 'already exists' in str(e):
                    if FORCE_RECREATE:
                        logger.warning(f"  ⚠️  Object exists, will be recreated (batch {i})")
                    else:
                        logger.warning(f"  ⚠️  Object already exists, skipping (batch {i})")
                        continue
                else:
                    logger.error(f"  ✗ Error in batch {i}: {e}")
                    raise

        logger.success(f"  ✓ {sql_file.name} executed successfully")
        return True

    except Exception as e:
        logger.error(f"  ✗ Failed to execute {sql_file.name}: {e}")
        return False


def drop_table_if_exists(cursor, conn, table_name):
    """Drop a table if it exists (for force recreate)"""
    try:
        cursor.execute(f"""
            IF OBJECT_ID('{table_name}', 'U') IS NOT NULL
                DROP TABLE {table_name}
        """)
        conn.commit()
        logger.info(f"  Dropped table {table_name}")
    except Exception as e:
        logger.warning(f"  Could not drop {table_name}: {e}")


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
    """Main table creation process"""
    logger.info("=" * 80)
    logger.info(f"CREATE TABLES IN AZURE SQL - ENVIRONMENT: {ENVIRONMENT.upper()}")
    logger.info("=" * 80)

    if FORCE_RECREATE:
        logger.warning("⚠️  FORCE_RECREATE is enabled - existing tables will be dropped")

    # Connect to Azure SQL with retry logic
    logger.info("Connecting to Azure SQL Database...")
    try:
        conn = connect_with_retry(AZURE_SQL_CONNECTION_STRING)
        cursor = conn.cursor()
    except Exception as e:
        logger.error(f"✗ Failed to connect to database: {e}")
        sys.exit(1)

    total_scripts = 0
    successful_scripts = 0
    failed_scripts = 0

    try:
        # Execute SQL scripts in order
        for category in SQL_SCRIPT_CATEGORIES:
            category_dir = TABLES_DIR / category

            if not category_dir.exists():
                logger.warning(f"Category directory not found: {category}")
                continue

            logger.info(f"\n{'='*80}")
            logger.info(f"Category: {category}")
            logger.info(f"{'='*80}")

            # Get all .sql files in this category
            sql_files = sorted(category_dir.glob('*.sql'))

            if not sql_files:
                logger.info(f"No SQL files found in {category}")
                continue

            for sql_file in sql_files:
                total_scripts += 1

                # If force recreate, drop table first (only for table creation scripts)
                if FORCE_RECREATE and category in ['00_REFERENCE', '01_METADATA', '02_ENTITIES', '03_RELATIONSHIPS', '04_LOOKUPS']:
                    table_name = sql_file.stem  # Assumes filename = table name
                    drop_table_if_exists(cursor, conn, table_name)

                # Execute the script
                if execute_sql_script(cursor, conn, sql_file):
                    successful_scripts += 1
                else:
                    failed_scripts += 1

        logger.info("\n" + "=" * 80)
        logger.info("SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total scripts: {total_scripts}")
        logger.success(f"Successful: {successful_scripts}")
        if failed_scripts > 0:
            logger.error(f"Failed: {failed_scripts}")
        logger.info("=" * 80)

        if failed_scripts > 0:
            logger.error("✗ Table creation completed with errors")
            sys.exit(1)
        else:
            logger.success("✓ All tables created successfully")

    except Exception as e:
        logger.error(f"✗ Fatal error during table creation: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()

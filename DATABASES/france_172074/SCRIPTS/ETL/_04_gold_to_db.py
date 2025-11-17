from pathlib import Path
import sys
import pyodbc
import petl as etl
import pandas as pd
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database helper
sys.path.insert(0, str(Path(__file__).parent.parent / 'SETUP'))
from ensure_database import ensure_database_exists  # type: ignore

# Configuration from .env
SERVER = os.getenv('SERVER_NAME')
DATABASE = os.getenv('DATABASE_NAME')
USER = os.getenv('SQL_LOGIN_USER')
PASSWORD = os.getenv('SQL_LOGIN_PASSWORD')
DRIVER = '{ODBC Driver 17 for SQL Server}'

# Validate required environment variables
if not all([SERVER, DATABASE, USER, PASSWORD]):
    logger.error("Missing required environment variables (SERVER_NAME, DATABASE_NAME, SQL_LOGIN_USER, SQL_LOGIN_PASSWORD)")
    exit(1)

# Type narrowing for Pylance
assert SERVER is not None
assert DATABASE is not None
assert USER is not None
assert PASSWORD is not None

# Ensure database exists before proceeding (auto-create enabled for invoke)
if not ensure_database_exists(SERVER, DATABASE, DRIVER, USER, PASSWORD, auto_create=True):
    exit(1)

# Paths (invoke's root path indication)
root_path = Path(__file__).parent.parent.parent.parent.parent
gold_dir = root_path / 'DATABASES' / 'france_172074' / 'DATA' / 'GOLD'

# Connection string with SQL Server authentication
connection_string = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD};Encrypt=no;'

# Check for truncate flag
truncate_mode = '--truncate' in sys.argv

# Tables to migrate (order matters for foreign keys)
# NOTE: Reference tables (farm_types, company_roles, person_roles) have fixed values
# defined in their SQL creation scripts and should NOT be migrated from CSV
TABLES = [
    # Entity tables
    ('persons.csv', 'persons'),
    ('companies.csv', 'companies'),
    ('farms.csv', 'farms'),
    # Relationship tables
    ('farm_referents.csv', 'farm_referents'),
    ('farm_company_roles.csv', 'farm_company_roles'),
    # Look-up tables
    ('farm_administrations.csv', 'farm_administrations'),
    ('farm_environmental_installations.csv', 'farm_environmental_installations'),
    ('farm_financial_guarantees.csv', 'farm_financial_guarantees'),
    ('farm_locations.csv', 'farm_locations'),
    ('farm_om_contracts.csv', 'farm_om_contracts'),
]

logger.info(f"Connecting to {SERVER}/{DATABASE}...")

with pyodbc.connect(connection_string) as conn:
    logger.success("Connected to database")

    # Clear tables if requested (use DELETE to handle FK constraints)
    if truncate_mode:
        logger.warning("Truncate mode: clearing all data tables...")
        cursor = conn.cursor()
        for _, table_name in reversed(TABLES):  # Reverse order for FK constraints
            cursor.execute(f"DELETE FROM {table_name}")
            logger.info(f"Cleared {table_name}")
        conn.commit()
        logger.success("All tables cleared")

    for csv_file, table_name in TABLES:
        csv_path = gold_dir / csv_file

        if not csv_path.exists():
            logger.warning(f"File not found: {csv_path}")
            continue

        logger.info(f"Migrating {csv_file} → {table_name}...")

        # Load CSV with PETL (UTF-8 encoding)
        table_data = etl.fromcsv(str(csv_path), encoding='utf-8')

        # Remove 'id' column if present (IDENTITY columns managed by SQL Server)
        if 'id' in etl.fieldnames(table_data):
            table_data = etl.cutout(table_data, 'id')

        # Convert empty strings to None (NULL) for all fields
        def empty_to_none(v):
            return None if v == '' else v

        table_data = etl.convertall(table_data, empty_to_none)

        # Convert float booleans (like 1.0, 0.0) to integers for BIT columns
        def float_to_int(v):
            if v is None or v == '':
                return None
            try:
                f = float(v)
                return int(f) if not pd.isna(f) else None
            except (ValueError, TypeError):
                return v

        # Apply to BIT columns if this is farm_administrations
        if table_name == 'farm_administrations' and 'has_remit_subscription' in etl.fieldnames(table_data):
            table_data = etl.convert(table_data, 'has_remit_subscription', float_to_int)

        # Get row count
        row_count = etl.nrows(table_data)

        if truncate_mode:
            # Simple insert after truncate
            etl.todb(table_data, conn, table_name, schema='dbo')
            logger.success(f"{table_name}: {row_count} rows inserted")
        else:
            # Upsert mode: check for existing UUIDs and update/insert accordingly
            cursor = conn.cursor()
            inserted = 0
            updated = 0

            for row in etl.dicts(table_data):
                # Get UUID column (varies by table)
                uuid_col = next((k for k in row.keys() if 'uuid' in k.lower()), None)

                if uuid_col and row[uuid_col]:
                    # Check if record exists
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {uuid_col} = ?", row[uuid_col])
                    result = cursor.fetchone()
                    exists = result[0] > 0 if result else False

                    if exists:
                        # Update existing record
                        set_clause = ', '.join([f"{k} = ?" for k in row.keys() if k != uuid_col])
                        values = [v for k, v in row.items() if k != uuid_col] + [row[uuid_col]]
                        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {uuid_col} = ?", *values)
                        updated += 1
                    else:
                        # Insert new record
                        cols = ', '.join(row.keys())
                        placeholders = ', '.join(['?'] * len(row))
                        cursor.execute(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})", *row.values())
                        inserted += 1
                else:
                    # No UUID - just insert (for reference tables or relationships)
                    cols = ', '.join(row.keys())
                    placeholders = ', '.join(['?'] * len(row))
                    try:
                        cursor.execute(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})", *row.values())
                        inserted += 1
                    except pyodbc.IntegrityError:
                        # Duplicate - skip
                        pass

            conn.commit()
            logger.success(f"{table_name}: {inserted} inserted, {updated} updated")

logger.success("All tables migrated successfully")
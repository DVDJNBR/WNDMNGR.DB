from pathlib import Path
import pyodbc
import petl as etl
from loguru import logger

# Configuration
SERVER = 'FRAMGNB107'
DATABASE = 'windmanager_france_test'
DRIVER = '{ODBC Driver 17 for SQL Server}'

# Paths
gold_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'GOLD'

# Connection string with Microsoft Entra authentication
connection_string = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

# Tables to migrate (order matters for foreign keys)
TABLES = [
    # Reference tables first
    ('farm_types.csv', 'farm_types'),
    ('company_roles.csv', 'company_roles'),
    ('person_roles.csv', 'person_roles'),
    # Entity tables
    ('persons.csv', 'persons'),
    ('farms.csv', 'farms'),
    # Relationship tables last
    ('farm_referents.csv', 'farm_referents'),
]

logger.info(f"Connecting to {SERVER}/{DATABASE}...")

with pyodbc.connect(connection_string) as conn:
    logger.success("Connected to database")

    # Delete existing data in reverse order (relationships → entities → references)
    logger.info("Cleaning existing data...")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.farm_referents")
    cursor.execute("DELETE FROM dbo.farms")
    cursor.execute("DELETE FROM dbo.persons")
    cursor.execute("DELETE FROM dbo.person_roles")
    cursor.execute("DELETE FROM dbo.company_roles")
    cursor.execute("DELETE FROM dbo.farm_types")
    cursor.commit()
    logger.success("Existing data cleaned")

    for csv_file, table_name in TABLES:
        csv_path = gold_dir / csv_file

        if not csv_path.exists():
            logger.warning(f"File not found: {csv_path}")
            continue

        logger.info(f"Migrating {csv_file} → {table_name}...")

        # Load CSV with PETL
        table_data = etl.fromcsv(str(csv_path))

        # Remove 'id' column if present (IDENTITY columns managed by SQL Server)
        if 'id' in etl.fieldnames(table_data):
            table_data = etl.cutout(table_data, 'id')

        # Get row count
        row_count = etl.nrows(table_data)

        # Insert data using PETL
        etl.todb(table_data, conn, table_name, schema='dbo')

        logger.success(f"{table_name}: {row_count} rows migrated")

logger.success("All tables migrated successfully")
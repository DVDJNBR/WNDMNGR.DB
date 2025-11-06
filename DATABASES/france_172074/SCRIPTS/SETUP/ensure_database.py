import pyodbc
import sys
from loguru import logger

def ensure_database_exists(server: str, database: str, driver: str = '{ODBC Driver 17 for SQL Server}', auto_create: bool = False) -> bool:
    """
    Check if database exists, create if needed.

    Args:
        server: SQL Server instance
        database: Database name
        driver: ODBC driver
        auto_create: If True, create without prompt. If False, prompt user.

    Returns True if database is ready, False otherwise.
    """
    # Connect to master to check/create database
    master_conn_str = f'DRIVER={driver};SERVER={server};DATABASE=master;Trusted_Connection=yes;TrustServerCertificate=yes;'

    try:
        with pyodbc.connect(master_conn_str) as conn:
            cursor = conn.cursor()

            # Check if database exists
            cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{database}'")
            exists = cursor.fetchone() is not None

            if exists:
                logger.info(f"Database '{database}' exists")
                return True

            # Database doesn't exist
            logger.warning(f"Database '{database}' does not exist on server '{server}'")

            # Auto-create or prompt
            should_create = auto_create
            if not auto_create:
                response = input(f"Do you want to create database '{database}'? (yes/no): ").strip().lower()
                should_create = response in ['yes', 'y', 'oui', 'o']

            if should_create:
                logger.info(f"Creating database '{database}'...")
                # CREATE DATABASE must run in autocommit mode (not in transaction)
                conn.autocommit = True
                # Use UTF-8 collation for proper accent handling
                cursor.execute(f"CREATE DATABASE [{database}] COLLATE French_CI_AS")
                logger.success(f"Database '{database}' created successfully with French_CI_AS collation")
                return True
            else:
                logger.error(f"Database creation declined. Cannot proceed.")
                return False

    except pyodbc.Error as ex:
        logger.error(f"Database check/creation failed: {ex}")
        return False

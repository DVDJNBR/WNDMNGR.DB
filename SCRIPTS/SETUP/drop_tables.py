import pyodbc
from loguru import logger
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERVER = os.getenv('SERVER_NAME')
DATABASE = os.getenv('DATABASE_NAME')
USER = os.getenv('SQL_LOGIN_USER')
PASSWORD = os.getenv('SQL_LOGIN_PASSWORD')

# Validate required environment variables
if not all([SERVER, DATABASE, USER, PASSWORD]):
    logger.error("Missing required environment variables (SERVER_NAME, DATABASE_NAME, SQL_LOGIN_USER, SQL_LOGIN_PASSWORD)")
    exit(1)

# Type narrowing for Pylance
assert SERVER is not None
assert DATABASE is not None
assert USER is not None
assert PASSWORD is not None

try:
    with pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER};DATABASE={DATABASE};'
        f'UID={USER};PWD={PASSWORD};Encrypt=no;'
    ).cursor() as cur:
        
        logger.info("Starting database cleanup...")
        
        # 1. Supprimer toutes les foreign keys
        logger.info("Dropping all foreign keys...")
        cur.execute("""
            DECLARE @sql NVARCHAR(MAX) = '';
            SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id)) + '.' + 
                        QUOTENAME(OBJECT_NAME(parent_object_id)) + 
                        ' DROP CONSTRAINT ' + QUOTENAME(name) + ';'
        FROM sys.foreign_keys;
            EXEC sp_executesql @sql;
        """)
        cur.commit()
        logger.success("All foreign keys dropped")
        
        # 2. Supprimer toutes les tables
        logger.info("Dropping all tables...")
        cur.execute("""
            DECLARE @sql NVARCHAR(MAX) = '';
            SELECT @sql += 'DROP TABLE ' + QUOTENAME(TABLE_SCHEMA) + '.' + QUOTENAME(TABLE_NAME) + ';'
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo';
            EXEC sp_executesql @sql;
        """)
        cur.commit()
        logger.success("All tables dropped")
        
        logger.success("Database cleanup completed successfully!")
        
except Exception as e:
    logger.error(f"Database cleanup failed: {e}")
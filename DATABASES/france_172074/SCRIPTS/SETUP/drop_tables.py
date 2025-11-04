import pyodbc
from loguru import logger
from pathlib import Path

SERVER = 'FRAMGNB107'
DATABASE = 'windmanager_france_test'

try:
    with pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER};DATABASE={DATABASE};'
        f'Trusted_Connection=yes;TrustServerCertificate=yes;'
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
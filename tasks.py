from invoke import task  # type: ignore
from pathlib import Path
from loguru import logger

###################
### SETUP TASKS ###
###################

@task
def init_db(c):
    """Initialize tables for France_172074 database"""
    logger.info("Script initialization")
    c.run(f"python {Path('DATABASES/france_172074/scripts/setup') / 'init_database.py'}")
    logger.success("France_172074 database initialized")

@task
def drop_db(c):
    """Drop all tables for France_172074 database"""
    logger.info("Script initialization")
    c.run(f"python {Path('DATABASES/france_172074/scripts/setup') / 'drop_tables.py'}")
    logger.warning("France_172074 database cleaned")

@task(drop_db, init_db)
def reset_db(c):
    """Drop and recreate database"""
    logger.warning("Database reset complete!")

#################
### ETL TASKS ###
#################

@task
def raw_to_bronze(c):
    """Extract Excel sheets to BRONZE layer"""
    logger.info("Extracting Excel to BRONZE...")
    c.run(f"python {Path('DATABASES/france_172074/scripts/etl') / '_01_raw_to_bronze.py'}")
    logger.success("Excel extracted to BRONZE!")

@task
def bronze_to_silver(c):
    """Clean and transform BRONZE to SILVER layer"""
    logger.info("Cleaning data from BRONZE to SILVER...")
    c.run(f"python {Path('DATABASES/france_172074/scripts/etl') / '_02_bronze_to_silver.py'}")
    logger.success("Data cleaned and saved to SILVER!")

@task
def silver_to_gold(c):
    """Transform SILVER to GOLD layer (dedupe, entities, relations)"""
    logger.info("Transforming SILVER to GOLD...")
    c.run(f"python {Path('DATABASES/france_172074/scripts/etl') / '_03_silver_to_gold.py'}")
    logger.success("Data transformed and saved to GOLD!")

@task
def gold_to_db(c):
    """Migrate GOLD data to SQL Server database"""
    logger.info("Migrating GOLD to database...")
    c.run(f"python {Path('DATABASES/france_172074/scripts/etl') / '_04_gold_to_db.py'}")
    logger.success("Data migrated to database!")

@task(raw_to_bronze, bronze_to_silver, silver_to_gold)
def etl_pipeline(c):
    """Run complete ETL pipeline (Bronze → Silver → Gold)"""
    logger.success("🎉 Full ETL pipeline complete!")

@task(raw_to_bronze, bronze_to_silver, silver_to_gold, gold_to_db)
def etl_full(c):
    """Run complete ETL pipeline including DB migration (Bronze → Silver → Gold → DB)"""
    logger.success("🎉 Full ETL pipeline with DB migration complete!")

##################
### FULL SETUP ###
##################

@task(reset_db, etl_pipeline)
def full_setup(c):
    """Complete setup: reset DB + run full ETL pipeline"""
    logger.success("🚀 Full setup complete: DB ready + data loaded!")
from invoke import task  # type: ignore
from pathlib import Path
from loguru import logger

###################
### SETUP TASKS ###
###################

@task
def setup_db(c):
    """Initialize database structure (tables, FKs)"""
    logger.info("Setting up database structure...")
    c.run(f"python {Path('SCRIPTS/SETUP') / 'init_database.py'}")
    logger.success("Database structure ready")

@task
def drop_db(c):
    """Drop all tables (dev only - use SSMS for prod!)"""
    logger.warning("Dropping all tables...")
    c.run(f"python {Path('SCRIPTS/SETUP') / 'drop_tables.py'}")
    logger.warning("All tables dropped")

@task(drop_db, setup_db)
def reset_db(c):
    """Drop and recreate database structure (dev/debug only)"""
    logger.warning("Database reset complete!")

@task
def wipe_and_reload(c):
    """DELETE all data and reload from GOLD (dev/debug - structure intact)"""
    logger.warning("Wiping all data and reloading from GOLD...")
    c.run(f"python {Path('SCRIPTS/ETL') / '_04_gold_to_db.py'} --truncate")
    logger.success("Data wiped and reloaded!")

@task
def ingest_data(c):
    """Load/update data from GOLD (upsert - no deletion)"""
    logger.info("Ingesting data from GOLD layer...")
    c.run(f"python {Path('SCRIPTS/ETL') / '_04_gold_to_db.py'}")
    logger.success("Data ingested from GOLD!")

#################
### ETL TASKS ###
#################

@task
def raw_to_bronze(c):
    """Extract Excel sheets to BRONZE layer"""
    logger.info("Extracting Excel to BRONZE...")
    c.run(f"python {Path('SCRIPTS/ETL') / '_01_raw_to_bronze.py'}")
    logger.success("Excel extracted to BRONZE!")

@task
def bronze_to_silver(c):
    """Clean and transform BRONZE to SILVER layer"""
    logger.info("Cleaning data from BRONZE to SILVER...")
    c.run(f"python {Path('SCRIPTS/ETL') / '_02_bronze_to_silver.py'}")
    logger.success("Data cleaned and saved to SILVER!")

@task
def validate_silver(c):
    """Validate SILVER data quality (BRONZE → SILVER)"""
    logger.info("Validating SILVER data quality...")
    c.run(f"python {Path('SCRIPTS/TESTS') / 'validate_bronze_to_silver.py'}")
    logger.success("SILVER data validation complete!")

@task
def silver_to_gold(c):
    """Transform SILVER to GOLD layer (dedupe, entities, relations)"""
    logger.info("Transforming SILVER to GOLD...")
    c.run(f"python {Path('SCRIPTS/ETL') / '_03_silver_to_gold.py'}")
    logger.success("Data transformed and saved to GOLD!")

@task
def validate_gold(c):
    """Validate GOLD data quality with random sampling tests"""
    logger.info("Validating GOLD data quality...")
    c.run(f"python {Path('SCRIPTS/TESTS') / 'validate_silver_to_gold.py'}")
    logger.success("GOLD data validation complete!")

@task(raw_to_bronze, bronze_to_silver, validate_silver, silver_to_gold, validate_gold)
def etl_pipeline(c):
    """Run ETL pipeline to GOLD layer with validation"""
    logger.success("[OK] ETL pipeline to GOLD complete!")

@task(etl_pipeline, ingest_data)
def etl_ingest(c):
    """Run ETL pipeline + ingest/update data (upsert - prod safe)"""
    logger.success("[OK] ETL pipeline + data ingestion complete!")

@task(etl_pipeline, wipe_and_reload)
def etl_wipe(c):
    """Run ETL pipeline + wipe and reload all data (dev only)"""
    logger.warning("[OK] ETL pipeline + data wipe complete!")

@task(reset_db, etl_pipeline, ingest_data)
def etl_full(c):
    """Full rebuild: reset DB structure + ETL + load (dev only)"""
    logger.warning("[OK] Full ETL pipeline with DB reset complete!")

#####################
### FULL PIPELINE ###
#####################

@task(setup_db, etl_pipeline, ingest_data)
def full_setup(c):
    """Initial setup: create DB structure + ETL + load data (first time)"""
    logger.success("🚀 Initial setup complete: DB ready + data loaded!")
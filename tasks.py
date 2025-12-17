from invoke import task  # type: ignore
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
import os
import requests
import time
import urllib3

# Disable SSL warnings (corporate proxy)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env
load_dotenv()

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

@task
def validate_lookups(c):
    """Validate lookup tables (farm_statuses, farm_substation_details, etc.)"""
    logger.info("Validating lookup tables...")
    c.run(f"python {Path('SCRIPTS/TESTS') / 'validate_lookup_tables.py'}")
    logger.success("Lookup tables validation complete!")

@task
def upload_gold_to_blob(c):
    """Upload GOLD CSV files to Azure Blob Storage"""
    logger.info("Uploading GOLD CSVs to Azure Blob Storage...")
    c.run(f"python {Path('SCRIPTS/ETL') / '_04_gold_to_blob.py'}")
    logger.success("GOLD files uploaded to Azure Blob!")

@task(raw_to_bronze, bronze_to_silver, validate_silver, silver_to_gold, validate_gold)
def etl_pipeline(c):
    """Run ETL pipeline to GOLD layer with validation"""
    logger.success("[OK] ETL pipeline to GOLD complete!")

@task(etl_pipeline, upload_gold_to_blob)
def etl_to_blob(c):
    """Run ETL pipeline + upload GOLD to Azure Blob"""
    logger.success("[OK] ETL pipeline + GOLD uploaded to blob!")

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

#############################
### GITHUB ACTIONS TASKS ###
#############################

def _get_github_headers():
    """Get GitHub API headers with authentication"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        logger.error("✗ GITHUB_TOKEN not found in .env file")
        raise ValueError("Missing GITHUB_TOKEN in .env")
    return {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

def _trigger_workflow(workflow_file, inputs=None):
    """Trigger a GitHub Actions workflow via API"""
    owner = os.getenv('GITHUB_REPO_OWNER', 'DVDJNBR')
    repo = os.getenv('GITHUB_REPO_NAME', 'WNDMNGR.DB')

    # Get current branch
    import subprocess
    try:
        current_branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
    except:
        current_branch = 'main'

    url = f'https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches'

    payload = {
        'ref': current_branch,
        'inputs': inputs or {}
    }

    try:
        response = requests.post(url, json=payload, headers=_get_github_headers(), verify=False)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"✗ API request failed: {e}")
        return False

def _get_workflow_runs(workflow_file, limit=5):
    """Get recent workflow runs"""
    owner = os.getenv('GITHUB_REPO_OWNER', 'DVDJNBR')
    repo = os.getenv('GITHUB_REPO_NAME', 'WNDMNGR.DB')

    url = f'https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/runs'

    try:
        response = requests.get(url, headers=_get_github_headers(), params={'per_page': limit}, verify=False)
        response.raise_for_status()
        return response.json()['workflow_runs']
    except requests.exceptions.RequestException as e:
        logger.error(f"✗ Failed to get workflow runs: {e}")
        return []

def _wait_for_workflow_completion(workflow_file, timeout=600):
    """Wait for the most recent workflow run to complete

    Args:
        workflow_file: The workflow filename (e.g., 'create-tables.yml')
        timeout: Maximum time to wait in seconds (default: 10 minutes)

    Returns:
        True if workflow completed successfully, False otherwise
    """
    start_time = time.time()
    check_interval = 10  # Check every 10 seconds

    logger.info(f"Polling workflow status every {check_interval} seconds (timeout: {timeout}s)...")

    while time.time() - start_time < timeout:
        runs = _get_workflow_runs(workflow_file, limit=1)

        if not runs:
            logger.warning("No workflow runs found, waiting...")
            time.sleep(check_interval)
            continue

        latest_run = runs[0]
        status = latest_run['status']
        conclusion = latest_run.get('conclusion')

        if status == 'completed':
            if conclusion == 'success':
                logger.success(f"✓ Workflow completed successfully!")
                return True
            else:
                logger.error(f"✗ Workflow failed with conclusion: {conclusion}")
                logger.error(f"   → {latest_run['html_url']}")
                return False

        elapsed = int(time.time() - start_time)
        logger.info(f"⏳ Workflow status: {status} (elapsed: {elapsed}s)")
        time.sleep(check_interval)

    logger.error(f"✗ Workflow timed out after {timeout} seconds")
    return False

@task
def gh_create_tables(c, force=False):
    """Trigger GitHub Actions workflow to create tables in Azure SQL

    Args:
        force: Force recreate tables (DANGEROUS - drops existing tables)
    """
    logger.info("Triggering 'Create Tables' workflow...")

    inputs = {
        'force_recreate': 'true' if force else 'false'
    }

    if _trigger_workflow('create-tables.yml', inputs):
        logger.success("✓ Workflow triggered!")
        logger.info("Check status: https://github.com/DVDJNBR/WNDMNGR.DB/actions")
        logger.info("Wait for completion before running gh-load-data")
    else:
        logger.error("✗ Failed to trigger workflow")

@task
def gh_load_data(c):
    """Trigger GitHub Actions workflow to load data to Azure SQL

    Note: Tables must be created first (run gh-create-tables)
    """
    logger.info("Triggering 'Load Database' workflow...")

    if _trigger_workflow('load-database.yml'):
        logger.success("✓ Workflow triggered!")
        logger.info("Monitor: https://github.com/DVDJNBR/WNDMNGR.DB/actions")
    else:
        logger.error("✗ Failed to trigger workflow")

@task
def gh_watch(c, workflow=None):
    """Watch GitHub Actions workflow runs

    Args:
        workflow: Specific workflow name (create-tables or load-database), or all if not specified
    """
    workflow_file = f"{workflow}.yml" if workflow else None

    if workflow_file:
        logger.info(f"Recent runs for {workflow}:")
        runs = _get_workflow_runs(workflow_file, limit=5)
    else:
        logger.info("Fetching recent workflow runs...")
        # Get runs for both workflows
        create_runs = _get_workflow_runs('create-tables.yml', limit=3)
        load_runs = _get_workflow_runs('load-database.yml', limit=3)
        runs = create_runs + load_runs
        runs = sorted(runs, key=lambda x: x['created_at'], reverse=True)[:10]

    if not runs:
        logger.warning("No workflow runs found")
        return

    for run in runs:
        status_icon = {
            'completed': '✅' if run['conclusion'] == 'success' else '❌',
            'in_progress': '⏳',
            'queued': '⏸️'
        }.get(run['status'], '❓')

        logger.info(f"{status_icon} [{run['name']}] {run['status']} - {run['created_at']}")
        logger.info(f"   → {run['html_url']}")

@task
def gh_deploy(c, force=False):
    """Deploy to Azure SQL via GitHub Actions (create tables + load data)

    Args:
        force: Force recreate tables (DANGEROUS)

    This runs workflows SEQUENTIALLY: create tables first, then waits for completion before loading data.
    """
    logger.info("🚀 Starting GitHub Actions deployment...")

    # Step 1: Trigger create tables
    logger.info("Step 1/2: Creating tables...")
    gh_create_tables(c, force=force)

    # Step 2: Wait for create-tables to complete
    logger.info("Waiting for 'Create Tables' workflow to complete...")
    if not _wait_for_workflow_completion('create-tables.yml', timeout=600):
        logger.error("✗ Create Tables workflow failed or timed out")
        logger.error("Cannot proceed with data loading. Fix the issue and try again.")
        return

    logger.success("✓ Tables created successfully!")

    # Step 3: Trigger load data
    logger.info("Step 2/2: Loading data...")
    gh_load_data(c)

    logger.success("🚀 Deployment workflows triggered!")
    logger.info("Monitor final status: python -m invoke gh-watch")
    logger.info("Or visit: https://github.com/DVDJNBR/WNDMNGR.DB/actions")

###########################
### SUPABASE TASKS ########
###########################

@task
def sql_to_db(c):
    """ETL Step 4: SQL to DB (Trigger GitHub Actions to setup database structure)"""
    logger.info("ETL STEP 4: SQL to DB (Setup database structure)")
    c.run(f"python {Path('SCRIPTS/ETL') / '_04_sql_to_db.py'}")

@task
def csv_to_db(c, truncate=False):
    """ETL Step 5: CSV to DB (Load GOLD data to Supabase)"""
    logger.info("ETL STEP 5: CSV to DB (Load data)")
    cmd = f"python {Path('SCRIPTS/ETL') / '_05_csv_to_db.py'}"
    if truncate:
        cmd += " --truncate"
    c.run(cmd)

@task(raw_to_bronze, bronze_to_silver, silver_to_gold)
def etl_to_gold(c):
    """Run ETL pipeline to GOLD layer (no database operations)"""
    logger.success("[OK] ETL pipeline to GOLD complete!")

@task(etl_to_gold, sql_to_db)
def supabase_setup(c):
    """Complete Supabase setup: ETL to GOLD then SQL to DB (structure only)

    Workflow:
    1. ETL: Excel to BRONZE to SILVER to GOLD (local)
    2. GitHub Actions: Upload SQL + Execute (create tables)
    """
    logger.info("=" * 80)
    logger.success("ETL + Database structure setup complete!")
    logger.info("Next: Run 'invoke csv-to-db' to load data")
    logger.info("=" * 80)

@task(etl_to_gold, sql_to_db, csv_to_db)
def supabase_full(c):
    """Complete Supabase pipeline: ETL to GOLD then SQL and CSV to DB

    Full workflow:
    1. ETL: Excel to BRONZE to SILVER to GOLD (local)
    2. SQL to DB: Setup structure (GitHub Actions)
    3. CSV to DB: Load data (Supabase API)
    """
    logger.info("=" * 80)
    logger.success("COMPLETE SUPABASE PIPELINE DONE!")
    logger.success("Structure created + Data loaded")
    logger.info("=" * 80)

@task(etl_to_blob)
def full_deploy(c, force=False):
    """Complete pipeline: ETL local → Upload blob → Deploy to Azure SQL

    Args:
        force: Force recreate tables (DANGEROUS)

    This is the COMPLETE workflow:
    1. ETL: Excel (P:\\) → BRONZE → SILVER → GOLD (local)
    2. Upload GOLD CSVs to Azure Blob Storage
    3. GitHub Actions: Create tables + Load data to Azure SQL

    Use this for end-to-end deployment from Excel to Azure SQL.
    """
    logger.info("=" * 80)
    logger.info("FULL DEPLOYMENT PIPELINE")
    logger.info("=" * 80)
    logger.success("✓ ETL completed and GOLD uploaded to blob")
    logger.info("Starting GitHub Actions deployment...")
    gh_deploy(c, force=force)
    logger.success("=" * 80)
    logger.success("✓ FULL DEPLOYMENT COMPLETE!")
    logger.success("=" * 80)
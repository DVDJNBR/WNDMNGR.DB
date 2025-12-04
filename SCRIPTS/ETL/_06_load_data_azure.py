"""
ETL Step 6: Load data to Azure SQL Database
Calls the Azure Function 'LoadData' to load all GOLD CSV files from Blob Storage
"""

import requests
import os
import time
import warnings
from loguru import logger

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Azure Function configuration (DEPRECATED - use GitHub Actions instead)
BASE_URL = 'https://func-windmanager-france-database-amcrfpd8bbgngbhm.francecentral-01.azurewebsites.net'
FUNCTION_KEY = os.getenv('AZURE_FUNCTION_KEY')

if not FUNCTION_KEY:
    print("ERROR: This script is deprecated. Use GitHub Actions workflow 'load-database.yml' instead.")
    exit(1)

def wake_up_database():
    """Wake up Azure SQL database by calling test-sql (handles auto-pause)"""

    test_url = f"{BASE_URL}/api/test-sql"
    logger.info("Waking up Azure SQL database...")

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_attempts}: Testing database connection...")
            response = requests.get(test_url, timeout=120, verify=False)

            if response.status_code == 200:
                logger.success("✓ Database is awake and ready!")
                return True
            else:
                logger.warning(f"Got HTTP {response.status_code}, retrying in 5s...")
                time.sleep(5)

        except requests.exceptions.Timeout:
            logger.warning("Timeout (database waking up), retrying in 5s...")
            time.sleep(5)
        except Exception as e:
            logger.warning(f"Error: {str(e)}, retrying in 5s...")
            time.sleep(5)

    logger.error("Failed to wake up database after 3 attempts")
    return False

def load_data_azure():
    """Call Azure Function to load all GOLD data into Azure SQL"""

    logger.info("=" * 80)
    logger.info("ETL STEP 6: LOAD DATA TO AZURE SQL")
    logger.info("=" * 80)

    # Step 1: Wake up the database first
    if not wake_up_database():
        logger.error("Cannot proceed without database connection")
        exit(1)

    # Step 2: Load data
    load_url = f"{BASE_URL}/api/load-data?code={FUNCTION_KEY}"
    logger.info(f"Calling Azure Function: {load_url}")
    logger.info("This may take several minutes...")

    try:
        response = requests.get(
            load_url,
            timeout=600,  # 10 minutes timeout
            verify=False
        )

        if response.status_code == 200:
            logger.success(f"✓ {response.text}")
        else:
            logger.error(f"✗ HTTP {response.status_code}: {response.text}")
            exit(1)

    except requests.exceptions.Timeout:
        logger.error("✗ Request timeout (10 minutes)")
        logger.info("Check Azure Function logs for more details")
        exit(1)
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
        exit(1)

    logger.info("=" * 80)
    logger.success("✓ Data loaded successfully to Azure SQL")
    logger.info("=" * 80)

if __name__ == '__main__':
    load_data_azure()

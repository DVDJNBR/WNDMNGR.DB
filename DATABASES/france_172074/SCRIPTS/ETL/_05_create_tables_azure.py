"""
ETL Step 5: Create SQL tables in Azure SQL Database
Calls the Azure Function 'CreateTables' to execute SQL scripts from Blob Storage
"""

import requests
import os
from loguru import logger

# Azure Function configuration (DEPRECATED - use GitHub Actions instead)
FUNCTION_URL = 'https://func-windmanager-france-database-amcrfpd8bbgngbhm.francecentral-01.azurewebsites.net/api/create-tables'
FUNCTION_KEY = os.getenv('AZURE_FUNCTION_KEY')

if not FUNCTION_KEY:
    print("ERROR: This script is deprecated. Use GitHub Actions workflow 'create-tables.yml' instead.")
    exit(1)

def create_tables_azure():
    """Call Azure Function to create all SQL tables"""

    logger.info("=" * 80)
    logger.info("ETL STEP 5: CREATE TABLES IN AZURE SQL")
    logger.info("=" * 80)

    logger.info(f"Calling Azure Function: {FUNCTION_URL}")

    try:
        response = requests.get(
            f"{FUNCTION_URL}?code={FUNCTION_KEY}",
            timeout=300,  # 5 minutes timeout
            verify=False  # Disable SSL verification for Azure
        )

        if response.status_code == 200:
            logger.success(f"✓ {response.text}")
        else:
            logger.error(f"✗ HTTP {response.status_code}: {response.text}")
            exit(1)

    except requests.exceptions.Timeout:
        logger.error("✗ Request timeout (5 minutes)")
        exit(1)
    except Exception as e:
        logger.error(f"✗ Error: {str(e)}")
        exit(1)

    logger.info("=" * 80)
    logger.success("✓ Tables created successfully in Azure SQL")
    logger.info("=" * 80)

if __name__ == '__main__':
    create_tables_azure()

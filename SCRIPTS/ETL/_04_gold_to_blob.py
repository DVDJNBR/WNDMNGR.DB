"""
ETL Step 4: Upload GOLD CSV files to Azure Blob Storage
"""

import os
from azure.storage.blob import BlobServiceClient
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv
from typing import cast

# Load environment variables
load_dotenv()

# Configuration
STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT')
STORAGE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_KEY')
CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER')

if not all([STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY, CONTAINER_NAME]):
    logger.error("Missing required environment variables: AZURE_STORAGE_ACCOUNT, AZURE_STORAGE_KEY, AZURE_STORAGE_CONTAINER")
    exit(1)

# Type narrowing for Pylance
assert STORAGE_ACCOUNT_NAME is not None
assert STORAGE_ACCOUNT_KEY is not None
assert CONTAINER_NAME is not None

# Paths
BASE_DIR = Path(__file__).parent.parent.parent  # SCRIPTS/ETL/ -> root
GOLD_DIR = BASE_DIR / 'DATA' / 'GOLD'

def upload_gold_to_blob():
    """Upload all GOLD CSV files to Azure Blob Storage"""

    logger.info("=" * 80)
    logger.info("ETL STEP 4: GOLD → AZURE BLOB STORAGE")
    logger.info("=" * 80)

    # Connect to Blob Storage
    logger.info(f"Connecting to Azure Blob Storage: {STORAGE_ACCOUNT_NAME}")
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(cast(str, CONTAINER_NAME))

    # Get all CSV files
    csv_files = sorted(GOLD_DIR.glob('*.csv'))
    logger.info(f"Found {len(csv_files)} CSV files in GOLD directory")

    uploaded_count = 0
    total_size = 0

    for csv_file in csv_files:
        blob_name = f"gold/{csv_file.name}"
        blob_client = container_client.get_blob_client(blob_name)

        with open(csv_file, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)

        file_size = csv_file.stat().st_size
        total_size += file_size
        logger.success(f"✓ {csv_file.name:<40} → gold/{csv_file.name} ({file_size / 1024:>8.2f} KB)")
        uploaded_count += 1

    logger.info("=" * 80)
    logger.success(f"✓ Uploaded {uploaded_count} files ({total_size / 1024:.2f} KB total)")
    logger.info("=" * 80)

if __name__ == '__main__':
    upload_gold_to_blob()

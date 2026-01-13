"""
ETL STEP 5: Wipe Database (OPTIONAL)
Wipe all data from Supabase database in reverse dependency order
Use this before loading data to ensure a clean slate
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from loguru import logger
import ssl
import urllib3
import httpx

# Disable SSL warnings for corporate proxy
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Load environment
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_API_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("Missing SUPABASE_URL or SUPABASE_API_KEY in .env")
    sys.exit(1)

# Ensure URL ends with /
if not SUPABASE_URL.endswith('/'):
    SUPABASE_URL = SUPABASE_URL + '/'

# Create httpx client with SSL verification disabled (corporate proxy)
http_client = httpx.Client(verify=False)

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Patch PostgREST session to use custom httpx client
if hasattr(supabase.postgrest, 'session'):
    supabase.postgrest.session = http_client

# Load order from _06_csv_to_db.py (must match for consistency)
LOAD_ORDER = [
    ('farm_types', 'farm_types.csv'),
    ('company_roles', 'company_roles.csv'),
    ('person_roles', 'person_roles.csv'),
    ('companies', 'companies.csv'),
    ('persons', 'persons.csv'),
    ('ice_detection_systems', 'ice_detection_systems.csv'),
    ('farms', 'farms.csv'),
    ('wind_turbine_generators', 'wind_turbine_generators.csv'),
    ('substations', 'substations.csv'),
    ('employees', 'employees.csv'),
    ('farm_company_roles', 'farm_company_roles.csv'),
    ('farm_referents', 'farm_referents.csv'),
    ('farm_administrations', 'farm_administrations.csv'),
    ('farm_environmental_installations', 'farm_environmental_installations.csv'),
    ('farm_financial_guarantees', 'farm_financial_guarantees.csv'),
    ('farm_locations', 'farm_locations.csv'),
    ('farm_om_contracts', 'farm_om_contracts.csv'),
    ('farm_tcma_contracts', 'farm_tcma_contracts.csv'),
    ('farm_statuses', 'farm_statuses.csv'),
    ('farm_substation_details', 'farm_substation_details.csv'),
    ('farm_turbine_details', 'farm_turbine_details.csv'),
    ('farm_ice_detection_systems', 'farm_ice_detection_systems.csv'),
]

# Map table names to the column to use for deletion (must be non-null)
# 'id' -> .neq('id', -1)
# 'uuid' -> .neq('uuid', '00000000-0000-0000-0000-000000000000')
# 'farm_uuid' -> .neq('farm_uuid', '00000000-0000-0000-0000-000000000000')

DELETE_KEYS = {
    'farm_types': 'id',
    'company_roles': 'id',
    'person_roles': 'id',
    'companies': 'uuid',
    'persons': 'uuid',
    'ice_detection_systems': 'uuid',
    'farms': 'uuid',
    'wind_turbine_generators': 'uuid',
    'substations': 'uuid',
    'employees': 'uuid',
    
    # All other farm_* tables usually have farm_uuid
    'farm_company_roles': 'farm_uuid',
    'farm_referents': 'farm_uuid',
    'farm_administrations': 'farm_uuid',
    'farm_environmental_installations': 'farm_uuid',
    'farm_financial_guarantees': 'farm_uuid',
    'farm_locations': 'farm_uuid',
    'farm_om_contracts': 'farm_uuid',
    'farm_tcma_contracts': 'farm_uuid',
    'farm_statuses': 'farm_uuid',
    'farm_substation_details': 'farm_uuid',
    'farm_turbine_details': 'wind_farm_uuid',  # Special case: uses wind_farm_uuid
    'farm_ice_detection_systems': 'farm_uuid',
}

def wipe_data():
    """Wipe all data from Supabase in reverse dependency order"""
    logger.warning("=" * 80)
    logger.warning("ETL STEP 5: WIPE DATABASE")
    logger.warning("=" * 80)
    logger.warning("⚠ Deleting all data in reverse dependency order")
    logger.warning("")

    # Process in reverse order (Children first, then parents)
    wipe_order = reversed(LOAD_ORDER)

    success_count = 0
    failed_count = 0

    for table_name, _ in wipe_order:
        key = DELETE_KEYS.get(table_name, 'id')  # Default to id

        try:
            if key == 'id':
                supabase.table(table_name).delete().neq('id', -1).execute()
            elif key == 'uuid':
                supabase.table(table_name).delete().neq('uuid', '00000000-0000-0000-0000-000000000000').execute()
            elif key == 'farm_uuid':
                supabase.table(table_name).delete().neq('farm_uuid', '00000000-0000-0000-0000-000000000000').execute()
            elif key == 'wind_farm_uuid':
                supabase.table(table_name).delete().neq('wind_farm_uuid', '00000000-0000-0000-0000-000000000000').execute()
            else:
                # Fallback
                supabase.table(table_name).delete().neq(key, -1).execute()

            logger.success(f"  ✓ {table_name} wiped")
            success_count += 1

        except Exception as e:
            logger.error(f"  ✗ Failed to wipe {table_name}: {str(e)[:150]}")
            failed_count += 1

    logger.info("")
    logger.warning("=" * 80)
    logger.warning("WIPE COMPLETE")
    logger.warning("=" * 80)
    logger.info(f"✓ Success: {success_count}/{len(LOAD_ORDER)}")
    logger.info(f"✗ Failed: {failed_count}/{len(LOAD_ORDER)}")
    logger.warning("=" * 80)

    if failed_count > 0:
        logger.error("Some tables failed to wipe - database may be in inconsistent state")
        sys.exit(1)

if __name__ == '__main__':
    wipe_data()
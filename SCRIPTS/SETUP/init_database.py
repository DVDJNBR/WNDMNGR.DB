import pyodbc
from loguru import logger
from pathlib import Path
from ensure_database import ensure_database_exists
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERVER = os.getenv('SERVER_NAME')
DATABASE = os.getenv('DATABASE_NAME')
USER = os.getenv('SQL_LOGIN_USER')
PASSWORD = os.getenv('SQL_LOGIN_PASSWORD')
DRIVER = '{ODBC Driver 17 for SQL Server}'

# Validate required environment variables
if not all([SERVER, DATABASE, USER, PASSWORD]):
    logger.error("Missing required environment variables (SERVER_NAME, DATABASE_NAME, SQL_LOGIN_USER, SQL_LOGIN_PASSWORD)")
    exit(1)

# Type narrowing for Pylance
assert SERVER is not None
assert DATABASE is not None
assert USER is not None
assert PASSWORD is not None

# Ensure database exists before proceeding (auto-create enabled for invoke)
if not ensure_database_exists(SERVER, DATABASE, DRIVER, USER, PASSWORD, auto_create=True):
    exit(1)

base_path = Path(__file__).parent.parent.parent
tables_path = base_path / 'TABLES'
references =  tables_path / '01_REFERENCES'
entities = tables_path / '02_ENTITIES'
relationships = tables_path / '03_RELATIONSHIPS'
look_ups = tables_path / '04_LOOK_UPS'
foreign_keys = tables_path / '05_FOREIGN_KEYS'


try:
    with pyodbc.connect(
        f'DRIVER={DRIVER};'
        f'SERVER={SERVER};DATABASE={DATABASE};'
        f'UID={USER};PWD={PASSWORD};Encrypt=no;'
    ).cursor() as cur:
        logger.success("Database connection established")
        ### REFERENCES
        cur.execute((references / 'company_roles.sql').read_text())
        logger.info('company_roles ensured')
        cur.execute((references / 'farm_types.sql').read_text())
        logger.info('farm_types ensured')
        cur.execute((references / 'person_roles.sql').read_text())
        logger.info('person_roles ensured')

        ### ENTITIES
        cur.execute((entities / 'companies.sql').read_text())
        logger.info('companies ensured')
        cur.execute((entities / 'employees.sql').read_text())
        logger.info('employees ensured')
        cur.execute((entities / 'farms.sql').read_text())
        logger.info('farms ensured')
        cur.execute((entities / 'ice_detection_systems.sql').read_text())
        logger.info('ice_detection_systems ensured')
        cur.execute((entities / 'persons.sql').read_text())
        logger.info('persons ensured')
        cur.execute((entities / 'substations.sql').read_text())
        logger.info('substations ensured')
        cur.execute((entities / 'wind_turbine_generators.sql').read_text())
        logger.info('wind_turbine_generators ensured')

        ### RELATIONSHIPS
        cur.execute((relationships / 'farm_company_roles.sql').read_text())
        logger.info('farm_company_roles ensured')
        cur.execute((relationships / 'farm_referents.sql').read_text())
        logger.info('farm_referents ensured')

        ### LOOK_UPS
        cur.execute((look_ups / 'farm_actual_performances.sql').read_text())
        logger.info('farm_actual_performances ensured')
        cur.execute((look_ups / 'farm_administrations.sql').read_text())
        logger.info('farm_administrations ensured')
        cur.execute((look_ups / 'farm_electrical_delegations.sql').read_text())
        logger.info('farm_electrical_delegations ensured')
        cur.execute((look_ups / 'farm_environmental_installations.sql').read_text())
        logger.info('farm_environmental_installations ensured')
        cur.execute((look_ups / 'farm_financial_guarantees.sql').read_text())
        logger.info('farm_financial_guarantees ensured')
        cur.execute((look_ups / 'farm_ice_detection_systems.sql').read_text())
        logger.info('farm_ice_detection_systems ensured')
        cur.execute((look_ups / 'farm_locations.sql').read_text())
        logger.info('farm_locations ensured')
        cur.execute((look_ups / 'farm_om_contracts.sql').read_text())
        logger.info('farm_om_contracts ensured')
        cur.execute((look_ups / 'farm_statuses.sql').read_text())
        logger.info('farm_statuses ensured')
        cur.execute((look_ups / 'farm_substation_details.sql').read_text())
        logger.info('farm_substation_details ensured')
        cur.execute((look_ups / 'farm_target_performances.sql').read_text())
        logger.info('farm_target_performances ensured')
        cur.execute((look_ups / 'farm_tcma_contracts.sql').read_text())
        logger.info('farm_tcma_contracts ensured')
        cur.execute((look_ups / 'farm_turbine_details.sql').read_text())
        logger.info('farm_turbine_details ensured')
        logger.success('All tables ready')
        ### FOREIGN KEYS
        cur.execute((foreign_keys / 'employees_fk.sql').read_text())
        logger.info('foreign keys for employees ensured')
        cur.execute((foreign_keys / 'substations_fk.sql').read_text())
        logger.info('foreign keys for substations ensured')
        cur.execute((foreign_keys / 'wind_turbine_generators_fk.sql').read_text())
        logger.info('foreign keys for wind_turbine_generators ensured')
        logger.success('All foreign keys ready')

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    logger.error(f"Database connection or query failed: {sqlstate} - {ex}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")

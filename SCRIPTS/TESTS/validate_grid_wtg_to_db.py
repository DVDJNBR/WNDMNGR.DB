"""
Validation GRID & WTG → Database
Tests de traçabilité avec random sampling pour les substations et turbines
"""

from pathlib import Path
import pandas as pd
import pyodbc
from loguru import logger
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from .env
SERVER = os.getenv('SERVER_NAME')
DATABASE = os.getenv('DATABASE_NAME')
USER = os.getenv('SQL_LOGIN_USER')
PASSWORD = os.getenv('SQL_LOGIN_PASSWORD')
DRIVER = '{ODBC Driver 17 for SQL Server}'

# Paths
silver_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'SILVER'

# Configuration
SAMPLE_SIZE = 3  # Nombre de lignes à tester au hasard
RANDOM_SEED = 42  # Pour reproductibilité

# Test counters
total_tests = 0
passed_tests = 0
failed_tests = 0


def log_test(test_name, passed, details=""):
    """Log test result avec loguru"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1

    if passed:
        passed_tests += 1
        logger.success(f"  ✓ {test_name}")
    else:
        failed_tests += 1
        logger.error(f"  ✗ {test_name}")
        if details:
            logger.error(f"    → {details}")


def validate_substation(silver_row, cursor):
    """
    Valide qu'une ligne GRID SILVER se retrouve correctement dans la DB
    """
    farm_code = silver_row['three_letter_code']
    pdl_name = silver_row['nom_du_pdl']

    logger.info(f"\n{'-'*80}")
    logger.info(f"[TRACE] Validating substation: {pdl_name} ({farm_code})")
    logger.info(f"{'-'*80}")

    # STEP 1: Vérifier que la farm existe
    logger.info("\n[1/3] Checking farm existence...")
    cursor.execute("SELECT uuid, code, project FROM farms WHERE code = ?", farm_code)
    farm = cursor.fetchone()

    log_test(
        f"Farm '{farm_code}' exists in DB",
        farm is not None,
        f"Farm not found in database"
    )

    if not farm:
        return False

    farm_uuid = farm.uuid
    logger.debug(f"   Farm UUID: {farm_uuid}, Project: {farm.project}")

    # STEP 2: Vérifier que la substation existe
    logger.info("\n[2/3] Checking substation existence...")
    cursor.execute("""
        SELECT uuid, substation_name, farm_code, gps_coordinates
        FROM substations
        WHERE farm_code = ? AND substation_name = ?
    """, farm_code, pdl_name)
    substation = cursor.fetchone()

    log_test(
        f"Substation '{pdl_name}' exists in DB",
        substation is not None,
        f"Substation not found in database"
    )

    if not substation:
        return False

    logger.debug(f"   Substation UUID: {substation.uuid}")

    # STEP 3: Vérifier les attributs
    logger.info("\n[3/3] Validating substation attributes...")

    log_test(
        f"Farm code matches: '{farm_code}'",
        substation.farm_code == farm_code,
        f"Expected '{farm_code}', got '{substation.farm_code}'"
    )

    log_test(
        f"Substation name matches: '{pdl_name}'",
        substation.substation_name == pdl_name,
        f"Expected '{pdl_name}', got '{substation.substation_name}'"
    )

    # GPS coordinates (peut être None)
    expected_gps = silver_row['coordonnees_gps'] if pd.notna(silver_row['coordonnees_gps']) else None
    actual_gps = substation.gps_coordinates

    log_test(
        f"GPS coordinates match",
        expected_gps == actual_gps,
        f"Expected '{expected_gps}', got '{actual_gps}'"
    )

    logger.success(f"✓ Substation validation complete for {pdl_name}")
    return True


def validate_turbine(silver_row, cursor):
    """
    Valide qu'une ligne WTG SILVER se retrouve correctement dans la DB
    """
    farm_code = silver_row['three_letter_code']
    serial_number = int(silver_row['wtg_serial_number']) if pd.notna(silver_row['wtg_serial_number']) else None

    if not serial_number:
        logger.warning(f"Skipping turbine with no serial number for farm {farm_code}")
        return True

    logger.info(f"\n{'-'*80}")
    logger.info(f"[TRACE] Validating turbine: Serial #{serial_number} ({farm_code})")
    logger.info(f"{'-'*80}")

    # STEP 1: Vérifier que la farm existe
    logger.info("\n[1/4] Checking farm existence...")
    cursor.execute("SELECT uuid, code, project FROM farms WHERE code = ?", farm_code)
    farm = cursor.fetchone()

    log_test(
        f"Farm '{farm_code}' exists in DB",
        farm is not None,
        f"Farm not found in database"
    )

    if not farm:
        return False

    farm_uuid = farm.uuid
    logger.debug(f"   Farm UUID: {farm_uuid}, Project: {farm.project}")

    # STEP 2: Vérifier qu'une substation existe pour cette farm
    logger.info("\n[2/4] Checking substation existence for this farm...")
    cursor.execute("SELECT uuid FROM substations WHERE farm_code = ?", farm_code)
    substation = cursor.fetchone()

    log_test(
        f"At least one substation exists for farm '{farm_code}'",
        substation is not None,
        f"No substation found for this farm"
    )

    if not substation:
        return False

    # STEP 3: Vérifier que la turbine existe
    logger.info("\n[3/4] Checking turbine existence...")
    cursor.execute("""
        SELECT uuid, serial_number, wtg_number, manufacturer, wtg_type, commercial_operation_date
        FROM wind_turbine_generators
        WHERE serial_number = ? AND farm_code = ?
    """, serial_number, farm_code)
    turbine = cursor.fetchone()

    log_test(
        f"Turbine #{serial_number} exists in DB",
        turbine is not None,
        f"Turbine not found in database"
    )

    if not turbine:
        return False

    logger.debug(f"   Turbine UUID: {turbine.uuid}")

    # STEP 4: Vérifier les attributs
    logger.info("\n[4/4] Validating turbine attributes...")

    log_test(
        f"Serial number matches: {serial_number}",
        turbine.serial_number == serial_number,
        f"Expected {serial_number}, got {turbine.serial_number}"
    )

    # WTG number (peut être None ou généré)
    expected_wtg_num = silver_row['num_wtg'] if pd.notna(silver_row['num_wtg']) else f'WTG-{serial_number}'
    log_test(
        f"WTG number matches: '{expected_wtg_num}'",
        turbine.wtg_number == expected_wtg_num,
        f"Expected '{expected_wtg_num}', got '{turbine.wtg_number}'"
    )

    # Manufacturer
    expected_manufacturer = silver_row['manufacturer'] if pd.notna(silver_row['manufacturer']) else None
    log_test(
        f"Manufacturer matches: '{expected_manufacturer}'",
        turbine.manufacturer == expected_manufacturer,
        f"Expected '{expected_manufacturer}', got '{turbine.manufacturer}'"
    )

    # WTG Type
    expected_type = silver_row['wtg_type'] if pd.notna(silver_row['wtg_type']) else None
    log_test(
        f"WTG type matches: '{expected_type}'",
        turbine.wtg_type == expected_type,
        f"Expected '{expected_type}', got '{turbine.wtg_type}'"
    )

    logger.success(f"✓ Turbine validation complete for Serial #{serial_number}")
    return True


def main():
    """Main validation function"""
    logger.info("="*80)
    logger.info("VALIDATION: GRID & WTG → Database")
    logger.info("="*80)

    # Connect to database
    connection_string = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD};Encrypt=no;'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    logger.success(f"Connected to {SERVER}/{DATABASE}")

    # Load SILVER data
    df_grid = pd.read_csv(silver_dir / 'dbgrid_sheet.csv', encoding='utf-8-sig')
    df_wtg = pd.read_csv(silver_dir / 'dbwtg_sheet.csv', encoding='utf-8-sig')

    logger.info(f"\nTotal GRID rows: {len(df_grid)}")
    logger.info(f"Total WTG rows: {len(df_wtg)}")

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST GRID (SUBSTATIONS)
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n\n" + "="*80)
    logger.info("TESTING GRID DATA (SUBSTATIONS)")
    logger.info("="*80)

    # Sample random rows
    grid_sample = df_grid.sample(n=min(SAMPLE_SIZE, len(df_grid)), random_state=RANDOM_SEED)

    for idx, row in grid_sample.iterrows():
        validate_substation(row, cursor)

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST WTG (WIND TURBINE GENERATORS)
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n\n" + "="*80)
    logger.info("TESTING WTG DATA (WIND TURBINE GENERATORS)")
    logger.info("="*80)

    # Sample random rows (filter out rows without serial number)
    wtg_with_serial = df_wtg[df_wtg['wtg_serial_number'].notna()]
    wtg_sample = wtg_with_serial.sample(n=min(SAMPLE_SIZE, len(wtg_with_serial)), random_state=RANDOM_SEED)

    for idx, row in wtg_sample.iterrows():
        validate_turbine(row, cursor)

    # ═══════════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n\n" + "="*80)
    logger.info("VALIDATION SUMMARY")
    logger.info("="*80)

    logger.info(f"Total tests run: {total_tests}")
    logger.success(f"Passed: {passed_tests}")
    if failed_tests > 0:
        logger.error(f"Failed: {failed_tests}")
    else:
        logger.success(f"Failed: {failed_tests}")

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    logger.info(f"Success rate: {success_rate:.1f}%")

    cursor.close()
    conn.close()

    if failed_tests == 0:
        logger.success("\n✓ All validation tests passed!")
        return 0
    else:
        logger.error(f"\n✗ {failed_tests} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())

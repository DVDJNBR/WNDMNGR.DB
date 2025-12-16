"""
Validation tests for lookup tables (farm_statuses, farm_substation_details, etc.)
Verifies that lookup tables have correct row counts and valid foreign keys
"""

from pathlib import Path
import pandas as pd
from loguru import logger
import sys

# Paths
root_path = Path(__file__).parent.parent.parent
silver_dir = root_path / 'DATA' / 'SILVER'
gold_dir = root_path / 'DATA' / 'GOLD'

# Test counters
total_tests = 0
passed_tests = 0
failed_tests = 0


def log_test(test_name, passed, details=""):
    """Log test result"""
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


def test_farm_statuses(df_database, df_farms, df_farm_statuses):
    """Test farm_statuses lookup table"""
    logger.info("\n" + "="*80)
    logger.info("Testing farm_statuses")
    logger.info("="*80)

    # Test 1: Row count should be <= farms (some farms may not be in database_sheet)
    log_test(
        "Row count is valid (≤ farms)",
        len(df_farm_statuses) <= len(df_farms),
        f"Expected ≤ {len(df_farms)} rows, got {len(df_farm_statuses)}"
    )

    # Log farms without status
    farms_with_status = set(df_farm_statuses['farm_code'])
    all_farms = set(df_farms['code'])
    missing_farms = all_farms - farms_with_status
    if missing_farms:
        logger.info(f"   Note: {len(missing_farms)} farms without status (not in database_sheet): {', '.join(sorted(missing_farms))}")

    # Test 2: All farm_uuids should exist in farms table
    valid_farm_uuids = set(df_farms['uuid'])
    status_farm_uuids = set(df_farm_statuses['farm_uuid'])
    invalid_uuids = status_farm_uuids - valid_farm_uuids

    log_test(
        "All farm_uuids are valid",
        len(invalid_uuids) == 0,
        f"Found {len(invalid_uuids)} invalid farm UUIDs"
    )

    # Test 3: Sample validation - pick random farm and verify status
    if len(df_database) > 0:
        sample = df_database.sample(n=min(3, len(df_database)), random_state=42)

        for _, row in sample.iterrows():
            farm_code = row['three_letter_code']
            farm = df_farms[df_farms['code'] == farm_code]

            if len(farm) == 0:
                continue

            farm_uuid = farm.iloc[0]['uuid']
            status_row = df_farm_statuses[df_farm_statuses['farm_uuid'] == farm_uuid]

            log_test(
                f"Farm {farm_code} has status entry",
                len(status_row) > 0,
                f"Missing status entry for farm {farm_code}"
            )

            if len(status_row) > 0:
                expected_wf_status = row['wf_status'] if pd.notna(row['wf_status']) else ''
                actual_wf_status = status_row.iloc[0]['farm_status']

                log_test(
                    f"Farm {farm_code} wf_status matches",
                    expected_wf_status == actual_wf_status,
                    f"Expected '{expected_wf_status}', got '{actual_wf_status}'"
                )


def test_farm_substation_details(df_database, df_farms, df_substations, df_substation_details, df_companies):
    """Test farm_substation_details lookup table"""
    logger.info("\n" + "="*80)
    logger.info("Testing farm_substation_details")
    logger.info("="*80)

    # Test 1: Row count should be <= number of farms (some farms may not have substations)
    log_test(
        "Row count is valid (≤ farms)",
        len(df_substation_details) <= len(df_farms),
        f"Expected ≤ {len(df_farms)} rows, got {len(df_substation_details)}"
    )

    # Test 2: All farm_uuids should exist in farms table
    valid_farm_uuids = set(df_farms['uuid'])
    details_farm_uuids = set(df_substation_details['farm_uuid'])
    invalid_uuids = details_farm_uuids - valid_farm_uuids

    log_test(
        "All farm_uuids are valid",
        len(invalid_uuids) == 0,
        f"Found {len(invalid_uuids)} invalid farm UUIDs"
    )

    # Test 3: All company UUIDs should exist
    valid_company_uuids = set(df_companies['uuid'])
    details_company_uuids = set(df_substation_details['substation_service_company_uuid'])
    invalid_company_uuids = details_company_uuids - valid_company_uuids

    log_test(
        "All company UUIDs are valid",
        len(invalid_company_uuids) == 0,
        f"Found {len(invalid_company_uuids)} invalid company UUIDs"
    )

    # Test 4: Verify station counts match actual substations
    for _, detail_row in df_substation_details.head(5).iterrows():
        farm_code = detail_row['farm_code']
        expected_count = detail_row['station_count']

        actual_count = len(df_substations[df_substations['farm_code'] == farm_code])

        log_test(
            f"Farm {farm_code} station count matches",
            expected_count == actual_count,
            f"Expected {expected_count} stations, found {actual_count}"
        )


def test_ice_detection_systems(df_database, df_farms, df_ice_systems, df_farm_ice_systems):
    """Test ice detection systems tables"""
    logger.info("\n" + "="*80)
    logger.info("Testing ice_detection_systems")
    logger.info("="*80)

    # Test 1: Should have at least 1 system
    log_test(
        "At least one ice detection system exists",
        len(df_ice_systems) > 0,
        "No ice detection systems found"
    )

    # Test 2: All systems should have valid boolean flags
    for _, sys in df_ice_systems.iterrows():
        log_test(
            f"System '{sys['ids_name']}' has valid flags",
            sys['automatic_stop'] in [0, 1] and sys['automatic_restart'] in [0, 1],
            f"Invalid flags: stop={sys['automatic_stop']}, restart={sys['automatic_restart']}"
        )

    # Test 3: All farm_uuids in farm_ice_systems should exist
    valid_farm_uuids = set(df_farms['uuid'])
    farm_ice_uuids = set(df_farm_ice_systems['farm_uuid'])
    invalid_uuids = farm_ice_uuids - valid_farm_uuids

    log_test(
        "All farm_uuids are valid",
        len(invalid_uuids) == 0,
        f"Found {len(invalid_uuids)} invalid farm UUIDs"
    )

    # Test 4: All ice system UUIDs should exist
    valid_ice_uuids = set(df_ice_systems['uuid'])
    farm_ice_system_uuids = set(df_farm_ice_systems['ice_detection_system_uuid'])
    invalid_ice_uuids = farm_ice_system_uuids - valid_ice_uuids

    log_test(
        "All ice detection system UUIDs are valid",
        len(invalid_ice_uuids) == 0,
        f"Found {len(invalid_ice_uuids)} invalid ice system UUIDs"
    )


def main():
    """Main validation function"""
    logger.info("=" * 80)
    logger.info("LOOKUP TABLES VALIDATION")
    logger.info("=" * 80)

    # Load data
    logger.info("\nLoading data files...")

    try:
        df_database = pd.read_csv(silver_dir / 'database_sheet.csv')
        logger.success(f"   ✓ SILVER database_sheet: {len(df_database)} rows")

        df_farms = pd.read_csv(gold_dir / 'farms.csv')
        logger.success(f"   ✓ GOLD farms: {len(df_farms)} rows")

        df_companies = pd.read_csv(gold_dir / 'companies.csv')
        logger.success(f"   ✓ GOLD companies: {len(df_companies)} rows")

        df_substations = pd.read_csv(gold_dir / 'substations.csv')
        logger.success(f"   ✓ GOLD substations: {len(df_substations)} rows")

        # Check if tables exist
        farm_statuses_path = gold_dir / 'farm_statuses.csv'
        substation_details_path = gold_dir / 'farm_substation_details.csv'
        ice_systems_path = gold_dir / 'ice_detection_systems.csv'
        farm_ice_systems_path = gold_dir / 'farm_ice_detection_systems.csv'

        has_farm_statuses = farm_statuses_path.exists()
        has_substation_details = substation_details_path.exists()
        has_ice_systems = ice_systems_path.exists()
        has_farm_ice_systems = farm_ice_systems_path.exists()

        if has_farm_statuses:
            df_farm_statuses = pd.read_csv(farm_statuses_path)
            logger.success(f"   ✓ GOLD farm_statuses: {len(df_farm_statuses)} rows")
        else:
            logger.warning(f"   ⚠ GOLD farm_statuses not found - run ETL script first")

        if has_substation_details:
            df_substation_details = pd.read_csv(substation_details_path)
            logger.success(f"   ✓ GOLD farm_substation_details: {len(df_substation_details)} rows")
        else:
            logger.warning(f"   ⚠ GOLD farm_substation_details not found - run ETL script first")

        if has_ice_systems:
            df_ice_systems = pd.read_csv(ice_systems_path)
            logger.success(f"   ✓ GOLD ice_detection_systems: {len(df_ice_systems)} rows")
        else:
            logger.warning(f"   ⚠ GOLD ice_detection_systems not found - run ETL script first")

        if has_farm_ice_systems:
            df_farm_ice_systems = pd.read_csv(farm_ice_systems_path)
            logger.success(f"   ✓ GOLD farm_ice_detection_systems: {len(df_farm_ice_systems)} rows")
        else:
            logger.warning(f"   ⚠ GOLD farm_ice_detection_systems not found - run ETL script first")

    except FileNotFoundError as e:
        logger.error(f"✗ File not found: {e}")
        logger.error("   Make sure to run the ETL script first!")
        sys.exit(1)

    # Run tests
    logger.info("\n" + "="*80)
    logger.info("STARTING VALIDATION TESTS")
    logger.info("="*80)

    if has_farm_statuses:
        test_farm_statuses(df_database, df_farms, df_farm_statuses)

    if has_substation_details:
        test_farm_substation_details(df_database, df_farms, df_substations, df_substation_details, df_companies)

    if has_ice_systems and has_farm_ice_systems:
        test_ice_detection_systems(df_database, df_farms, df_ice_systems, df_farm_ice_systems)

    # Summary
    logger.info("\n" + "="*80)
    logger.info("TEST SUMMARY")
    logger.info("="*80)

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    logger.info(f"\nStatistics:")
    logger.info(f"   Total tests run: {total_tests}")
    logger.info(f"   Tests passed: {passed_tests} ({success_rate:.1f}%)")
    logger.info(f"   Tests failed: {failed_tests}")

    if failed_tests == 0:
        logger.success("\n" + "="*80)
        logger.success("ALL VALIDATION TESTS PASSED!")
        logger.success("="*80 + "\n")
        return 0
    else:
        logger.error("\n" + "="*80)
        logger.error(f"{failed_tests} TESTS FAILED")
        logger.error("="*80 + "\n")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

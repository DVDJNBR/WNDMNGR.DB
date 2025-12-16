"""
Validation BRONZE → SILVER ETL
Tests de qualité des données et traçabilité
"""

from pathlib import Path
import pandas as pd
from loguru import logger
import sys

# Paths
bronze_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'BRONZE'
silver_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'SILVER'

# Configuration
SAMPLE_SIZE = 5  # Nombre de lignes à tracer au hasard
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


def validate_row_lineage(bronze_row, silver_row):
    """
    Validate that a BRONZE row is correctly transformed into SILVER
    """
    # Find code in BRONZE (column name contains "Abbreviation")
    code = None
    for col in bronze_row.index:
        if 'Abbreviation' in col:
            code = bronze_row[col]
            break

    if code is None:
        logger.error("[ERROR] Could not find code column in BRONZE row")
        return False

    logger.info(f"\n{'-'*80}")
    logger.info(f"[TRACE] Tracing row with code: {code}")
    logger.info(f"{'-'*80}")

    # Verify that key data is preserved
    log_test(
        f"Code preserved: '{code}'",
        silver_row['code'] == code,
        f"BRONZE: {code}, SILVER: {silver_row['code']}"
    )

    # Verify SPV (column is "Windfarm" in BRONZE)
    bronze_spv = None
    for col in bronze_row.index:
        if col == 'Windfarm':
            bronze_spv = bronze_row[col]
            break

    if bronze_spv:
        log_test(
            f"SPV preserved",
            str(silver_row['spv']).strip() == str(bronze_spv).strip(),
            f"BRONZE: '{bronze_spv}', SILVER: '{silver_row['spv']}'"
        )

    # Verify project (column is "WF common name" in BRONZE)
    bronze_project = None
    for col in bronze_row.index:
        if 'common name' in col:
            bronze_project = bronze_row[col]
            break

    if bronze_project:
        log_test(
            f"Project preserved",
            str(silver_row['project']).strip() == str(bronze_project).strip(),
            f"BRONZE: '{bronze_project}', SILVER: '{silver_row['project']}'"
        )

    # Verify farm_type (column is "Farm Type" in BRONZE)
    bronze_type = bronze_row.get('Farm Type')
    if bronze_type:
        log_test(
            f"Farm type preserved",
            str(silver_row['farm_type']).strip() == str(bronze_type).strip(),
            f"BRONZE: '{bronze_type}', SILVER: '{silver_row['farm_type']}'"
        )

    logger.success(f"[OK] Row {code} validation complete")
    return True


def main():
    """Main validation function"""

    logger.info("=" * 80)
    logger.info("BRONZE -> SILVER VALIDATION - Data Quality Tests")
    logger.info("=" * 80)

    # Load data
    logger.info("\n[LOAD] Loading data files...")

    try:
        df_bronze = pd.read_csv(bronze_dir / 'repartition_sheet.csv')
        logger.success(f"   [OK] BRONZE: {len(df_bronze)} rows, {len(df_bronze.columns)} columns")

        df_silver = pd.read_csv(silver_dir / 'repartition_sheet.csv')
        logger.success(f"   [OK] SILVER: {len(df_silver)} rows, {len(df_silver.columns)} columns")

    except FileNotFoundError as e:
        logger.error(f"[ERROR] File not found: {e}")
        logger.error("   Make sure to run the ETL scripts first!")
        sys.exit(1)

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 1: Row count preservation
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n" + "="*80)
    logger.info("TEST 1: Row Count Preservation")
    logger.info("="*80)

    log_test(
        "No rows lost in transformation",
        len(df_bronze) == len(df_silver),
        f"BRONZE: {len(df_bronze)} rows, SILVER: {len(df_silver)} rows"
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 2: Column validation
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n" + "="*80)
    logger.info("TEST 2: Column Validation")
    logger.info("="*80)

    expected_columns = [
        'owner', 'spv', 'project', 'code', 'farm_type',
        'technical_manager', 'substitute_technical_manager',
        'key_account_manager', 'substitute_key_account_manager',
        'electrical_manager', 'controller_responsible',
        'controller_deputy', 'administrative_responsible',
        'administrative_deputy'
    ]

    missing_columns = set(expected_columns) - set(df_silver.columns)
    log_test(
        "All expected columns present in SILVER",
        len(missing_columns) == 0,
        f"Missing: {missing_columns}" if missing_columns else ""
    )

    if len(missing_columns) == 0:
        logger.info(f"   [OK] Found all {len(expected_columns)} expected columns")

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 3: Data type validation
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n" + "="*80)
    logger.info("TEST 3: Data Type Validation")
    logger.info("="*80)

    # All columns should be object/string type (since we're dealing with names and codes)
    for col in expected_columns:
        if col in df_silver.columns:
            is_object = df_silver[col].dtype == 'object'
            log_test(
                f"Column '{col}' has correct type (object/string)",
                is_object,
                f"Got type: {df_silver[col].dtype}"
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 4: Value validation
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n" + "="*80)
    logger.info("TEST 4: Value Validation")
    logger.info("="*80)

    # Check farm_type values
    valid_farm_types = ['Wind', 'Solar', 'Hybrid']
    invalid_types = df_silver[~df_silver['farm_type'].isin(valid_farm_types)]['farm_type'].unique()

    log_test(
        "All farm_type values are valid (Wind/Solar/Hybrid)",
        len(invalid_types) == 0,
        f"Invalid types found: {invalid_types.tolist()}" if len(invalid_types) > 0 else ""
    )

    # Check for duplicate codes
    duplicate_codes = df_silver[df_silver['code'].duplicated()]['code'].tolist()
    log_test(
        "No duplicate farm codes",
        len(duplicate_codes) == 0,
        f"Duplicates: {duplicate_codes}" if duplicate_codes else ""
    )

    # Check for empty/null critical fields
    critical_fields = ['code', 'spv', 'project', 'farm_type']

    for field in critical_fields:
        null_count = df_silver[field].isna().sum()
        empty_count = (df_silver[field] == '').sum()

        log_test(
            f"No null/empty values in '{field}'",
            null_count == 0 and empty_count == 0,
            f"Nulls: {null_count}, Empty: {empty_count}"
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 5: Data completeness
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n" + "="*80)
    logger.info("TEST 5: Data Completeness")
    logger.info("="*80)

    # Check that each farm has at least one person assigned
    person_columns = [
        'technical_manager', 'substitute_technical_manager',
        'key_account_manager', 'substitute_key_account_manager',
        'electrical_manager', 'controller_responsible',
        'controller_deputy', 'administrative_responsible',
        'administrative_deputy'
    ]

    farms_without_persons = []
    for idx, row in df_silver.iterrows():
        has_person = False
        for col in person_columns:
            if pd.notna(row.get(col)) and row.get(col) != '':
                has_person = True
                break

        if not has_person:
            farms_without_persons.append(row['code'])

    log_test(
        "All farms have at least one person assigned",
        len(farms_without_persons) == 0,
        f"Farms without persons: {farms_without_persons}"
    )

    # Calculate completeness percentage for person columns
    for col in person_columns:
        if col in df_silver.columns:
            filled = df_silver[col].notna().sum()
            percentage = (filled / len(df_silver)) * 100
            logger.info(f"   {col}: {filled}/{len(df_silver)} ({percentage:.1f}% filled)")

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 6: Data cleaning validation
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n" + "="*80)
    logger.info("TEST 6: Data Cleaning Validation")
    logger.info("="*80)

    # Check for leading/trailing spaces in critical fields
    for field in critical_fields:
        if field in df_silver.columns:
            has_spaces = df_silver[field].astype(str).str.strip() != df_silver[field].astype(str)
            rows_with_spaces = has_spaces.sum()

            log_test(
                f"No leading/trailing spaces in '{field}'",
                rows_with_spaces == 0,
                f"Found {rows_with_spaces} rows with spaces"
            )

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 7: Random sampling - trace specific rows
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n" + "="*80)
    logger.info("TEST 7: Random Sampling - Trace Rows BRONZE → SILVER")
    logger.info("="*80)

    logger.info(f"\n[RANDOM] Random sampling: selecting {SAMPLE_SIZE} rows to trace...")

    sample_size = min(SAMPLE_SIZE, len(df_silver))
    sample_silver = df_silver.sample(n=sample_size, random_state=RANDOM_SEED)

    logger.info(f"   Selected farms: {', '.join(sample_silver['code'].tolist())}")

    # Create column mapping from BRONZE to SILVER (BRONZE columns have \n characters)
    bronze_to_silver_map = {
        'WF\nAbbreviation': 'code',
        'Windfarm': 'spv',
        'WF common name': 'project',
        'Owner of\nWF': 'owner',
        'Farm Type': 'farm_type'
    }

    # Find the actual code column in BRONZE
    code_col_bronze = None
    for col in df_bronze.columns:
        if 'Abbreviation' in col or col == 'WF\nAbbreviation':
            code_col_bronze = col
            break

    if code_col_bronze is None:
        logger.error("[ERROR] Could not find code column in BRONZE data")
    else:
        for idx, silver_row in sample_silver.iterrows():
            code = silver_row['code']

            # Find corresponding row in BRONZE using the actual column name
            bronze_match = df_bronze[df_bronze[code_col_bronze] == code]

            if len(bronze_match) == 0:
                logger.error(f"   [ERROR] Code {code} not found in BRONZE!")
                continue

            bronze_row = bronze_match.iloc[0]
            validate_row_lineage(bronze_row, silver_row)

    # Summary
    logger.info("\n\n" + "="*80)
    logger.info("TEST SUMMARY")
    logger.info("="*80)

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    logger.info(f"\n[STATS] Statistics:")
    logger.info(f"   Total tests run: {total_tests}")
    logger.info(f"   Tests passed: {passed_tests} ({success_rate:.1f}%)")
    logger.info(f"   Tests failed: {failed_tests}")

    if failed_tests == 0:
        logger.success("\n" + "="*80)
        logger.success("ALL VALIDATION TESTS PASSED!")
        logger.success("BRONZE -> SILVER transformation is VALID")
        logger.success("="*80 + "\n")
        return 0
    else:
        logger.error("\n" + "="*80)
        logger.error(f"{failed_tests} TESTS FAILED")
        logger.error("Please review the ETL transformation logic")
        logger.error("="*80 + "\n")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

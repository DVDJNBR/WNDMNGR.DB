"""
Validation SILVER → GOLD ETL
Tests de traçabilité avec random sampling (pas de données en dur!)
"""

from pathlib import Path
import pandas as pd
from loguru import logger
import sys

# Paths
silver_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'SILVER'
gold_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'GOLD'

# Configuration
SAMPLE_SIZE = 5  # Nombre de lignes à tester au hasard
RANDOM_SEED = 42  # Pour reproductibilité (optionnel)

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


def validate_farm_lineage(silver_row, df_farms, df_farm_types, df_persons, df_referents, df_person_roles):
    """
    Valide qu'une ligne SILVER se retrouve correctement dans GOLD avec toutes ses relations
    """
    farm_code = silver_row['code']

    logger.info(f"\n{'-'*80}")
    logger.info(f"[TRACE] Validating farm: {farm_code} ({silver_row['project']})")
    logger.info(f"{'-'*80}")

    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 1: Vérifier que la farm existe dans GOLD
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n[1/4] Checking farm existence in GOLD...")

    gold_farm = df_farms[df_farms['code'] == farm_code]

    log_test(
        f"Farm '{farm_code}' exists in GOLD",
        len(gold_farm) > 0,
        f"Farm not found in GOLD farms table"
    )

    if len(gold_farm) == 0:
        logger.error(f"[ERROR] Cannot continue validation for {farm_code}")
        return False

    gold_farm = gold_farm.iloc[0]
    farm_uuid = gold_farm['uuid']
    logger.debug(f"   Farm UUID: {farm_uuid}")

    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 2: Vérifier les attributs de la farm
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n[2/4] Validating farm attributes...")

    log_test(
        f"SPV matches: '{silver_row['spv']}'",
        gold_farm['spv'] == silver_row['spv'],
        f"Expected '{silver_row['spv']}', got '{gold_farm['spv']}'"
    )

    log_test(
        f"Project matches: '{silver_row['project']}'",
        gold_farm['project'] == silver_row['project'],
        f"Expected '{silver_row['project']}', got '{gold_farm['project']}'"
    )

    # Vérifier farm_type_id
    farm_type_name = silver_row['farm_type']
    farm_type = df_farm_types[df_farm_types['type_title'] == farm_type_name]

    if len(farm_type) > 0:
        expected_type_id = farm_type.iloc[0]['id']
        log_test(
            f"Farm type matches: '{farm_type_name}' (id={expected_type_id})",
            gold_farm['farm_type_id'] == expected_type_id,
            f"Expected type_id {expected_type_id}, got {gold_farm['farm_type_id']}"
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # STEP 3: Vérifier les personnes
    # ═══════════════════════════════════════════════════════════════════════════
    logger.info("\n[3/4] Validating persons...")

    person_columns = {
        'technical_manager': 'Technical Manager',
        'substitute_technical_manager': 'Substitute Technical Manager',
        'key_account_manager': 'Key Account Manager',
        'substitute_key_account_manager': 'Substitute Key Account Manager',
        'electrical_manager': 'Electrical Manager',
        'controller_responsible': 'Controller Responsible',
        'controller_deputy': 'Controller Deputy',
        'administrative_responsible': 'Administrative responsible',
        'administrative_deputy': 'Administrative Deputy'
    }

    persons_checked = 0

    for col_name, role_name in person_columns.items():
        if col_name not in silver_row.index:
            continue

        person_name = silver_row[col_name]

        if pd.isna(person_name) or person_name == '':
            continue

        logger.info(f"\n   [PERSON] Checking: {role_name} = '{person_name}'")
        persons_checked += 1

        # Parse name
        name_parts = person_name.split()
        if len(name_parts) < 2:
            logger.warning(f"      ⚠ Invalid name format, skipping")
            continue

        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])

        # Find person in GOLD
        gold_person = df_persons[
            (df_persons['first_name'] == first_name) &
            (df_persons['last_name'] == last_name)
        ]

        log_test(
            f"Person '{person_name}' exists in GOLD",
            len(gold_person) > 0,
            f"Person not found: {first_name} {last_name}"
        )

        if len(gold_person) == 0:
            continue

        person_uuid = gold_person.iloc[0]['uuid']
        logger.debug(f"      Person UUID: {person_uuid}")

        # ═══════════════════════════════════════════════════════════════════════
        # STEP 4: Vérifier la relation farm-person-role
        # ═══════════════════════════════════════════════════════════════════════

        # Get role_id
        role = df_person_roles[df_person_roles['role_name'] == role_name]

        if len(role) == 0:
            logger.error(f"      Role '{role_name}' not found in person_roles")
            continue

        role_id = role.iloc[0]['id']

        # Find relationship in farm_referents
        referent = df_referents[
            (df_referents['farm_uuid'] == farm_uuid) &
            (df_referents['person_uuid'] == person_uuid) &
            (df_referents['role_id'] == role_id)
        ]

        log_test(
            f"Relationship exists: {farm_code} ← {person_name} ← {role_name}",
            len(referent) > 0,
            f"Relationship not found in farm_referents"
        )

        # Verify farm_code consistency
        if len(referent) > 0:
            log_test(
                f"farm_code in referent table is correct",
                referent.iloc[0]['farm_code'] == farm_code,
                f"Expected '{farm_code}', got '{referent.iloc[0]['farm_code']}'"
            )

    if persons_checked == 0:
        logger.warning("   [WARNING] No persons to check for this farm")
    else:
        logger.success(f"   [OK] Checked {persons_checked} persons")

    logger.success(f"\n[OK] Farm {farm_code} validation complete")
    return True


def main():
    """Main validation function"""

    logger.info("=" * 80)
    logger.info("SILVER -> GOLD VALIDATION - Random Sampling Tests")
    logger.info("=" * 80)

    # Load data
    logger.info("\n[LOAD] Loading data files...")

    try:
        df_silver = pd.read_csv(silver_dir / 'repartition_sheet.csv')
        logger.success(f"   [OK] SILVER: {len(df_silver)} rows")

        df_farms = pd.read_csv(gold_dir / 'farms.csv')
        logger.success(f"   [OK] GOLD farms: {len(df_farms)} rows")

        df_persons = pd.read_csv(gold_dir / 'persons.csv')
        logger.success(f"   [OK] GOLD persons: {len(df_persons)} rows")

        df_farm_types = pd.read_csv(gold_dir / 'farm_types.csv')
        logger.success(f"   [OK] GOLD farm_types: {len(df_farm_types)} rows")

        df_person_roles = pd.read_csv(gold_dir / 'person_roles.csv')
        logger.success(f"   [OK] GOLD person_roles: {len(df_person_roles)} rows")

        df_referents = pd.read_csv(gold_dir / 'farm_referents.csv')
        logger.success(f"   [OK] GOLD farm_referents: {len(df_referents)} rows")

    except FileNotFoundError as e:
        logger.error(f"[ERROR] File not found: {e}")
        logger.error("   Make sure to run the ETL script first!")
        sys.exit(1)

    # ═══════════════════════════════════════════════════════════════════════════
    # Random sampling
    # ═══════════════════════════════════════════════════════════════════════════

    logger.info(f"\n[RANDOM] Random sampling: selecting {SAMPLE_SIZE} farms to validate...")

    sample_size = min(SAMPLE_SIZE, len(df_silver))
    sample = df_silver.sample(n=sample_size, random_state=RANDOM_SEED)

    logger.info(f"   Selected farms: {', '.join(sample['code'].tolist())}")

    # ═══════════════════════════════════════════════════════════════════════════
    # Validate each sampled farm
    # ═══════════════════════════════════════════════════════════════════════════

    logger.info("\n\n" + "="*80)
    logger.info("STARTING VALIDATION TESTS")
    logger.info("="*80)

    for idx, row in sample.iterrows():
        validate_farm_lineage(
            row,
            df_farms,
            df_farm_types,
            df_persons,
            df_referents,
            df_person_roles
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════════════════════════

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
        logger.success("SILVER -> GOLD transformation is VALID")
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

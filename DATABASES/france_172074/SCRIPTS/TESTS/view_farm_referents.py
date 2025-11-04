"""
Create a consolidated view of farm referents with human-readable information.
Joins farm_referents, farms, persons, and person_roles to create an easy-to-read CSV.
"""

import pandas as pd
from pathlib import Path

# Define paths
DATA_DIR = Path(__file__).parent.parent.parent / "DATA" / "GOLD"
OUTPUT_DIR = Path(__file__).parent / "DATA"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "farm_referents_view.csv"

def create_farm_referents_view():
    """
    Create a consolidated view of farm referents joining all related tables.
    Output columns: farm_code, spv, role_name, first_name, last_name
    """

    # Read all necessary CSV files
    print("Reading CSV files...")
    farm_referents = pd.read_csv(DATA_DIR / "farm_referents.csv")
    farms = pd.read_csv(DATA_DIR / "farms.csv")
    persons = pd.read_csv(DATA_DIR / "persons.csv")
    person_roles = pd.read_csv(DATA_DIR / "person_roles.csv")

    print(f"Loaded {len(farm_referents)} farm referent relationships")
    print(f"Loaded {len(farms)} farms")
    print(f"Loaded {len(persons)} persons")
    print(f"Loaded {len(person_roles)} person roles")

    # Join farm_referents with farms to get SPV and project info
    result = farm_referents.merge(
        farms[['uuid', 'spv', 'project', 'code']],
        left_on='farm_uuid',
        right_on='uuid',
        how='left',
        suffixes=('', '_farm')
    )

    # Join with persons to get names
    result = result.merge(
        persons[['uuid', 'first_name', 'last_name']],
        left_on='person_uuid',
        right_on='uuid',
        how='left',
        suffixes=('', '_person')
    )

    # Join with person_roles to get role names
    result = result.merge(
        person_roles[['id', 'role_name']],
        left_on='person_role_id',
        right_on='id',
        how='left'
    )

    # Select and order columns for final output
    final_columns = ['code', 'spv', 'project', 'role_name', 'first_name', 'last_name']
    result_final = result[final_columns].copy()

    # Sort by farm code and role name for better readability
    result_final = result_final.sort_values(['code', 'role_name'])

    # Rename columns for clarity
    result_final.columns = ['farm_code', 'spv', 'project', 'role', 'first_name', 'last_name']

    # Export to CSV
    result_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    print(f"\n[OK] Successfully created view with {len(result_final)} rows")
    print(f"[OK] Output saved to: {OUTPUT_FILE}")

    # Display sample of results
    print("\nSample of results (first 10 rows):")
    print(result_final.head(10).to_string(index=False))

    # Summary statistics
    print(f"\nSummary:")
    print(f"- Total farm-referent relationships: {len(result_final)}")
    print(f"- Unique farms: {result_final['farm_code'].nunique()}")
    print(f"- Unique roles: {result_final['role'].nunique()}")
    print(f"- Unique persons: {result_final[['first_name', 'last_name']].drop_duplicates().shape[0]}")

    # Group by role to see distribution
    print("\nReferents by role:")
    role_counts = result_final['role'].value_counts()
    for role, count in role_counts.items():
        print(f"  - {role}: {count} farms")

    return result_final

if __name__ == "__main__":
    try:
        df = create_farm_referents_view()
    except Exception as e:
        print(f"Error: {e}")
        raise

"""
Create a consolidated view of farm company roles.
Joins farm_company_roles, farms, companies, and company_roles to create an easy-to-read CSV.
"""

import pandas as pd
from pathlib import Path

# Define paths
DATA_DIR = Path(__file__).parent.parent.parent / "DATA" / "GOLD"
OUTPUT_DIR = Path(__file__).parent / "DATA"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "farm_company_roles_view.csv"

def create_farm_company_roles_view():
    """
    Create a consolidated view of farm company roles joining all related tables.
    Output columns: farm_code, spv, project, role, company_name
    """

    # Read all necessary CSV files
    print("Reading CSV files...")
    farm_company_roles = pd.read_csv(DATA_DIR / "farm_company_roles.csv")
    farms = pd.read_csv(DATA_DIR / "farms.csv")
    companies = pd.read_csv(DATA_DIR / "companies.csv")
    company_roles = pd.read_csv(DATA_DIR / "company_roles.csv")

    print(f"Loaded {len(farm_company_roles)} farm company role relationships")
    print(f"Loaded {len(farms)} farms")
    print(f"Loaded {len(companies)} companies")
    print(f"Loaded {len(company_roles)} company roles")

    # Join farm_company_roles with farms to get SPV and project info
    result = farm_company_roles.merge(
        farms[['uuid', 'spv', 'project', 'code']],
        left_on='farm_uuid',
        right_on='uuid',
        how='left',
        suffixes=('', '_farm')
    )

    # Join with companies to get company names
    result = result.merge(
        companies[['uuid', 'name']],
        left_on='company_uuid',
        right_on='uuid',
        how='left',
        suffixes=('', '_company')
    )

    # Join with company_roles to get role names
    result = result.merge(
        company_roles[['id', 'role_name']],
        left_on='company_role_id',
        right_on='id',
        how='left'
    )

    # Select and order columns for final output
    final_columns = ['code', 'spv', 'project', 'role_name', 'name']
    result_final = result[final_columns].copy()

    # Sort by farm code and role name for better readability
    result_final = result_final.sort_values(['code', 'role_name'])

    # Rename columns for clarity
    result_final.columns = ['farm_code', 'spv', 'project', 'role', 'company_name']

    # Export to CSV
    result_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    print(f"\n[OK] Successfully created view with {len(result_final)} rows")
    print(f"[OK] Output saved to: {OUTPUT_FILE}")

    # Display sample of results
    print("\nSample of results (first 10 rows):")
    print(result_final.head(10).to_string(index=False))

    # Summary statistics
    print(f"\nSummary:")
    print(f"- Total farm-company relationships: {len(result_final)}")
    print(f"- Unique farms: {result_final['farm_code'].nunique()}")
    print(f"- Unique roles: {result_final['role'].nunique()}")
    print(f"- Unique companies: {result_final['company_name'].nunique()}")

    # Group by role to see distribution
    print("\nCompany relationships by role:")
    role_counts = result_final['role'].value_counts()
    for role, count in role_counts.items():
        print(f"  - {role}: {count} farms")

    # Group by company
    print("\nFarms by company:")
    company_counts = result_final['company_name'].value_counts()
    for company, count in company_counts.items():
        print(f"  - {company}: {count} farms")

    return result_final

if __name__ == "__main__":
    try:
        df = create_farm_company_roles_view()
    except Exception as e:
        print(f"Error: {e}")
        raise

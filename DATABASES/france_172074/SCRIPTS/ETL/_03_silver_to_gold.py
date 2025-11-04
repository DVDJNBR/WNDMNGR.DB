from pathlib import Path
import pandas as pd
from loguru import logger
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Personnel codes (RGPD compliance)
PERS_LCH = os.getenv('PERS_LCH')

# Paths
silver_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'SILVER'
gold_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'GOLD'
gold_dir.mkdir(parents=True, exist_ok=True)

###########################
### REFERENCE TABLES ######
###########################

logger.info("Creating reference tables...")

# Farm Types
df_farm_types = pd.DataFrame({
    'id': [1, 2, 3],
    'type_title': ['Wind', 'Solar', 'Hybrid']
})
df_farm_types.to_csv(gold_dir / 'farm_types.csv', index=False)
logger.success(f"farm_types: {len(df_farm_types)} rows")

# Company Roles
COMPANY_ROLES = sorted([
    'Customer',
    'Portfolio',
    'Asset Manager',
    'Legal Representative',
    'Bank Domiciliation',
    'Project Developer',
    'Co-developer',
    'WTG Service Provider',
    'Substation Service Provider',
    'Grid Operator',
    'OM Main Service Company',
    'OM Service Provider',
    'Chartered Accountant',
    'Legal Auditor',
    'Energy Trader'
])

df_company_roles = pd.DataFrame({'role_name': COMPANY_ROLES})
df_company_roles.insert(0, 'id', df_company_roles.index + 1)
df_company_roles.to_csv(gold_dir / 'company_roles.csv', index=False)
logger.success(f"company_roles: {len(df_company_roles)} rows")

# Person Roles
PERSON_ROLES = sorted([
    'Head of Technical Management',
    'Technical Manager',
    'Substitute Technical Manager',
    'HSE Coordination',
    'Electrical Manager',
    'Controller Responsible',
    'Controller Deputy',
    'Administrative responsible',
    'Administrative Deputy',
    'Control Room Operator',
    'Field Crew Manager',
    'Environmental Department Manager',
    'Key Account Manager',
    'Substitute Key Account Manager',
    'Asset Manager',
    'Legal Representative',
    'Overseer',
    'Commercial Controller'
])

df_person_roles = pd.DataFrame({'role_name': PERSON_ROLES})
df_person_roles.insert(0, 'id', df_person_roles.index + 1)
df_person_roles.to_csv(gold_dir / 'person_roles.csv', index=False)
logger.success(f"person_roles: {len(df_person_roles)} rows")

###########################
### ENTITY TABLES #########
###########################

logger.info("Creating entity tables...")

# Load source data
df_repartition = pd.read_csv(silver_dir / 'repartition_sheet.csv', encoding='utf-8-sig')  # type: ignore
df_database = pd.read_csv(silver_dir / 'database_sheet.csv', encoding='utf-8-sig')  # type: ignore

# Step 1: Extract all persons (from repartition + legal representatives)
person_columns = [
    'technical_manager', 'substitute_technical_manager',
    'key_account_manager', 'substitute_key_account_manager',
    'electrical_manager', 'controller_responsible', 'controller_deputy',
    'administrative_responsible', 'administrative_deputy'
]

all_persons = []
for col in person_columns:
    if col in df_repartition.columns:
        all_persons.extend(df_repartition[col].dropna().unique())

all_persons_series = pd.Series(all_persons).str.strip().replace('', pd.NA).dropna()
persons_exploded = all_persons_series.str.split(r' \+ ', regex=True).explode().unique()

# Add legal representative persons
unique_legal_reps = df_database['legal_representative'].dropna().unique()
legal_rep_companies = [rep for rep in unique_legal_reps if rep != '' and any(kw in rep.lower() for kw in ['gestion', 'actifs', 'sas', 'sarl'])]
legal_rep_persons = [rep for rep in unique_legal_reps if rep != '' and len(rep.split()) == 2 and rep not in legal_rep_companies]

# Extract persons from database_sheet columns (control room, field crew, HSE, overseer, commercial controller)
database_person_columns = ['control_room_l1', 'field_crew', 'hse_coordination', 'overseer', 'commercial_controller', 'substitute_commercial_controller']
company_keywords = ['société', 'statkraft', 'seris', 'loire', 'france', 'sas', 'sarl', 'gestion', 'securite', 'securitas']

database_persons = []
for col in database_person_columns:
    if col in df_database.columns:
        unique_values = df_database[col].dropna().unique()
        for val in unique_values:
            val_str = str(val).strip()
            # Filter out empty strings and companies using keywords
            if val_str != '' and not any(kw in val_str.lower() for kw in company_keywords):
                database_persons.append(val_str)

all_persons_list = list(persons_exploded) + legal_rep_persons + database_persons

df_persons = pd.DataFrame({'full_name': all_persons_list})
df_persons = (
    df_persons[df_persons['full_name'] != '']
    .drop_duplicates()
    .reset_index(drop=True)
    .assign(
        first_name=lambda df: df['full_name'].str.split().str[0],
        last_name=lambda df: df['full_name'].str.split().str[1:].str.join(' ')
    )
    [['first_name', 'last_name']]
)

# Step 2: Extract all companies (customers + legal representatives + portfolio + asset manager + developers + service companies + auditors + traders + grid + banks)
unique_customers = df_database['customer'].dropna().unique()
unique_portfolios = df_database['portfolio_name'].dropna().unique()
unique_asset_managers = df_database['asset_manager'].dropna().unique()
unique_project_developers = df_database['project_developer'].dropna().unique()
unique_co_developers = df_database['co_developper'].dropna().unique()
unique_main_service = df_database['main_service_company'].dropna().unique()
unique_service_providers = df_database['service_provider'].dropna().unique()
unique_chartered_accountants = df_database['expert_comptable_chartered_accountant'].dropna().unique()
unique_legal_auditors = df_database['commissaire_aux_comptes_legal_auditor'].dropna().unique()
unique_energy_traders = df_database['energy_trader'].dropna().unique()
unique_substation_service = df_database['transfer_station_power_station_service_company'].dropna().unique()
unique_grid_operators = df_database['grid_operator'].dropna().unique()
unique_bank_domiciliation = df_database['bank_domiciliation'].dropna().unique()
unique_wtg_service = df_database['wec_service_company'].dropna().unique()

all_companies_list = (
    list(unique_customers) +
    legal_rep_companies +
    list(unique_portfolios) +
    list(unique_asset_managers) +
    list(unique_project_developers) +
    list(unique_co_developers) +
    list(unique_main_service) +
    list(unique_service_providers) +
    list(unique_chartered_accountants) +
    list(unique_legal_auditors) +
    list(unique_energy_traders) +
    list(unique_substation_service) +
    list(unique_grid_operators) +
    list(unique_bank_domiciliation) +
    list(unique_wtg_service)
)

df_companies = pd.DataFrame({'name': all_companies_list})
df_companies = (
    df_companies[df_companies['name'] != '']
    .drop_duplicates()
    .reset_index(drop=True)
)

# Step 3: Extract farms
df_farms = (
    df_repartition[['spv', 'project', 'code', 'farm_type']]
    .drop_duplicates()
    .reset_index(drop=True)
    .merge(df_farm_types, left_on='farm_type', right_on='type_title', how='left')
    .drop(['type_title', 'farm_type'], axis=1)
    .rename(columns={'id': 'farm_type_id'})
)

# Step 4: Add UUIDs to all entities
df_persons.insert(0, 'uuid', [str(uuid.uuid4()) for _ in range(len(df_persons))])
df_companies.insert(0, 'uuid', [str(uuid.uuid4()) for _ in range(len(df_companies))])
df_farms.insert(0, 'uuid', [str(uuid.uuid4()) for _ in range(len(df_farms))])

# Step 5: Save entity tables
df_persons.to_csv(gold_dir / 'persons.csv', index=False)
df_companies.to_csv(gold_dir / 'companies.csv', index=False)
df_farms.to_csv(gold_dir / 'farms.csv', index=False)

logger.success(f"persons: {len(df_persons)} rows")
logger.success(f"companies: {len(df_companies)} rows")
logger.success(f"farms: {len(df_farms)} rows")

###########################
### RELATIONSHIP TABLES ###
###########################

logger.info("Creating relationship tables...")

# Create lookups for farm_referents
person_lookup = df_persons.set_index(['first_name', 'last_name'])['uuid'].to_dict()
role_lookup = df_person_roles.set_index('role_name')['id'].to_dict()
farm_lookup = df_farms.set_index('code')['uuid'].to_dict()

def get_person_uuid(full_name):
    if pd.isna(full_name) or full_name == '':
        return None
    parts = full_name.split()
    if len(parts) < 2:
        return None
    first_name = parts[0]
    last_name = ' '.join(parts[1:])
    return person_lookup.get((first_name, last_name))

# Map column names to role names
column_to_role = {
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

# Build farm_referents table
referents_list = []

for col_name, role_name in column_to_role.items():
    if col_name in df_repartition.columns:
        role_id = role_lookup.get(role_name)

        for _, row in df_repartition.iterrows():
            farm_uuid = farm_lookup.get(row['code'])
            person_name = row[col_name]

            if pd.notna(person_name) and person_name != '':
                person_uuid = get_person_uuid(person_name)

                if farm_uuid and person_uuid:
                    referents_list.append({
                        'farm_uuid': farm_uuid,
                        'farm_code': row['code'],
                        'person_role_id': role_id,
                        'company_role_id': None,
                        'person_uuid': person_uuid,
                        'company_uuid': None
                    })

df_farm_referents = pd.DataFrame(referents_list).drop_duplicates()
df_farm_referents.to_csv(gold_dir / 'farm_referents.csv', index=False)
logger.success(f"farm_referents: {len(df_farm_referents)} rows")

# Farm Company Roles - Link farms to companies with their roles
# Create lookups
company_lookup = df_companies.set_index('name')['uuid'].to_dict()
company_role_lookup = df_company_roles.set_index('role_name')['id'].to_dict()

# Match farm codes between database_sheet and farms
# Use three_letter_code from database_sheet to match with code in farms
farm_company_roles_list = []

for _, row in df_database.iterrows():
    farm_code = row['three_letter_code']
    customer_name = row['customer']

    if pd.notna(farm_code) and pd.notna(customer_name) and customer_name != '':
        farm_uuid = farm_lookup.get(farm_code)
        company_uuid = company_lookup.get(customer_name)
        # Get the "Customer" role ID
        customer_role_id = company_role_lookup.get('Customer')

        if farm_uuid and company_uuid and customer_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': company_uuid,
                'company_role_id': customer_role_id
            })

    # Add legal representative (if company)
    legal_rep = row['legal_representative']
    if pd.notna(legal_rep) and legal_rep != '' and legal_rep in legal_rep_companies:
        legal_rep_company_uuid = company_lookup.get(legal_rep)
        legal_rep_role_id = company_role_lookup.get('Legal Representative')
        if farm_uuid and legal_rep_company_uuid and legal_rep_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': legal_rep_company_uuid,
                'company_role_id': legal_rep_role_id
            })

    # Add portfolio
    portfolio = row['portfolio_name']
    if pd.notna(portfolio) and portfolio != '':
        portfolio_company_uuid = company_lookup.get(portfolio)
        portfolio_role_id = company_role_lookup.get('Portfolio')
        if farm_uuid and portfolio_company_uuid and portfolio_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': portfolio_company_uuid,
                'company_role_id': portfolio_role_id
            })

    # Add asset manager
    asset_manager = row['asset_manager']
    if pd.notna(asset_manager) and asset_manager != '':
        asset_manager_uuid = company_lookup.get(asset_manager)
        asset_manager_role_id = company_role_lookup.get('Asset Manager')
        if farm_uuid and asset_manager_uuid and asset_manager_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': asset_manager_uuid,
                'company_role_id': asset_manager_role_id
            })

    # Add project developer
    project_dev = row['project_developer']
    if pd.notna(project_dev) and project_dev != '':
        project_dev_uuid = company_lookup.get(project_dev)
        project_dev_role_id = company_role_lookup.get('Project Developer')
        if farm_uuid and project_dev_uuid and project_dev_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': project_dev_uuid,
                'company_role_id': project_dev_role_id
            })

    # Add co-developer
    co_dev = row['co_developper']
    if pd.notna(co_dev) and co_dev != '':
        co_dev_uuid = company_lookup.get(co_dev)
        co_dev_role_id = company_role_lookup.get('Co-developer')
        if farm_uuid and co_dev_uuid and co_dev_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': co_dev_uuid,
                'company_role_id': co_dev_role_id
            })

    # Add main service company
    main_service = row['main_service_company']
    if pd.notna(main_service) and main_service != '':
        main_service_uuid = company_lookup.get(main_service.strip())  # Strip to handle 'Enercon ' with trailing space
        main_service_role_id = company_role_lookup.get('OM Main Service Company')
        if farm_uuid and main_service_uuid and main_service_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': main_service_uuid,
                'company_role_id': main_service_role_id
            })

    # Add service provider
    service_prov = row['service_provider']
    if pd.notna(service_prov) and service_prov != '':
        service_prov_uuid = company_lookup.get(service_prov)
        service_prov_role_id = company_role_lookup.get('OM Service Provider')
        if farm_uuid and service_prov_uuid and service_prov_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': service_prov_uuid,
                'company_role_id': service_prov_role_id
            })

    # Add chartered accountant
    chartered_acc = row['expert_comptable_chartered_accountant']
    if pd.notna(chartered_acc) and chartered_acc != '':
        chartered_acc_uuid = company_lookup.get(chartered_acc)
        chartered_acc_role_id = company_role_lookup.get('Chartered Accountant')
        if farm_uuid and chartered_acc_uuid and chartered_acc_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': chartered_acc_uuid,
                'company_role_id': chartered_acc_role_id
            })

    # Add legal auditor
    legal_auditor = row['commissaire_aux_comptes_legal_auditor']
    if pd.notna(legal_auditor) and legal_auditor != '':
        legal_auditor_uuid = company_lookup.get(legal_auditor)
        legal_auditor_role_id = company_role_lookup.get('Legal Auditor')
        if farm_uuid and legal_auditor_uuid and legal_auditor_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': legal_auditor_uuid,
                'company_role_id': legal_auditor_role_id
            })

    # Add energy trader
    energy_trader = row['energy_trader']
    if pd.notna(energy_trader) and energy_trader != '' and energy_trader.strip() != '':
        energy_trader_uuid = company_lookup.get(energy_trader.strip())
        energy_trader_role_id = company_role_lookup.get('Energy Trader')
        if farm_uuid and energy_trader_uuid and energy_trader_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': energy_trader_uuid,
                'company_role_id': energy_trader_role_id
            })

    # Add substation service provider
    substation_service = row['transfer_station_power_station_service_company']
    if pd.notna(substation_service) and substation_service != '':
        substation_service_uuid = company_lookup.get(substation_service)
        substation_service_role_id = company_role_lookup.get('Substation Service Provider')
        if farm_uuid and substation_service_uuid and substation_service_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': substation_service_uuid,
                'company_role_id': substation_service_role_id
            })

    # Add grid operator
    grid_operator = row['grid_operator']
    if pd.notna(grid_operator) and grid_operator != '' and grid_operator.strip() != '':
        grid_operator_uuid = company_lookup.get(grid_operator.strip())
        grid_operator_role_id = company_role_lookup.get('Grid Operator')
        if farm_uuid and grid_operator_uuid and grid_operator_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': grid_operator_uuid,
                'company_role_id': grid_operator_role_id
            })

    # Add bank domiciliation
    bank_dom = row['bank_domiciliation']
    if pd.notna(bank_dom) and bank_dom != '' and bank_dom.strip() != '':
        bank_dom_uuid = company_lookup.get(bank_dom.strip())
        bank_dom_role_id = company_role_lookup.get('Bank Domiciliation')
        if farm_uuid and bank_dom_uuid and bank_dom_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': bank_dom_uuid,
                'company_role_id': bank_dom_role_id
            })

    # Add WTG service provider
    wtg_service = row['wec_service_company']
    if pd.notna(wtg_service) and wtg_service != '':
        wtg_service_uuid = company_lookup.get(wtg_service)
        wtg_service_role_id = company_role_lookup.get('WTG Service Provider')
        if farm_uuid and wtg_service_uuid and wtg_service_role_id:
            farm_company_roles_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'company_uuid': wtg_service_uuid,
                'company_role_id': wtg_service_role_id
            })

df_farm_company_roles = pd.DataFrame(farm_company_roles_list).drop_duplicates()
df_farm_company_roles.to_csv(gold_dir / 'farm_company_roles.csv', index=False)
logger.success(f"farm_company_roles: {len(df_farm_company_roles)} rows")

# Add legal representative persons to farm_referents
legal_rep_role_id = role_lookup.get('Legal Representative')
for _, row in df_database.iterrows():
    farm_code = row['three_letter_code']
    legal_rep = row['legal_representative']

    if pd.notna(legal_rep) and legal_rep != '' and legal_rep in legal_rep_persons:
        farm_uuid = farm_lookup.get(farm_code)
        person_uuid = get_person_uuid(legal_rep)

        if farm_uuid and person_uuid and legal_rep_role_id:
            referents_list.append({
                'farm_uuid': farm_uuid,
                'farm_code': farm_code,
                'person_role_id': legal_rep_role_id,
                'company_role_id': None,
                'person_uuid': person_uuid,
                'company_uuid': None
            })

# Add database_sheet person columns to farm_referents
database_column_to_role = {
    'control_room_l1': 'Control Room Operator',
    'field_crew': 'Field Crew Manager',
    'hse_coordination': 'HSE Coordination',
    'overseer': 'Overseer',
    'commercial_controller': 'Commercial Controller',
    'substitute_commercial_controller': 'Commercial Controller'
}

for _, row in df_database.iterrows():
    farm_code = row['three_letter_code']
    farm_uuid = farm_lookup.get(farm_code)

    for col_name, role_name in database_column_to_role.items():
        if col_name in df_database.columns:
            person_name = row[col_name]

            if pd.notna(person_name) and person_name != '':
                person_name_str = str(person_name).strip()
                # Skip companies
                if not any(kw in person_name_str.lower() for kw in company_keywords):
                    person_uuid = get_person_uuid(person_name_str)
                    role_id = role_lookup.get(role_name)

                    if farm_uuid and person_uuid and role_id:
                        referents_list.append({
                            'farm_uuid': farm_uuid,
                            'farm_code': farm_code,
                            'person_role_id': role_id,
                            'company_role_id': None,
                            'person_uuid': person_uuid,
                            'company_uuid': None
                        })

# Add Louis Chenel as "Head of Technical Management" for all farms
louis_chenel_uuid = get_person_uuid(PERS_LCH)
head_tech_mgmt_role_id = role_lookup.get('Head of Technical Management')

if louis_chenel_uuid and head_tech_mgmt_role_id:
    for farm_code, farm_uuid in farm_lookup.items():
        referents_list.append({
            'farm_uuid': farm_uuid,
            'farm_code': farm_code,
            'person_role_id': head_tech_mgmt_role_id,
            'company_role_id': None,
            'person_uuid': louis_chenel_uuid,
            'company_uuid': None
        })
    logger.info(f"Added {PERS_LCH} as Head of Technical Management for all {len(farm_lookup)} farms")

# Re-save farm_referents with all persons (legal reps + database_sheet persons + Louis Chenel)
df_farm_referents = pd.DataFrame(referents_list).drop_duplicates()
df_farm_referents.to_csv(gold_dir / 'farm_referents.csv', index=False)
logger.success(f"farm_referents (updated with all persons): {len(df_farm_referents)} rows")

logger.success("All GOLD tables created successfully")
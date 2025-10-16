from pathlib import Path
import pandas as pd
from loguru import logger
import uuid

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
    'OM Service Provider'
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
    'Chartered Accountant',
    'Legal Auditor',
    'Asset Manager',
    'Legal Representative'
])

df_person_roles = pd.DataFrame({'role_name': PERSON_ROLES})
df_person_roles.insert(0, 'id', df_person_roles.index + 1)
df_person_roles.to_csv(gold_dir / 'person_roles.csv', index=False)
logger.success(f"person_roles: {len(df_person_roles)} rows")

###########################
### ENTITY TABLES #########
###########################

logger.info("Creating entity tables...")

# Load repartition sheet
df_repartition = pd.read_csv(silver_dir / 'repartition_sheet.csv')  # type: ignore

# Persons
person_columns = [
    'technical_manager',
    'substitute_technical_manager',
    'key_account_manager',
    'substitute_key_account_manager',
    'electrical_manager',
    'controller_responsible',
    'controller_deputy',
    'administrative_controller',
    'administrative_deputy'
]

all_persons = []
for col in person_columns:
    if col in df_repartition.columns:
        persons_in_column = df_repartition[col].dropna().unique()
        all_persons.extend(persons_in_column)

all_persons_series = pd.Series(all_persons).str.strip().replace('', pd.NA).dropna()
persons_exploded = all_persons_series.str.split(' \+ ').explode().unique()

df_persons = pd.DataFrame({'full_name': persons_exploded})
df_persons = (
    df_persons[df_persons['full_name'] != '']
    .drop_duplicates()
    .reset_index(drop=True)
    .assign(
        first_name=lambda df: df['full_name'].str.split().str[0],
        last_name=lambda df: df['full_name'].str.split().str[1:].str.join(' ')
    )
    .drop('full_name', axis=1)
)
df_persons.insert(0, 'uuid', [str(uuid.uuid4()) for _ in range(len(df_persons))])
# email, mobile, person_type are optional and will remain NULL in DB
df_persons[['uuid', 'first_name', 'last_name']].to_csv(gold_dir / 'persons.csv', index=False)
logger.success(f"persons: {len(df_persons)} rows")

# Farms
df_farms = (
    df_repartition[['spv', 'project', 'code', 'farm_type']]
    .drop_duplicates()
    .reset_index(drop=True)
    .merge(df_farm_types, left_on='farm_type', right_on='type_title', how='left')
    .drop(['type_title', 'farm_type'], axis=1)
    .rename(columns={'id': 'farm_type_id'})
)
df_farms.insert(0, 'uuid', [str(uuid.uuid4()) for _ in range(len(df_farms))])
df_farms.to_csv(gold_dir / 'farms.csv', index=False)
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
                        'role_id': role_id,
                        'person_uuid': person_uuid,
                        'company_uuid': None
                    })

df_farm_referents = pd.DataFrame(referents_list).drop_duplicates()
# Remove company_uuid column since we're not using it yet
df_farm_referents = df_farm_referents.drop('company_uuid', axis=1)
df_farm_referents.to_csv(gold_dir / 'farm_referents.csv', index=False)
logger.success(f"farm_referents: {len(df_farm_referents)} rows")

logger.success("All GOLD tables created successfully")
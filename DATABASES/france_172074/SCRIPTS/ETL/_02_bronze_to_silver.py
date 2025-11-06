import janitor
from pathlib import Path
import pandas as pd
import re
from loguru import logger
import os
from dotenv import load_dotenv
import unicodedata

import icecream as ic

# Load environment variables
load_dotenv()

# Personnel codes (RGPD compliance)
PERS_MMA = os.getenv('PERS_MMA')
PERS_MMA_SHORT = os.getenv('PERS_MMA_SHORT')
PERS_GCA = os.getenv('PERS_GCA')
PERS_HOM = os.getenv('PERS_HOM')
PERS_FRA = os.getenv('PERS_FRA')
PERS_ADE = os.getenv('PERS_ADE')
PERS_VCH = os.getenv('PERS_VCH')
PERS_AVI = os.getenv('PERS_AVI')
PERS_ALA = os.getenv('PERS_ALA')
PERS_LCH = os.getenv('PERS_LCH')
PERS_LCH_SHORT = os.getenv('PERS_LCH_SHORT')

# Names to invert
PERS_INVERTED_STR = os.getenv('PERS_INVERTED', '')
PERS_INVERTED = [name.strip() for name in PERS_INVERTED_STR.split(',') if name.strip()]

# Paths
bronze_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'BRONZE'
silver_dir = Path('DATABASES') / 'france_172074' / 'DATA' / 'SILVER'
silver_dir.mkdir(parents=True, exist_ok=True)

############################
### CLEAN DATABASE SHEET ###
############################

logger.info("Starting to clean Database sheet...")
df_database = (
    pd.read_csv(bronze_dir / "database_sheet.csv", encoding='utf-8-sig')  # type: ignore
    .rename(columns=lambda x: x.strip())
    .clean_names(case_type="snake", strip_accents=True) 
    .rename(columns=lambda x: x.strip('_').replace('\n', '')) # remove leading/trailing underscores and newlines in col names
    .rename({"end_date_of_o&m_contract":"end_date_of_om_contract"}, axis=1)
    .fillna("") 
    .map(lambda x: re.sub(r'\s+', ' ', x) if isinstance(x, str) else x)
    .transform_columns(
        ["customer", "region", "departement", "commune", "head_office_address", "legal_representative",
        "duty_dreal_contact", "prefecture_name", "prefecture_address", "windmanager_subsidiary",
        "portfolio_name", "asset_manager", "project_developer", "co_developper",
        "wec_supplier", "wec_service_company", "transfer_station_power_station_service_company",
        "delegataire_electrique_nf_c18_510", "sub_delegataire_electrique_nf_c18_510", "overseer",
        "main_service_company", "service_provider", "expert_comptable_chartered_accountant",
        "commissaire_aux_comptes_legal_auditor", "energy_trader", "tariff_aggregator", "vppa_name"],
        lambda x: str(x).title().replace("-", " ")
                        .replace(" De ", " de ").replace(" D'", " d'").replace(" Du ", " du ").replace(" Des ", " des ")
                        .replace(" La ", " la ").replace(" Le ", " le ").replace(" Les ", " les ")
                        .replace(" Et ", " et ").replace(" Sur ", " sur ")
                        .replace(" Rue ", " rue ").replace(" Avenue ", " avenue ").replace(" Boulevard ", " boulevard ")
    )
    .transform_columns(["region", "departement", "commune"], lambda x: str(x).replace(" ", "-"))
    .transform_column("duty_dreal_contact", lambda x: str(x).replace(" ", "-").replace("Dreal-", "DREAL "))
    .transform_columns(["siret", "vat_number"], lambda x: str(x).replace(" ", ""))
    .transform_column("land_lease_payment_date", lambda x: str(x).title())
    .transform_columns(
        ["control_room_l1", "field_crew", "hse_coordination",
         "commercial_controller", "substitute_commercial_controller"],
        lambda x: str(x).title()
    )
)

### Convert types
# integers
df_database.account_number = pd.to_numeric(df_database.account_number, errors='coerce').astype('Int64')
df_database.siret = pd.to_numeric(df_database.siret, errors='coerce').astype('Int64')
df_database.last_toc = pd.to_numeric(df_database.last_toc, errors='coerce').astype('Int64')
df_database.transfer_station_power_station = pd.to_numeric(df_database.transfer_station_power_station, errors='coerce').astype('Int64')
df_database.dismantling_provision_indexation_date = pd.to_numeric(df_database.dismantling_provision_indexation_date, errors='coerce').astype('Int64')
# floats
df_database.km_ar_arras = pd.to_numeric(df_database.km_ar_arras, errors='coerce').astype('Float64')
df_database.km_ar_nantes = pd.to_numeric(df_database.km_ar_nantes, errors='coerce').astype('Float64')
df_database.temps_ar_arras_en_h = pd.to_numeric(df_database.temps_ar_arras_en_h, errors='coerce').astype('Float64')
df_database.temps_ar_vertou_en_h = pd.to_numeric(df_database.temps_ar_vertou_en_h, errors='coerce').astype('Float64')
df_database.peages_arras = pd.to_numeric(df_database.peages_arras, errors='coerce').astype('Float64')
df_database.peages_nantes = pd.to_numeric(df_database.peages_nantes, errors='coerce').astype('Float64')
df_database.tcma_compensation_rate = pd.to_numeric(df_database.tcma_compensation_rate, errors='coerce').astype('Float64')
df_database.financial_guarantee_amount = pd.to_numeric(df_database.financial_guarantee_amount, errors='coerce').astype('Float64')
df_database.vppa_tariff_m_wh = pd.to_numeric(df_database.vppa_tariff_m_wh, errors='coerce').astype('Float64')
df_database.production_target_bank_m_wh_an = pd.to_numeric(df_database.production_target_bank_m_wh_an, errors='coerce').astype('Float64')
df_database.productible_actual_2020_m_wh = pd.to_numeric(df_database.productible_actual_2020_m_wh, errors='coerce').astype('Float64')
df_database.productible_actual_2021_m_wh = pd.to_numeric(df_database.productible_actual_2021_m_wh, errors='coerce').astype('Float64')
df_database.productible_actual_2022_m_wh = pd.to_numeric(df_database.productible_actual_2022_m_wh, errors='coerce').astype('Float64')
df_database.productible_actual_2023_m_wh = pd.to_numeric(df_database.productible_actual_2023_m_wh, errors='coerce').astype('Float64')
df_database.revenue_target_2020 = pd.to_numeric(df_database.revenue_target_2020, errors='coerce').astype('Float64')
df_database.revenue_target_2021 = pd.to_numeric(df_database.revenue_target_2021, errors='coerce').astype('Float64')
df_database.revenue_target_2022 = pd.to_numeric(df_database.revenue_target_2022, errors='coerce').astype('Float64')
df_database.revenue_target_2023 = pd.to_numeric(df_database.revenue_target_2023, errors='coerce').astype('Float64')
df_database.revenue_target_2024 = pd.to_numeric(df_database.revenue_target_2024, errors='coerce').astype('Float64')
df_database.revenue_actual_2020 = pd.to_numeric(df_database.revenue_actual_2020, errors='coerce').astype('Float64')
df_database.revenue_actual_2021 = pd.to_numeric(df_database.revenue_actual_2021, errors='coerce').astype('Float64')
df_database.revenue_actual_2022 = pd.to_numeric(df_database.revenue_actual_2022, errors='coerce').astype('Float64')
df_database.revenue_actual_2023 = pd.to_numeric(df_database.revenue_actual_2023, errors='coerce').astype('Float64')
# datetimes
df_database.tcma_signature_date = pd.to_datetime(df_database.tcma_signature_date, errors='coerce')
df_database.tcma_entree_en_vigueur = pd.to_datetime(df_database.tcma_entree_en_vigueur, errors='coerce')
df_database.beginning_of_remuneration = pd.to_datetime(df_database.beginning_of_remuneration, errors='coerce')
df_database.end_date_of_tcma = pd.to_datetime(df_database.end_date_of_tcma, errors='coerce')
df_database.drei_date = pd.to_datetime(df_database.drei_date, errors='coerce')
df_database.end_date_of_om_contract = pd.to_datetime(df_database.end_date_of_om_contract, errors='coerce')
df_database.start_date_agregator_contract = pd.to_datetime(df_database.start_date_agregator_contract, errors='coerce')
df_database.tarif_start_date = pd.to_datetime(df_database.tarif_start_date, errors='coerce')
df_database.tarif_end_date = pd.to_datetime(df_database.tarif_end_date, errors='coerce')
df_database.vppa_start = pd.to_datetime(df_database.vppa_start, errors='coerce')
df_database.vapp_duration = pd.to_datetime(df_database.vapp_duration, errors='coerce')
df_database.financial_guarantee_due_date = pd.to_datetime(df_database.financial_guarantee_due_date, errors='coerce')

### Save
df_database.to_csv(silver_dir / "database_sheet.csv", index=False)
logger.success("Database sheet cleaned and saved to SILVER")


###########################
### CLEAN DB WTG ##########
###########################

logger.info("Starting to clean DB WTG sheet...")
df_dbwtg = (
    pd.read_csv(bronze_dir / "dbwtg_sheet.csv", encoding='utf-8-sig')  # type: ignore
    .clean_names(case_type="snake", strip_accents=True)
    .fillna("")
    .transform_columns(["spv", "project"], lambda x: str(x).title())
)
# converts
df_dbwtg.wtg_serial_number = pd.to_numeric(df_dbwtg.wtg_serial_number, errors='coerce').astype('Int64')
df_dbwtg.cod = pd.to_datetime(df_dbwtg.cod, errors='coerce')
# saves
df_dbwtg.to_csv(silver_dir / "dbwtg_sheet.csv", index=False)
logger.success("DB WTG sheet cleaned and saved to SILVER")


###########################
### CLEAN DB GRID #########
###########################

logger.info("Starting to clean DB GRID sheet...")
df_dbgrid = (
    pd.read_csv(bronze_dir / "dbgrid_sheet.csv", encoding='utf-8-sig')  # type: ignore
    .clean_names(case_type="snake", strip_accents=True)
    .fillna("")
    .transform_columns(["customer", "spv", "project", "nom_du_pdl", "grid_operator", "pdl_service_company"], lambda x: str(x).title())
)

df_dbgrid.to_csv(silver_dir / "dbgrid_sheet.csv", index=False)
logger.success("DB GRID sheet cleaned and saved to SILVER")


################################
### CLEAN REPARTITION SHEET ###
################################

logger.info("Starting to clean Repartition sheet...")
df_repartition = (
    pd.read_csv(bronze_dir / "repartition_sheet.csv", encoding='utf-8-sig')  # type: ignore
    .rename(columns=lambda x: x.replace('\n', '_'))
    .clean_names(case_type="snake", strip_accents=True)
    .rename(columns=lambda x: x.strip('_'))
    .fillna("")
    .map(lambda x: re.sub(r'\s+', ' ', x).strip() if isinstance(x, str) else x)
    .transform_columns(
        ["technical_manager_by_windfarm", "kam", "electrical_manager",
         "controller_responsible", "controller_deputy",
         "administrative_responsible", "administrative_deputy"],
        lambda x: str(x).title()
    )
    .assign(
        owner_of_wf=lambda df: df['owner_of_wf'].replace('', pd.NA).ffill(),
        controller_responsible=lambda df: df['controller_responsible'].replace('Pas De Gestion Commerciale Pour Ce Portefeuille', ''),
        technical_manager_by_windfarm=lambda df: df['technical_manager_by_windfarm'].replace(PERS_MMA_SHORT.title(), PERS_MMA.title()),
        kam=lambda df: df['kam'].str.replace(f'+ {PERS_LCH_SHORT.title()}', f'+ {PERS_LCH.title()}', regex=False)
    )
)

# Create new columns
df_repartition['farm_type'] = df_repartition['wf_abbreviation'].apply(lambda x: 'Solar' if x == 'ESM' else 'Wind')
df_repartition['substitute_technical_manager'] = df_repartition['technical_manager_by_windfarm'].replace({
    PERS_MMA: PERS_GCA,
    PERS_GCA: PERS_MMA,
    PERS_HOM: PERS_FRA,
    PERS_FRA: PERS_HOM,
    PERS_ADE: PERS_VCH,
    PERS_VCH: PERS_ADE
})
df_repartition['substitute_key_account_manager'] = df_repartition['kam'].replace({
    PERS_AVI: PERS_ALA,
    PERS_ALA: PERS_AVI,
    f'{PERS_ALA} + {PERS_LCH}': PERS_AVI
})

# Reorder columns
cols = df_repartition.columns.tolist()
col_order = (
    cols[0:4] +  # owner_of_wf, windfarm, wf_common_name, wf_abbreviation
    ['farm_type'] +
    [cols[4]] +  # technical_manager_by_windfarm
    ['substitute_technical_manager'] +
    [cols[5]] +  # kam
    ['substitute_key_account_manager'] +
    cols[6:-3]  # rest without the 3 new columns
)
df_repartition = df_repartition[col_order]

# Rename columns
df_repartition = df_repartition.rename(columns={
    'owner_of_wf': 'owner',
    'windfarm': 'spv',
    'wf_common_name': 'project',
    'wf_abbreviation': 'code',
    'technical_manager_by_windfarm': 'technical_manager',
    'kam': 'key_account_manager'
})

# Deduplicate accents in person columns (keep version with accents)
person_cols_repartition = ['technical_manager', 'substitute_technical_manager', 'key_account_manager',
                           'substitute_key_account_manager', 'electrical_manager', 'controller_responsible',
                           'controller_deputy', 'administrative_responsible', 'administrative_deputy']
person_cols_database = ['control_room_l1', 'field_crew', 'hse_coordination', 'commercial_controller',
                        'substitute_commercial_controller', 'legal_representative']

# Build accent deduplication map from both dataframes
all_person_values = []
for col in person_cols_repartition:
    if col in df_repartition.columns:
        all_person_values.extend(df_repartition[col].dropna().unique())
for col in person_cols_database:
    if col in df_database.columns:
        all_person_values.extend(df_database[col].dropna().unique())

unaccented_map = {}
for val in all_person_values:
    if val != '':
        val_str = str(val)
        unaccented = ''.join(c for c in unicodedata.normalize('NFD', val_str) if unicodedata.category(c) != 'Mn')
        if unaccented not in unaccented_map or (val_str != unaccented and unaccented_map[unaccented] == unaccented):
            unaccented_map[unaccented] = val_str

# Apply deduplication to repartition
for col in person_cols_repartition:
    if col in df_repartition.columns:
        df_repartition[col] = df_repartition[col].map(
            lambda x: unaccented_map.get(''.join(c for c in unicodedata.normalize('NFD', str(x)) if unicodedata.category(c) != 'Mn'), x) if pd.notna(x) and x != '' else x
        )

# Apply deduplication to database
for col in person_cols_database:
    if col in df_database.columns:
        df_database[col] = df_database[col].map(
            lambda x: unaccented_map.get(''.join(c for c in unicodedata.normalize('NFD', str(x)) if unicodedata.category(c) != 'Mn'), x) if pd.notna(x) and x != '' else x
        )

# Re-save database with deduplicated names
df_database.to_csv(silver_dir / "database_sheet.csv", index=False)

df_repartition.to_csv(silver_dir / "repartition_sheet.csv", index=False)
logger.success("Repartition sheet cleaned and saved to SILVER")

logger.success("All sheets cleaned and saved to SILVER layer")
import janitor
from pathlib import Path
import pandas as pd
import re
from loguru import logger

############################
### CLEAN DATABASE SHEET ###
############################

logger.info("Starting to clean Database sheet...")
# Reads and regex
df_database = (
    pd.read_csv(Path("data/excel_database/sheets/bronze") / "database_sheet.csv") #type: ignore <-- pylance error on pyjanitor syntax
    .clean_names(case_type="snake", strip_accents=True) 
    .rename({"end_date_of_o&m_contract":"end_date_of_om_contract"}, axis=1)
    .fillna("") # avoid NaN to become "Nan" 
    .map(lambda x: re.sub(r'\s+', ' ', x) if isinstance(x, str) else x) # avoid " / " to become "-/-" and handles multiple spaces 
    .transform_columns(["spv", "project", "customer"], lambda x: str(x).title())
    .transform_columns(["region", "departement", "commune", "head_office_address", "legal_representative", 
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
                                        ) # Handle French title case rules
    .transform_columns(["region", "departement", "commune"], lambda x: str(x).replace(" ", "-"))    
    .transform_column("duty_dreal_contact", lambda x: str(x).replace(" ", "-").replace("Dreal-", "DREAL "))    
    .transform_columns(["siret", "vat_number"], lambda x: str(x).replace(" ", ""))
    .transform_column("land_lease_payment_date", lambda x: str(x).title())
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
df_database.temps_ar_arras_en_h_ = pd.to_numeric(df_database.temps_ar_arras_en_h_, errors='coerce').astype('Float64')
df_database.temps_ar_vertou_en_h_ = pd.to_numeric(df_database.temps_ar_vertou_en_h_, errors='coerce').astype('Float64')
df_database.peages_arras = pd.to_numeric(df_database.peages_arras, errors='coerce').astype('Float64')
df_database.peages_nantes = pd.to_numeric(df_database.peages_nantes, errors='coerce').astype('Float64')
df_database.tcma_compensation_rate = pd.to_numeric(df_database.tcma_compensation_rate, errors='coerce').astype('Float64')
df_database.financial_guarantee_amount = pd.to_numeric(df_database.financial_guarantee_amount, errors='coerce').astype('Float64')
df_database.vppa_tariff_mwh = pd.to_numeric(df_database.vppa_tariff_mwh, errors='coerce').astype('Float64')
df_database.production_target_bank_mwh_an_ = pd.to_numeric(df_database.production_target_bank_mwh_an_, errors='coerce').astype('Float64')
df_database.productible_actual_2020_mwh_ = pd.to_numeric(df_database.productible_actual_2020_mwh_, errors='coerce').astype('Float64')
df_database.productible_actual_2021_mwh_ = pd.to_numeric(df_database.productible_actual_2021_mwh_, errors='coerce').astype('Float64')
df_database.productible_actual_2022_mwh_ = pd.to_numeric(df_database.productible_actual_2022_mwh_, errors='coerce').astype('Float64')
df_database.productible_actual_2023_mwh_ = pd.to_numeric(df_database.productible_actual_2023_mwh_, errors='coerce').astype('Float64')
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


### saves
df_database.to_csv(Path("data/excel_database/sheets/silver") / "database_sheet_silver.csv", index=False)
logger.info("Database sheet cleaned and saved to silver layer")


###########################
### CLEAN DB WTG ##########
###########################

# reads
df_dbwtg = (
    pd.read_csv(Path("data/excel_database/sheets/bronze") / "dbwtg_sheet.csv") #type: ignore <-- pylance error on pyjanitor syntax
    .clean_names(case_type="snake", strip_accents=True)
    .fillna("")
    .transform_columns(["spv", "project"], lambda x: str(x).title())
)
# converts
df_dbwtg.wtg_serial_number = pd.to_numeric(df_dbwtg.wtg_serial_number, errors='coerce').astype('Int64')
df_dbwtg.cod = pd.to_datetime(df_dbwtg.cod, errors='coerce')
#saves
df_dbwtg.to_csv(Path("data/excel_database/sheets/silver") / "dbwtg_sheet_silver.csv", index=False)
logger.info("DB WTG sheet cleaned and saved to silver layer")



###########################
###  CLEAN DB GRID #########
###########################

db_dbgrid = (
    pd.read_csv(Path("data/excel_database/sheets/bronze") / "dbgrid_sheet.csv") #type: ignore <-- pylance error on pyjanitor syntax
    .clean_names(case_type="snake", strip_accents=True)
    .fillna("")
    .transform_columns(["customer", "spv", "project", "nom_du_pdl", "grid_operator", "pdl_service_company", ], lambda x: str(x).title())
)

db_dbgrid.to_csv(Path("data/excel_database/sheets/silver") / "dbgrid_sheet_silver.csv", index=False)
logger.info("DB Grid sheet cleaned and saved to silver layer")

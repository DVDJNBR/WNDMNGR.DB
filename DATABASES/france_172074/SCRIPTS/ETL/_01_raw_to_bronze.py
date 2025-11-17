from pathlib import Path
import pandas as pd
from loguru import logger
import pdfplumber

# Configuration
DATABASE_EXCEL_FILENAME = "2025_Base De Donnée_V1.xlsx"
DATABASE_EXCEL_PATH = Path("P:") / "windmanager" / "00_Share point general" / DATABASE_EXCEL_FILENAME

# Paths (absolute from repository root)
root_path = Path(__file__).parent.parent.parent.parent.parent  # Go up to repo root
REPARTITION_PDF_PATH = root_path / 'DATABASES' / 'france_172074' / 'DATA' / '2025.11.06_Répartition des parcs.pdf'

# Architecture Medallion
BRONZE_DIR = root_path / 'DATABASES' / 'france_172074' / 'DATA' / 'BRONZE'
BRONZE_DIR.mkdir(parents=True, exist_ok=True)

###########################
### READ DATABASE SHEET ###
###########################
logger.info("Reading Database sheet...")
(
    pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DataBase', header=1)
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(BRONZE_DIR / 'database_sheet.csv', index=False, encoding='utf-8-sig')
)
logger.success("Database sheet exported to BRONZE")

###########################
### READ DB GRID SHEET ###
##########################
logger.info("Reading DB GRID sheet...")
(
    pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DB GRID')
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(BRONZE_DIR / 'dbgrid_sheet.csv', index=False, encoding='utf-8-sig')
)
logger.success("DB GRID sheet exported to BRONZE")

##########################
### READ DB WTG SHEET ###
##########################
logger.info("Reading DB WTG sheet...")
(
    pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DB WTG')
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(BRONZE_DIR / 'dbwtg_sheet.csv', index=False, encoding='utf-8-sig')
)
logger.success("DB WTG sheet exported to BRONZE")

################################
### READ REPARTITION PDF ###
################################
logger.info("Reading Repartition PDF...")
with pdfplumber.open(REPARTITION_PDF_PATH) as pdf:
    raw_tables = pdf.pages[0].extract_tables()
    df_repartition = pd.DataFrame(data=raw_tables[0][1:], columns=raw_tables[0][0])

df_repartition.to_csv(BRONZE_DIR / 'repartition_sheet.csv', index=False, encoding='utf-8-sig')
logger.success("Repartition sheet exported to BRONZE")
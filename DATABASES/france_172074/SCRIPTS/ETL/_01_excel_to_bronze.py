from pathlib import Path
import pandas as pd
from loguru import logger

# Configuration
DATABASE_EXCEL_FILENAME = "2025_Base De Donnée_V1.xlsx"
DATABASE_EXCEL_PATH = Path("P:") / "windmanager" / "00_Share point general" / DATABASE_EXCEL_FILENAME

# Architecture Medallion
BRONZE_DIR = Path('DATABASES') / 'france_172074' / 'BRONZE'
BRONZE_DIR.mkdir(parents=True, exist_ok=True)

###########################
### READ DATABASE SHEET ###
###########################
logger.info("Reading Database sheet...")
(
    pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DataBase', header=1)
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(BRONZE_DIR / 'database_sheet.csv', index=False)
)
logger.success("Database sheet exported to BRONZE")

###########################
### READ DB GRID SHEET ###
##########################
logger.info("Reading DB GRID sheet...")
(
    pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DB GRID')
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(BRONZE_DIR / 'dbgrid_sheet.csv', index=False)
)
logger.success("DB GRID sheet exported to BRONZE")

##########################
### READ DB WTG SHEET ###
##########################
logger.info("Reading DB WTG sheet...")
(
    pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DB WTG')
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(BRONZE_DIR / 'dbwtg_sheet.csv', index=False)
)
logger.success("DB WTG sheet exported to BRONZE")
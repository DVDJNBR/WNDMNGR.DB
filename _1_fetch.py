from pathlib import Path
import pandas as pd
from loguru import logger

# Configuration
database_excel_filename = "2025_Base De Donnée_V1.xlsx"
database_excel_path = Path("P:") / "windmanager" / "00_Share point general" / database_excel_filename
output_dir = Path('data') / 'excel_database' / 'sheets' / 'bronze'
output_dir.mkdir(parents=True, exist_ok=True)

##############################
### READ DATABASE SHEET ###
##############################
logger.info("Reading Database sheet...")
(
    pd.read_excel(database_excel_path, sheet_name='DataBase', header=1)
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(output_dir / 'database_sheet.csv', index=False)
)
logger.success("Database sheet exported to CSV")

##############################
### READ DB GRID SHEET ###
##############################
logger.info("Reading DB GRID sheet...")
(
    pd.read_excel(database_excel_path, sheet_name='DB GRID')
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(output_dir / 'dbgrid_sheet.csv', index=False)
)
logger.success("DB GRID sheet exported to CSV")

##############################
### READ DB WTG SHEET ###
##############################
logger.info("Reading DB WTG sheet...")
(
    pd.read_excel(database_excel_path, sheet_name='DB WTG')
    .dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')
    .to_csv(output_dir / 'dbwtg_sheet.csv', index=False)
)
logger.success("DB WTG sheet exported to CSV")

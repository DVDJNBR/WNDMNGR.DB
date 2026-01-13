from pathlib import Path
import pandas as pd
from loguru import logger
import pdfplumber

# Configuration
DATABASE_EXCEL_FILENAME = "2025_Base De Donnée_V1.xlsx"
DATABASE_EXCEL_PATH = Path("P:") / "windmanager" / "00_Share point general" / DATABASE_EXCEL_FILENAME

# Paths (absolute from repository root)
root_path = Path(__file__).parent.parent.parent  # SCRIPTS/ETL/ -> root
REPARTITION_PDF_PATH = root_path / 'DATA' / '2025.12.09_Répartition des parcs.pdf'

# Architecture Medallion
BRONZE_DIR = root_path / 'DATA' / 'BRONZE'
BRONZE_DIR.mkdir(parents=True, exist_ok=True)

################################
### READ REPARTITION PDF ###
################################
logger.info("Reading Repartition PDF...")
with pdfplumber.open(REPARTITION_PDF_PATH) as pdf:
    raw_tables = pdf.pages[0].extract_tables()
    df_repartition = pd.DataFrame(data=raw_tables[0][1:], columns=raw_tables[0][0])

    # Clean column names (handle newlines from PDF wrapping)
    df_repartition.columns = df_repartition.columns.str.replace('\n', ' ', regex=False).str.strip()
    logger.info(f"Columns found: {df_repartition.columns.tolist()}")

# Filter out Statkraft-owned farms (no longer managed)
logger.info("Filtering out Statkraft-owned farms...")
initial_count = len(df_repartition)
df_repartition = df_repartition[df_repartition['Owner of WF'] != 'Statkraft']
filtered_count = initial_count - len(df_repartition)
logger.info(f"Filtered out {filtered_count} Statkraft-owned farms")

# Get list of valid farm codes (excluding Statkraft)
valid_farm_codes = df_repartition['WF Abbreviation'].unique()

df_repartition.to_csv(BRONZE_DIR / 'repartition_sheet.csv', index=False, encoding='utf-8-sig')
logger.success("Repartition sheet exported to BRONZE")

###########################
### READ DATABASE SHEET ###
###########################
logger.info("Reading Database sheet...")
df_database = pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DataBase', header=1)
df_database = df_database.dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')

# Filter to only include farms not owned by Statkraft
initial_db_count = len(df_database)
df_database = df_database[df_database['Three-letter-code'].isin(valid_farm_codes)]
db_filtered_count = initial_db_count - len(df_database)
logger.info(f"Filtered out {db_filtered_count} Statkraft farm rows from Database sheet")

df_database.to_csv(BRONZE_DIR / 'database_sheet.csv', index=False, encoding='utf-8-sig')
logger.success("Database sheet exported to BRONZE")

###########################
### READ DB GRID SHEET ###
##########################
logger.info("Reading DB GRID sheet...")
df_grid = pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DB GRID')
df_grid = df_grid.dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')

# Filter to only include farms not owned by Statkraft
initial_grid_count = len(df_grid)
df_grid = df_grid[df_grid['Three-letter-code'].isin(valid_farm_codes)]
grid_filtered_count = initial_grid_count - len(df_grid)
logger.info(f"Filtered out {grid_filtered_count} Statkraft farm rows from DB GRID sheet")

df_grid.to_csv(BRONZE_DIR / 'dbgrid_sheet.csv', index=False, encoding='utf-8-sig')
logger.success("DB GRID sheet exported to BRONZE")

##########################
### READ DB WTG SHEET ###
##########################
logger.info("Reading DB WTG sheet...")
df_wtg = pd.read_excel(DATABASE_EXCEL_PATH, sheet_name='DB WTG')
df_wtg = df_wtg.dropna(subset=['SPV', 'Project', 'Three-letter-code'], how='all')

# Filter to only include farms not owned by Statkraft
initial_wtg_count = len(df_wtg)
df_wtg = df_wtg[df_wtg['Three-letter-code'].isin(valid_farm_codes)]
wtg_filtered_count = initial_wtg_count - len(df_wtg)
logger.info(f"Filtered out {wtg_filtered_count} Statkraft turbine rows from DB WTG sheet")

df_wtg.to_csv(BRONZE_DIR / 'dbwtg_sheet.csv', index=False, encoding='utf-8-sig')
logger.success("DB WTG sheet exported to BRONZE")
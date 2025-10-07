# from .ingestion_tracking import IngestionTracking
# from .service_report import ServiceReport
# from .service_report_checklist import ServiceReportChecklist

# Lookups
from .farm_type import FarmType
from .person_role import PersonRole
from .company_role import CompanyRole
from .maintenance_type import MaintenanceType

# Entities
from .person import Person
from .employee import Employee
from .company import Company
from .farm import Farm
from .substation import Substation
from .wind_turbine_generator import WindTurbineGenerator
from .tcma_contract import TcmaContract
from .ice_detection_system import IceDetectionSystem
from .tariff import Tariff

# Relations
from .farm_company_role import FarmCompanyRole
from .farm_ice_detection_system import FarmIceDetectionSystem
from .farm_referent import FarmReferent

# Details
from .farm_status import FarmStatus
from .drei import Drei
from .icpe import Icpe
from .farm_location import FarmLocation
from .wind_farm_turbine_detail import WindFarmTurbineDetail
from .farm_substation_detail import FarmSubstationDetail
from .farm_operation_maintenance import FarmOperationMaintenance
from .farm_administration import FarmAdministration
from .farm_target_performance import FarmTargetPerformance
from .farm_actual_performance import FarmActualPerformance
from .farm_financial_guarantee import FarmFinancialGuarantee
from .farm_legal_auditor import FarmLegalAuditor

__all__ = [
    # Existing models
    # "IngestionTracking",
    # "ServiceReport",
    # "ServiceReportChecklist",
    
    # Lookups
    "FarmType",
    "PersonRole",
    "CompanyRole",
    "MaintenanceType",
    
    # Entities
    "Person",
    "Employee",
    "Company",
    "Farm",
    "Substation",
    "WindTurbineGenerator",
    "TcmaContract",
    "IceDetectionSystem",
    "Tariff",
    
    # Relations
    "FarmCompanyRole",
    "FarmIceDetectionSystem",
    "FarmReferent",
    
    # Details
    "FarmStatus",
    "Drei",
    "Icpe",
    "FarmLocation",
    "WindFarmTurbineDetail",
    "FarmSubstationDetail",
    "FarmOperationMaintenance",
    "FarmAdministration",
    "FarmTargetPerformance",
    "FarmActualPerformance",
    "FarmFinancialGuarantee",
    "FarmLegalAuditor"
]
    

def load_all_schemas():
    """
    Loads all schemas from the models module and logs the loaded tables.
    This function ensures all models are imported and available to SQLModel.
    """
    from loguru import logger
    from sqlmodel import SQLModel
    logger.info("Starting SQLModel schema loading process...")

    # Access the global SQLModel metadata object
    metadata = SQLModel.metadata

    # Check if metadata is initialized and has tables
    if metadata and metadata.tables:
        loaded_tables = sorted(metadata.tables.keys())
        num_tables = len(loaded_tables)

        logger.info(f"Total SQLModel schemas loaded: {num_tables}")
        for table_name in loaded_tables:
            # You can log more details if needed, e.g., metadata.tables[table_name].columns.keys()
            logger.debug(f"  - Loaded table: {table_name}") 

        logger.info("SQLModel schema loading completed successfully.")
        # Optionally, log the metadata object itself for very deep debugging (can be verbose)
        # logger.debug(f"SQLModel.metadata object: {metadata}")
    else:
        logger.warning("No SQLModel schemas found or metadata is not initialized. Please verify your model definitions.")
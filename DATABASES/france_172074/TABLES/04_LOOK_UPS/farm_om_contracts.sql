IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_om_contracts'
)
BEGIN
    CREATE TABLE dbo.farm_om_contracts (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        service_contract_type NVARCHAR(100) NOT NULL,
        contract_end_date DATE NOT NULL,
        CONSTRAINT fk_fom_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
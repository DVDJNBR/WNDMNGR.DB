IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_substation_details'
)
BEGIN
    CREATE TABLE dbo.farm_substation_details (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        station_count INT NOT NULL,
        substation_service_company_uuid NVARCHAR(36) NOT NULL
    );
END
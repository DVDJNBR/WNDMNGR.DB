IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'wind_turbine_generators'
)
BEGIN
    CREATE TABLE dbo.wind_turbine_generators (
        uuid NVARCHAR(36) PRIMARY KEY,
        serial_number INT NOT NULL,
        wtg_number NVARCHAR(50) NOT NULL,
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        substation_uuid NVARCHAR(36) NOT NULL,
        manufacturer_uuid NVARCHAR(36) NOT NULL,
        wtg_type INT NOT NULL,
        commercial_operation_date DATE NOT NULL
    );
END
IF NOT EXISTS (
    SELECT *
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'dbo'
    AND TABLE_NAME = 'farm_environmental_installations'
)
BEGIN
    CREATE TABLE dbo.farm_environmental_installations (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        aip_number NVARCHAR(50),
        duty_dreal_contact NVARCHAR(100),
        prefecture_name NVARCHAR(100),
        prefecture_address NVARCHAR(255),
        CONSTRAINT fk_fenv_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
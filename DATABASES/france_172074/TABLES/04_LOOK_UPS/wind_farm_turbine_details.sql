IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'wind_farm_turbine_details'
)
BEGIN
    CREATE TABLE dbo.wind_farm_turbine_details (
        wind_farm_uuid NVARCHAR(36) PRIMARY KEY,
        wind_farm_code NVARCHAR(10) NOT NULL,
        turbine_count INT NOT NULL,
        manufacturer NVARCHAR(100) NOT NULL,
        turbine_age INT NOT NULL,
        supplier NVARCHAR(100) NOT NULL,
        hub_height_m DECIMAL(10,2) NOT NULL,
        rotor_diameter_m DECIMAL(10,2) NOT NULL,
        tip_height_m DECIMAL(10,2) NOT NULL,
        rated_power_installed_mw DECIMAL(10,2) NOT NULL,
        total_mmw DECIMAL(10,2) NOT NULL,
        last_toc DATE,
        dismantling_provision_date DATE
    );
END
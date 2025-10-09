IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_actual_performances'
)
BEGIN
    CREATE TABLE dbo.farm_actual_performances (
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        year INT NOT NULL,
        amount DECIMAL(15,2) NOT NULL,
        PRIMARY KEY (farm_uuid, year),
        CONSTRAINT fk_fap_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_statuses'
)
BEGIN
    CREATE TABLE dbo.farm_statuses (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        farm_status NVARCHAR(50) NOT NULL,
        tcma_status NVARCHAR(50) NOT NULL,
        CONSTRAINT fk_fstatus_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
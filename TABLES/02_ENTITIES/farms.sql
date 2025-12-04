IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farms'
)
BEGIN
    CREATE TABLE dbo.farms (
        uuid NVARCHAR(36) PRIMARY KEY,
        spv NVARCHAR(100) NOT NULL,
        project NVARCHAR(100) NOT NULL,
        code NVARCHAR(10) NOT NULL UNIQUE,
        farm_type_id INT NOT NULL,
        CONSTRAINT fk_farms_type FOREIGN KEY (farm_type_id) REFERENCES dbo.farm_types(id)
    );
END
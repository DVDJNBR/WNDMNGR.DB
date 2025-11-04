IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'substations'
)
BEGIN
    CREATE TABLE dbo.substations (
        uuid NVARCHAR(36) PRIMARY KEY,
        substation_name NVARCHAR(100) NOT NULL,
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        gps_coordinates NVARCHAR(50)
    );
END
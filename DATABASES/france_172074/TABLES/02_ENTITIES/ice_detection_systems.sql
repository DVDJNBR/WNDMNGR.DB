IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'ice_detection_systems'
)
BEGIN
    CREATE TABLE dbo.ice_detection_systems (
        uuid NVARCHAR(36) PRIMARY KEY,
        ids_name NVARCHAR(100) NOT NULL,
        automatic_stop BIT NOT NULL,
        automatic_restart BIT NOT NULL
    );
END
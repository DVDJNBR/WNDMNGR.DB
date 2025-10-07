-- Table: farm_ice_detection_systems
-- Description: Relations entre fermes et systèmes de détection de glace
IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_ice_detection_systems'
)
BEGIN
    CREATE TABLE dbo.farm_ice_detection_systems (
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        ice_detection_system_uuid NVARCHAR(36) NOT NULL,
    );
END
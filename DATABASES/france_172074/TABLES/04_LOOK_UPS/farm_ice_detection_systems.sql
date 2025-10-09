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
        PRIMARY KEY (farm_uuid, ice_detection_system_uuid),
        CONSTRAINT fk_fids_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
        CONSTRAINT fk_fids_system FOREIGN KEY (ice_detection_system_uuid) REFERENCES dbo.ice_detection_systems(uuid)
    );
END
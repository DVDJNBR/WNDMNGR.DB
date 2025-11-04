IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_locations'
)
BEGIN
    CREATE TABLE dbo.farm_locations (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        map_reference NVARCHAR(255),
        country NVARCHAR(100) NOT NULL,
        region NVARCHAR(100) NOT NULL,
        department NVARCHAR(100) NOT NULL,
        municipality NVARCHAR(100) NOT NULL,
        arras_round_trip_distance_km DECIMAL(10,2),
        vertou_round_trip_duration_h DECIMAL(10,2),
        arras_toll_eur DECIMAL(10,2),
        nantes_toll_eur DECIMAL(10,2),
        CONSTRAINT fk_floc_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
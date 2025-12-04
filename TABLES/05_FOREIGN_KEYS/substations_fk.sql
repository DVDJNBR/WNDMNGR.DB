IF NOT EXISTS (
    SELECT * 
    FROM sys.foreign_keys 
    WHERE name = 'fk_substations_farm' 
    AND parent_object_id = OBJECT_ID('dbo.substations')
)
BEGIN
    ALTER TABLE dbo.substations 
    ADD CONSTRAINT fk_substations_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid);
END
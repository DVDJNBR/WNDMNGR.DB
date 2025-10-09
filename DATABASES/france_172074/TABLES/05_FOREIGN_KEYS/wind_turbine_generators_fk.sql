IF NOT EXISTS (
    SELECT * FROM sys.foreign_keys 
    WHERE name IN ('fk_wtg_farm', 'fk_wtg_substation', 'fk_wtg_manufacturer')
    AND parent_object_id = OBJECT_ID('dbo.wind_turbine_generators')
)
BEGIN
    ALTER TABLE dbo.wind_turbine_generators 
    ADD CONSTRAINT fk_wtg_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
        CONSTRAINT fk_wtg_substation FOREIGN KEY (substation_uuid) REFERENCES dbo.substations(uuid),
        CONSTRAINT fk_wtg_manufacturer FOREIGN KEY (manufacturer_uuid) REFERENCES dbo.companies(uuid);
END
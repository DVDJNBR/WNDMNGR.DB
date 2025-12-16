IF NOT EXISTS (
    SELECT * FROM sys.foreign_keys
    WHERE name = 'fk_wtg_farm'
    AND parent_object_id = OBJECT_ID('public.wind_turbine_generators')
)

    ALTER TABLE public.wind_turbine_generators
    ADD CONSTRAINT fk_wtg_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid);

IF NOT EXISTS (
    SELECT * FROM sys.foreign_keys
    WHERE name = 'fk_wtg_substation'
    AND parent_object_id = OBJECT_ID('public.wind_turbine_generators')
)

    ALTER TABLE public.wind_turbine_generators
    ADD CONSTRAINT fk_wtg_substation FOREIGN KEY (substation_uuid) REFERENCES public.substations(uuid);
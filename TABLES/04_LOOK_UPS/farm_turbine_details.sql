CREATE TABLE IF NOT EXISTS public.farm_turbine_details (
        wind_farm_uuid VARCHAR(36) PRIMARY KEY,
        wind_farm_code VARCHAR(10) NOT NULL,
        turbine_count INT NOT NULL,
        manufacturer VARCHAR(100) NOT NULL,
        turbine_age INT NOT NULL,
        supplier VARCHAR(100) NOT NULL,
        hub_height_m DECIMAL(10,2) NOT NULL,
        rotor_diameter_m DECIMAL(10,2) NOT NULL,
        tip_height_m DECIMAL(10,2) NOT NULL,
        rated_power_installed_mw DECIMAL(10,2) NOT NULL,
        total_mmw DECIMAL(10,2) NOT NULL,
        last_toc DATE,
        dismantling_provision_date DATE,
        CONSTRAINT fk_ftd_farm FOREIGN KEY (wind_farm_uuid) REFERENCES public.farms(uuid)
    )
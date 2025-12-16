CREATE TABLE IF NOT EXISTS public.farm_environmental_installations (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        aip_number VARCHAR(50),
        duty_dreal_contact VARCHAR(100),
        prefecture_name VARCHAR(100),
        prefecture_address VARCHAR(255),
        CONSTRAINT fk_fenv_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    )
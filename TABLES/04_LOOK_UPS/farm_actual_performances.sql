CREATE TABLE IF NOT EXISTS public.farm_actual_performances (
        farm_uuid VARCHAR(36) NOT NULL,
        farm_code VARCHAR(10) NOT NULL,
        year INT NOT NULL,
        amount DECIMAL(15,2) NOT NULL,
        PRIMARY KEY (farm_uuid, year),
        CONSTRAINT fk_fap_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    )
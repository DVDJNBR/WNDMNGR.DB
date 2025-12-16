CREATE TABLE IF NOT EXISTS public.farm_target_performances (
        farm_uuid VARCHAR(36) NOT NULL,
        farm_code VARCHAR(10) NOT NULL,
        year INT NOT NULL,
        amount DECIMAL(15,2) NOT NULL,
        PRIMARY KEY (farm_uuid, year),
        CONSTRAINT fk_ftp_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    )
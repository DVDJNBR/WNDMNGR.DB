CREATE TABLE IF NOT EXISTS public.farm_statuses (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        farm_status VARCHAR(50) NOT NULL,
        tcma_status VARCHAR(50) NOT NULL,
        CONSTRAINT fk_fstatus_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    )
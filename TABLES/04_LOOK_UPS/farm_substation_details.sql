CREATE TABLE IF NOT EXISTS public.farm_substation_details (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        station_count INT NOT NULL,
        substation_service_company_uuid VARCHAR(36) NOT NULL,
        CONSTRAINT fk_fsd_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid),
        CONSTRAINT fk_fsd_company FOREIGN KEY (substation_service_company_uuid) REFERENCES public.companies(uuid)
    )
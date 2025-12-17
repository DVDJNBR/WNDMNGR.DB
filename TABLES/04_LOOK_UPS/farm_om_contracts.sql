CREATE TABLE IF NOT EXISTS public.farm_om_contracts (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        service_contract_type VARCHAR(100),
        contract_end_date DATE,
        CONSTRAINT fk_fom_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    );
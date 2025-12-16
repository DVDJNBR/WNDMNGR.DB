CREATE TABLE IF NOT EXISTS public.farm_tcma_contracts (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        wf_status VARCHAR(50),
        tcma_status VARCHAR(50),
        contract_type VARCHAR(50),
        signature_date DATE,
        effective_date DATE,
        beginning_of_remuneration DATE,
        end_date DATE,
        compensation_rate DECIMAL(10,4),
        CONSTRAINT fk_tcma_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    )
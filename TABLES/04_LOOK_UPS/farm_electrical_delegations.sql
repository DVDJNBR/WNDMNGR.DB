CREATE TABLE IF NOT EXISTS public.farm_electrical_delegations (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        in_place BOOLEAN NOT NULL,
        drei_date DATE NOT NULL,
        electrical_delegate_uuid VARCHAR(36) NOT NULL,
        CONSTRAINT fk_fed_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid),
        CONSTRAINT fk_fed_delegate FOREIGN KEY (electrical_delegate_uuid) REFERENCES public.companies(uuid)
    )
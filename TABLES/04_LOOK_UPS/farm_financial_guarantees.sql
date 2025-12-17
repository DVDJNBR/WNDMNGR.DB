CREATE TABLE IF NOT EXISTS public.farm_financial_guarantees (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        amount DECIMAL(15,2),
        due_date DATE,
        CONSTRAINT fk_ffg_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    );
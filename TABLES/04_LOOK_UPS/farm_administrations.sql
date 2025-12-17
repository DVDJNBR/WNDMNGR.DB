CREATE TABLE IF NOT EXISTS public.farm_administrations (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        account_number VARCHAR(50),
        siret_number VARCHAR(20),
        vat_number VARCHAR(20),
        head_office_address VARCHAR(255),
        legal_representative VARCHAR(100),
        has_remit_subscription BOOLEAN,
        financial_guarantee_amount DECIMAL(15,2),
        financial_guarantee_due_date DATE,
        land_lease_payment_date VARCHAR(50),
        windmanager_subsidiary VARCHAR(100) NOT NULL,
        CONSTRAINT fk_fadmin_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    );
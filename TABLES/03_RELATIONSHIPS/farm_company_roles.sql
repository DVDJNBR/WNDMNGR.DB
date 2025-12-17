CREATE TABLE IF NOT EXISTS public.farm_company_roles (
        farm_uuid VARCHAR(36) NOT NULL,
        farm_code VARCHAR(10) NOT NULL,
        company_uuid VARCHAR(36) NOT NULL,
        company_role_id INT NOT NULL,
        PRIMARY KEY (farm_uuid, company_uuid, company_role_id),
        CONSTRAINT fk_fcr_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid),
        CONSTRAINT fk_fcr_company FOREIGN KEY (company_uuid) REFERENCES public.companies(uuid),
        CONSTRAINT fk_fcr_role FOREIGN KEY (company_role_id) REFERENCES public.company_roles(id)
    );
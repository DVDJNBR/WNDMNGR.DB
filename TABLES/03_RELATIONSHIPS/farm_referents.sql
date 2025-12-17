CREATE TABLE IF NOT EXISTS public.farm_referents (
        uuid VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid(),
        farm_uuid VARCHAR(36) NOT NULL,
        farm_code VARCHAR(10) NOT NULL,
        person_role_id INT,
        company_role_id INT,
        person_uuid VARCHAR(36),
        company_uuid VARCHAR(36),
        CONSTRAINT fk_fr_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid),
        CONSTRAINT fk_fr_person_role FOREIGN KEY (person_role_id) REFERENCES public.person_roles(id),
        CONSTRAINT fk_fr_company_role FOREIGN KEY (company_role_id) REFERENCES public.company_roles(id),
        CONSTRAINT fk_fr_person FOREIGN KEY (person_uuid) REFERENCES public.persons(uuid),
        CONSTRAINT fk_fr_company FOREIGN KEY (company_uuid) REFERENCES public.companies(uuid),
        CONSTRAINT chk_referent_type CHECK (
            (person_uuid IS NOT NULL AND person_role_id IS NOT NULL AND company_uuid IS NULL AND company_role_id IS NULL) OR
            (company_uuid IS NOT NULL AND company_role_id IS NOT NULL AND person_uuid IS NULL AND person_role_id IS NULL)
        )
    );
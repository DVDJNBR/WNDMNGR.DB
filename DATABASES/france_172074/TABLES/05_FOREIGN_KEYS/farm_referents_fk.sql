ALTER TABLE dbo.farm_referents 
ADD CONSTRAINT fk_fr_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
    CONSTRAINT fk_fr_role FOREIGN KEY (role_id) REFERENCES dbo.person_roles(id),
    CONSTRAINT fk_fr_person FOREIGN KEY (person_uuid) REFERENCES dbo.persons(uuid),
    CONSTRAINT fk_fr_company FOREIGN KEY (company_uuid) REFERENCES dbo.companies(uuid);
IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_referents'
)
BEGIN
    CREATE TABLE dbo.farm_referents (
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        person_role_id INT,
        company_role_id INT,
        person_uuid NVARCHAR(36),
        company_uuid NVARCHAR(36),
        PRIMARY KEY (farm_uuid, COALESCE(person_role_id, 0), COALESCE(company_role_id, 0)),
        CONSTRAINT fk_fr_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
        CONSTRAINT fk_fr_person_role FOREIGN KEY (person_role_id) REFERENCES dbo.person_roles(id),
        CONSTRAINT fk_fr_company_role FOREIGN KEY (company_role_id) REFERENCES dbo.company_roles(id),
        CONSTRAINT fk_fr_person FOREIGN KEY (person_uuid) REFERENCES dbo.persons(uuid),
        CONSTRAINT fk_fr_company FOREIGN KEY (company_uuid) REFERENCES dbo.companies(uuid),
        CONSTRAINT chk_referent_type CHECK (
            (person_uuid IS NOT NULL AND person_role_id IS NOT NULL AND company_uuid IS NULL AND company_role_id IS NULL) OR
            (company_uuid IS NOT NULL AND company_role_id IS NOT NULL AND person_uuid IS NULL AND person_role_id IS NULL)
        )
    );
END
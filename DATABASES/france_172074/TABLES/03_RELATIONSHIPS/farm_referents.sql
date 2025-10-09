IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_referents'
)
BEGIN
    CREATE TABLE dbo.farm_referents (
        uuid NVARCHAR(36) PRIMARY KEY,
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        role_id INT NOT NULL,
        person_uuid NVARCHAR(36),
        company_uuid NVARCHAR(36),
        CONSTRAINT fk_fr_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
        CONSTRAINT fk_fr_role FOREIGN KEY (role_id) REFERENCES dbo.person_roles(id),
        CONSTRAINT fk_fr_person FOREIGN KEY (person_uuid) REFERENCES dbo.persons(uuid),
        CONSTRAINT fk_fr_company FOREIGN KEY (company_uuid) REFERENCES dbo.companies(uuid)
    );
END
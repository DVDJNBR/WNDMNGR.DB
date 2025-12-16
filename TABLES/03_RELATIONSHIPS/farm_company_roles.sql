IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_company_roles'
)
BEGIN
    CREATE TABLE dbo.farm_company_roles (
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        company_uuid NVARCHAR(36) NOT NULL,
        company_role_id INT NOT NULL,
        PRIMARY KEY (farm_uuid, company_uuid, company_role_id),
        CONSTRAINT fk_fcr_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
        CONSTRAINT fk_fcr_company FOREIGN KEY (company_uuid) REFERENCES dbo.companies(uuid),
        CONSTRAINT fk_fcr_role FOREIGN KEY (company_role_id) REFERENCES dbo.company_roles(id)
    );
END
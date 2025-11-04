IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_legal_auditors'
)
BEGIN
    CREATE TABLE dbo.farm_legal_auditors (
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        company_uuid NVARCHAR(36) NOT NULL,
        mandate_end_date DATE NOT NULL,
        PRIMARY KEY (farm_uuid, company_uuid),
        CONSTRAINT fk_fla_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
        CONSTRAINT fk_fla_company FOREIGN KEY (company_uuid) REFERENCES dbo.companies(uuid)
    );
END
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
        company_role_uuid NVARCHAR(36) NOT NULL,
        PRIMARY KEY (farm_uuid, company_uuid, company_role_uuid)
    );
END
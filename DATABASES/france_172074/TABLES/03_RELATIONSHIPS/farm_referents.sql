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
        role_uuid NVARCHAR(36) NOT NULL,
        person_uuid NVARCHAR(36),
        company_uuid NVARCHAR(36)
    );
END
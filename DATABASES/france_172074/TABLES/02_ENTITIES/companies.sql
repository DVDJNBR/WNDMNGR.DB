IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'companies'
)
BEGIN
    CREATE TABLE dbo.companies (
        uuid NVARCHAR(36) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL
    );
END

IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'company_roles'
)
BEGIN
    CREATE TABLE dbo.company_roles (
        id INT IDENTITY(1,1) PRIMARY KEY,
        role_name NVARCHAR(50) NOT NULL UNIQUE
    );
END
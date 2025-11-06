IF NOT EXISTS (
    SELECT *
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'dbo'
    AND TABLE_NAME = 'company_roles'
)
BEGIN
    CREATE TABLE dbo.company_roles (
        id INT PRIMARY KEY,
        role_name NVARCHAR(50) NOT NULL UNIQUE
    );
END

-- Insert fixed reference values if not already present
IF NOT EXISTS (SELECT * FROM dbo.company_roles)
BEGIN
    INSERT INTO dbo.company_roles (id, role_name) VALUES
        (1, 'Asset Manager'),
        (2, 'Bank Domiciliation'),
        (3, 'Chartered Accountant'),
        (4, 'Co-developer'),
        (5, 'Customer'),
        (6, 'Energy Trader'),
        (7, 'Grid Operator'),
        (8, 'Legal Auditor'),
        (9, 'Legal Representative'),
        (10, 'OM Main Service Company'),
        (11, 'OM Service Provider'),
        (12, 'Portfolio'),
        (13, 'Project Developer'),
        (14, 'Substation Service Provider'),
        (15, 'WTG Service Provider');
END
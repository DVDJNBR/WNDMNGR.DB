IF NOT EXISTS (
    SELECT *
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'dbo'
    AND TABLE_NAME = 'person_roles'
)
BEGIN
    CREATE TABLE dbo.person_roles (
        id INT PRIMARY KEY,
        role_name NVARCHAR(50) NOT NULL UNIQUE
    );
END

-- Insert fixed reference values if not already present
IF NOT EXISTS (SELECT * FROM dbo.person_roles)
BEGIN
    INSERT INTO dbo.person_roles (id, role_name) VALUES
        (1, 'Administrative Deputy'),
        (2, 'Administrative responsible'),
        (3, 'Asset Manager'),
        (4, 'Commercial Controller'),
        (5, 'Control Room Operator'),
        (6, 'Controller Deputy'),
        (7, 'Controller Responsible'),
        (8, 'Electrical Manager'),
        (9, 'Environmental Department Manager'),
        (10, 'Field Crew Manager'),
        (11, 'HSE Coordination'),
        (12, 'Head of Technical Management'),
        (13, 'Key Account Manager'),
        (14, 'Legal Representative'),
        (15, 'Overseer'),
        (16, 'Substitute Key Account Manager'),
        (17, 'Substitute Technical Manager'),
        (18, 'Technical Manager');
END
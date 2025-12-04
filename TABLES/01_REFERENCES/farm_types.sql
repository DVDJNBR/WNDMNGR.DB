IF NOT EXISTS (
    SELECT *
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'dbo'
    AND TABLE_NAME = 'farm_types'
)
BEGIN
    CREATE TABLE dbo.farm_types (
        id INT PRIMARY KEY,
        type_title NVARCHAR(50) NOT NULL UNIQUE
    );
END

-- Insert fixed reference values if not already present
IF NOT EXISTS (SELECT * FROM dbo.farm_types)
BEGIN
    INSERT INTO dbo.farm_types (id, type_title) VALUES
        (1, 'Wind'),
        (2, 'Solar'),
        (3, 'Hybrid');
END
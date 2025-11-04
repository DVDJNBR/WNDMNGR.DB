IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_types'
)
BEGIN
    CREATE TABLE dbo.farm_types (
        id INT IDENTITY(1,1) PRIMARY KEY,
        type_title NVARCHAR(50) NOT NULL UNIQUE
    );
END
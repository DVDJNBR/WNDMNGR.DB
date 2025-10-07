IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'persons'
)
BEGIN
    CREATE TABLE dbo.persons (
        uuid NVARCHAR(36) PRIMARY KEY,
        first_name NVARCHAR(100) NOT NULL,
        last_name NVARCHAR(100) NOT NULL,
        email NVARCHAR(255) UNIQUE NOT NULL,
        mobile NVARCHAR(20),
        person_type NVARCHAR(50)
    );
END


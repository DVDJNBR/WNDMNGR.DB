IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'employees')
BEGIN
    CREATE TABLE dbo.employees (
        uuid NVARCHAR(36) PRIMARY KEY,
        person_uuid NVARCHAR(36) NOT NULL,
        trigram NVARCHAR(3) UNIQUE NOT NULL,
        landline INT,
        job_title NVARCHAR(100) NOT NULL
    );
END

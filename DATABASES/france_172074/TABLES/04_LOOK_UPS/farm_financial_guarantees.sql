IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_financial_guarantees'
)
BEGIN
    CREATE TABLE dbo.farm_financial_guarantees (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        amount DECIMAL(15,2) NOT NULL,
        due_date DATE NOT NULL
    );
END
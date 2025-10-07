IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'tcma_contracts'
)
BEGIN
    CREATE TABLE dbo.tcma_contracts (
        uuid NVARCHAR(36) PRIMARY KEY,
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        signature_date DATE NOT NULL,
        effective_date DATE NOT NULL,
        end_date DATE NOT NULL,
        compensation_rate DECIMAL(10,2) NOT NULL
    );
END
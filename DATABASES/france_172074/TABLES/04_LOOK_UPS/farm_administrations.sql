IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_administrations'
)
BEGIN
    CREATE TABLE dbo.farm_administrations (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        account_number NVARCHAR(50) NOT NULL,
        siret_number NVARCHAR(14) NOT NULL,
        vat_number NVARCHAR(20) NOT NULL,
        head_office_address NVARCHAR(255) NOT NULL,
        legal_representative NVARCHAR(100) NOT NULL,
        bank_domiciliation NVARCHAR(100) NOT NULL,
        has_remit_subscription BIT NOT NULL,
        financial_guarantee_amount DECIMAL(15,2) NOT NULL,
        financial_guarantee_date DATE NOT NULL,
        land_lease_payment_date DATE NOT NULL,
        windmanager_subsidiary NVARCHAR(100) NOT NULL,
        CONSTRAINT fk_fadmin_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
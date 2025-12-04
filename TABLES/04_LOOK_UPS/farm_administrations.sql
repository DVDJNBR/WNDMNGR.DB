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
        account_number NVARCHAR(50),
        siret_number NVARCHAR(20),
        vat_number NVARCHAR(20),
        head_office_address NVARCHAR(255),
        legal_representative NVARCHAR(100),
        has_remit_subscription BIT,
        financial_guarantee_amount DECIMAL(15,2),
        financial_guarantee_due_date DATE,
        land_lease_payment_date NVARCHAR(50),
        windmanager_subsidiary NVARCHAR(100) NOT NULL,
        CONSTRAINT fk_fadmin_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_tariffs'
)
BEGIN
    CREATE TABLE dbo.farm_tariffs (
        uuid NVARCHAR(36) PRIMARY KEY,
        farm_uuid NVARCHAR(36) NOT NULL,
        farm_code NVARCHAR(10) NOT NULL,
        aggregator_contract_signature_date DATE NOT NULL,
        aggregator_contract_start_date DATE NOT NULL,
        aggregator_contract_duration INT NOT NULL,
        has_active_edf_contract BIT NOT NULL,
        tariff_ppa_type NVARCHAR(50) NOT NULL,
        tariff_start_date DATE NOT NULL,
        tariff_end_date DATE NOT NULL,
        duration INT NOT NULL,
        energy_price_per_kwh DECIMAL(10,4) NOT NULL,
        vppa_name NVARCHAR(100),
        vppa_start_date DATE,
        vppa_duration INT,
        quantity DECIMAL(10,2),
        vppa_tariff_per_mwh DECIMAL(10,2),
        CONSTRAINT fk_ftariffs_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
IF NOT EXISTS (
    SELECT *
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'dbo'
    AND TABLE_NAME = 'farm_tcma_contracts'
)
BEGIN
    CREATE TABLE dbo.farm_tcma_contracts (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        wf_status NVARCHAR(50),
        tcma_status NVARCHAR(50),
        contract_type NVARCHAR(50),
        signature_date DATE,
        effective_date DATE,
        beginning_of_remuneration DATE,
        end_date DATE,
        compensation_rate DECIMAL(10,4),
        CONSTRAINT fk_tcma_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid)
    );
END
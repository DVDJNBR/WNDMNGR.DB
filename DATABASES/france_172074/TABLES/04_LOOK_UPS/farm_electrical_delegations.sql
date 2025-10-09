IF NOT EXISTS (
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'dbo' 
    AND TABLE_NAME = 'farm_electrical_delegations'
)
BEGIN
    CREATE TABLE dbo.farm_electrical_delegations (
        farm_uuid NVARCHAR(36) PRIMARY KEY,
        farm_code NVARCHAR(10) NOT NULL,
        in_place BIT NOT NULL,
        drei_date DATE NOT NULL,
        electrical_delegate_uuid NVARCHAR(36) NOT NULL,
        CONSTRAINT fk_fed_farm FOREIGN KEY (farm_uuid) REFERENCES dbo.farms(uuid),
        CONSTRAINT fk_fed_delegate FOREIGN KEY (electrical_delegate_uuid) REFERENCES dbo.companies(uuid)
    );
END
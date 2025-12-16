CREATE TABLE IF NOT EXISTS public.wind_turbine_generators (
        uuid VARCHAR(36) PRIMARY KEY,
        serial_number INT NOT NULL,
        wtg_number VARCHAR(50) NOT NULL,
        farm_uuid VARCHAR(36) NOT NULL,
        farm_code VARCHAR(10) NOT NULL,
        substation_uuid VARCHAR(36) NOT NULL,
        manufacturer VARCHAR(100),
        wtg_type VARCHAR(50),
        commercial_operation_date DATE
    )
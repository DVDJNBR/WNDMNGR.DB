CREATE TABLE IF NOT EXISTS public.substations (
        uuid VARCHAR(36) PRIMARY KEY,
        substation_name VARCHAR(100) NOT NULL,
        farm_uuid VARCHAR(36) NOT NULL,
        farm_code VARCHAR(10) NOT NULL,
        gps_coordinates VARCHAR(50)
    );
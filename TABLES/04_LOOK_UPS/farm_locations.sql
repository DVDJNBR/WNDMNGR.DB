CREATE TABLE IF NOT EXISTS public.farm_locations (
        farm_uuid VARCHAR(36) PRIMARY KEY,
        farm_code VARCHAR(10) NOT NULL,
        map_reference VARCHAR(255),
        country VARCHAR(100),
        region VARCHAR(100),
        department VARCHAR(100),
        municipality VARCHAR(100),
        arras_round_trip_distance_km DECIMAL(10,2),
        vertou_round_trip_duration_h DECIMAL(10,2),
        arras_toll_eur DECIMAL(10,2),
        nantes_toll_eur DECIMAL(10,2),
        CONSTRAINT fk_floc_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid)
    );
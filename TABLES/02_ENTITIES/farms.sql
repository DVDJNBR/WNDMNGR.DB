CREATE TABLE IF NOT EXISTS public.farms (
        uuid VARCHAR(36) PRIMARY KEY,
        spv VARCHAR(100) NOT NULL,
        project VARCHAR(100) NOT NULL,
        code VARCHAR(10) NOT NULL UNIQUE,
        farm_type_id INT NOT NULL,
        CONSTRAINT fk_farms_type FOREIGN KEY (farm_type_id) REFERENCES public.farm_types(id)
    )
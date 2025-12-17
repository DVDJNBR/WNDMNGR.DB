CREATE TABLE IF NOT EXISTS public.farm_ice_detection_systems (
        farm_uuid VARCHAR(36) NOT NULL,
        farm_code VARCHAR(10) NOT NULL,
        ice_detection_system_uuid VARCHAR(36) NOT NULL,
        PRIMARY KEY (farm_uuid, ice_detection_system_uuid),
        CONSTRAINT fk_fids_farm FOREIGN KEY (farm_uuid) REFERENCES public.farms(uuid),
        CONSTRAINT fk_fids_system FOREIGN KEY (ice_detection_system_uuid) REFERENCES public.ice_detection_systems(uuid)
    );
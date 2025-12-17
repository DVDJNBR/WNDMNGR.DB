CREATE TABLE IF NOT EXISTS public.ice_detection_systems (
        uuid VARCHAR(36) PRIMARY KEY,
        ids_name VARCHAR(100) NOT NULL,
        automatic_stop BOOLEAN NOT NULL,
        automatic_restart BOOLEAN NOT NULL
    );
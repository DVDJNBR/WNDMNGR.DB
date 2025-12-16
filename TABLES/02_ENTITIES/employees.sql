CREATE TABLE IF NOT EXISTS public.employees (
        uuid VARCHAR(36) PRIMARY KEY,
        person_uuid VARCHAR(36) NOT NULL,
        trigram VARCHAR(3) UNIQUE NOT NULL,
        landline INT,
        job_title VARCHAR(100) NOT NULL
    )
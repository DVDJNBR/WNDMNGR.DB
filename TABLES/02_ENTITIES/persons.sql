CREATE TABLE IF NOT EXISTS public.persons (
        uuid VARCHAR(36) PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(255),
        mobile VARCHAR(20),
        person_type VARCHAR(50)
    )
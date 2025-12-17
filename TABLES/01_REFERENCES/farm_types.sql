CREATE TABLE IF NOT EXISTS public.farm_types (
        id INT PRIMARY KEY,
        type_title VARCHAR(50) NOT NULL UNIQUE
    );

-- Insert fixed reference values if not already present
INSERT INTO public.farm_types (id, type_title) VALUES
        (1, 'Wind'),
        (2, 'Solar'),
        (3, 'Hybrid');
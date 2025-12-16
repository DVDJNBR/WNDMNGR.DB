CREATE TABLE IF NOT EXISTS public.person_roles (
        id INT PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL UNIQUE
    )

-- Insert fixed reference values if not already present
INSERT INTO public.person_roles (id, role_name) VALUES
        (1, 'Administrative Deputy'),
        (2, 'Administrative responsible'),
        (3, 'Asset Manager'),
        (4, 'Commercial Controller'),
        (5, 'Control Room Operator'),
        (6, 'Controller Deputy'),
        (7, 'Controller Responsible'),
        (8, 'Electrical Manager'),
        (9, 'Environmental Department Manager'),
        (10, 'Field Crew Manager'),
        (11, 'HSE Coordination'),
        (12, 'Head of Technical Management'),
        (13, 'Key Account Manager'),
        (14, 'Legal Representative'),
        (15, 'Overseer'),
        (16, 'Substitute Key Account Manager'),
        (17, 'Substitute Technical Manager'),
        (18, 'Technical Manager')
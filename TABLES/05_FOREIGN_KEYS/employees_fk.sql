IF NOT EXISTS (
    SELECT * 
    FROM sys.foreign_keys 
    WHERE name = 'fk_employees_person' 
    AND parent_object_id = OBJECT_ID('public.employees')
)

    ALTER TABLE public.employees 
    ADD CONSTRAINT fk_employees_person 
    FOREIGN KEY (person_uuid) REFERENCES public.persons(uuid);
IF NOT EXISTS (
    SELECT * 
    FROM sys.foreign_keys 
    WHERE name = 'fk_employees_person' 
    AND parent_object_id = OBJECT_ID('dbo.employees')
)
BEGIN
    ALTER TABLE dbo.employees 
    ADD CONSTRAINT fk_employees_person 
    FOREIGN KEY (person_uuid) REFERENCES dbo.persons(uuid);
END
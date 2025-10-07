ALTER TABLE dbo.employees 
ADD CONSTRAINT fk_employees_person FOREIGN KEY (person_uuid) REFERENCES dbo.persons(uuid);
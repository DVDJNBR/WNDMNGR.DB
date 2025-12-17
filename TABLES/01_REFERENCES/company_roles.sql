CREATE TABLE IF NOT EXISTS public.company_roles (
        id INT PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL UNIQUE
    );

-- Insert fixed reference values if not already present
INSERT INTO public.company_roles (id, role_name) VALUES
        (1, 'Asset Manager'),
        (2, 'Bank Domiciliation'),
        (3, 'Chartered Accountant'),
        (4, 'Co-developer'),
        (5, 'Customer'),
        (6, 'Energy Trader'),
        (7, 'Grid Operator'),
        (8, 'Legal Auditor'),
        (9, 'Legal Representative'),
        (10, 'OM Main Service Company'),
        (11, 'OM Service Provider'),
        (12, 'Portfolio'),
        (13, 'Project Developer'),
        (14, 'Substation Service Provider'),
        (15, 'WTG Service Provider');
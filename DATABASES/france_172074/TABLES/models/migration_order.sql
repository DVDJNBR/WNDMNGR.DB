-- Ordre d'exécution des scripts SQL pour éviter les conflits de contraintes foreign key
-- Ce script doit être exécuté dans l'ordre suivant :

-- 1. Tables de référence (sans dépendances)
-- farm_types.sql
-- person_roles.sql  
-- company_roles.sql
-- maintenance_types.sql
-- ice_detection_systems.sql

-- 2. Tables d'entités principales
-- persons.sql
-- employees.sql
-- companies.sql
-- farms.sql

-- 3. Tables dépendantes des entités principales
-- substations.sql (dépend de farms)

-- 4. Tables complexes avec multiples dépendances
-- wind_turbine_generators.sql (dépend de farms, substations, companies)
-- tcma_contracts.sql (dépend de farms)
-- tariffs.sql (dépend de farms)

-- 5. Tables de relation
-- farm_company_roles.sql (dépend de farms, companies, company_roles)
-- farm_ice_detection_systems.sql (dépend de farms, ice_detection_systems)
-- farm_referents.sql (dépend de farms, person_roles, persons, companies)

-- 6. Tables de détails (dépendent de farms)
-- drei.sql (dépend de farms, companies)
-- icpe.sql (dépend de farms)
-- farm_statuses.sql (dépend de farms)
-- farm_locations.sql (dépend de farms)
-- wind_farm_turbine_details.sql (dépend de farms)
-- farm_substation_details.sql (dépend de farms, companies)
-- farm_operation_maintenances.sql (dépend de farms)
-- farm_administrations.sql (dépend de farms)
-- farm_target_performances.sql (dépend de farms)
-- farm_actual_performances.sql (dépend de farms)
-- farm_financial_guarantees.sql (dépend de farms)
-- farm_legal_auditors.sql (dépend de farms, companies)

-- 7. Tables orphelines
-- maintenances.sql (aucune dépendance)
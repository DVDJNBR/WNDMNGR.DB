-- Contraintes FOREIGN KEY pour toutes les tables
-- À exécuter APRÈS la création de toutes les tables

-- 1. Tables de référence (lookups) - Aucune foreign key

-- 2. Entités principales
-- employees -> persons
ALTER TABLE employees ADD CONSTRAINT fk_employees_person 
FOREIGN KEY (person_uuid) REFERENCES persons(uuid);

-- farms -> farm_types
ALTER TABLE farms ADD CONSTRAINT fk_farms_type 
FOREIGN KEY (type_id) REFERENCES farm_types(id);

-- 3. Tables dépendantes
-- substations -> farms
ALTER TABLE substations ADD CONSTRAINT fk_substations_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- 4. Tables complexes
-- wind_turbine_generators -> farms, substations, companies
ALTER TABLE wind_turbine_generators ADD CONSTRAINT fk_wtg_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

ALTER TABLE wind_turbine_generators ADD CONSTRAINT fk_wtg_substation 
FOREIGN KEY (substation_uuid) REFERENCES substations(uuid);

ALTER TABLE wind_turbine_generators ADD CONSTRAINT fk_wtg_manufacturer 
FOREIGN KEY (manufacturer_uuid) REFERENCES companies(uuid);

-- tcma_contracts -> farms
ALTER TABLE tcma_contracts ADD CONSTRAINT fk_tcma_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- tariffs -> farms
ALTER TABLE tariffs ADD CONSTRAINT fk_tariffs_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- 5. Tables de relation
-- farm_company_roles -> farms, companies, company_roles
ALTER TABLE farm_company_roles ADD CONSTRAINT fk_fcr_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

ALTER TABLE farm_company_roles ADD CONSTRAINT fk_fcr_company 
FOREIGN KEY (company_uuid) REFERENCES companies(uuid);

ALTER TABLE farm_company_roles ADD CONSTRAINT fk_fcr_role 
FOREIGN KEY (company_role_uuid) REFERENCES company_roles(uuid);

-- farm_ice_detection_systems -> farms, ice_detection_systems
ALTER TABLE farm_ice_detection_systems ADD CONSTRAINT fk_fids_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

ALTER TABLE farm_ice_detection_systems ADD CONSTRAINT fk_fids_system 
FOREIGN KEY (ice_detection_system_uuid) REFERENCES ice_detection_systems(uuid);

-- farm_referents -> farms, person_roles, persons, companies
ALTER TABLE farm_referents ADD CONSTRAINT fk_fr_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

ALTER TABLE farm_referents ADD CONSTRAINT fk_fr_role 
FOREIGN KEY (role_uuid) REFERENCES person_roles(uuid);

ALTER TABLE farm_referents ADD CONSTRAINT fk_fr_person 
FOREIGN KEY (person_uuid) REFERENCES persons(uuid);

ALTER TABLE farm_referents ADD CONSTRAINT fk_fr_company 
FOREIGN KEY (company_uuid) REFERENCES companies(uuid);

-- 6. Tables de détails
-- drei -> farms, companies
ALTER TABLE drei ADD CONSTRAINT fk_drei_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

ALTER TABLE drei ADD CONSTRAINT fk_drei_delegate 
FOREIGN KEY (electrical_delegate_uuid) REFERENCES companies(uuid);

-- icpe -> farms
ALTER TABLE icpe ADD CONSTRAINT fk_icpe_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- farm_statuses -> farms
ALTER TABLE farm_statuses ADD CONSTRAINT fk_fs_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- farm_locations -> farms
ALTER TABLE farm_locations ADD CONSTRAINT fk_fl_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- wind_farm_turbine_details -> farms
ALTER TABLE wind_farm_turbine_details ADD CONSTRAINT fk_wftd_farm 
FOREIGN KEY (wind_farm_uuid) REFERENCES farms(uuid);

-- farm_substation_details -> farms, companies
ALTER TABLE farm_substation_details ADD CONSTRAINT fk_fsd_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

ALTER TABLE farm_substation_details ADD CONSTRAINT fk_fsd_company 
FOREIGN KEY (substation_service_company_uuid) REFERENCES companies(uuid);

-- farm_operation_maintenances -> farms
ALTER TABLE farm_operation_maintenances ADD CONSTRAINT fk_fom_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- farm_administrations -> farms
ALTER TABLE farm_administrations ADD CONSTRAINT fk_fa_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- farm_target_performances -> farms
ALTER TABLE farm_target_performances ADD CONSTRAINT fk_ftp_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- farm_actual_performances -> farms
ALTER TABLE farm_actual_performances ADD CONSTRAINT fk_fap_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- farm_financial_guarantees -> farms
ALTER TABLE farm_financial_guarantees ADD CONSTRAINT fk_ffg_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

-- farm_legal_auditors -> farms, companies
ALTER TABLE farm_legal_auditors ADD CONSTRAINT fk_fla_farm 
FOREIGN KEY (farm_uuid) REFERENCES farms(uuid);

ALTER TABLE farm_legal_auditors ADD CONSTRAINT fk_fla_company 
FOREIGN KEY (company_uuid) REFERENCES companies(uuid);
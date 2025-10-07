ALTER TABLE dbo.farms 
ADD CONSTRAINT fk_farms_type FOREIGN KEY (type_id) REFERENCES dbo.farm_types(id);
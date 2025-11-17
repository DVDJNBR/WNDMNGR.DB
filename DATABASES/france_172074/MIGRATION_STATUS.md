# État de Migration des Colonnes - Base de Données France 172074

Ce document suit l'état de migration des colonnes des trois feuilles Excel sources vers la base de données SQL Server.

**Instructions :** Cochez une seule case par ligne pour indiquer le statut de chaque colonne.

--- 

## 1. Feuille "DataBase" (database_sheet.csv)

**Progression :** 36.6% (45/123 colonnes migrées)

| Colonne | Migrée | À migrer | Non nécessaire | Destination / Notes |
|---------|:------:|:--------:|:--------------:|---------------------|
| SPV | [x] | [ ] | [ ] | `farms.spv` |
| Project | [x] | [ ] | [ ] | `farms.project` |
| Three-letter-code | [x] | [ ] | [ ] | `farms.code` |
| Customer | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Customer) |
| Account number | [x] | [ ] | [ ] | `farm_administrations.account_number` |
| WF qty | [ ] | [x] | [ ] | |
| Project type | [ ] | [x] | [ ] | |
| WF status | [ ] | [x] | [ ] | |
| TCMA Status | [ ] | [x] | [ ] | |
| Map reference | [x] | [ ] | [ ] | `farm_locations.map_reference` |
| Region | [x] | [ ] | [ ] | `farm_locations.region` |
| Département | [x] | [ ] | [ ] | `farm_locations.department` |
| Commune | [x] | [ ] | [ ] | `farm_locations.municipality` |
| KM AR Arras | [x] | [ ] | [ ] | `farm_locations.arras_round_trip_distance_km` |
| KM AR Nantes | [ ] | [ ] | [x] | Pas implémenté (seulement Arras stocké) |
| Temps AR Arras (en h) | [ ] | [ ] | [x] | Pas implémenté (seulement Vertou stocké) |
| Temps AR Vertou (en h) | [x] | [ ] | [ ] | `farm_locations.vertou_round_trip_duration_h` |
| PEAGES Arras | [x] | [ ] | [ ] | `farm_locations.arras_toll_eur` |
| Peages Nantes | [x] | [ ] | [ ] | `farm_locations.nantes_toll_eur` |
| SIRET | [x] | [ ] | [ ] | `farm_administrations.siret_number` |
| VAT number | [x] | [ ] | [ ] | `farm_administrations.vat_number` |
| Head office address | [x] | [ ] | [ ] | `farm_administrations.head_office_address` |
| Legal representative | [x] | [ ] | [ ] | `farm_administrations.legal_representative` + `persons` ou `companies` |
| Bank domiciliation | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Bank Domiciliation) |
| REMIT subscription | [x] | [ ] | [ ] | `farm_administrations.has_remit_subscription` |
| portfolio name | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Portfolio) |
| Asset Manager | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Asset Manager) |
| Project developer | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Project Developer) |
| Co-developper | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Co-developer) |
| Number of WEC | [ ] | [x] | [ ] | |
| type of WEC | [ ] | [x] | [ ] | |
| WEC Age | [ ] | [x] | [ ] | |
| WEC Supplier | [ ] | [x] | [ ] | |
| Hub Height (m) | [ ] | [x] | [ ] | |
| Rotor diam (m) | [ ] | [x] | [ ] | |
| Tip Height (m) | [ ] | [x] | [ ] | |
| rated power (MW) installed | [ ] | [x] | [ ] | |
| total MW | [ ] | [x] | [ ] | |
| Last TOC | [ ] | [x] | [ ] | |
| WEC service company | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: WTG Service Provider) |
| transfer station / power station | [ ] | [x] | [ ] | |
| Transfer station/power station service company | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Substation Service Provider) |
| Grid operator | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Grid Operator) |
| Contract type | [ ] | [x] | [ ] | |
| TCMA signature date | [ ] | [x] | [ ] | |
| TCMA Entrée en vigueur | [ ] | [x] | [ ] | |
| Beginning of remuneration | [ ] | [x] | [ ] | |
| End date of TCMA | [ ] | [x] | [ ] | |
| TCMA compensation rate | [ ] | [x] | [ ] | |
| Arras Technical Management | [ ] | [x] | [ ] | |
| Control room (L1) | [x] | [ ] | [ ] | `persons` + `farm_referents` (role: Control Room Operator) |
| Technical Operations Management (L2) | [ ] | [x] | [ ] | |
| Field Crew | [x] | [ ] | [ ] | `persons` + `farm_referents` (role: Field Crew Manager) |
| Environnemental department | [ ] | [x] | [ ] | |
| DREI in place | [ ] | [x] | [ ] | |
| DREI Date | [ ] | [x] | [ ] | |
| Délegataire Electrique NF C18-510 | [ ] | [x] | [ ] | |
| Sub Délegataire Electrique NF C18-510 | [ ] | [x] | [ ] | |
| Electrical Engineering | [ ] | [x] | [ ] | |
| HSE Coordination | [x] | [ ] | [ ] | `persons` + `farm_referents` (role: HSE Coordination) |
| TM | [ ] | [x] | [ ] | |
| Substitute TM | [ ] | [x] | [ ] | |
| Ice detection system | [ ] | [x] | [ ] | |
| Overseer | [x] | [ ] | [ ] | `persons` + `farm_referents` (role: Overseer) |
| Main Service company | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: OM Main Service Company) |
| Service provider | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: OM Service Provider) |
| Service contract type | [x] | [ ] | [ ] | `farm_om_contracts.service_contract_type` |
| End date of O&M contract | [x] | [ ] | [ ] | `farm_om_contracts.contract_end_date` |
| Key account manager | [ ] | [x] | [ ] | |
| Substitute key account manager | [ ] | [x] | [ ] | |
| Commercial controller | [x] | [ ] | [ ] | `persons` + `farm_referents` (role: Commercial Controller) |
| substitute commercial controller | [ ] | [x] | [ ] | |
| Accountant | [ ] | [x] | [ ] | |
| Substitute accountant | [ ] | [x] | [ ] | |
| Expert comptable Chartered accountant | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Chartered Accountant) |
| Commissaire aux comptes Legal auditor | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Legal Auditor) |
| End date of legal auditor mandate | [ ] | [x] | [ ] | |
| Energy trader | [x] | [ ] | [ ] | `companies.name` + `farm_company_roles` (role: Energy Trader) |
| Agregator contract signature date | [ ] | [x] | [ ] | |
| Start date agregator contract | [ ] | [x] | [ ] | |
| Duration aggregator contract | [ ] | [x] | [ ] | |
| Tariff aggregator | [ ] | [x] | [ ] | |
| Active EDF contract | [ ] | [x] | [ ] | |
| Tarif PPA type | [ ] | [x] | [ ] | |
| Tarif Start Date | [ ] | [x] | [ ] | |
| Tarif end date | [ ] | [x] | [ ] | |
| Duration | [ ] | [x] | [ ] | |
| Energy price per Kwh | [ ] | [x] | [ ] | |
| VPPA name | [ ] | [x] | [ ] | |
| VPPA start | [ ] | [x] | [ ] | |
| VAPP duration | [ ] | [x] | [ ] | |
| Quantity | [ ] | [x] | [ ] | |
| VPPA tariff /MWh | [ ] | [x] | [ ] | |
| Production target Bank (MWh/an) | [ ] | [x] | [ ] | |
| Production target Investor (MWh/an) | [ ] | [x] | [ ] | |
| Productible Actual 2020 (MWh) | [ ] | [x] | [ ] | |
| Productible Actual 2021 (MWh) | [ ] | [x] | [ ] | |
| Productible Actual 2022 (MWh) | [ ] | [x] | [ ] | |
| Productible Actual 2023 (MWh) | [ ] | [x] | [ ] | |
| Revenue target 2020 | [ ] | [x] | [ ] | |
| Revenue target 2021 | [ ] | [x] | [ ] | |
| Revenue target 2022 | [ ] | [x] | [ ] | |
| Revenue target 2023 | [ ] | [x] | [ ] | |
| Revenue target 2024 | [ ] | [x] | [ ] | |
| Revenue Actual 2020 | [ ] | [x] | [ ] | |
| Revenue Actual 2021 | [ ] | [x] | [ ] | |
| Revenue Actual 2022 | [ ] | [x] | [ ] | |
| Revenue Actual 2023 | [ ] | [x] | [ ] | |
| AIP Number | [x] | [ ] | [ ] | `farm_environmental_installations.aip_number` |
| Duty DREAL contact | [x] | [ ] | [ ] | `farm_environmental_installations.duty_dreal_contact` |
| Prefecture Name | [x] | [ ] | [ ] | `farm_environmental_installations.prefecture_name` |
| Prefecture address | [x] | [ ] | [ ] | `farm_environmental_installations.prefecture_address` |
| Financial guarantee amount | [x] | [ ] | [ ] | `farm_financial_guarantees.amount` |
| Financial guarantee due date | [x] | [ ] | [ ] | `farm_financial_guarantees.due_date` |
| Dismantling provision indexation date | [ ] | [x] | [ ] | |
| Land lease payment date | [x] | [ ] | [ ] | `farm_administrations.land_lease_payment_date` |
| Country | [x] | [ ] | [ ] | `farm_locations.country` |
| windmanager subsidiary | [x] | [ ] | [ ] | `farm_administrations.windmanager_subsidiary` |

---

## 2. Feuille "DB GRID" (dbgrid_sheet.csv)

**Progression :** 0.0% (0/10 colonnes migrées)

| Colonne | Migrée | À migrer | Non nécessaire | Destination / Notes |
|---------|:------:|:--------:|:--------------:|---------------------|
| Customer | [ ] | [x] | [ ] | |
| Nom des Parcs Eoliens | [ ] | [x] | [ ] | |
| SPV | [ ] | [x] | [ ] | |
| Project | [ ] | [x] | [ ] | |
| Three-letter-code | [ ] | [x] | [ ] | |
| Nom du PDL | [ ] | [x] | [ ] | |
| Grid operator | [ ] | [x] | [ ] | |
| PDL Service company | [ ] | [x] | [ ] | |
| Coordonnées GPS | [ ] | [x] | [ ] | |
| Communes ( Departements) | [ ] | [x] | [ ] | |

---

## 3. Feuille "DB WTG" (dbwtg_sheet.csv)

**Progression :** 0.0% (0/14 colonnes migrées)

| Colonne | Migrée | À migrer | Non nécessaire | Destination / Notes |
|---------|:------:|:--------:|:--------------:|---------------------|
| Three-letter-code | [ ] | [x] | [ ] | |
| SPV | [ ] | [x] | [ ] | |
| Project | [ ] | [x] | [ ] | |
| WF name in Rotorsoft | [ ] | [x] | [ ] | |
| WTG serial number | [ ] | [x] | [ ] | |
| Num WTG | [ ] | [x] | [ ] | |
| COD | [ ] | [x] | [ ] | Commercial Operation Date |
| WTG type | [ ] | [x] | [ ] | |
| WTG version | [ ] | [x] | [ ] | |
| Manufacturer | [ ] | [x] | [ ] | |
| Hub height [m] | [ ] | [x] | [ ] | |
| Rotor diameter [m] | [ ] | [x] | [ ] | |
| Tip Height (m) | [ ] | [x] | [ ] | |
| Rated Power [MW] | [ ] | [x] | [ ] | |

---

## Résumé Global

| Feuille | Total | Migrées | À migrer | Non nécessaires | Progression |
|---------|:-----:|:-------:|:--------:|:---------------:|:-----------:|
| **DataBase** | 123 | 45 | 76 | 2 | **36.6%** |
| **DB GRID** | 10 | 0 | 10 | 0 | **0.0%** |
| **DB WTG** | 14 | 0 | 14 | 0 | **0.0%** |
| **TOTAL** | **147** | **45** | **100** | **2** | **31.0%** |

---

**Dernière mise à jour :** 2025-11-17

**Note :** Le calcul du pourcentage de progression est basé sur : `Migrées / (Migrées + À migrer) × 100`

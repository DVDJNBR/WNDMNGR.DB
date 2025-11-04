# CHANGELOG



## v0.1.0 (2025-11-04)

### Ci

* ci: add semantic release workflow and enhance ETL pipeline

- Add GitHub Actions workflow for automated semantic versioning
- Configure python-semantic-release in pyproject.toml
- Add validation tasks to ETL pipeline (validate_silver, validate_gold)
- Fix person extraction regex in silver_to_gold script
- Update administrative_controller to administrative_responsible

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`2cc4a9c`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/2cc4a9c34b448a516f6b88d45e052a8841b6ca88))

### Feature

* feat(etl): add new person roles and UTF-8 encoding support

- Add UTF-8-sig encoding across all ETL pipeline files
- Add new person roles: Overseer, Commercial Controller
- Integrate database_sheet person columns (control_room_l1, field_crew, hse_coordination, overseer, commercial_controller, substitute_commercial_controller)
- Implement company filtering using keywords to exclude entities like &#34;Société Seris&#34;, &#34;Statkraft France&#34;
- Add Louis Chenel as Head of Technical Management for all farms

Results:
- Persons: 27 → 63 (+36)
- Person roles: 16 → 18 (+2)
- Farm referents: 422 → 716 (+294 relationships)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`21371aa`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/21371aafdfb26f3179e29b212fde668d5307be1f))

* feat(etl): complete gold layer with all company and person relationships

- Refactored silver_to_gold ETL pipeline with clean entity-first architecture
- Added distinction between person and company roles for farm relationships
- Split farm_referents.role_id into person_role_id and company_role_id with proper constraints
- Normalized customer column with .title() in bronze_to_silver

Entities created:
- 65 companies (customers, portfolios, asset managers, developers, service providers, banks, auditors, traders, grid operators)
- 27 persons (technical managers, controllers, administrators, legal representatives)
- 47 farms

Relationships created:
- 422 farm_referents (person-farm relationships with 16 person roles)
- 557 farm_company_roles (company-farm relationships with 15 company roles)

All database_sheet columns integrated:
- Customer, Portfolio, Asset Manager, Project Developer, Co-developer
- Legal Representative (person &amp; company), OM Main/Service, WTG Service, Substation Service
- Chartered Accountant, Legal Auditor, Energy Trader, Grid Operator, Bank Domiciliation

Test scripts added:
- view_farm_referents.py: person relationships view
- view_farm_company_roles.py: company relationships view
- Output saved to TESTS/DATA/ (gitignored)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`3e3dc30`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/3e3dc3022461c894caf8ae3835dcec645177c6d8))

### Unknown

* Merge branch &#39;FT/DB_MODEL&#39; into main

Completed database model implementation with ETL pipeline enhancements:
- Added UTF-8 encoding support across all ETL files
- Integrated new person roles (Overseer, Commercial Controller)
- Added database_sheet person columns extraction
- Implemented Louis Chenel as Head of Technical Management for all farms

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`a6e6d6e`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/a6e6d6e8a607eb74cc2ff50ff492588960da3022))

* Ingestion on a good way .... need to fix etl for pipeline 16-10 ([`f1d3f12`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/f1d3f124547cb8788fdd54246eb02120c120eda4))

* Modeling ok (change persons) + switching to star schema ([`ba19926`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/ba199264dbeb4478d3488c5ea2914abd2841c213))

* FIXED(bronze to silver) ([`7103727`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/71037270b006cf5de87fa3d3c2703582b8ad21cf))

* Data model ok ... switching to ETL ([`b4ce816`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/b4ce81637eda82e3a9e747492b75e590541ef199))

* Added FK sql scripts ([`b679118`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/b679118256ea5c121d72f93178c8ceb35c895906))

* :construction: Feat(DDL)Script for tables definitions working. Needs FK and .py rewriting ([`2588b9f`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/2588b9f60f9018678ff72d9f52648c6f5cfac95b))

* SQL Server Data modeling after connexion success ([`1935a98`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/1935a98acec2ac1819e9a113f01178c65fd839c2))

* Initial commit ([`20c0af7`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/20c0af72ff896c21d693b467e62868e0658452c0))

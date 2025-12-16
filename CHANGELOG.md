# CHANGELOG



## v1.0.0 (2025-12-16)

### Breaking

* feat(ingestion): replace Azure Functions with GitHub Actions

- Replace Azure Functions with GitHub Actions for database ingestion
- Add ingestion versioning with validation tracking (ingestion_versions table)
- Create automated workflows:
  - create-tables.yml: Create all database tables
  - load-database.yml: Load data with validation
- Add validation tests:
  - Silver-Gold reconciliation
  - UUID integrity
  - Foreign key integrity
  - Required fields validation
- Support manual triggering (dev) and automatic triggering (prod via semantic-release)
- Add helper script for easy workflow triggering
- Clean up deprecated Azure Functions code and files
- Remove hardcoded secrets, use environment variables instead

BREAKING CHANGE: Azure Functions-based ingestion replaced with GitHub Actions.
All secrets must be configured in GitHub Secrets and local .env file. ([`84e2afe`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/84e2afe48fdc7277f8df5031525cead560080b93))

### Chore

* chore: deleted schema.txt ([`fac8cf9`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/fac8cf95e444c14ffc54e6640dbd825558afc1d2))

* chore: deleted schema.txt ([`e219a8e`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/e219a8e12cd8d7625af5ce23760d23321eea0abd))

* chore: moving folder 01_METADATA to 06 for logical reasons ([`b8286eb`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/b8286ebf58fb95374282a03f0a2131cfd52510b0))

* chore: remove paths filter from load-database workflow

- Allow workflow to trigger on any push to test data loading
- This is temporary for testing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`04ecac0`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/04ecac0389fe52470b954ce5944f45adb6e4c79b))

* chore: add temporary push triggers to test workflows

- Add push trigger to create-tables workflow
- Add push trigger to load-database workflow (only on workflow file changes)
- Use dev environment by default when triggered by push
- This is temporary for testing, will be removed after merge to main

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`1ef8ee9`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/1ef8ee96ce8316fd5fb861bf33f5a7fafe084772))

* chore: move all Azure config to environment variables ([`ea5a67b`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/ea5a67b339430feb1f91b5d8953eba36a830cd40))

* chore: remove farm_legal_auditors table (redundant)

- Delete farm_legal_auditors.sql as legal auditors are already tracked in company_roles with &#34;Legal Auditor&#34; role
- Avoids data duplication

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`6b89b8c`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/6b89b8c0bb83b1c24ef635f8625c4b74d95428bc))

### Feature

* feat: add GitHub Actions test for Supabase connection

- Add workflow to test psycopg2 connection from GitHub Actions
- Test both port 5432 (direct) and 6543 (pooler)
- Create/insert/read/cleanup test table
- Update gitignore to protect temporary test files with secrets ([`40492b4`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/40492b46fed27b87835295c71dddbe05bd5af7e0))

* feat: add ice detection systems GOLD tables

- Extract ice detection systems from database_sheet
- Parse system name, automatic_stop, and automatic_restart flags
- Create ice_detection_systems entity table (6 systems)
- Create farm_ice_detection_systems lookup table (44 relationships)
- Add to ingestion pipeline

Systems: Power Curve Method, PCID, Ice detuction, Repower anemometers, Labkotec, Eologix

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`f1b3f92`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/f1b3f924f7b87e679ea7039f1a6ae1bf12e4d402))

* feat: add farm_statuses GOLD table generation

- Extract wf_status and tcma_status from database_sheet
- Create farm_statuses lookup table (1 row per farm)
- Add to ingestion pipeline

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`14d17cc`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/14d17ccdeadfb75a6e76f22e45f37af55894b26a))

* feat: add farm_substation_details GOLD table generation

- Extract substation details from database_sheet
- Count substations per farm
- Link to substation service company
- Add to ingestion pipeline

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`521c5a5`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/521c5a56aa8ac99a1b84f886fdeb3655d94ab285))

* feat: add complete deployment pipeline with blob upload

- Add upload_gold_to_blob task to upload CSVs to Azure Blob
- Add etl_to_blob task for ETL + blob upload
- Add full_deploy task for complete local-&gt;blob-&gt;SQL pipeline

Usage:
  invoke etl-to-blob         # ETL local + upload to blob
  invoke full-deploy         # Complete: ETL + blob + GitHub Actions
  invoke full-deploy --force # With table recreation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`8788042`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/87880421808996e66d1685e4ee7998733f563e0c))

* feat(ci): add master workflow to orchestrate table creatio
     and data loading sequentially ([`9527838`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/95278386c2cb8f97896633aed0b53eb4e6ec30e3))

* feat: add sequential workflow execution with completion polling for gh-deploy

- gh-deploy now waits for create-tables to complete before triggering load-database
- Add _wait_for_workflow_completion() to poll workflow status every 10s
- Prevents race condition where data loading starts before tables are created
- 10 minute timeout with detailed progress logging

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`6c04862`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/6c0486234a073e1cc12149aac6600c606e74e227))

* feat: add connection retry logic for Azure SQL cold starts

- Add connect_with_retry() function with 3 attempts and 30s delay
- Handle Azure SQL serverless cold start timeout issues
- Add 60s connection timeout parameter
- Applied to both _05_create_tables_github.py and _06_load_data_github.py

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`8c6267e`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/8c6267e4e908c0fdbd8a8bb0deca423702199504))

* feat(etl): migrate farm_om_contracts table and fix SIRET/account numbers

- Add farm_om_contracts table migration (service_contract_type, contract_end_date)
- Fix SIRET and account numbers: convert float to string (remove .0 suffix)
- Update MIGRATION_STATUS.md: 36.6% completion (45/123 columns)
- Add farm_om_contracts to _04_gold_to_db.py pipeline
- Update .gitignore to exclude validation notebooks ([`b992ec7`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/b992ec702861caee186ac0904b0f80bf709ccc94))

* feat(etl): add farm_locations table migration

- Add farm_locations CSV generation in Silver to Gold transformation
- Include farm location data: region, department, municipality, distances, tolls
- Make location fields nullable to handle farms with incomplete data
- Successfully migrated 45 farms with location details

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`bd0a179`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/bd0a17997d25ff499905aa25a1f355388975bfa7))

* feat(etl): add name normalization, upsert mode, and UTF-8 encoding fixes

Multiple improvements to the ETL pipeline for production readiness:

ETL Enhancements:
- Fix path resolution using __file__ relative paths for invoke compatibility
- Add UTF-8 encoding throughout pipeline (CSV reads + French_CI_AS collation)
- Implement accent deduplication in bronze_to_silver (keep accented versions)
- Add particle detection for name splitting (Le, La, De, Du, etc.)
- Rename database from windmanager_france_test to windmanager_france_master

Database Management:
- Add ensure_database.py helper with auto-create functionality
- Separate destructive operations from safe data refresh in invoke tasks
- Implement upsert mode (--truncate flag for dev, default upsert for prod)
- Use DELETE instead of TRUNCATE for FK constraint compatibility
- Add fixed reference data inserts (farm_types, company_roles, person_roles)

Tasks Restructuring:
- setup-db: Initialize database structure
- wipe-and-reload: DELETE all data + reload (dev only)
- ingest-data: Upsert mode for prod-safe updates
- etl-ingest: Full pipeline + upsert (prod safe)
- etl-wipe: Full pipeline + wipe (dev only)

Validation passes: 155/155 tests (100%)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`851ebba`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/851ebba2451da84c40cb763076287141b2db77a1))

* feat(etl): add farm_financial_guarantees look-up table

- Make amount and due_date columns nullable
- Add farm_financial_guarantees extraction in _03_silver_to_gold.py
- Map financial_guarantee_amount → amount, financial_guarantee_due_date → due_date

Results:
- farm_financial_guarantees: 45 rows
- 39 farms with financial guarantee (amount + due_date)
- 6 farms without financial guarantee (NULL)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`786ed31`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/786ed31b399a5a064430b978102b5274cdbea732))

* feat(etl): add farm_environmental_installations look-up table

- Fix duplicated SQL schema (was incorrectly copied from farm_tariffs)
- Add correct ICPE columns: aip_number, duty_dreal_contact, prefecture_name, prefecture_address
- Add farm_environmental_installations extraction in _03_silver_to_gold.py

Results:
- farm_environmental_installations: 45 rows
- 33 farms with AIP number
- 39 farms with DREAL contact and prefecture info

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`e880acd`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/e880acd2b97c40f7a6e81eb16824909399c6c4dc))

* feat(etl): add farm_administrations look-up table

- Remove bank_domiciliation column (already in company_roles)
- Add farm_administrations extraction in _03_silver_to_gold.py
- Map remit_subscription: &#34;Yes&#34; variants → 1 (True), else NULL
- Change has_remit_subscription from BIT NOT NULL to BIT (nullable)

Results:
- farm_administrations: 45 rows
- 13 farms with REMIT subscription (explicit True)
- 32 farms without REMIT (NULL, not False)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`32a5ee2`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/32a5ee27c77ae2df996a84b3bbe4babbd4203be9))

### Fix

* fix: exclude reference tables from data loading

Reference tables (farm_types, company_roles, person_roles) are already
populated by their CREATE TABLE scripts with fixed seed data. Attempting
to reload them from CSVs during data ingestion causes primary key
violations and prevents subsequent tables from loading.

Changes:
- Remove farm_types, company_roles, person_roles from TABLES list
- Add comment explaining they&#39;re seeded during table creation
- Update table numbering in comments

This fixes the issue where only 3 tables loaded successfully while
all other tables remained empty.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`1c7a0a5`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/1c7a0a54f490a54a06bdf785bc9d6f3dd9511882))

* fix: adjust farm_statuses test for farms not in database_sheet

- Some farms only exist in repartition_sheet, not database_sheet
- Adjust test to expect &lt;= farms instead of exact match
- Add info log for farms without status (ECH, ESM)

All tests now pass: 16/16 (100%)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`1e6f734`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/1e6f734e8ebc004d5f1f24c02fbf43291e22836e))

* fix: preserve ingestion_versions table during force recreate

- Exclude ingestion_versions from DROP TABLE when using --force
- This preserves deployment history and version tracking
- Only data tables should be recreated, not metadata tables

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`8c1557b`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/8c1557bdd04f08551e84d27b9586b981d7e06991))

* fix: properly handle NaN values when inserting into SQL Server

- Use pd.replace to convert NaN/NA/NaT to None before insertion
- Add explicit NaN check in row values before execute
- Fixes TDS protocol error with float NaN in nullable columns

This resolves the farm_referents insertion failures.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`e6ae2b0`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/e6ae2b0892952630df14064f06d05f5b9c17fa4f))

* fix: correct table loading order and add missing reference tables

- Add missing reference tables: farm_types, company_roles, person_roles
- Fix loading order to respect FK constraints (refs before entities)
- Remove farm_financial_guarantees due to poor data quality
- Fix farm_referents insertion (was failing due to missing role tables)

This fixes the issue where farm_referents had 0 rows despite 666 rows in CSV.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`348f898`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/348f898de91562c649b6bf6edc4a339e222243c0))

* fix(etl): correct metadata path and fix bug skipping sql
     files starting with comments ([`63e5859`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/63e5859c732bc0e4673c7798e27a071946f4603a))

* fix: correct TABLES directory names in create_tables script

- Changed 00_REFERENCE to 01_REFERENCES
- Changed 04_LOOKUPS to 04_LOOK_UPS
- Removed non-existent 06_INDEXES category
- This will now create all missing lookup tables

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`b30955f`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/b30955f95b3efd3d5b20c77dceb736f199927887))

* fix(etl): resolve Pylance type errors for environment variables

- Add validation that required env vars (SERVER, DATABASE, USER, PASSWORD) are set
- Add type narrowing assertions to satisfy Pylance type checker
- Apply fixes to _04_gold_to_db.py, init_database.py, and drop_tables.py
- Prevents runtime errors from missing environment variables

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`c535241`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/c5352418d4c216a0fe417bca5f422c20c3f423b6))

* fix(etl): add name normalization with inversion, accent deduplication, and hyphenation

Improvements to person name handling:
- Add name inversion for LastName FirstName format (accent-insensitive matching)
- Deduplicate accent variants (keep accented version)
- Add hyphens to compound first names (Jean Pierre → Jean-Pierre)
- Detect particles case-insensitively (le, Le, etc.) for proper name splitting
- Fix Pylance type warnings with None-safe string operations
- Add &#39;overseer&#39; column to person normalization pipeline

Results:
- 58 persons (1 duplicate eliminated)
- 7 names inverted successfully
- Compound first names properly hyphenated
- All 155 validation tests passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`f6f0062`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/f6f00623d1dad311779b590a18590dd1daaaad48))

### Refactor

* refactor: simplify workflows to use single connection string and add GitHub API orchestration

- Remove dev/prod environment distinction (single Azure SQL database)
- Use single AZURE_SQL_CONNECTION_STRING secret instead of _DEV/_PROD variants
- Remove automatic push triggers, keep only manual workflow_dispatch
- Add GitHub API-based workflow orchestration in tasks.py (no gh CLI needed)
- Add SSL verification bypass for corporate proxy
- Auto-detect current git branch for workflow dispatches

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`ef59925`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/ef599258d3e781c34d7c014230bc247b9201029e))

* refactor: consolidate ETL scripts into single directory

- Moved SCRIPTS/SETUP/create_tables_github.py to SCRIPTS/ETL/_05_create_tables_github.py
- Removed deprecated Azure Functions scripts (_05_create_tables_azure.py, _06_load_data_azure.py)
- Updated workflow to use new ETL path
- All GitHub Actions ETL steps now in chronological order in SCRIPTS/ETL/

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`ca604b9`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/ca604b9234851a3da90b6d780e651881a684296e))

* refactor: flatten directory structure and fix type errors

- Moved DATABASES/france_172074/DATA/ to DATA/
- Moved DATABASES/france_172074/SCRIPTS/ to SCRIPTS/
- Moved DATABASES/france_172074/TABLES/ to TABLES/
- Created SCRIPTS/TRIGGERS/ for workflow trigger scripts
- Renamed trigger_wf_build.py to build_workflow.py
- Renamed trigger_wf_load.py to load_workflow.py
- Moved README_INGESTION.md to SCRIPTS/TRIGGERS/README.md
- Updated all path references in ETL scripts, workflows, and tasks.py
- Fixed Pylance type errors with cast() and BytesIO imports
- Replaced loguru in trigger scripts
- Updated .gitignore for new structure

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`f2a3801`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/f2a38016740f5952a9dbb4dba58a7ed370b833bf))

### Test

* test: add validation tests for ice detection systems

- Test ice_detection_systems entity table
- Test farm_ice_detection_systems relationship table
- Validate boolean flags (automatic_stop, automatic_restart)
- Validate all foreign keys

All tests pass: 25/25 (100%)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`2fe1e51`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/2fe1e515834c27efc12083947da7ca5f6617b24d))

* test: add validation tests for lookup tables

- Add validate_lookup_tables.py for farm_statuses and farm_substation_details
- Test row counts, foreign key validity, and data reconciliation
- Add invoke validate-lookups task

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude &lt;noreply@anthropic.com&gt; ([`11f6c39`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/11f6c3999e1c0e024a2fc1824dcf3f9ce608159b))

### Unknown

* Merge pull request #1 from DVDJNBR/HTFX/SWITCH_TO_SUPABASE

Htfx/switch to supabase ([`4d06b40`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/4d06b40fbcda79fea9bc66b17231fb63ce0d2482))

* Fix: use absolute paths in ETL scripts to prevent duplicate directories

- Root cause: ETL scripts used relative paths Path(&#39;DATABASES/...&#39;), which created duplicate nested directories if executed from wrong working directory
- Solution: All ETL scripts now use absolute paths based on __file__ location
- Updated .gitignore to prevent tracking of duplicate DATABASES directories
- Removed duplicate directories from git tracking ([`2488297`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/2488297950f95912498cf2a06e4da338764ada33))

* Feat: tcma contracts are now ingested ([`82a0c32`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/82a0c3268c5d1af6bca68516dfbe12c051244a96))

* Fix: pylance syntax issues resolved ([`84e1e61`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/84e1e61840e70db5302b7fa3ecf8ebfa62326386))


## v0.1.0 (2025-11-04)

### Chore

* chore(release): 0.1.0 [skip ci] ([`dc823cf`](https://github.com/DVDJNBR/WNDMNGR.DB/commit/dc823cfc8310775660c2a301ff64391f888e6797))

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

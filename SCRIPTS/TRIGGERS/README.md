# Architecture d'Ingestion avec GitHub Actions

## 🎯 Vue d'ensemble

Ce système remplace les Azure Functions par GitHub Actions pour peupler la base de données Azure SQL depuis Azure Blob Storage, avec versioning et validation automatique.

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LOCAL (Ton PC)                              │
│                                                                 │
│  Pipeline ETL:                                                  │
│  _01_raw_to_bronze.py    → Bronze CSV                          │
│  _02_bronze_to_silver.py → Silver CSV                          │
│  _03_silver_to_gold.py   → Gold CSV                            │
│  _04_gold_to_blob.py     → Upload vers Azure Blob              │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Upload CSV
                         ▼
         ┌───────────────────────────────┐
         │   Azure Blob Storage          │
         │   (windmanager-data/gold/)    │
         └───────────┬───────────────────┘
                     │
                     │ Déclenche manuellement ou auto (release)
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS                                │
│                                                                 │
│  Workflow: load-database.yml                                   │
│  ├─ Vide les tables (ordre FK)                                 │
│  ├─ Télécharge CSV depuis Blob                                 │
│  ├─ Charge dans Azure SQL                                      │
│  ├─ Valide l'intégrité:                                        │
│  │  • Silver-Gold reconciliation                               │
│  │  • UUID integrity                                           │
│  │  • Foreign keys                                             │
│  │  • Required fields                                          │
│  └─ Crée version d'ingestion                                   │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Insère données
                         ▼
         ┌───────────────────────────────┐
         │   Azure SQL Database          │
         │   • Tables de données         │
         │   • ingestion_versions        │
         └───────────────────────────────┘
```

## 🔄 Workflow de Développement

### Branche `dev` (Développement)

```bash
# 1. Tu travailles sur dev
git checkout dev

# 2. (Première fois seulement) Créer les tables via GitHub Actions
# Va sur Actions → Create Tables → Run workflow → Sélectionne "dev"

# 3. Tu lances ton pipeline ETL local
python DATABASES/france_172074/SCRIPTS/ETL/_01_raw_to_bronze.py
python DATABASES/france_172074/SCRIPTS/ETL/_02_bronze_to_silver.py
python DATABASES/france_172074/SCRIPTS/ETL/_03_silver_to_gold.py
python DATABASES/france_172074/SCRIPTS/ETL/_04_gold_to_blob.py

# 4. Tu déclenches manuellement l'ingestion (3 options):

## Option A: Via GitHub UI
# - Va sur https://github.com/YOUR_USERNAME/WNDMNGR.DB/actions/workflows/load-database.yml
# - Clique "Run workflow"
# - Sélectionne branche "dev" et environnement "dev"

## Option B: Via script helper
python trigger_ingestion.py --env dev --branch dev

## Option C: Via curl
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/YOUR_USERNAME/WNDMNGR.DB/actions/workflows/load-database.yml/dispatches \
  -d '{"ref":"dev","inputs":{"environment":"dev"}}'

# 4. La DB dev est peuplée avec versioning et validation
# 5. Tu peux bosser avec la DB même si les données ne sont pas finales
```

### Branche `main` (Production)

```bash
# 1. Quand tu es prêt pour la prod
git checkout main
git merge dev

# 2. Push vers main
git push origin main

# 3. Semantic Release se déclenche automatiquement:
#    - Analyse les commits conventionnels
#    - Crée un tag (ex: v1.2.3)
#    - Publie une release GitHub

# 4. La release déclenche automatiquement l'ingestion:
#    - Workflow load-database.yml s'exécute
#    - Cible l'environnement "prod"
#    - Peuple la DB prod avec validation
```

## 📊 Table de Versioning

Chaque ingestion crée une entrée dans `ingestion_versions`:

```sql
SELECT
    version_number,
    ingestion_date,
    triggered_by,
    status,
    validation_passed,
    test_silver_gold_reconciliation,
    test_uuid_integrity,
    test_foreign_keys,
    test_required_fields,
    total_rows_inserted,
    execution_time_seconds
FROM ingestion_versions
ORDER BY version_number DESC;
```

## ✅ Tests de Validation

Le script `_06_load_data_github.py` exécute 4 tests automatiques:

### 1. Silver-Gold Reconciliation
Vérifie que le nombre de lignes correspond entre Silver et Gold:
- `database_sheet.csv` ↔ `farms.csv`
- `dbwtg_sheet.csv` ↔ `wind_turbine_generators.csv`
- `dbgrid_sheet.csv` ↔ `substations.csv`

### 2. UUID Integrity
Vérifie que tous les UUIDs sont:
- Non NULL
- Uniques
- Valides (format UUID)

### 3. Foreign Keys
Vérifie l'intégrité référentielle:
- `farm_referents.farm_uuid` → `farms.uuid`
- `wind_turbine_generators.farm_uuid` → `farms.uuid`
- `substations.farm_uuid` → `farms.uuid`
- etc.

### 4. Required Fields
Vérifie que les champs critiques sont peuplés:
- `persons.first_name`, `persons.last_name`
- `companies.name`
- `farms.code`, `farms.spv`, `farms.project`
- etc.

## 🔧 Configuration Requise

### GitHub Secrets à configurer

Vai sur `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

#### Pour DEV:
```
AZURE_SQL_CONNECTION_STRING_DEV=
"Driver={ODBC Driver 18 for SQL Server};
Server=tcp:sql-windmanager-france-dev.database.windows.net,1433;
Database=sqldb-windmanager-france-dev;
Uid=sqladmin;Pwd=YOUR_PASSWORD;
Encrypt=yes;TrustServerCertificate=no;"
```

#### Pour PROD:
```
AZURE_SQL_CONNECTION_STRING_PROD=
"Driver={ODBC Driver 18 for SQL Server};
Server=tcp:sql-windmanager-france.database.windows.net,1433;
Database=sqldb-windmanager-france;
Uid=sqladmin;Pwd=YOUR_PASSWORD;
Encrypt=yes;TrustServerCertificate=no;"
```

#### Storage (commun):
```
AZURE_STORAGE_CONNECTION_STRING=
"DefaultEndpointsProtocol=https;
AccountName=stwindmanagerfrance;
AccountKey=YOUR_KEY;
EndpointSuffix=core.windows.net"
```

### Pour le script helper (optionnel)

Ajouter à `.env` local:
```bash
GITHUB_TOKEN=ghp_your_personal_access_token_here
```

Créer un token: https://github.com/settings/tokens
- Scope requis: `workflow`

## 📋 Ordre de Chargement des Tables

Les tables sont vidées et chargées dans cet ordre (respect des FK):

1. `persons`
2. `companies`
3. `farms`
4. `farm_referents`
5. `farm_company_roles`
6. `farm_administrations`
7. `farm_environmental_installations`
8. `farm_financial_guarantees`
9. `farm_locations`
10. `farm_om_contracts`
11. `farm_tcma_contracts`
12. `farm_turbine_details`
13. `substations`
14. `wind_turbine_generators`

## 🚨 En Cas d'Échec

### Consulter les logs

1. Va sur https://github.com/YOUR_USERNAME/WNDMNGR.DB/actions
2. Clique sur le workflow "Load Database"
3. Clique sur le run échoué
4. Consulte les logs détaillés

### Rollback manuel

Si une version d'ingestion a échoué, tu peux:
1. Consulter `ingestion_versions` pour voir quelle version a réussi
2. Relancer le workflow manuellement
3. Les tables seront vidées et rechargées

### Erreurs courantes

**"Connection timeout"**
→ La DB Azure SQL est en auto-pause, elle se réveille automatiquement

**"UUID integrity failed"**
→ Régénère les CSV GOLD (run `_03_silver_to_gold.py`)

**"Foreign key validation failed"**
→ Vérifie que tous les CSV sont bien uploadés dans le Blob

## 🎯 Avantages de cette Architecture

| Critère | Ancien (Azure Functions) | Nouveau (GitHub Actions) |
|---------|-------------------------|--------------------------|
| **Coût** | Free tier limité | 2000 min/mois gratuit |
| **Timeout** | ⚠️ 10 min max | ✅ 30 min (configurable) |
| **Cold Start** | ⚠️ 30-60s | ✅ ~20s |
| **Réseau** | ❌ Port 1433 bloqué | ✅ Pas de restriction |
| **Versioning** | ❌ Aucun | ✅ Natif |
| **Validation** | ❌ Manuelle | ✅ Automatique |
| **Rollback** | ⚠️ Manuel | ✅ Version tracking |
| **Logs** | Azure Portal | ✅ GitHub UI |

## 📚 Commits Conventionnels (pour Semantic Release)

Format: `<type>(<scope>): <description>`

**Types:**
- `feat:` Nouvelle fonctionnalité → version MINOR (1.X.0)
- `fix:` Bug fix → version PATCH (1.0.X)
- `BREAKING CHANGE:` Changement majeur → version MAJOR (X.0.0)
- `docs:` Documentation
- `chore:` Maintenance
- `refactor:` Refactoring

**Exemples:**
```bash
git commit -m "feat(etl): add farm_turbine_details table"
git commit -m "fix(ingestion): handle NULL UUID values"
git commit -m "feat(etl): migrate TCMA contracts

BREAKING CHANGE: Table structure changed"
```

## 🔗 Liens Utiles

- **GitHub Actions**: https://github.com/YOUR_USERNAME/WNDMNGR.DB/actions
- **Releases**: https://github.com/YOUR_USERNAME/WNDMNGR.DB/releases
- **Workflows**: https://github.com/YOUR_USERNAME/WNDMNGR.DB/tree/main/.github/workflows

---

**Dernière mise à jour**: 2025-12-04
**Version**: 1.0.0

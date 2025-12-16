# Edge Function: Execute SQL from Storage

Cette Edge Function permet d'exécuter des fichiers SQL stockés dans Supabase Storage.

## Setup (ONE-TIME)

### 1. Créer la fonction PostgreSQL

Va sur SQL Editor: https://supabase.com/dashboard/project/egmwfzmjkpqjpzlcnqya/sql/new

Copie-colle le contenu de `setup.sql` et exécute-le.

### 2. Déployer l'Edge Function

**Option A: Via Dashboard (RECOMMANDÉ)**

1. Va sur: https://supabase.com/dashboard/project/egmwfzmjkpqjpzlcnqya/functions
2. Clique "Create a new function"
3. Name: `execute-sql`
4. Copie-colle le contenu de `index.ts`
5. Deploy

**Option B: Via Supabase CLI**

```bash
# Install Supabase CLI (si pas déjà fait)
npm install -g supabase

# Login
supabase login

# Link to project
supabase link --project-ref egmwfzmjkpqjpzlcnqya

# Deploy function
supabase functions deploy execute-sql
```

## Usage

### Depuis Python (GitHub Actions)

```python
import requests
import os

supabase_url = os.getenv('SUPABASE_URL')
service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

response = requests.post(
    f'{supabase_url}/functions/v1/execute-sql',
    headers={
        'Authorization': f'Bearer {service_key}',
        'Content-Type': 'application/json'
    },
    json={
        'filePath': '01_REFERENCES/company_roles.sql'
    }
)

print(response.json())
```

### Réponse

```json
{
  "success": true,
  "filePath": "01_REFERENCES/company_roles.sql",
  "totalStatements": 1,
  "successCount": 1,
  "failCount": 0,
  "results": [
    {
      "statement": 1,
      "preview": "CREATE TABLE company_roles...",
      "success": true,
      "data": {"success": true, "message": "SQL executed successfully"}
    }
  ]
}
```

## Flow complet

```
GitHub Actions
    ↓
1. Upload .sql → Storage (via Supabase API)
    ↓
2. POST → Edge Function execute-sql
    ↓
3. Edge Function → Download .sql from Storage
    ↓
4. Edge Function → Call exec_sql() for each statement
    ↓
5. PostgreSQL → Execute CREATE TABLE
    ↓
6. Return → Success/Error
```

"""
Setup Database - Trigger GitHub Actions workflow to create all tables
Part of ETL pipeline: LOAD step (schema setup)
"""
import os
import sys
import subprocess
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings (corporate proxy)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
load_dotenv()

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def _get_github_headers():
    """Get GitHub API headers with authentication"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("X GitHub Token not found in .env file")
        sys.exit(1)
    return {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

def trigger_setup_workflow():
    """Trigger the setup-database.yml workflow via GitHub API"""

    print("=" * 60)
    print("ETL STEP 4: SQL to DB (Setup database structure)")
    print("=" * 60)
    print()

    owner = os.getenv('GITHUB_REPO_OWNER', 'DVDJNBR')
    repo = os.getenv('GITHUB_REPO_NAME', 'WNDMNGR.DB')

    # Get current branch
    try:
        current_branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
    except:
        current_branch = 'main'

    url = f'https://api.github.com/repos/{owner}/{repo}/actions/workflows/setup-database.yml/dispatches'

    payload = {
        'ref': current_branch,
        'inputs': {}
    }

    print(f"Triggering workflow on branch: {current_branch}")
    print()

    try:
        response = requests.post(url, json=payload, headers=_get_github_headers(), verify=False)
        response.raise_for_status()

        print("✓ Workflow triggered successfully!")
        print()
        print("Monitor progress:")
        print(f"  https://github.com/{owner}/{repo}/actions/workflows/setup-database.yml")
        print()
        print("=" * 60)
        print("NEXT STEPS:")
        print("1. Wait for workflow to complete (~2-5 min)")
        print("2. Check results in GitHub Actions")
        print("3. If successful, run csv-to-db to load data")
        print("=" * 60)
        print()

        return True

    except requests.exceptions.RequestException as e:
        print(f"X Failed to trigger workflow: {e}")
        return False


if __name__ == '__main__':
    success = trigger_setup_workflow()
    sys.exit(0 if success else 1)

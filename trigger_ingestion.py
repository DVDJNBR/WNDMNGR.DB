#!/usr/bin/env python3
"""
Helper script to trigger GitHub Actions workflow for database ingestion
"""

import os
import sys
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'YOUR_GITHUB_USERNAME'  # TODO: Update with your GitHub username
REPO_NAME = 'WNDMNGR.DB'
WORKFLOW_FILE = 'load-database.yml'

def trigger_workflow(environment='dev', branch='FT/GITHUB_ACTIONS_INGESTION'):
    """Trigger the load-database workflow via GitHub API"""

    if not GITHUB_TOKEN:
        print("❌ Error: GITHUB_TOKEN not found in environment variables")
        print("Please create a GitHub Personal Access Token and add it to your .env file:")
        print("  1. Go to https://github.com/settings/tokens")
        print("  2. Generate new token (classic) with 'workflow' scope")
        print("  3. Add to .env: GITHUB_TOKEN=your_token_here")
        sys.exit(1)

    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches'

    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    data = {
        'ref': branch,
        'inputs': {
            'environment': environment
        }
    }

    print(f"🚀 Triggering database ingestion workflow...")
    print(f"   Environment: {environment}")
    print(f"   Branch: {branch}")

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        print(f"✅ Workflow triggered successfully!")
        print(f"\nView progress at:")
        print(f"https://github.com/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}")
    else:
        print(f"❌ Failed to trigger workflow")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trigger database ingestion workflow')
    parser.add_argument(
        '--env',
        choices=['dev', 'prod'],
        default='dev',
        help='Target environment (default: dev)'
    )
    parser.add_argument(
        '--branch',
        default='FT/GITHUB_ACTIONS_INGESTION',
        help='Branch to run workflow on (default: FT/GITHUB_ACTIONS_INGESTION)'
    )

    args = parser.parse_args()

    trigger_workflow(environment=args.env, branch=args.branch)

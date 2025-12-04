#!/usr/bin/env python3
"""
Helper script to trigger GitHub Actions workflow for database ingestion
"""

import os
import sys
import requests
import argparse
import warnings
from dotenv import load_dotenv
from loguru import logger

# Suppress SSL warnings (Zscaler proxy)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('GITHUB_REPO_OWNER')
REPO_NAME = os.getenv('GITHUB_REPO_NAME')
WORKFLOW_FILE = 'load-database.yml'

def trigger_workflow(environment='dev', branch='FT/GITHUB_ACTIONS_INGESTION'):
    """Trigger the load-database workflow via GitHub API"""

    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not found in environment variables")
        logger.info("Please create a GitHub Personal Access Token and add it to your .env file:")
        logger.info("  1. Go to https://github.com/settings/tokens")
        logger.info("  2. Generate new token (classic) with 'workflow' scope")
        logger.info("  3. Add to .env: GITHUB_TOKEN=your_token_here")
        sys.exit(1)

    if not REPO_OWNER or not REPO_NAME:
        logger.error("GITHUB_REPO_OWNER or GITHUB_REPO_NAME not found in .env")
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

    logger.info("Triggering database ingestion workflow...")
    logger.info(f"Environment: {environment}")
    logger.info(f"Branch: {branch}")

    response = requests.post(url, headers=headers, json=data, verify=False)

    if response.status_code == 204:
        logger.success("Workflow triggered successfully!")
        logger.info(f"View progress at: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}")
    else:
        logger.error(f"Failed to trigger workflow (HTTP {response.status_code})")
        logger.error(f"Response: {response.text}")
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

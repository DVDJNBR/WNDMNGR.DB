"""
Setup Database - Trigger GitHub Actions workflow to create all tables
Part of ETL pipeline: LOAD step (schema setup)
"""
import subprocess
import sys
import time
from pathlib import Path

def check_gh_cli():
    """Check if GitHub CLI is installed"""
    try:
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ GitHub CLI not found!")
        print("Install: https://cli.github.com/")
        return False


def trigger_setup_workflow():
    """Trigger the setup-database.yml workflow via GitHub CLI"""

    print("=" * 60)
    print("ETL STEP 3: SETUP DATABASE (Create Tables)")
    print("=" * 60)
    print()

    if not check_gh_cli():
        return False

    print("[1] Triggering GitHub Actions workflow: setup-database.yml")
    print()

    try:
        # Trigger workflow
        result = subprocess.run(
            ['gh', 'workflow', 'run', 'setup-database.yml'],
            capture_output=True,
            text=True,
            check=True
        )

        print("✓ Workflow triggered!")
        print()
        print("Monitor progress:")
        print("  https://github.com/DVDJNBR/WNDMNGR.DB/actions/workflows/setup-database.yml")
        print()
        print("Or use: gh run watch")
        print()

        # Wait a bit then show status
        print("Waiting 3 seconds...")
        time.sleep(3)

        print()
        print("[2] Checking workflow status...")

        status_result = subprocess.run(
            ['gh', 'run', 'list', '--workflow=setup-database.yml', '--limit=1'],
            capture_output=True,
            text=True
        )

        print(status_result.stdout)

        print()
        print("=" * 60)
        print("NEXT STEPS:")
        print("1. Wait for workflow to complete (~2-5 min)")
        print("2. Check results in GitHub Actions")
        print("3. If successful, run _04_load_data.py to insert data")
        print("=" * 60)
        print()

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to trigger workflow!")
        print(f"Error: {e.stderr}")
        return False


if __name__ == '__main__':
    success = trigger_setup_workflow()
    sys.exit(0 if success else 1)

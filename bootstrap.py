#!/usr/bin/env python3
"""
bootstrap.py - Single-command setup for pyproject-template

This script downloads the necessary tools from the pyproject-template repository
and executes the repository setup wizard. It bridges the gap between a raw
curl command and the modular package structure of the template.

Usage:
    curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/bootstrap.py \
        | python3

What it does:
    1. Creates a temporary directory
    2. Downloads tools/pyproject_template/* files (setup_repo.py, utils.py, etc.)
    3. Sets up the python path
    4. Runs setup_repo.py
    5. Cleans up
"""

import sys
import tempfile
import urllib.request
from pathlib import Path

# Base URL for raw files
REPO_OWNER = "endavis"
REPO_NAME = "pyproject-template"
BRANCH = "main"
BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}"

# Files needed for setup
FILES = [
    "tools/pyproject_template/__init__.py",
    "tools/pyproject_template/utils.py",
    "tools/pyproject_template/setup_repo.py",
    "tools/pyproject_template/configure.py",
]


def download_file(url: str, dest: Path) -> None:
    try:
        with urllib.request.urlopen(url) as response:  # nosec B310
            content = response.read().decode("utf-8")
            dest.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        sys.exit(1)


def main() -> None:
    print(f"🚀 Bootstrapping {REPO_NAME} setup...")

    # Create temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        root_path = Path(temp_dir)

        # Recreate the package structure: tools/pyproject_template/
        pkg_dir = root_path / "tools" / "pyproject_template"
        pkg_dir.mkdir(parents=True, exist_ok=True)

        # Download files
        for file_path in FILES:
            url = f"{BASE_URL}/{file_path}"
            dest = pkg_dir / Path(file_path).name
            print(f"  Downloading {Path(file_path).name}...")
            download_file(url, dest)

        print("\nStarting setup wizard...\n")

        # Add the temp root to sys.path so 'tools.pyproject_template' can be imported
        sys.path.insert(0, str(root_path))

        # Import and run the setup module
        try:
            from tools.pyproject_template.setup_repo import main as run_setup

            run_setup()
        except ImportError as e:
            print(f"Error importing setup script: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Setup failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)

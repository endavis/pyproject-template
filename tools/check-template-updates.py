#!/usr/bin/env python3
"""
check-template-updates.py - Compare project against latest template

This script fetches the latest pyproject-template release and shows which files
differ from the template. User can then manually review and merge changes.

Usage:
    python tools/check-template-updates.py
    python tools/check-template-updates.py --template-version v2.2.0
    python tools/check-template-updates.py --skip-changelog

Requirements:
    - Git installed
    - Python 3.12+
    - Internet connection (to fetch template)

Author: Generated from pyproject-template
License: MIT
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess  # nosec B404
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

# Template repository info
TEMPLATE_REPO = "endavis/pyproject-template"
TEMPLATE_URL = f"https://github.com/{TEMPLATE_REPO}"
DEFAULT_ARCHIVE_URL = f"{TEMPLATE_URL}/archive/refs/heads/main.zip"


# ANSI color codes
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"
    NC = "\033[0m"  # No Color


class Logger:
    """Simple logging utility with colored output."""

    @staticmethod
    def info(msg: str) -> None:
        print(f"{Colors.BLUE}ℹ{Colors.NC} {msg}")  # noqa: RUF001

    @staticmethod
    def success(msg: str) -> None:
        print(f"{Colors.GREEN}✓{Colors.NC} {msg}")

    @staticmethod
    def warning(msg: str) -> None:
        print(f"{Colors.YELLOW}⚠{Colors.NC} {msg}")

    @staticmethod
    def error(msg: str) -> None:
        print(f"{Colors.RED}✗{Colors.NC} {msg}", file=sys.stderr)

    @staticmethod
    def header(msg: str) -> None:
        print(f"\n{Colors.BOLD}{msg}{Colors.NC}")
        print("━" * 60)


def get_latest_release() -> str | None:
    """Get the latest release tag from GitHub API."""
    api_url = f"https://api.github.com/repos/{TEMPLATE_REPO}/releases/latest"
    try:
        with urllib.request.urlopen(api_url) as response:  # nosec B310
            data = json.loads(response.read())
            tag_name: str | None = data.get("tag_name")
            return tag_name
    except Exception as e:
        Logger.warning(f"Could not fetch latest release: {e}")
        return None


def download_template(target_dir: Path, version: str | None = None) -> Path:
    """Download and extract template to target directory."""
    # Determine download URL
    if version:
        archive_url = f"{TEMPLATE_URL}/archive/refs/tags/{version}.zip"
    else:
        archive_url = DEFAULT_ARCHIVE_URL

    Logger.info(f"Downloading template from {archive_url}...")

    # Download archive
    archive_path = target_dir / "template-archive.zip"
    try:
        urllib.request.urlretrieve(archive_url, archive_path)  # nosec B310
    except Exception as e:
        Logger.error(f"Failed to download template: {e}")
        sys.exit(1)

    # Extract archive
    extract_dir = target_dir / "extracted"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    Logger.info("Extracting archive...")
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, "r") as zf:
            # Filter out dangerous paths
            for member in zf.namelist():
                if member.startswith("/") or ".." in member:
                    continue
                zf.extract(member, extract_dir)
        # GitHub zips have a top-level directory
        contents = list(extract_dir.iterdir())
        template_root = contents[0] if contents and contents[0].is_dir() else extract_dir
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, "r:*") as tf:
            safe_members = [
                m
                for m in tf.getmembers()
                if m.name and not (m.name.startswith("/") or ".." in m.name)
            ]
            tf.extractall(extract_dir, members=safe_members)  # nosec B202
        contents = list(extract_dir.iterdir())
        template_root = contents[0] if contents and contents[0].is_dir() else extract_dir
    else:
        Logger.error("Unknown archive format")
        sys.exit(1)

    # Clean up archive
    archive_path.unlink()

    Logger.success(f"Template extracted to {template_root}")
    return template_root


def open_changelog(template_dir: Path) -> None:
    """Open CHANGELOG.md in user's editor."""
    changelog = template_dir / "CHANGELOG.md"
    if not changelog.exists():
        Logger.warning("CHANGELOG.md not found in template")
        return

    editor = os.environ.get("EDITOR", "less")

    print(f"\n{Colors.CYAN}Opening CHANGELOG.md for review...{Colors.NC}")
    print("(Close the editor when you're done)\n")

    try:
        subprocess.run([editor, str(changelog)], check=True)
    except subprocess.CalledProcessError:
        Logger.warning(f"Failed to open editor '{editor}'")
    except FileNotFoundError:
        Logger.warning(f"Editor '{editor}' not found, skipping changelog view")


def compare_files(project_root: Path, template_root: Path) -> list[Path]:
    """Compare project files against template and return list of different files."""
    # Files/directories to skip
    skip_patterns = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "tmp",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "*.pyc",
        "*.pyo",
        "uv.lock",
        ".envrc.local",
        "site",  # mkdocs build output
    }

    different_files: list[Path] = []

    # Walk through template files
    for template_file in template_root.rglob("*"):
        if not template_file.is_file():
            continue

        # Skip ignored patterns
        rel_path = template_file.relative_to(template_root)
        if any(part in skip_patterns for part in rel_path.parts):
            continue
        if any(rel_path.match(pattern) for pattern in skip_patterns):
            continue

        # Compare with project file
        project_file = project_root / rel_path

        if not project_file.exists() or not filecmp.cmp(template_file, project_file, shallow=False):
            different_files.append(rel_path)

    return sorted(different_files)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare your project against the latest pyproject-template."
    )
    parser.add_argument(
        "--template-version",
        type=str,
        default=None,
        help=(
            "Compare against specific template version tag (e.g., v2.2.0). "
            "Defaults to latest release."
        ),
    )
    parser.add_argument(
        "--skip-changelog",
        action="store_true",
        help="Skip opening CHANGELOG.md in editor",
    )
    parser.add_argument(
        "--keep-template",
        action="store_true",
        help="Keep downloaded template after comparison (don't clean up)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    project_root = Path.cwd()
    tmp_dir = project_root / "tmp"
    tmp_dir.mkdir(exist_ok=True)

    # Get template version
    if args.template_version:
        version = args.template_version
        Logger.info(f"Comparing against template version: {version}")
    else:
        version = get_latest_release()
        if version:
            Logger.info(f"Latest template release: {version}")
        else:
            Logger.info("Comparing against template main branch")

    # Download template
    template_dir = download_template(tmp_dir, version)

    # Open CHANGELOG.md for review
    if not args.skip_changelog:
        open_changelog(template_dir)

    # Compare files
    Logger.header("Comparing your project to template")
    different_files = compare_files(project_root, template_dir)

    if not different_files:
        Logger.success("Your project matches the template perfectly!")
        print("\nNo differences found.")
    else:
        count = len(different_files)
        print(f"\n{Colors.YELLOW}Files different from template ({count} files):{Colors.NC}")
        print("━" * 60)

        for file_path in different_files:
            project_file = project_root / file_path
            if project_file.exists():
                print(f"  {file_path}")
            else:
                print(f"  {file_path} {Colors.CYAN}(new in template){Colors.NC}")

        # Show how to compare
        Logger.header("How to Review Changes")
        template_rel = template_dir.relative_to(project_root)
        print(f"Template files downloaded to: {Colors.CYAN}{template_rel}{Colors.NC}\n")

        print("To compare specific files:")
        # Show a few example diff commands
        for file_path in different_files[:3]:
            project_file = project_root / file_path
            template_file = template_dir / file_path
            if project_file.exists():
                print(f"  diff {file_path} {template_file.relative_to(project_root)}")

        if len(different_files) > 3:
            print(f"  ... ({len(different_files) - 3} more files)")

        print(f"\nOr browse all template files: {template_dir.relative_to(project_root)}/")

    # Cleanup
    if not args.keep_template:
        print()
        Logger.info("Cleaning up downloaded template...")
        shutil.rmtree(template_dir.parent)
        Logger.success("Cleanup complete")
    else:
        print()
        Logger.info(f"Template kept at: {template_dir.relative_to(project_root)}")

    print()


if __name__ == "__main__":
    main()

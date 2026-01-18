"""
Shared utilities for pyproject-template tools.
"""

import json
import re
import shutil
import subprocess  # nosec B404
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Any


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
        print(f"{Colors.BLUE}i{Colors.NC} {msg}")

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
    def step(msg: str) -> None:
        print(f"\n{Colors.CYAN}▸{Colors.NC} {msg}")

    @staticmethod
    def header(msg: str) -> None:
        print(f"\n{Colors.BOLD}{msg}{Colors.NC}")
        print("━" * 60)


def prompt(question: str, default: str = "") -> str:
    """Prompt user for input with optional default value."""
    if default:
        p = f"{Colors.CYAN}?{Colors.NC} {question} [{Colors.GREEN}{default}{Colors.NC}]: "
        response = input(p).strip()
        return response or default
    while True:
        response = input(f"{Colors.CYAN}?{Colors.NC} {question}: ").strip()
        if response:
            return response
        Logger.warning("This field is required. Please enter a value.")


def prompt_confirm(question: str, default: bool = False) -> bool:
    """Prompt user for yes/no confirmation."""
    if default:
        p = f"{Colors.CYAN}?{Colors.NC} {question} [{Colors.GREEN}Y{Colors.NC}/n]: "
        response = input(p).strip().lower()
        return response in ("", "y", "yes")
    else:
        p = f"{Colors.CYAN}?{Colors.NC} {question} [y/{Colors.GREEN}N{Colors.NC}]: "
        response = input(p).strip().lower()
        return response in ("y", "yes")


def validate_package_name(name: str) -> str:
    """Validate and convert to valid Python package name."""
    # Convert to lowercase and replace invalid characters with underscores
    package_name = re.sub(r"[^a-z0-9_]", "_", name.lower())
    # Remove leading/trailing underscores
    package_name = package_name.strip("_")
    # Ensure it doesn't start with a number
    if package_name and package_name[0].isdigit():
        package_name = f"_{package_name}"
    return package_name


def validate_pypi_name(name: str) -> str:
    """Convert to valid PyPI package name (kebab-case)."""
    # Convert to lowercase and replace invalid characters with hyphens
    pypi_name = re.sub(r"[^a-z0-9-]", "-", name.lower())
    # Remove leading/trailing hyphens
    pypi_name = pypi_name.strip("-")
    # Collapse multiple hyphens
    pypi_name = re.sub(r"-+", "-", pypi_name)
    return pypi_name


def validate_email(email: str) -> bool:
    """Basic email validation."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def update_file(filepath: Path, replacements: dict[str, str]) -> None:
    """Update file with string replacements.

    Special handling for 'package_name': only replaces when NOT followed by '='
    to preserve Python keyword argument syntax (e.g., package_name="value").
    """
    if not filepath.exists():
        return
    try:
        content = filepath.read_text(encoding="utf-8")
        for old, new in replacements.items():
            if old == "package_name":
                # Use regex to replace 'package_name' only when NOT followed by '='
                # This preserves keyword argument syntax like package_name="value"
                content = re.sub(r"package_name(?!=)", new, content)
            else:
                content = content.replace(old, new)
        filepath.write_text(content, encoding="utf-8")
    except UnicodeDecodeError:
        pass  # Skip binary files


def download_and_extract_archive(url: str, target_dir: Path) -> Path:
    """Download and extract a zip/tar archive from a URL."""
    archive_path = target_dir / "archive.tmp"

    Logger.info(f"Downloading from {url}...")
    try:
        urllib.request.urlretrieve(url, archive_path)  # nosec B310
    except Exception as e:
        Logger.error(f"Failed to download archive: {e}")
        sys.exit(1)

    extract_dir = target_dir / "extracted"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    Logger.info("Extracting archive...")

    try:
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as zf:
                # Filter out dangerous paths
                for member in zf.namelist():
                    if member.startswith("/") or ".." in member:
                        continue
                    zf.extract(member, extract_dir)
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r:*") as tf:
                # Filter out dangerous members
                safe_members = [
                    m
                    for m in tf.getmembers()
                    if m.name and not (m.name.startswith("/") or ".." in m.name)
                ]
                tf.extractall(extract_dir, members=safe_members)  # nosec B202
        else:
            raise ValueError("Unknown archive format")
    except Exception as e:
        Logger.error(f"Failed to extract archive: {e}")
        sys.exit(1)
    finally:
        if archive_path.exists():
            archive_path.unlink()

    # If the archive contains a single top-level directory, return that
    contents = list(extract_dir.iterdir())
    if len(contents) == 1 and contents[0].is_dir():
        return contents[0]
    return extract_dir


class GitHubCLI:
    """Wrapper for GitHub CLI commands."""

    @staticmethod
    def run(
        args: list[str], check: bool = True, capture: bool = True
    ) -> subprocess.CompletedProcess[str]:
        """Run a gh command."""
        cmd = ["gh", *args]
        try:
            result = subprocess.run(
                cmd,
                check=check,
                capture_output=capture,
                text=True,
            )
            return result
        except subprocess.CalledProcessError as e:
            if capture:
                Logger.error(f"Command failed: {' '.join(cmd)}")
                if e.stderr:
                    print(e.stderr, file=sys.stderr)
            raise

    @staticmethod
    def api(endpoint: str, method: str = "GET", data: dict[str, Any] | None = None) -> Any:
        """Make a GitHub API call."""
        args = ["api", endpoint, "-X", method]
        if data:
            args.append("--input")
            args.append("-")

        result = subprocess.run(
            ["gh", *args],
            input=json.dumps(data) if data else None,
            capture_output=True,
            text=True,
            check=True,
        )

        if result.stdout:
            return json.loads(result.stdout)
        return None

    @staticmethod
    def is_authenticated() -> bool:
        """Check if gh is authenticated."""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

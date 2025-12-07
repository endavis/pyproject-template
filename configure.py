#!/usr/bin/env python3
"""Interactive/non-interactive script to configure the project template.

Modes:
- Interactive (default): prompts for values with defaults pulled from pyproject.toml.
- Auto: use values from pyproject.toml (and git remote) with no prompts (--auto).
Optional: skip final confirmation with --yes.
"""

import os
import re
import shutil
import sys
from pathlib import Path
import argparse
from typing import Optional

try:
    import tomllib  # py312+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure the project template.")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Use values from pyproject.toml (and git remote) without prompts.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt (useful with --auto).",
    )
    return parser.parse_args()


def prompt(question: str, default: str = "") -> str:
    """Prompt user for input with optional default value."""
    if default:
        response = input(f"{question} [{default}]: ").strip()
        return response or default
    while True:
        response = input(f"{question}: ").strip()
        if response:
            return response
        print("This field is required. Please enter a value.")


def validate_package_name(name: str) -> str:
    """Validate and convert to valid Python package name."""
    # Convert to lowercase and replace invalid characters with underscores
    package_name = re.sub(r"[^a-z0-9_]", "_", name.lower())
    # Remove leading/trailing underscores
    package_name = package_name.strip("_")
    # Ensure it doesn't start with a number
    if package_name[0].isdigit():
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
    """Update file with string replacements."""
    if not filepath.exists():
        return

    content = filepath.read_text()
    for old, new in replacements.items():
        content = content.replace(old, new)
    filepath.write_text(content)


def read_pyproject(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def find_backup_pyproject() -> Optional[Path]:
    """Find the most recent backup pyproject.toml from migration helper (in tmp/)."""
    candidates = []
    for backup_dir in Path("tmp").glob("template-migration-backup-*"):
        pyproject = backup_dir / "pyproject.toml"
        if pyproject.exists():
            candidates.append(pyproject)
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def guess_github_user(pyproject_data: dict) -> str:
    repo_url = (
        pyproject_data.get("project", {})
        .get("urls", {})
        .get("Repository")
    )
    if repo_url:
        parts = repo_url.rstrip("/").split("/")
        if len(parts) >= 2:
            return parts[-2]

    # Fallback: try git remote origin
    try:
        import subprocess

        url = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        if url.endswith(".git"):
            url = url[:-4]
        # handle git@github.com:org/repo or https://github.com/org/repo
        if "github.com" in url:
            url = url.replace("git@github.com:", "https://github.com/")
            parts = url.rstrip("/").split("/")
            if len(parts) >= 2:
                return parts[-2]
    except Exception:
        pass

    return ""


def first_author(pyproject_data: dict) -> tuple[str, str]:
    authors = pyproject_data.get("project", {}).get("authors", [])
    if not authors:
        return "", ""
    author = authors[0]
    return author.get("name", ""), author.get("email", "")


def read_readme_title(readme_path: Path) -> str:
    if not readme_path.exists():
        return ""
    for line in readme_path.read_text().splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def load_defaults(pyproject_path: Path) -> dict[str, str]:
    data = read_pyproject(pyproject_path)
    project = data.get("project", {})
    project_name = project.get("name", "")
    package_name = validate_package_name(project_name) if project_name else ""
    pypi_name = validate_pypi_name(project_name) if project_name else ""
    description = project.get("description") or read_readme_title(Path("README.md"))
    author_name, author_email = first_author(data)
    github_user = guess_github_user(data)

    # If current pyproject still has template placeholders, try backup for real values
    backup_pyproject = find_backup_pyproject()
    if backup_pyproject:
        backup_data = read_pyproject(backup_pyproject)
        b_project = backup_data.get("project", {})

        def not_placeholder(val: str, placeholders: set[str]) -> bool:
            return bool(val) and val not in placeholders

        if not_placeholder(project_name, {"package_name", "Package Name", ""}):
            pass
        else:
            project_name = b_project.get("name", project_name)
            package_name = validate_package_name(project_name) if project_name else package_name
            pypi_name = validate_pypi_name(project_name) if project_name else pypi_name

        if not_placeholder(description, {"A short description of your package", ""}):
            pass
        else:
            description = b_project.get("description", description)

        b_author_name, b_author_email = first_author(backup_data)
        if not_placeholder(author_name, {"Your Name", ""}):
            pass
        else:
            author_name = b_author_name or author_name
        if not_placeholder(author_email, {"your.email@example.com", ""}):
            pass
        else:
            author_email = b_author_email or author_email

        if not_placeholder(github_user, {"username", ""}):
            pass
        else:
            github_user = guess_github_user(backup_data) or github_user

    return {
        "project_name": project_name,
        "package_name": package_name,
        "pypi_name": pypi_name,
        "description": description,
        "author_name": author_name,
        "author_email": author_email,
        "github_user": github_user,
    }


def require(value: str, label: str) -> str:
    if value:
        return value
    raise SystemExit(f"❌ Missing required value for {label} (supply in pyproject.toml or via prompt).")


def main() -> int:
    """Run the configuration wizard."""
    args = parse_args()
    defaults = load_defaults(Path("pyproject.toml"))

    print("=" * 70)
    print("Python Project Template Configuration")
    print("=" * 70)
    print("\nThis script will help you set up your new Python project.\n")

    # Gather project information
    print("Project Information")
    print("-" * 70)

    if args.auto:
        project_name = require(defaults["project_name"], "[project].name")
        package_name = require(defaults["package_name"], "package name")
        pypi_name = require(defaults["pypi_name"], "PyPI name")
        description = require(defaults["description"], "description")
        author_name = require(defaults["author_name"], "author name")
        author_email = require(defaults["author_email"], "author email")
        if not validate_email(author_email):
            raise SystemExit("❌ Invalid email format in pyproject.toml")
        github_user = require(defaults["github_user"], "GitHub user (from Repository URL or git remote)")
        enable_dependabot = False
    else:
        project_name = prompt("Project name (human-readable)", defaults["project_name"] or "My Awesome Project")

        suggested_package = validate_package_name(project_name)
        suggested_pypi = validate_pypi_name(project_name)

        package_name = prompt("Python package name", defaults["package_name"] or suggested_package)
        package_name = validate_package_name(package_name)

        pypi_name = prompt("PyPI package name", defaults["pypi_name"] or suggested_pypi)
        pypi_name = validate_pypi_name(pypi_name)

        description = prompt("Short description", defaults["description"] or "A short description of your package")

        author_name = prompt("Author name", defaults["author_name"] or "Your Name")

        while True:
            author_email = prompt("Author email", defaults["author_email"] or "your.email@example.com")
            if validate_email(author_email):
                break
            print("❌ Invalid email format. Please try again.")

        github_user = prompt("GitHub username", defaults["github_user"] or "username")

    # Optional features
    if args.auto:
        enable_dependabot = False
    else:
        print("\n" + "-" * 70)
        print("Optional Features")
        print("-" * 70)
        enable_dependabot = input(
            "Enable Dependabot for automatic dependency updates? [y/N]: "
        ).strip().lower() in ("y", "yes")

    # Confirm configuration
    print("\n" + "=" * 70)
    print("Configuration Summary")
    print("=" * 70)
    print(f"Project Name:     {project_name}")
    print(f"Package Name:     {package_name}")
    print(f"PyPI Name:        {pypi_name}")
    print(f"Description:      {description}")
    print(f"Author:           {author_name} <{author_email}>")
    print(f"GitHub:           {github_user}")
    print(f"Dependabot:       {'Enabled' if enable_dependabot else 'Disabled'}")
    print("=" * 70)

    if not args.yes:
        confirm = input("\nProceed with configuration? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("❌ Configuration cancelled.")
            return 1

    print("\n🔧 Configuring project...")

    # Define replacements
    # IMPORTANT: Longer/Specific replacements must come before shorter substrings
    replacements = {
        # URLs (Specific matches first)
        "https://github.com/username/package_name": f"https://github.com/{github_user}/{package_name}",
        "https://github.com/original-owner/package_name": f"https://github.com/{github_user}/{package_name}",
        "https://codecov.io/gh/username/package_name": f"https://codecov.io/gh/{github_user}/{package_name}",
        "https://codecov.io/gh/username/package_name/branch/main/graph/badge.svg": f"https://codecov.io/gh/{github_user}/{package_name}/branch/main/graph/badge.svg",
        "https://github.com/username/package_name/actions/workflows/ci.yml/badge.svg": f"https://github.com/{github_user}/{package_name}/actions/workflows/ci.yml/badge.svg",
        "https://github.com/username": f"https://github.com/{github_user}",
        
        # Files and Paths
        "package-name.svg": f"{pypi_name}.svg",
        "package-name/": f"{pypi_name}/",
        
        # General Placeholders (Substrings)
        "package_name": package_name,
        "package-name": pypi_name,
        "Package Name": project_name,
        "A short description of your package": description,
        "Your Name": author_name,
        "your.email@example.com": author_email,
        # Note: "username" is NOT replaced globally to avoid breaking code variables (e.g. in extensions.md)
    }

    # Update files
    files_to_update = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "dodo.py",
        "mkdocs.yml",
        "AGENTS.md",
        "CHANGELOG.md",
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        ".github/workflows/testpypi.yml",
        ".github/CONTRIBUTING.md",
        ".github/SECURITY.md",
        ".github/CODEOWNERS",
        ".github/pull_request_template.md",
        ".envrc",
    ]

    for file_path in files_to_update:
        path = Path(file_path)
        if path.exists():
            print(f"  ✓ Updating {file_path}")
            update_file(path, replacements)
    
    # Update docs directory
    docs_dir = Path("docs")
    if docs_dir.exists():
        print("  ✓ Updating documentation files")
        for md_file in docs_dir.rglob("*.md"):
            update_file(md_file, replacements)

    # Update issue/PR templates
    issue_template_dir = Path(".github/ISSUE_TEMPLATE")
    if issue_template_dir.exists():
        print("  ✓ Updating issue templates")
        for md_file in issue_template_dir.rglob("*.md"):
            update_file(md_file, replacements)

    # Update examples directory
    examples_dir = Path("examples")
    if examples_dir.exists():
        print("  ✓ Updating example files")
        for file_path in examples_dir.rglob("*"):
            if file_path.suffix in {".py", ".md"}:
                update_file(file_path, replacements)

    # Rename package directory
    old_package_dir = Path("src/package_name")
    new_package_dir = Path(f"src/{package_name}")

    if old_package_dir.exists() and old_package_dir != new_package_dir:
        if new_package_dir.exists():
            print(
                f"  ⚠️  src/{package_name} already exists; "
                "skipping rename of src/package_name"
            )
        else:
            print(f"  ✓ Renaming src/package_name → src/{package_name}")
            shutil.move(str(old_package_dir), str(new_package_dir))
    elif not old_package_dir.exists():
        print("  ⚠️  src/package_name not found; assuming code already relocated")

    # Update imports in renamed package
    if new_package_dir.exists():
        for py_file in new_package_dir.rglob("*.py"):
            update_file(py_file, replacements)

    # Update test files
    test_dir = Path("tests")
    if test_dir.exists():
        print("  ✓ Updating test files")
        for py_file in test_dir.rglob("*.py"):
            update_file(py_file, replacements)

    # Enable Dependabot if requested
    dependabot_example = Path(".github/dependabot.yml.example")
    dependabot_config = Path(".github/dependabot.yml")
    if enable_dependabot and dependabot_example.exists():
        print("  ✓ Enabling Dependabot")
        shutil.copy(dependabot_example, dependabot_config)

    print("\n✅ Configuration complete!")
    print("\n" + "=" * 70)
    print("Next Steps")
    print("=" * 70)
    print("1. Review the changes: git diff")
    print("2. Initialize git repository: git init")
    print("3. Install dependencies: uv sync --all-extras --dev")
    print("4. Install pre-commit hooks: uv run pre-commit install")
    print("5. Run tests: uv run pytest")
    print("6. Cut a prerelease (if desired): uv run doit release_dev")
    print("7. Start coding!")
    print("=" * 70)

    # Self-destruct
    print("\n🗑️  Removing configure.py (self-destruct)...")
    try:
        Path(__file__).unlink()
        print("  ✓ configure.py removed")
    except Exception as e:
        print(f"  ⚠️  Could not remove configure.py: {e}")
        print("  → You can safely delete it manually")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Configuration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

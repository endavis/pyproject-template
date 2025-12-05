#!/usr/bin/env python3
"""Interactive script to configure the project template.

This script:
1. Prompts for project details (name, author, email, description)
2. Renames the package directory
3. Updates all template placeholders
4. Self-destructs after successful completion

Run this script immediately after cloning the template.
"""

import os
import re
import shutil
import sys
from pathlib import Path


def prompt(question: str, default: str = "") -> str:
    """Prompt user for input with optional default value."""
    if default:
        response = input(f"{question} [{default}]: ").strip()
        return response or default
    else:
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


def main() -> int:
    """Run the configuration wizard."""
    print("=" * 70)
    print("Python Project Template Configuration")
    print("=" * 70)
    print("\nThis script will help you set up your new Python project.\n")

    # Check if already configured
    if not Path("src/package_name").exists():
        print("❌ Error: Template appears to already be configured.")
        print("   (src/package_name directory not found)")
        return 1

    # Gather project information
    print("Project Information")
    print("-" * 70)

    project_name = prompt("Project name (human-readable)", "My Awesome Project")

    # Suggest package names
    suggested_package = validate_package_name(project_name)
    suggested_pypi = validate_pypi_name(project_name)

    package_name = prompt("Python package name", suggested_package)
    package_name = validate_package_name(package_name)

    pypi_name = prompt("PyPI package name", suggested_pypi)
    pypi_name = validate_pypi_name(pypi_name)

    description = prompt("Short description", "A short description of your package")

    author_name = prompt("Author name", "Your Name")

    while True:
        author_email = prompt("Author email", "your.email@example.com")
        if validate_email(author_email):
            break
        print("❌ Invalid email format. Please try again.")

    github_user = prompt("GitHub username", "username")

    # Optional features
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

    confirm = input("\nProceed with configuration? [y/N]: ").strip().lower()
    if confirm not in ("y", "yes"):
        print("❌ Configuration cancelled.")
        return 1

    print("\n🔧 Configuring project...")

    # Define replacements
    replacements = {
        "package_name": package_name,
        "package-name": pypi_name,
        "Package Name": project_name,
        "A short description of your package": description,
        "Your Name": author_name,
        "your.email@example.com": author_email,
        "username": github_user,
    }

    # Update files
    files_to_update = [
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "dodo.py",
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        ".github/workflows/testpypi.yml",
    ]

    for file_path in files_to_update:
        path = Path(file_path)
        if path.exists():
            print(f"  ✓ Updating {file_path}")
            update_file(path, replacements)

    # Rename package directory
    old_package_dir = Path("src/package_name")
    new_package_dir = Path(f"src/{package_name}")

    if old_package_dir.exists() and old_package_dir != new_package_dir:
        print(f"  ✓ Renaming src/package_name → src/{package_name}")
        shutil.move(str(old_package_dir), str(new_package_dir))

    # Update imports in renamed package
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
    print("6. Start coding!")
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

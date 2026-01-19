import json
import os
import platform
import re
import shutil
import subprocess  # nosec B404 - subprocess is required for doit tasks
import sys
import urllib.request
from typing import Any

from doit.action import CmdAction
from doit.tools import title_with_actions
from rich.console import Console
from rich.panel import Panel

# Configuration
DOIT_CONFIG = {
    "verbosity": 2,
    "default_tasks": ["list"],
}

# Use direnv-managed UV_CACHE_DIR if available, otherwise use tmp/
# Set in os.environ so subprocesses inherit it (cross-platform compatible)
UV_CACHE_DIR = os.environ.get("UV_CACHE_DIR", "tmp/.uv_cache")
os.environ["UV_CACHE_DIR"] = UV_CACHE_DIR


def success_message() -> None:
    """Print success message after all checks pass."""
    console = Console()
    console.print()
    console.print(
        Panel.fit(
            "[bold green]✓ All checks passed![/bold green]", border_style="green", padding=(1, 2)
        )
    )
    console.print()


# --- Setup / Install Tasks ---


def task_install() -> dict[str, Any]:
    """Install package with dependencies."""
    return {
        "actions": [
            "uv sync",
        ],
        "title": title_with_actions,
    }


def task_install_dev() -> dict[str, Any]:
    """Install package with dev dependencies."""
    return {
        "actions": [
            "uv sync --all-extras --dev",
        ],
        "title": title_with_actions,
    }


def task_cleanup() -> dict[str, Any]:
    """Clean build and cache artifacts (deep clean)."""

    def clean_artifacts() -> None:
        console = Console()
        console.print("[bold yellow]Performing deep clean...[/bold yellow]")
        console.print()

        # Remove build artifacts
        console.print("[cyan]Removing build artifacts...[/cyan]")
        dirs = [
            "build",
            "dist",
            ".eggs",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        ]
        for d in dirs:
            if os.path.exists(d):
                console.print(f"  [dim]Removing {d}...[/dim]")
                if os.path.isdir(d):
                    shutil.rmtree(d)
                else:
                    os.remove(d)

        # Remove *.egg-info directories
        for item in os.listdir("."):
            if item.endswith(".egg-info") and os.path.isdir(item):
                console.print(f"  [dim]Removing {item}...[/dim]")
                shutil.rmtree(item)

        # Clear tmp/ directory but keep the directory and .gitkeep
        console.print("[cyan]Clearing tmp/ directory...[/cyan]")
        if os.path.exists("tmp"):
            for item in os.listdir("tmp"):
                if item != ".gitkeep":
                    path = os.path.join("tmp", item)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
        else:
            os.makedirs("tmp", exist_ok=True)

        # Ensure .gitkeep exists
        gitkeep = os.path.join("tmp", ".gitkeep")
        if not os.path.exists(gitkeep):
            open(gitkeep, "a").close()

        # Recursive removal of Python cache
        console.print("[cyan]Removing Python cache files...[/cyan]")
        for root, dirs_list, files in os.walk("."):
            # Skip .venv directory
            if ".venv" in dirs_list:
                dirs_list.remove(".venv")

            for d in dirs_list:
                if d == "__pycache__":
                    full_path = os.path.join(root, d)
                    console.print(f"  [dim]Removing {full_path}...[/dim]")
                    shutil.rmtree(full_path)

            for f in files:
                if f.endswith((".pyc", ".pyo")) or f.startswith(".coverage"):
                    full_path = os.path.join(root, f)
                    console.print(f"  [dim]Removing {full_path}...[/dim]")
                    os.remove(full_path)

        console.print()
        console.print(
            Panel.fit(
                "[bold green]✓ Deep clean complete![/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

    return {
        "actions": [clean_artifacts],
        "title": title_with_actions,
    }


# --- Development Tasks ---


def task_test() -> dict[str, Any]:
    """Run pytest with parallel execution."""
    return {
        "actions": ["uv run pytest -n auto -v"],
        "title": title_with_actions,
    }


def task_coverage() -> dict[str, Any]:
    """Run pytest with coverage (note: parallel execution disabled for accurate coverage)."""
    return {
        "actions": [
            "uv run pytest "
            "--cov=package_name --cov-report=term-missing "
            "--cov-report=html:tmp/htmlcov --cov-report=xml:tmp/coverage.xml -v"
        ],
        "title": title_with_actions,
    }


def task_lint() -> dict[str, Any]:
    """Run ruff linting."""
    return {
        "actions": ["uv run ruff check src/ tests/"],
        "title": title_with_actions,
    }


def task_format() -> dict[str, Any]:
    """Format code with ruff."""
    return {
        "actions": [
            "uv run ruff format src/ tests/",
            "uv run ruff check --fix src/ tests/",
        ],
        "title": title_with_actions,
    }


def task_format_check() -> dict[str, Any]:
    """Check code formatting without modifying files."""
    return {
        "actions": ["uv run ruff format --check src/ tests/"],
        "title": title_with_actions,
    }


def task_type_check() -> dict[str, Any]:
    """Run mypy type checking (uses pyproject.toml configuration)."""
    cmd = "uv run mypy src/"
    return {
        "actions": [cmd],
        "title": title_with_actions,
    }


def task_check() -> dict[str, Any]:
    """Run all checks (format, lint, type check, security, spelling, test)."""
    return {
        "actions": [success_message],
        "task_dep": ["format_check", "lint", "type_check", "security", "spell_check", "test"],
        "title": title_with_actions,
    }


def task_audit() -> dict[str, Any]:
    """Run security audit with pip-audit (requires security extras)."""
    return {
        "actions": [
            "uv run pip-audit --skip-editable || "
            "echo 'pip-audit not installed. Run: uv sync --extra security'"
        ],
        "title": title_with_actions,
    }


def task_security() -> dict[str, Any]:
    """Run security checks with bandit (requires security extras)."""
    return {
        "actions": [
            "uv run bandit -c pyproject.toml -r src/ || "
            "echo 'bandit not installed. Run: uv sync --extra security'"
        ],
        "title": title_with_actions,
    }


def task_spell_check() -> dict[str, Any]:
    """Check spelling in code and documentation."""
    return {
        "actions": ["uv run codespell src/ tests/ docs/ README.md"],
        "title": title_with_actions,
    }


def task_fmt_pyproject() -> dict[str, Any]:
    """Format pyproject.toml with pyproject-fmt."""
    return {
        "actions": ["uv run pyproject-fmt pyproject.toml"],
        "title": title_with_actions,
    }


def task_licenses() -> dict[str, Any]:
    """Check licenses of dependencies (requires security extras)."""
    return {
        "actions": [
            "uv run pip-licenses --format=markdown --order=license || "
            "echo 'pip-licenses not installed. Run: uv sync --extra security'"
        ],
        "title": title_with_actions,
    }


def task_commit() -> dict[str, Any]:
    """Interactive commit with commitizen (ensures conventional commit format)."""
    return {
        "actions": ["uv run cz commit || " "echo 'commitizen not installed. Run: uv sync'"],
        "title": title_with_actions,
    }


def task_bump() -> dict[str, Any]:
    """Bump version automatically based on conventional commits."""
    return {
        "actions": ["uv run cz bump || " "echo 'commitizen not installed. Run: uv sync'"],
        "title": title_with_actions,
    }


def task_changelog() -> dict[str, Any]:
    """Generate CHANGELOG from conventional commits."""
    return {
        "actions": ["uv run cz changelog || " "echo 'commitizen not installed. Run: uv sync'"],
        "title": title_with_actions,
    }


def task_pre_commit_install() -> dict[str, Any]:
    """Install pre-commit hooks."""
    return {
        "actions": ["uv run pre-commit install"],
        "title": title_with_actions,
    }


def task_pre_commit_run() -> dict[str, Any]:
    """Run pre-commit on all files."""
    return {
        "actions": ["uv run pre-commit run --all-files"],
        "title": title_with_actions,
    }


# --- Documentation Tasks ---


def task_docs_serve() -> dict[str, Any]:
    """Serve documentation locally with live reload."""
    return {
        "actions": ["uv run mkdocs serve"],
        "title": title_with_actions,
    }


def task_docs_build() -> dict[str, Any]:
    """Build documentation site."""
    return {
        "actions": ["uv run mkdocs build"],
        "title": title_with_actions,
    }


def task_docs_deploy() -> dict[str, Any]:
    """Deploy documentation to GitHub Pages."""
    return {
        "actions": ["uv run mkdocs gh-deploy --force"],
        "title": title_with_actions,
    }


def task_update_deps() -> dict[str, Any]:
    """Update dependencies and run tests to verify."""

    def update_dependencies() -> None:
        console = Console()
        console.print()
        console.print(
            Panel.fit("[bold cyan]Updating Dependencies[/bold cyan]", border_style="cyan")
        )
        console.print()

        print("Checking for outdated dependencies...")
        print()
        subprocess.run(
            ["uv", "pip", "list", "--outdated"],
            env={**os.environ, "UV_CACHE_DIR": UV_CACHE_DIR},
            check=False,
        )

        print()
        print("=" * 70)
        print("Updating all dependencies (including extras)...")
        print("=" * 70)
        print()

        # Update dependencies and refresh lockfile
        result = subprocess.run(
            ["uv", "sync", "--all-extras", "--dev", "--upgrade"],
            env={**os.environ, "UV_CACHE_DIR": UV_CACHE_DIR},
        )

        if result.returncode != 0:
            print("\n❌ Dependency update failed!")
            sys.exit(1)

        print()
        print("=" * 70)
        print("Running tests to verify updates...")
        print("=" * 70)
        print()

        # Run all checks
        check_result = subprocess.run(["doit", "check"])

        print()
        if check_result.returncode == 0:
            print("=" * 70)
            print(" " * 20 + "✓ All checks passed!")
            print("=" * 70)
            print()
            print("Next steps:")
            print("1. Review the changes: git diff pyproject.toml")
            print("2. Test thoroughly")
            print("3. Commit the updated dependencies")
        else:
            print("=" * 70)
            print("⚠ Warning: Some checks failed after update")
            print("=" * 70)
            print()
            print("You may need to:")
            print("1. Fix compatibility issues")
            print("2. Update code for breaking changes")
            print("3. Revert problematic updates")
            sys.exit(1)

    return {
        "actions": [update_dependencies],
        "title": title_with_actions,
    }


def task_release_dev(type: str = "alpha") -> dict[str, Any]:
    """Create a pre-release (alpha/beta) tag for TestPyPI and push to GitHub.

    Args:
        type (str): Pre-release type (e.g., 'alpha', 'beta', 'rc'). Defaults to 'alpha'.
    """

    def create_dev_release() -> None:
        console = Console()
        console.print("=" * 70)
        console.print(f"[bold green]Starting {type} release tagging...[/bold green]")
        console.print("=" * 70)
        console.print()

        # Check if on main branch
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if current_branch != "main":
            console.print(
                f"[bold yellow]⚠ Warning: Not on main branch "
                f"(currently on {current_branch})[/bold yellow]"
            )
            response = input("Continue anyway? (y/N) ").strip().lower()
            if response != "y":
                console.print("[bold red]❌ Release cancelled.[/bold red]")
                sys.exit(1)

        # Check for uncommitted changes
        status = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if status:
            console.print("[bold red]❌ Error: Uncommitted changes detected.[/bold red]")
            console.print(status)
            sys.exit(1)

        # Pull latest changes
        console.print("\n[cyan]Pulling latest changes...[/cyan]")
        try:
            subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
            console.print("[green]✓ Git pull successful.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Error pulling latest changes:[/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Run checks
        console.print("\n[cyan]Running all pre-release checks...[/cyan]")
        try:
            subprocess.run(["doit", "check"], check=True, capture_output=True, text=True)
            console.print("[green]✓ All checks passed.[/green]")
        except subprocess.CalledProcessError as e:
            console.print(
                "[bold red]❌ Pre-release checks failed! "
                "Please fix issues before tagging.[/bold red]"
            )
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Automated version bump and tagging
        console.print(f"\n[cyan]Bumping version ({type}) and updating changelog...[/cyan]")
        try:
            # Use cz bump --prerelease <type> --changelog
            result = subprocess.run(
                ["uv", "run", "cz", "bump", "--prerelease", type, "--changelog"],
                env={**os.environ, "UV_CACHE_DIR": UV_CACHE_DIR},
                check=True,
                capture_output=True,
                text=True,
            )
            console.print(f"[green]✓ Version bumped to {type}.[/green]")
            console.print(f"[dim]{result.stdout}[/dim]")
            # Extract new version
            version_match = re.search(r"Bumping to version (\d+\.\d+\.\d+[^\s]*)", result.stdout)
            new_version = version_match.group(1) if version_match else "unknown"

        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ commitizen bump failed![/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        console.print(f"\n[cyan]Pushing tag v{new_version} to origin...[/cyan]")
        try:
            subprocess.run(
                ["git", "push", "--follow-tags", "origin", current_branch],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print("[green]✓ Tags pushed to origin.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Error pushing tag to origin:[/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        console.print("\n" + "=" * 70)
        console.print(f"[bold green]✓ Development release {new_version} complete![/bold green]")
        console.print("=" * 70)
        console.print("\nNext steps:")
        console.print("1. Monitor GitHub Actions (testpypi.yml) for the TestPyPI publish.")
        console.print("2. Verify on TestPyPI once the workflow completes.")

    return {
        "actions": [create_dev_release],
        "params": [
            {
                "name": "type",
                "short": "t",
                "long": "type",
                "default": "alpha",
                "help": "Pre-release type (alpha, beta, rc)",
            }
        ],
        "title": title_with_actions,
    }


def task_release(increment: str = "") -> dict[str, Any]:
    """Automate release: bump version, update CHANGELOG, and push to GitHub (triggers CI/CD).

    Args:
        increment (str): Force version increment type (MAJOR, MINOR, PATCH). Auto-detects if empty.
    """

    def automated_release() -> None:
        console = Console()
        console.print("=" * 70)
        console.print("[bold green]Starting automated release process...[/bold green]")
        console.print("=" * 70)
        console.print()

        # Check if on main branch
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if current_branch != "main":
            console.print(
                f"[bold yellow]⚠ Warning: Not on main branch "
                f"(currently on {current_branch})[/bold yellow]"
            )
            response = input("Continue anyway? (y/N) ").strip().lower()
            if response != "y":
                console.print("[bold red]❌ Release cancelled.[/bold red]")
                sys.exit(1)

        # Check for uncommitted changes
        status = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if status:
            console.print("[bold red]❌ Error: Uncommitted changes detected.[/bold red]")
            console.print(status)
            sys.exit(1)

        # Pull latest changes
        console.print("\n[cyan]Pulling latest changes...[/cyan]")
        try:
            subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
            console.print("[green]✓ Git pull successful.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Error pulling latest changes:[/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Governance validation
        console.print("\n[bold cyan]Running governance validations...[/bold cyan]")

        # Validate merge commit format (blocking)
        if not validate_merge_commits(console):
            console.print("\n[bold red]❌ Merge commit validation failed![/bold red]")
            console.print("[yellow]Please ensure all merge commits follow the format:[/yellow]")
            console.print("[yellow]  <type>: <subject> (merges PR #XX, closes #YY)[/yellow]")
            sys.exit(1)

        # Validate issue links (warning only)
        validate_issue_links(console)

        console.print("[bold green]✓ Governance validations complete.[/bold green]")

        # Run all checks
        console.print("\n[cyan]Running all pre-release checks...[/cyan]")
        try:
            subprocess.run(["doit", "check"], check=True, capture_output=True, text=True)
            console.print("[green]✓ All checks passed.[/green]")
        except subprocess.CalledProcessError as e:
            console.print(
                "[bold red]❌ Pre-release checks failed! "
                "Please fix issues before releasing.[/bold red]"
            )
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Automated version bump and CHANGELOG generation using commitizen
        console.print("\n[cyan]Bumping version and generating CHANGELOG with commitizen...[/cyan]")
        try:
            # Use cz bump --changelog --merge-prerelease to update version,
            # changelog, commit, and tag. This consolidates pre-release changes
            # into the final release entry
            bump_cmd = ["uv", "run", "cz", "bump", "--changelog", "--merge-prerelease"]
            if increment:
                bump_cmd.extend(["--increment", increment.upper()])
                console.print(f"[dim]Forcing {increment.upper()} version bump[/dim]")
            result = subprocess.run(
                bump_cmd,
                env={**os.environ, "UV_CACHE_DIR": UV_CACHE_DIR},
                check=True,
                capture_output=True,
                text=True,
            )
            console.print(
                "[green]✓ Version bumped and CHANGELOG updated (merged pre-releases).[/green]"
            )
            console.print(f"[dim]{result.stdout}[/dim]")
            # Extract new version from cz output (example: "Bumping to version 1.0.0")
            version_match = re.search(r"Bumping to version (\d+\.\d+\.\d+)", result.stdout)
            # Fallback to "unknown" if regex fails
            new_version = version_match.group(1) if version_match else "unknown"

        except subprocess.CalledProcessError as e:
            console.print(
                "[bold red]❌ commitizen bump failed! "
                "Ensure your commit history is conventional.[/bold red]"
            )
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(
                f"[bold red]❌ An unexpected error occurred during commitizen bump: {e}[/bold red]"
            )
            sys.exit(1)

        # Push commits and tags to GitHub
        console.print("\n[cyan]Pushing commits and tags to GitHub...[/cyan]")
        try:
            subprocess.run(
                ["git", "push", "--follow-tags", "origin", current_branch],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print("[green]✓ Pushed new commits and tags to GitHub.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Error pushing to GitHub:[/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        console.print("\n" + "=" * 70)
        console.print(f"[bold green]✓ Automated release {new_version} complete![/bold green]")
        console.print("=" * 70)
        console.print("\nNext steps:")
        console.print("1. Monitor GitHub Actions for build and publish.")
        console.print(
            "2. Check TestPyPI: [link=https://test.pypi.org/project/package-name/]https://test.pypi.org/project/package-name/[/link]"
        )
        console.print(
            "3. Check PyPI: [link=https://pypi.org/project/package-name/]https://pypi.org/project/package-name/[/link]"
        )
        console.print("4. Verify the updated CHANGELOG.md in the repository.")

    return {
        "actions": [automated_release],
        "params": [
            {
                "name": "increment",
                "short": "i",
                "long": "increment",
                "default": "",
                "help": "Force increment (MAJOR, MINOR, PATCH). Auto-detects if empty.",
            }
        ],
        "title": title_with_actions,
    }


def task_release_pr(increment: str = "") -> dict[str, Any]:
    """Create a release PR with changelog updates (PR-based workflow).

    This task creates a release branch, updates the changelog, and opens a PR.
    After the PR is merged, use `doit release_tag` to tag the release.

    Args:
        increment (str): Force version increment type (MAJOR, MINOR, PATCH). Auto-detects if empty.
    """

    def create_release_pr() -> None:
        console = Console()
        console.print("=" * 70)
        console.print("[bold green]Starting PR-based release process...[/bold green]")
        console.print("=" * 70)
        console.print()

        # Check if on main branch
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if current_branch != "main":
            console.print(
                f"[bold red]❌ Error: Must be on main branch "
                f"(currently on {current_branch})[/bold red]"
            )
            sys.exit(1)

        # Check for uncommitted changes
        status = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if status:
            console.print("[bold red]❌ Error: Uncommitted changes detected.[/bold red]")
            console.print(status)
            sys.exit(1)

        # Pull latest changes
        console.print("\n[cyan]Pulling latest changes...[/cyan]")
        try:
            subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
            console.print("[green]✓ Git pull successful.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Error pulling latest changes:[/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Governance validation
        console.print("\n[bold cyan]Running governance validations...[/bold cyan]")

        # Validate merge commit format (blocking)
        if not validate_merge_commits(console):
            console.print("\n[bold red]❌ Merge commit validation failed![/bold red]")
            console.print("[yellow]Please ensure all merge commits follow the format:[/yellow]")
            console.print("[yellow]  <type>: <subject> (merges PR #XX, closes #YY)[/yellow]")
            sys.exit(1)

        # Validate issue links (warning only)
        validate_issue_links(console)

        console.print("[bold green]✓ Governance validations complete.[/bold green]")

        # Run all checks
        console.print("\n[cyan]Running all pre-release checks...[/cyan]")
        try:
            subprocess.run(["doit", "check"], check=True, capture_output=True, text=True)
            console.print("[green]✓ All checks passed.[/green]")
        except subprocess.CalledProcessError as e:
            console.print(
                "[bold red]❌ Pre-release checks failed! "
                "Please fix issues before releasing.[/bold red]"
            )
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Get next version using commitizen
        console.print("\n[cyan]Determining next version...[/cyan]")
        try:
            get_next_cmd = ["uv", "run", "cz", "bump", "--get-next"]
            if increment:
                get_next_cmd.extend(["--increment", increment.upper()])
                console.print(f"[dim]Forcing {increment.upper()} version bump[/dim]")
            result = subprocess.run(
                get_next_cmd,
                env={**os.environ, "UV_CACHE_DIR": UV_CACHE_DIR},
                check=True,
                capture_output=True,
                text=True,
            )
            next_version = result.stdout.strip()
            console.print(f"[green]✓ Next version: {next_version}[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to determine next version.[/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Create release branch
        branch_name = f"release/v{next_version}"
        console.print(f"\n[cyan]Creating branch {branch_name}...[/cyan]")
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print(f"[green]✓ Created branch {branch_name}[/green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]❌ Failed to create branch {branch_name}.[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Update changelog
        console.print("\n[cyan]Updating CHANGELOG.md...[/cyan]")
        try:
            changelog_cmd = ["uv", "run", "cz", "changelog", "--incremental"]
            subprocess.run(
                changelog_cmd,
                env={**os.environ, "UV_CACHE_DIR": UV_CACHE_DIR},
                check=True,
                capture_output=True,
                text=True,
            )
            console.print("[green]✓ CHANGELOG.md updated.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to update changelog.[/bold red]")
            console.print(f"[red]Stdout: {e.stdout}[/red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            # Cleanup: go back to main
            subprocess.run(["git", "checkout", "main"], capture_output=True)
            subprocess.run(["git", "branch", "-D", branch_name], capture_output=True)
            sys.exit(1)

        # Commit changelog
        console.print("\n[cyan]Committing changelog...[/cyan]")
        try:
            subprocess.run(
                ["git", "add", "CHANGELOG.md"],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"chore: update changelog for v{next_version}"],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print("[green]✓ Changelog committed.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to commit changelog.[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            # Cleanup
            subprocess.run(["git", "checkout", "main"], capture_output=True)
            subprocess.run(["git", "branch", "-D", branch_name], capture_output=True)
            sys.exit(1)

        # Push branch
        console.print(f"\n[cyan]Pushing branch {branch_name}...[/cyan]")
        try:
            subprocess.run(
                ["git", "push", "-u", "origin", branch_name],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print("[green]✓ Branch pushed.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to push branch.[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Create PR using doit pr
        console.print("\n[cyan]Creating pull request...[/cyan]")
        try:
            pr_title = f"release: v{next_version}"
            pr_body = f"""## Description
Release v{next_version}

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (would cause existing functionality to not work as expected)
- [ ] Documentation update
- [x] Release

## Changes Made
- Updated CHANGELOG.md for v{next_version}

## Testing
- [ ] All existing tests pass

## Checklist
- [x] My changes generate no new warnings

## Additional Notes
After this PR is merged, run `doit release_tag` to create the version tag
and trigger the release workflow.
"""
            # Use gh CLI directly since we're in a non-interactive context
            subprocess.run(
                [
                    "gh",
                    "pr",
                    "create",
                    "--title",
                    pr_title,
                    "--body",
                    pr_body,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print("[green]✓ Pull request created.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to create PR.[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        console.print("\n" + "=" * 70)
        console.print(f"[bold green]✓ Release PR for v{next_version} created![/bold green]")
        console.print("=" * 70)
        console.print("\nNext steps:")
        console.print("1. Review and merge the PR.")
        console.print("2. After merge, run: doit release_tag")

    return {
        "actions": [create_release_pr],
        "params": [
            {
                "name": "increment",
                "short": "i",
                "long": "increment",
                "default": "",
                "help": "Force increment (MAJOR, MINOR, PATCH). Auto-detects if empty.",
            }
        ],
        "title": title_with_actions,
    }


def task_release_tag() -> dict[str, Any]:
    """Tag the release after a release PR is merged.

    This task finds the most recently merged release PR, extracts the version,
    creates a git tag, and pushes it to trigger the release workflow.
    """

    def create_release_tag() -> None:
        console = Console()
        console.print("=" * 70)
        console.print("[bold green]Creating release tag...[/bold green]")
        console.print("=" * 70)
        console.print()

        # Check if on main branch
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if current_branch != "main":
            console.print(
                f"[bold red]❌ Error: Must be on main branch "
                f"(currently on {current_branch})[/bold red]"
            )
            sys.exit(1)

        # Pull latest changes
        console.print("\n[cyan]Pulling latest changes...[/cyan]")
        try:
            subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
            console.print("[green]✓ Git pull successful.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Error pulling latest changes:[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Find the most recently merged release PR
        console.print("\n[cyan]Finding merged release PR...[/cyan]")
        try:
            result = subprocess.run(
                [
                    "gh",
                    "pr",
                    "list",
                    "--state",
                    "merged",
                    "--search",
                    "release: v in:title",
                    "--limit",
                    "1",
                    "--json",
                    "title,mergedAt,headRefName",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            import json

            prs = json.loads(result.stdout)
            if not prs:
                console.print("[bold red]❌ No merged release PR found.[/bold red]")
                console.print(
                    "[yellow]Ensure a release PR with title 'release: vX.Y.Z' was merged.[/yellow]"
                )
                sys.exit(1)

            pr = prs[0]
            pr_title = pr["title"]
            branch_name = pr["headRefName"]

            # Extract version from PR title (format: "release: vX.Y.Z")
            version_match = re.search(r"release:\s*v?(\d+\.\d+\.\d+)", pr_title)
            if not version_match:
                # Try extracting from branch name (format: "release/vX.Y.Z")
                version_match = re.search(r"release/v?(\d+\.\d+\.\d+)", branch_name)

            if not version_match:
                console.print("[bold red]❌ Could not extract version from PR.[/bold red]")
                console.print(f"[yellow]PR title: {pr_title}[/yellow]")
                console.print(f"[yellow]Branch: {branch_name}[/yellow]")
                sys.exit(1)

            version = version_match.group(1)
            tag_name = f"v{version}"
            console.print(f"[green]✓ Found release PR: {pr_title}[/green]")
            console.print(f"[green]✓ Version to tag: {tag_name}[/green]")

        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to find release PR.[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Check if tag already exists
        existing_tags = subprocess.run(
            ["git", "tag", "-l", tag_name],
            capture_output=True,
            text=True,
        ).stdout.strip()
        if existing_tags:
            console.print(f"[bold red]❌ Tag {tag_name} already exists.[/bold red]")
            sys.exit(1)

        # Create tag
        console.print(f"\n[cyan]Creating tag {tag_name}...[/cyan]")
        try:
            subprocess.run(
                ["git", "tag", tag_name],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print(f"[green]✓ Tag {tag_name} created.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to create tag.[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        # Push tag
        console.print(f"\n[cyan]Pushing tag {tag_name}...[/cyan]")
        try:
            subprocess.run(
                ["git", "push", "origin", tag_name],
                check=True,
                capture_output=True,
                text=True,
            )
            console.print(f"[green]✓ Tag {tag_name} pushed.[/green]")
        except subprocess.CalledProcessError as e:
            console.print("[bold red]❌ Failed to push tag.[/bold red]")
            console.print(f"[red]Stderr: {e.stderr}[/red]")
            sys.exit(1)

        console.print("\n" + "=" * 70)
        console.print(f"[bold green]✓ Release {tag_name} tagged![/bold green]")
        console.print("=" * 70)
        console.print("\nNext steps:")
        console.print("1. Monitor GitHub Actions for build and publish.")
        console.print(
            "2. Check TestPyPI: [link=https://test.pypi.org/project/package-name/]https://test.pypi.org/project/package-name/[/link]"
        )
        console.print(
            "3. Check PyPI: [link=https://pypi.org/project/package-name/]https://pypi.org/project/package-name/[/link]"
        )

    return {
        "actions": [create_release_tag],
        "title": title_with_actions,
    }


# --- Build & Publish Tasks ---


def task_build() -> dict[str, Any]:
    """Build package."""
    return {
        "actions": ["uv build"],
        "title": title_with_actions,
    }


def task_publish() -> dict[str, Any]:
    """Build and publish package to PyPI."""

    def publish_cmd() -> str:
        token = os.environ.get("PYPI_TOKEN")
        if not token:
            raise RuntimeError("PYPI_TOKEN environment variable must be set.")
        return "uv publish --token '{token}'"

    return {
        "actions": ["uv build", CmdAction(publish_cmd)],
        "title": title_with_actions,
    }


# --- Installation Helper Tasks ---


def _get_latest_github_release(repo: str) -> str:
    """Helper to get latest GitHub release version."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(url)

    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        request.add_header("Authorization", f"token {github_token}")

    with urllib.request.urlopen(request) as response:  # nosec B310 - URL is hardcoded GitHub API
        data = json.loads(response.read().decode())
        tag_name: str = data["tag_name"]
        return tag_name.lstrip("v")


def _install_direnv() -> None:
    """Install direnv if not already installed."""
    if shutil.which("direnv"):
        version = subprocess.run(
            ["direnv", "--version"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        print(f"✓ direnv already installed: {version}")
        return

    print("Installing direnv...")
    version = _get_latest_github_release("direnv/direnv")
    print(f"Latest version: {version}")

    system = platform.system().lower()
    install_dir = os.path.expanduser("~/.local/bin")
    if not os.path.exists(install_dir):
        os.makedirs(install_dir, exist_ok=True)

    if system == "linux":
        bin_url = (
            f"https://github.com/direnv/direnv/releases/download/v{version}/direnv.linux-amd64"
        )
        bin_path = os.path.join(install_dir, "direnv")
        print(f"Downloading {bin_url}...")
        urllib.request.urlretrieve(bin_url, bin_path)  # nosec B310 - downloading from hardcoded GitHub release URL
        os.chmod(bin_path, 0o755)  # nosec B103 - rwxr-xr-x is required for executable binary
    elif system == "darwin":
        subprocess.run(["brew", "install", "direnv"], check=True)
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    print("✓ direnv installed.")
    print("\nIMPORTANT: Add direnv hook to your shell:")
    print("  Bash: echo 'eval \"$(direnv hook bash)\"'")
    print("  Zsh:  echo 'eval \"$(direnv hook zsh)\"'")


def task_install_direnv() -> dict[str, Any]:
    """Install direnv for automatic environment loading."""
    return {
        "actions": [_install_direnv],
        "title": title_with_actions,
    }


# ==============================================================================
# Governance Validation Helpers
# ==============================================================================


def validate_merge_commits(console: "Console") -> bool:
    """Validate that all merge commits follow the required format.

    Returns:
        bool: True if all merge commits are valid, False otherwise.
    """
    import re

    console.print("\n[cyan]Validating merge commit format...[/cyan]")

    # Get merge commits since last tag (or all if no tags)
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
        )
        last_tag = result.stdout.strip() if result.returncode == 0 else ""
        range_spec = f"{last_tag}..HEAD" if last_tag else "HEAD"

        result = subprocess.run(
            ["git", "log", "--merges", "--pretty=format:%h %s", range_spec],
            capture_output=True,
            text=True,
        )
        merge_commits = result.stdout.strip().split("\n") if result.stdout.strip() else []

    except Exception as e:
        console.print(f"[yellow]⚠ Could not check merge commits: {e}[/yellow]")
        return True  # Don't block on this check

    if not merge_commits or merge_commits == [""]:
        console.print("[green]✓ No merge commits to validate.[/green]")
        return True

    # Pattern: <type>: <subject> (merges PR #XX, closes #YY) or (merges PR #XX)
    merge_pattern = re.compile(
        r"^[a-f0-9]+\s+(feat|fix|refactor|docs|test|chore|ci|perf):\s.+\s"
        r"\(merges PR #\d+(?:, closes #\d+)?\)$"
    )

    invalid_commits = []
    for commit in merge_commits:
        if commit and not merge_pattern.match(commit):
            invalid_commits.append(commit)

    if invalid_commits:
        console.print("[bold red]❌ Invalid merge commit format found:[/bold red]")
        for commit in invalid_commits:
            console.print(f"  [red]{commit}[/red]")
        console.print("\n[yellow]Expected format:[/yellow]")
        console.print("  <type>: <subject> (merges PR #XX, closes #YY)")
        console.print("  <type>: <subject> (merges PR #XX)")
        return False

    console.print("[green]✓ All merge commits follow required format.[/green]")
    return True


def validate_issue_links(console: "Console") -> bool:
    """Validate that commits (except docs) reference issues.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    import re

    console.print("\n[cyan]Validating issue links in commits...[/cyan]")

    try:
        # Get commits since last tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
        )
        last_tag = result.stdout.strip() if result.returncode == 0 else ""
        # If no tags, check last 10 commits
        range_spec = f"{last_tag}..HEAD" if last_tag else "HEAD~10..HEAD"

        result = subprocess.run(
            ["git", "log", "--pretty=format:%h %s", range_spec],
            capture_output=True,
            text=True,
        )
        commits = result.stdout.strip().split("\n") if result.stdout.strip() else []

    except Exception as e:
        console.print(f"[yellow]⚠ Could not check issue links: {e}[/yellow]")
        return True  # Don't block on this check

    if not commits or commits == [""]:
        console.print("[green]✓ No commits to validate.[/green]")
        return True

    issue_pattern = re.compile(r"#\d+")
    docs_pattern = re.compile(r"^[a-f0-9]+\s+docs:", re.IGNORECASE)

    commits_without_issues = []
    for commit in commits:
        if commit:
            # Skip docs commits
            if docs_pattern.match(commit):
                continue
            # Skip merge commits (already validated separately)
            if "merge" in commit.lower():
                continue
            # Check for issue reference
            if not issue_pattern.search(commit):
                commits_without_issues.append(commit)

    if commits_without_issues:
        console.print("[bold yellow]⚠ Warning: Some commits don't reference issues:[/bold yellow]")
        for commit in commits_without_issues[:5]:  # Show first 5
            console.print(f"  [yellow]{commit}[/yellow]")
        if len(commits_without_issues) > 5:
            console.print(f"  [dim]...and {len(commits_without_issues) - 5} more[/dim]")
        console.print("\n[dim]This is a warning only - release can continue.[/dim]")
        console.print("[dim]Consider linking commits to issues for better traceability.[/dim]")
    else:
        console.print("[green]✓ All non-docs commits reference issues.[/green]")

    return True  # Warning only, don't block release


# ==============================================================================
# GitHub Issue & PR Creation Tasks
# ==============================================================================

# Issue templates for editor mode
ISSUE_TEMPLATE_FEATURE = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Problem
<!-- Required: What problem does this feature solve? -->
Describe the problem or limitation you're experiencing.

## Proposed Solution
<!-- Required: How do you envision this feature working? -->
Clear description of what you want to happen.

## Success Criteria
<!-- Optional: How will we know this is complete? Delete section if not needed. -->
- [ ] Feature implements X functionality
- [ ] Tests added and passing
- [ ] Documentation updated

## Additional Context
<!-- Optional: Links, examples, screenshots. Delete section if not needed. -->
Any other relevant information.
"""

ISSUE_TEMPLATE_BUG = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Bug Description
<!-- Required: A clear description of the bug -->
Describe the bug and its impact.

## Steps to Reproduce
<!-- Required: Step-by-step instructions -->
1. Run command `...`
2. With input `...`
3. Observe error `...`

## Expected vs Actual Behavior
<!-- Required: What should happen vs what actually happens -->
**Expected:** The function should return a valid result
**Actual:** The function raises an error

## Environment
<!-- Optional: System information. Delete section if not needed. -->
- Python: 3.12
- OS: Ubuntu 22.04
- Package version: 1.0.0

## Error Output
<!-- Optional: Paste error messages or stack traces. Delete section if not needed. -->
```
Paste error output here
```

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Screenshots, related issues, workarounds attempted.
"""

ISSUE_TEMPLATE_REFACTOR = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Current Code Issue
<!-- Required: Describe the code that needs refactoring -->
Describe what code currently exists, where it's located, and what problems it causes.

## Proposed Improvement
<!-- Required: How you propose to refactor the code -->
Describe the refactoring approach and what the code will look like after.

## Success Criteria
<!-- Optional: How will we know the refactoring is successful? Delete section if not needed. -->
- [ ] Code duplication eliminated
- [ ] All existing tests still pass
- [ ] New tests added for refactored code

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Performance impact, breaking change considerations, migration steps.
"""

ISSUE_TEMPLATE_DOC = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Documentation Type
<!-- Required: What kind of documentation change? -->
New guide / Update existing / Fix incorrect info / Add examples / API docs

## Description
<!-- Required: What documentation is needed? -->
Describe the documentation that is missing or needs improvement.

## Suggested Location
<!-- Optional: Where should this documentation live? Delete section if not needed. -->
- docs/getting-started/
- docs/examples/
- README.md

## Success Criteria
<!-- Optional: How will we know the documentation is complete? Delete section if not needed. -->
- [ ] Topic is fully explained
- [ ] Code examples included
- [ ] Added to navigation/index

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Links to related documentation, examples from other projects.
"""

ISSUE_TEMPLATE_CHORE = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Chore Type
<!-- Required: What kind of maintenance task? -->
CI/CD / Dependencies / Tooling / Cleanup / Configuration

## Description
<!-- Required: What needs to be done and why? -->
Describe the maintenance task.

## Proposed Changes
<!-- Optional: What specific changes need to be made? Delete section if not needed. -->
- Update file X
- Modify configuration Y
- Add/remove dependency Z

## Success Criteria
<!-- Optional: How will we know this task is complete? Delete section if not needed. -->
- [ ] CI passes
- [ ] No breaking changes
- [ ] Documentation updated if needed

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Related issues, urgency, dependencies on other tasks.
"""

PR_TEMPLATE = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.
# Mark checkboxes with [x] where applicable.

## Description
<!-- Required: What does this PR do? -->
Provide a clear description of your changes.

## Related Issue
<!-- Link to the issue this PR addresses -->
Closes #ISSUE_NUMBER

## Type of Change
<!-- Mark ONE with [x] -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Test improvement

## Changes Made
<!-- List the main changes -->
- Change 1
- Change 2
- Change 3

## Testing
<!-- Mark with [x] what applies -->
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Manually tested the changes

## Checklist
<!-- Mark with [x] what you've done -->
- [ ] My code follows the code style of this project (ran `doit format`)
- [ ] I have run linting checks (`doit lint`)
- [ ] I have run type checking (`doit type_check`)
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass (`doit test`)
- [ ] I have updated the documentation accordingly
- [ ] I have updated the CHANGELOG.md
- [ ] My changes generate no new warnings

## Screenshots (if applicable)
<!-- Add screenshots or delete this section -->
N/A

## Additional Notes
<!-- Any other information or delete this section -->
N/A
"""


def _get_editor() -> str:
    """Get the user's preferred editor."""
    return os.environ.get("EDITOR", os.environ.get("VISUAL", "vi"))


def _open_editor_with_template(template: str, suffix: str = ".md") -> str | None:
    """Open editor with template and return the edited content.

    Args:
        template: The template content to start with
        suffix: File suffix for the temp file

    Returns:
        The edited content (without comment lines), or None if aborted/unchanged
    """
    import tempfile

    console = Console()
    editor = _get_editor()

    # Create temp file with template
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
        f.write(template)
        temp_path = f.name

    try:
        # Open editor
        console.print(f"[dim]Opening {editor}...[/dim]")
        result = subprocess.run([editor, temp_path])

        if result.returncode != 0:
            console.print("[red]Editor exited with error.[/red]")
            return None

        # Read the edited content
        with open(temp_path) as f:
            content = f.read()

        # Remove comment lines (starting with #) and HTML comments
        lines = []
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#") and not stripped.startswith("##"):
                continue  # Skip comment lines but keep ## headers
            lines.append(line)

        edited = "\n".join(lines)

        # Remove HTML comments <!-- ... -->
        edited = re.sub(r"<!--.*?-->", "", edited, flags=re.DOTALL)

        # Clean up extra blank lines
        edited = re.sub(r"\n{3,}", "\n\n", edited).strip()

        return edited

    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def _parse_markdown_sections(content: str) -> dict[str, str]:
    """Parse markdown content into sections by ## headers.

    Args:
        content: Markdown content with ## headers

    Returns:
        Dict mapping section names to their content
    """
    sections: dict[str, str] = {}
    current_section = ""
    current_content: list[str] = []

    for line in content.split("\n"):
        if line.startswith("## "):
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def _validate_issue_content(sections: dict[str, str], issue_type: str, console: "Console") -> bool:
    """Validate that required sections have content.

    Args:
        sections: Parsed markdown sections
        issue_type: Type of issue (feature, bug, refactor, doc, chore)
        console: Rich console for output

    Returns:
        True if valid, False otherwise
    """
    required: dict[str, list[str]] = {
        "feature": ["Problem", "Proposed Solution"],
        "bug": ["Bug Description", "Steps to Reproduce", "Expected vs Actual Behavior"],
        "refactor": ["Current Code Issue", "Proposed Improvement"],
        "doc": ["Documentation Type", "Description"],
        "chore": ["Chore Type", "Description"],
    }

    missing = []
    placeholder_patterns = [
        "describe the",
        "clear description",
        "paste error",
        "any other relevant",
        "delete section if not needed",
    ]

    for section_name in required.get(issue_type, []):
        content = sections.get(section_name, "").strip()
        if not content:
            missing.append(section_name)
            continue

        # Check for placeholder text
        content_lower = content.lower()
        for pattern in placeholder_patterns:
            if pattern in content_lower:
                console.print(
                    f"[yellow]Warning: '{section_name}' may contain placeholder text.[/yellow]"
                )
                break

    if missing:
        console.print(f"[red]Missing required sections: {', '.join(missing)}[/red]")
        return False

    return True


def _read_body_file(file_path: str, console: "Console") -> str | None:
    """Read body content from a file.

    Args:
        file_path: Path to the file
        console: Rich console for output

    Returns:
        File content, or None if error
    """
    from pathlib import Path

    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        return None

    try:
        return path.read_text()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return None


def task_issue() -> dict[str, Any]:
    """Create a GitHub issue using the appropriate template.

    Supports five issue types: feature, bug, refactor, doc, chore.
    Labels are automatically applied based on the issue type.

    Three modes:
    1. Interactive (default): Opens $EDITOR with template
    2. --body-file: Reads body from a file
    3. --title + --body: Provides content directly (for AI/scripts)

    Examples:
        Interactive:  doit issue --type=feature
        From file:    doit issue --type=doc --title="Add guide" --body-file=issue.md
        Direct:       doit issue --type=chore --title="Update CI" --body="## Description\\n..."
    """

    def create_issue(
        type: str,
        title: str | None = None,
        body: str | None = None,
        body_file: str | None = None,
    ) -> None:
        console = Console()
        console.print()
        console.print(
            Panel.fit(
                f"[bold cyan]Creating {type} Issue[/bold cyan]",
                border_style="cyan",
            )
        )
        console.print()

        # Validate type
        valid_types = ["feature", "bug", "refactor", "doc", "chore"]
        if type not in valid_types:
            console.print(f"[red]Invalid type: {type}. Must be one of: {valid_types}[/red]")
            sys.exit(1)

        # Map type to labels and template
        type_config = {
            "feature": {"labels": "enhancement,needs-triage", "template": ISSUE_TEMPLATE_FEATURE},
            "bug": {"labels": "bug,needs-triage", "template": ISSUE_TEMPLATE_BUG},
            "refactor": {"labels": "refactor,needs-triage", "template": ISSUE_TEMPLATE_REFACTOR},
            "doc": {"labels": "documentation,needs-triage", "template": ISSUE_TEMPLATE_DOC},
            "chore": {"labels": "chore,needs-triage", "template": ISSUE_TEMPLATE_CHORE},
        }
        config = type_config[type]
        labels = config["labels"]

        # Determine body content
        if body_file:
            # Mode 2: Read from file
            body_content = _read_body_file(body_file, console)
            if body_content is None:
                sys.exit(1)
        elif body:
            # Mode 3: Direct body provided
            body_content = body
        else:
            # Mode 1: Interactive editor
            console.print(
                f"[dim]Opening editor with {type} template. "
                "Fill in the sections, save, and exit.[/dim]"
            )
            body_content = _open_editor_with_template(config["template"])
            if body_content is None:
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(0)

        # Parse and validate
        sections = _parse_markdown_sections(body_content)
        if not _validate_issue_content(sections, type, console):
            console.print("[red]Issue content validation failed.[/red]")
            sys.exit(1)

        # Get title if not provided
        if not title:
            console.print("[cyan]Issue title:[/cyan]")
            title = input("> ").strip()
            if not title:
                console.print("[red]Title is required.[/red]")
                sys.exit(1)

        # Create the issue
        console.print("\n[cyan]Creating issue...[/cyan]")
        try:
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "create",
                    "--title",
                    title,
                    "--body",
                    body_content,
                    "--label",
                    labels,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            issue_url = result.stdout.strip()
            console.print()
            console.print(
                Panel.fit(
                    f"[bold green]Issue created successfully![/bold green]\n\n{issue_url}",
                    border_style="green",
                )
            )
        except subprocess.CalledProcessError as e:
            console.print("[red]Failed to create issue:[/red]")
            console.print(f"[red]{e.stderr}[/red]")
            sys.exit(1)

    return {
        "actions": [create_issue],
        "params": [
            {
                "name": "type",
                "short": "t",
                "long": "type",
                "default": "feature",
                "help": "Issue type: feature, bug, refactor, doc, chore",
            },
            {"name": "title", "long": "title", "default": None, "help": "Issue title"},
            {"name": "body", "long": "body", "default": None, "help": "Issue body (markdown)"},
            {
                "name": "body_file",
                "long": "body-file",
                "default": None,
                "help": "Read body from file",
            },
        ],
        "title": title_with_actions,
    }


def task_pr() -> dict[str, Any]:
    """Create a GitHub PR using the repository template.

    Auto-detects current branch and linked issue from branch name.

    Three modes:
    1. Interactive (default): Opens $EDITOR with template
    2. --body-file: Reads body from a file
    3. --title + --body: Provides content directly (for AI/scripts)

    Examples:
        Interactive:  doit pr
        From file:    doit pr --title="feat: add export" --body-file=pr.md
        Direct:       doit pr --title="feat: add export" --body="## Description\\n..."
    """

    def create_pr(
        title: str | None = None,
        body: str | None = None,
        body_file: str | None = None,
        draft: bool = False,
    ) -> None:
        console = Console()
        console.print()
        console.print(
            Panel.fit("[bold cyan]Creating Pull Request[/bold cyan]", border_style="cyan")
        )
        console.print()

        # Check we're not on main
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        if current_branch == "main":
            console.print("[red]Cannot create PR from main branch.[/red]")
            console.print("[yellow]Create a feature branch first.[/yellow]")
            sys.exit(1)

        console.print(f"[dim]Current branch: {current_branch}[/dim]")

        # Try to extract issue number from branch name (e.g., feat/42-description)
        detected_issue = None
        branch_issue_match = re.search(r"/(\d+)-", current_branch)
        if branch_issue_match:
            detected_issue = branch_issue_match.group(1)
            console.print(f"[dim]Detected issue from branch: #{detected_issue}[/dim]")

        # Determine body content
        if body_file:
            # Mode 2: Read from file
            body_content = _read_body_file(body_file, console)
            if body_content is None:
                sys.exit(1)
        elif body:
            # Mode 3: Direct body provided
            body_content = body
        else:
            # Mode 1: Interactive editor
            # Pre-fill issue number if detected
            template = PR_TEMPLATE
            if detected_issue:
                template = template.replace("#ISSUE_NUMBER", f"#{detected_issue}")

            console.print(
                "[dim]Opening editor with PR template. Fill in the sections, save, and exit.[/dim]"
            )
            body_content = _open_editor_with_template(template)
            if body_content is None:
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(0)

        # Validate PR has description
        sections = _parse_markdown_sections(body_content)
        description = sections.get("Description", "").strip()
        if not description or description == "Provide a clear description of your changes.":
            console.print("[red]Description is required.[/red]")
            sys.exit(1)

        # Get title if not provided
        if not title:
            console.print("[cyan]PR title (e.g., 'feat: add export feature'):[/cyan]")
            title = input("> ").strip()
            if not title:
                console.print("[red]Title is required.[/red]")
                sys.exit(1)

        # Create the PR
        console.print("\n[cyan]Creating PR...[/cyan]")
        cmd = ["gh", "pr", "create", "--title", title, "--body", body_content]
        if draft:
            cmd.append("--draft")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            pr_url = result.stdout.strip()
            console.print()
            console.print(
                Panel.fit(
                    f"[bold green]PR created successfully![/bold green]\n\n{pr_url}",
                    border_style="green",
                )
            )
        except subprocess.CalledProcessError as e:
            console.print("[red]Failed to create PR:[/red]")
            console.print(f"[red]{e.stderr}[/red]")
            sys.exit(1)

    return {
        "actions": [create_pr],
        "params": [
            {"name": "title", "long": "title", "default": None, "help": "PR title"},
            {"name": "body", "long": "body", "default": None, "help": "PR body (markdown)"},
            {
                "name": "body_file",
                "long": "body-file",
                "default": None,
                "help": "Read body from file",
            },
            {
                "name": "draft",
                "long": "draft",
                "type": bool,
                "default": False,
                "help": "Create as draft PR",
            },
        ],
        "title": title_with_actions,
    }

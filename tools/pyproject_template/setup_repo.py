#!/usr/bin/env python3
"""
setup-repo.py - Automated GitHub Repository Setup from pyproject-template

This script automates the creation and configuration of a new GitHub repository
based on the pyproject-template. It handles repository creation, settings
configuration, branch protection, and placeholder replacement.

Usage:
    python3 setup-repo.py
    curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/bootstrap.py \
        | python3

Requirements:
    - GitHub CLI (gh) installed and authenticated
    - Git installed
    - Python 3.12+

Author: Generated from pyproject-template
License: MIT
"""

import os
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any

# Support running as script or as module
_script_dir = Path(__file__).parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

# Import shared utilities
from utils import (  # noqa: E402
    FILES_TO_UPDATE,
    TEMPLATE_REPO,
    Colors,
    GitHubCLI,
    Logger,
    command_exists,
    get_git_config,
    prompt,
    prompt_confirm,
    update_file,
    update_test_files,
)


class RepositorySetup:
    """Main class for repository setup orchestration."""

    # Use TEMPLATE_REPO from utils.py as the single source of truth
    TEMPLATE_FULL = TEMPLATE_REPO

    def __init__(self) -> None:
        self.config: dict[str, Any] = {}
        self.start_dir = os.getcwd()

    def print_banner(self) -> None:
        """Print welcome banner."""
        print()
        print(
            f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗{Colors.NC}"
        )
        print(
            f"{Colors.CYAN}║                                                           ║{Colors.NC}"
        )
        print(
            f"{Colors.CYAN}║     Python Project Template - Repository Setup            ║{Colors.NC}"
        )
        print(
            f"{Colors.CYAN}║                                                           ║{Colors.NC}"
        )
        print(
            f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════╝{Colors.NC}"
        )
        print()

    def check_requirements(self) -> None:
        """Check that all required tools are installed."""
        Logger.step("Checking requirements...")

        # Check for gh CLI
        if not command_exists("gh"):
            Logger.error("GitHub CLI (gh) is not installed")
            print("  Install from: https://cli.github.com/")
            sys.exit(1)

        gh_version = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
        ).stdout.split("\n")[0]
        Logger.success(f"GitHub CLI found: {gh_version}")

        # Check gh authentication
        if not GitHubCLI.is_authenticated():
            Logger.error("GitHub CLI is not authenticated")
            print("  Run: gh auth login")
            sys.exit(1)
        Logger.success("GitHub CLI authenticated")

        # Check token type and permissions
        self._check_token_permissions()

        # Check for git
        if not command_exists("git"):
            Logger.error("Git is not installed")
            print("  Install from: https://git-scm.com/downloads")
            sys.exit(1)

        git_version = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
        ).stdout.strip()
        Logger.success(f"Git found: {git_version}")

        # Check for uv
        if not command_exists("uv"):
            Logger.error("uv is not installed")
            print("  Install from: https://docs.astral.sh/uv/getting-started/installation/")
            sys.exit(1)

        uv_version = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
        ).stdout.strip()
        Logger.success(f"uv found: {uv_version}")

    def _check_token_permissions(self) -> None:
        """Check GitHub token type and permissions."""
        Logger.info("Checking GitHub token permissions...")

        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
        )
        auth_info = result.stderr + result.stdout

        if "github_pat_" in auth_info or "gho_" in auth_info:
            Logger.warning("You're using a Personal Access Token (PAT)")
            print()
            print(f"  {Colors.YELLOW}Required permissions for fine-grained PAT:{Colors.NC}")
            print("  - Repository permissions:")
            print("    • Administration: Read and write")
            print("    • Contents: Read and write")
            print("    • Metadata: Read")
            print()
            print(f"  {Colors.YELLOW}To create/update your PAT:{Colors.NC}")
            print("  1. Go to: https://github.com/settings/tokens?type=beta")
            print("  2. Create new token or edit existing")
            print("  3. Select 'All repositories' or specific repos")
            print("  4. Add the permissions listed above")
            print("  5. Generate token and run: gh auth login")
            print()

            if not prompt_confirm("Do you have the required permissions configured?", default=True):
                Logger.error("Please configure your PAT with required permissions first")
                sys.exit(1)
        else:
            Logger.success("Token type appears to be OAuth (recommended)")

    def gather_inputs(self) -> None:
        """Gather repository configuration from user."""
        Logger.step("Gathering repository information...")
        print()

        # Repository name
        self.config["repo_name"] = prompt("Repository name")

        # Organization (optional)
        if prompt_confirm("Create in an organization?"):
            self.config["repo_owner"] = prompt("Organization name")
        else:
            # Get current user
            user_info = GitHubCLI.api("user")
            self.config["repo_owner"] = user_info["login"]

        self.config["repo_full"] = f"{self.config['repo_owner']}/{self.config['repo_name']}"

        # Visibility
        self.config["visibility"] = (
            "public" if prompt_confirm("Make repository public?", default=True) else "private"
        )

        # Package configuration
        print()
        Logger.info("Package configuration (used for placeholder replacement)")

        default_package = self.config["repo_name"].replace("-", "_")
        self.config["package_name"] = prompt(
            "Python package name (import name)", default=default_package
        )
        self.config["pypi_name"] = prompt("PyPI package name", default=self.config["repo_name"])
        self.config["description"] = prompt(
            "Package description",
            default="A Python project based on pyproject-template",
        )

        # Get git config for defaults
        git_name = get_git_config("user.name", "")
        git_email = get_git_config("user.email", "")

        self.config["author_name"] = prompt("Author name", default=git_name)
        self.config["author_email"] = prompt("Author email", default=git_email)

        # Confirmation
        print()
        Logger.step("Configuration summary:")
        print(f"  Repository: {self.config['repo_full']}")
        print(f"  Visibility: {self.config['visibility']}")
        print(f"  Package name: {self.config['package_name']}")
        print(f"  PyPI name: {self.config['pypi_name']}")
        print(f"  Description: {self.config['description']}")
        print(f"  Author: {self.config['author_name']} <{self.config['author_email']}>")
        print()

        if not prompt_confirm("Proceed with these settings?", default=True):
            Logger.warning("Setup cancelled by user")
            sys.exit(0)

    def create_github_repository(self) -> None:
        """Create repository on GitHub from template (without cloning)."""
        Logger.step("Creating repository on GitHub from template...")

        try:
            # Use REST API to create from template
            data = {
                "owner": self.config["repo_owner"],
                "name": self.config["repo_name"],
                "description": self.config["description"],
                "private": self.config["visibility"] == "private",
                "include_all_branches": False,
            }

            GitHubCLI.api(f"repos/{self.TEMPLATE_FULL}/generate", method="POST", data=data)
            Logger.success(f"Repository created: https://github.com/{self.config['repo_full']}")

        except subprocess.CalledProcessError as e:
            Logger.error("Failed to create repository from template")
            print()

            # Always show the actual error message
            if e.stderr:
                print(f"{Colors.RED}Error details:{Colors.NC}")
                print(f"  {e.stderr.strip()}")
                print()

            # Provide specific help for known errors
            if e.stderr and "Resource not accessible by personal access token" in e.stderr:
                print(f"{Colors.YELLOW}Solution:{Colors.NC}")
                print()
                print(f"1. {Colors.CYAN}Re-authenticate with OAuth (recommended):{Colors.NC}")
                print("   gh auth logout")
                print("   gh auth login")
                print("   # Choose: GitHub.com → HTTPS → Login with browser")
                print()
                print(f"2. {Colors.CYAN}Or update your fine-grained PAT:{Colors.NC}")
                print("   https://github.com/settings/tokens?type=beta")
                print("   Required permissions:")
                print("   - Administration: Read and write")
                print("   - Contents: Read and write")
                print("   - Metadata: Read")
                print()
            elif e.stderr and "name already exists" in e.stderr.lower():
                print(f"{Colors.YELLOW}Solution:{Colors.NC}")
                print(f"  A repository named '{self.config['repo_name']}' already exists.")
                print("  Choose a different name or delete the existing repository at:")
                print(f"  https://github.com/{self.config['repo_full']}/settings")
                print()

            sys.exit(1)

        # Wait a moment for repo to be fully ready
        import time

        time.sleep(2)

    def clone_repository(self) -> None:
        """Clone the repository locally and change to its directory."""
        Logger.step("Cloning repository locally...")

        try:
            GitHubCLI.run(
                ["repo", "clone", self.config["repo_full"], self.config["repo_name"]], capture=False
            )
            Logger.success("Repository cloned locally")
        except subprocess.CalledProcessError:
            Logger.error("Failed to clone repository")
            print(f"  You can try cloning manually: gh repo clone {self.config['repo_full']}")
            sys.exit(1)

        # Change to repo directory
        os.chdir(self.config["repo_name"])

    def configure_placeholders(self) -> None:
        """Configure project placeholders by replacing template strings."""
        Logger.step("Configuring project placeholders...")

        try:
            # Define replacements
            replacements = {
                # URLs
                "https://github.com/username/package_name": f"https://github.com/{self.config['repo_owner']}/{self.config['package_name']}",
                f"https://github.com/username/{self.config['package_name']}": f"https://github.com/{self.config['repo_owner']}/{self.config['package_name']}",
                "gh username/package_name": f"gh {self.config['repo_owner']}/{self.config['package_name']}",
                "username/package_name": f"{self.config['repo_owner']}/{self.config['package_name']}",
                "username": self.config["repo_owner"],
                # Package names
                "package_name": self.config["package_name"],
                "package-name": self.config["pypi_name"],
                "Package Name": self.config["repo_name"],
                # Metadata
                "A short description of your package": self.config["description"],
                "Your Name": self.config["author_name"],
                "your.email@example.com": self.config["author_email"],
            }

            # Update main configuration files (using shared constant from utils.py)
            for file_path in FILES_TO_UPDATE:
                path = Path(file_path)
                if path.exists():
                    update_file(path, replacements)

            # Update documentation files
            docs_dir = Path("docs")
            if docs_dir.exists():
                for doc_file in docs_dir.rglob("*.md"):
                    update_file(doc_file, replacements)

            # Update test files (limited replacements to preserve test data)
            tests_dir = Path("tests")
            if tests_dir.exists():
                update_test_files(tests_dir, self.config["package_name"])

            # Remove template tool tests (they're only for the template itself)
            tool_tests_dir = Path("tests/pyproject_template")
            if tool_tests_dir.exists():
                shutil.rmtree(tool_tests_dir)
                Logger.info("Removed template tool tests (tests/pyproject_template/)")

            # Update source files
            src_dir = Path("src")
            if src_dir.exists():
                for src_file in src_dir.rglob("*.py"):
                    update_file(src_file, replacements)

            # Update issue templates
            issue_templates_dir = Path(".github/ISSUE_TEMPLATE")
            if issue_templates_dir.exists():
                for template_file in issue_templates_dir.glob("*.md"):
                    update_file(template_file, replacements)
                # Also update config.yml if it exists
                config_file = issue_templates_dir / "config.yml"
                if config_file.exists():
                    update_file(config_file, replacements)

            # Update example files
            examples_dir = Path("examples")
            if examples_dir.exists():
                for example_file in examples_dir.rglob("*"):
                    if example_file.is_file():
                        update_file(example_file, replacements)

            # Rename package directory
            old_package_dir = Path("src/package_name")
            new_package_dir = Path(f"src/{self.config['package_name']}")
            if old_package_dir.exists() and old_package_dir != new_package_dir:
                shutil.move(str(old_package_dir), str(new_package_dir))
                Logger.success(f"Renamed package directory to src/{self.config['package_name']}")

            Logger.success("Placeholders configured")

            # Commit the changes
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            commit_msg = f"""
chore: configure project from template

- Set project name to {self.config['repo_name']}
- Configure package as {self.config['package_name']}
- Set author to {self.config['author_name']}

🤖 Generated with setup-repo.py"""

            # Use --no-verify to bypass pre-commit hooks (like no-commit-to-main)
            # This is necessary because we are initializing the repo on main
            subprocess.run(
                ["git", "commit", "-m", commit_msg, "--no-verify"], check=True, capture_output=True
            )
            subprocess.run(["git", "push"], check=True, capture_output=True)
            Logger.success("Changes committed and pushed")

        except Exception as e:
            Logger.warning(f"Placeholder configuration failed: {e}")
            import traceback

            traceback.print_exc()

    def setup_development_environment(self) -> None:
        """Set up the development environment with dependencies and pre-commit hooks."""
        Logger.step("Setting up development environment...")

        try:
            # Install dependencies
            Logger.info("Installing dependencies with uv sync --all-extras...")
            result = subprocess.run(
                ["uv", "sync", "--all-extras"],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                Logger.warning("Failed to install dependencies")
                Logger.info("You can install manually with: uv sync --all-extras")
                return

            Logger.success("Dependencies installed")

            # Install pre-commit hooks
            Logger.info("Installing pre-commit hooks...")
            result = subprocess.run(
                ["uv", "run", "pre-commit", "install"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                Logger.success("Pre-commit hooks installed")
            else:
                Logger.warning("Failed to install pre-commit hooks")
                Logger.info("You can install manually with: uv run pre-commit install")

            # Fix linting issues (including import ordering)
            # Note: We run ruff directly with --fix because doit lint only checks,
            # doesn't auto-fix. This fixes import ordering (I001) and other auto-fixable issues.
            Logger.info("Fixing linting issues with ruff...")
            subprocess.run(
                ["uv", "run", "ruff", "check", "--fix", "."],
                capture_output=True,
                text=True,
            )

            # Format pyproject.toml using doit task
            Logger.info("Formatting pyproject.toml...")
            subprocess.run(
                ["uv", "run", "doit", "fmt_pyproject"],
                capture_output=True,
                text=True,
            )

            # Format code using doit task
            Logger.info("Formatting code with ruff...")
            subprocess.run(
                ["uv", "run", "doit", "format"],
                capture_output=True,
                text=True,
            )

            # Run validation checks BEFORE committing
            Logger.info("Running validation checks (doit check)...")
            check_result = subprocess.run(
                ["uv", "run", "doit", "check"],
                capture_output=False,
                text=True,
            )

            if check_result.returncode != 0:
                Logger.error("Validation checks failed")
                print()
                print(f"{Colors.YELLOW}Please fix the issues above before continuing.{Colors.NC}")
                print("The formatting changes have been applied but not committed.")
                print()
                print("After fixing issues, you can commit with:")
                print("  git add .")
                print("  git commit -m 'chore: apply code formatting'")
                print("  git push")
                print()
                return

            Logger.success("All validation checks passed")

            # Check if there are any formatting changes to commit
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
            )

            if result.stdout.strip():
                Logger.info("Committing formatting changes...")
                subprocess.run(["git", "add", "."], check=True, capture_output=True)
                commit_msg = """
chore: apply code formatting

- Fix linting issues with ruff
- Format pyproject.toml with pyproject-fmt
- Format code with ruff

🤖 Generated with setup-repo.py"""
                commit_result = subprocess.run(
                    ["git", "commit", "-m", commit_msg, "--no-verify"],
                    capture_output=True,
                    text=True,
                )
                if commit_result.returncode != 0:
                    Logger.error("Failed to commit formatting changes")
                    print()
                    print(f"{Colors.RED}Git commit error:{Colors.NC}")
                    if commit_result.stderr:
                        print(f"  {commit_result.stderr.strip()}")
                    if commit_result.stdout:
                        print(f"  {commit_result.stdout.strip()}")
                    print()
                    print(f"{Colors.YELLOW}Possible solutions:{Colors.NC}")
                    print("  1. Check pre-commit hook output above for specific issues")
                    print("  2. Fix any failing pre-commit checks manually")
                    print("  3. Run: git status")
                    print("  4. Review changes and commit manually")
                    print()
                    return

                push_result = subprocess.run(
                    ["git", "push"],
                    capture_output=True,
                    text=True,
                )
                if push_result.returncode != 0:
                    Logger.error("Failed to push formatting changes")
                    if push_result.stderr:
                        print(f"  Error: {push_result.stderr.strip()}")
                    print("  You can push manually later with: git push")
                else:
                    Logger.success("Formatting changes committed and pushed")
            else:
                Logger.success("No formatting changes needed")

        except subprocess.CalledProcessError as e:
            Logger.error("Development environment setup failed")
            print()
            print(f"{Colors.RED}Error details:{Colors.NC}")
            if e.stderr:
                print(f"  {e.stderr.strip()}")
            if e.stdout:
                print(f"  {e.stdout.strip()}")
            print()
            print(f"{Colors.YELLOW}You can complete setup manually with:{Colors.NC}")
            print("  cd", self.config["repo_name"])
            print("  uv sync --all-extras")
            print("  uv run pre-commit install")
            print("  uv run doit check")
            print()
        except Exception as e:
            Logger.error(f"Development environment setup failed: {e}")
            print()
            import traceback

            print(f"{Colors.RED}Full error:{Colors.NC}")
            traceback.print_exc()
            print()
            print(f"{Colors.YELLOW}You can complete setup manually with:{Colors.NC}")
            print("  cd", self.config["repo_name"])
            print("  uv sync --all-extras")
            print("  uv run pre-commit install")
            print("  uv run doit check")
            print()

    def configure_repository_settings(self) -> None:
        """Configure repository settings to match template."""
        Logger.step("Configuring repository settings...")

        try:
            # Get ALL settings from template repository
            template_settings = GitHubCLI.api(f"repos/{self.TEMPLATE_FULL}")

            # Read-only fields that should not be copied
            readonly_fields = {
                # URLs
                "archive_url",
                "assignees_url",
                "blobs_url",
                "branches_url",
                "clone_url",
                "collaborators_url",
                "comments_url",
                "commits_url",
                "compare_url",
                "contents_url",
                "contributors_url",
                "deployments_url",
                "downloads_url",
                "events_url",
                "forks_url",
                "git_commits_url",
                "git_refs_url",
                "git_tags_url",
                "git_url",
                "hooks_url",
                "html_url",
                "issue_comment_url",
                "issue_events_url",
                "issues_url",
                "keys_url",
                "labels_url",
                "languages_url",
                "merges_url",
                "milestones_url",
                "notifications_url",
                "pulls_url",
                "releases_url",
                "ssh_url",
                "stargazers_url",
                "statuses_url",
                "subscribers_url",
                "subscription_url",
                "svn_url",
                "tags_url",
                "teams_url",
                "trees_url",
                "url",
                # IDs and metadata
                "id",
                "node_id",
                "owner",
                "full_name",
                "name",
                # Timestamps
                "created_at",
                "updated_at",
                "pushed_at",
                # Counts and computed values
                "forks",
                "forks_count",
                "open_issues",
                "open_issues_count",
                "size",
                "stargazers_count",
                "watchers",
                "watchers_count",
                "subscribers_count",
                "network_count",
                # Other read-only
                "fork",
                "language",
                "license",
                "permissions",
                "disabled",
                "mirror_url",
                "default_branch",  # Keep as main
                "private",  # Set separately via visibility
                "is_template",  # Don't make new repos templates
                # Deprecated
                "use_squash_pr_title_as_default",
            }

            # Build settings data by copying all writable fields from template
            data = {}
            for key, value in template_settings.items():
                if key not in readonly_fields and value is not None:
                    data[key] = value

            # Override description with user's description
            data["description"] = self.config["description"]

            # Check if repository is in an organization
            owner_info = GitHubCLI.api(f"users/{self.config['repo_owner']}")
            is_org = owner_info.get("type") == "Organization"

            # Remove allow_forking if not an org repo (only applies to orgs)
            if not is_org and "allow_forking" in data:
                data.pop("allow_forking")

            # Remove security_and_analysis - we'll handle it separately
            security_settings = data.pop("security_and_analysis", None)

            # Apply all settings in one call
            GitHubCLI.api(f"repos/{self.config['repo_full']}", method="PATCH", data=data)
            Logger.success("Repository settings configured")

            # Configure security and analysis settings separately
            if security_settings:
                self._configure_security_settings({"security_and_analysis": security_settings})

        except subprocess.CalledProcessError as e:
            Logger.warning("Repository settings configuration failed")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")
            Logger.info("You can configure settings manually at:")
            Logger.info(f"  https://github.com/{self.config['repo_full']}/settings")

    def _configure_security_settings(self, template_settings: dict[str, Any]) -> None:
        """Configure security and analysis settings."""
        security_settings = template_settings.get("security_and_analysis", {})

        if not security_settings:
            return

        # Enable secret scanning if template has it
        if security_settings.get("secret_scanning", {}).get("status") == "enabled":
            try:
                GitHubCLI.api(
                    f"repos/{self.config['repo_full']}/secret-scanning",
                    method="PATCH",
                    data={"status": "enabled"},
                )
                Logger.success("Secret scanning enabled")
            except subprocess.CalledProcessError as e:
                # 404 is expected for free/private repos that don't support this
                if "404" in str(e.stderr):
                    if self.config.get("visibility") == "public":
                        Logger.success("Secret scanning enabled (default for public repos)")
                    else:
                        Logger.info("Secret scanning not available (requires GHAS or public repo)")
                else:
                    Logger.warning("Secret scanning configuration failed")
                    if e.stderr:
                        print(f"  Error: {e.stderr.strip()}")

        # Enable secret scanning push protection if template has it
        if security_settings.get("secret_scanning_push_protection", {}).get("status") == "enabled":
            try:
                GitHubCLI.api(
                    f"repos/{self.config['repo_full']}/secret-scanning/push-protection",
                    method="PATCH",
                    data={"status": "enabled"},
                )
                Logger.success("Secret scanning push protection enabled")
            except subprocess.CalledProcessError as e:
                if "404" in str(e.stderr):
                    if self.config.get("visibility") == "public":
                        Logger.success(
                            "Secret scanning push protection enabled (default for public repos)"
                        )
                    else:
                        Logger.info(
                            "Secret scanning push protection not available for this repository"
                        )
                else:
                    Logger.warning("Secret scanning push protection configuration failed")
                    if e.stderr:
                        print(f"  Error: {e.stderr.strip()}")

        # Enable Dependabot security updates if template has it
        if security_settings.get("dependabot_security_updates", {}).get("status") == "enabled":
            try:
                GitHubCLI.api(
                    f"repos/{self.config['repo_full']}/automated-security-fixes",
                    method="PUT",
                )
                Logger.success("Dependabot security updates enabled")
            except subprocess.CalledProcessError as e:
                Logger.warning("Dependabot security updates configuration failed")
                if e.stderr:
                    print(f"  Error: {e.stderr.strip()}")

    def configure_branch_protection(self) -> None:
        """Configure branch protection using rulesets."""
        Logger.step("Configuring branch protection rulesets...")

        try:
            # Get rulesets from template
            template_rulesets = GitHubCLI.api(f"repos/{self.TEMPLATE_FULL}/rulesets")

            if not template_rulesets:
                Logger.warning("No rulesets found in template repository")
                return

            # Replicate each ruleset
            for template_ruleset in template_rulesets:
                # Get full ruleset details
                ruleset_id = template_ruleset["id"]
                full_ruleset = GitHubCLI.api(f"repos/{self.TEMPLATE_FULL}/rulesets/{ruleset_id}")

                # Prepare ruleset data for creation (remove read-only fields)
                ruleset_data = {
                    "name": full_ruleset["name"],
                    "target": full_ruleset["target"],
                    "enforcement": full_ruleset["enforcement"],
                    "bypass_actors": full_ruleset.get("bypass_actors", []),
                    "conditions": full_ruleset.get("conditions", {}),
                    "rules": full_ruleset.get("rules", []),
                }

                # Create ruleset in new repository
                GitHubCLI.api(
                    f"repos/{self.config['repo_full']}/rulesets",
                    method="POST",
                    data=ruleset_data,
                )
                Logger.success(f"Ruleset '{full_ruleset['name']}' configured")

        except subprocess.CalledProcessError as e:
            Logger.warning("Branch protection ruleset configuration failed")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")
            Logger.info("You can configure rulesets manually at:")
            Logger.info(f"  https://github.com/{self.config['repo_full']}/settings/rules")

    def replicate_labels(self) -> None:
        """Replicate labels from template."""
        Logger.step("Replicating labels from template...")

        try:
            # Get labels from template
            labels = GitHubCLI.api(f"repos/{self.TEMPLATE_FULL}/labels")

            if not labels:
                Logger.warning("Could not retrieve labels from template")
                return

            # Create each label
            for label in labels:
                try:
                    label_data = {
                        "name": label["name"],
                        "color": label["color"],
                        "description": label.get("description", ""),
                    }
                    GitHubCLI.api(
                        f"repos/{self.config['repo_full']}/labels",
                        method="POST",
                        data=label_data,
                    )
                except subprocess.CalledProcessError:
                    # Label might already exist, skip
                    pass

            Logger.success("Labels replicated")

        except subprocess.CalledProcessError as e:
            Logger.warning("Failed to retrieve labels from template")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")

    def enable_github_pages(self) -> None:
        """Enable GitHub Pages."""
        Logger.step("Enabling GitHub Pages...")

        try:
            data = {
                "source": {
                    "branch": "gh-pages",
                    "path": "/",
                }
            }
            GitHubCLI.api(f"repos/{self.config['repo_full']}/pages", method="POST", data=data)
            Logger.success("GitHub Pages enabled")
        except subprocess.CalledProcessError:
            Logger.warning("GitHub Pages not enabled (gh-pages branch doesn't exist yet)")
            Logger.info("Pages will be enabled automatically after first docs deployment")

    def configure_codeql(self) -> None:
        """Configure CodeQL code scanning to match template."""
        Logger.step("Configuring CodeQL code scanning...")

        try:
            # Get CodeQL setup from template
            template_codeql = GitHubCLI.api(
                f"repos/{self.TEMPLATE_FULL}/code-scanning/default-setup"
            )

            if template_codeql.get("state") != "configured":
                Logger.info("CodeQL not configured in template, skipping")
                return

            # Replicate CodeQL configuration
            codeql_data = {
                "state": "configured",
                "query_suite": template_codeql.get("query_suite", "default"),
            }

            # Add languages if specified (will auto-detect if not provided)
            if template_codeql.get("languages"):
                codeql_data["languages"] = template_codeql["languages"]

            GitHubCLI.api(
                f"repos/{self.config['repo_full']}/code-scanning/default-setup",
                method="PATCH",
                data=codeql_data,
            )
            Logger.success(
                f"CodeQL configured with {template_codeql.get('query_suite', 'default')} query suite"
            )

        except subprocess.CalledProcessError as e:
            Logger.warning("CodeQL configuration failed")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")
            Logger.info("You can configure CodeQL manually at:")
            Logger.info(f"  https://github.com/{self.config['repo_full']}/security/code-scanning")

    def print_manual_steps(self) -> None:
        """Print manual steps that need to be completed."""
        print()
        print(
            f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗{Colors.NC}"
        )
        print(
            f"{Colors.CYAN}║                  Setup Complete! 🎉                       ║{Colors.NC}"
        )
        print(
            f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════╝{Colors.NC}"
        )
        print()
        Logger.success(
            f"Repository created and configured: https://github.com/{self.config['repo_full']}"
        )
        print()

        Logger.step("Manual steps required:")
        print()
        print(f"  {Colors.YELLOW}[ ]{Colors.NC} Add PyPI token to repository secrets:")
        print(f"      gh secret set PYPI_TOKEN --repo {self.config['repo_full']}")
        print()
        print(
            f"  {Colors.YELLOW}[ ]{Colors.NC} Add TestPyPI token to repository secrets (optional):"
        )
        print(f"      gh secret set TEST_PYPI_TOKEN --repo {self.config['repo_full']}")
        print()
        print(
            f"  {Colors.YELLOW}[ ]{Colors.NC} Add Codecov token to repository secrets (optional):"
        )
        print(f"      gh secret set CODECOV_TOKEN --repo {self.config['repo_full']}")
        print()
        print(f"  {Colors.YELLOW}[ ]{Colors.NC} Review and adjust repository settings:")
        print(f"      https://github.com/{self.config['repo_full']}/settings")
        print()
        print(f"  {Colors.YELLOW}[ ]{Colors.NC} Review branch protection rulesets:")
        print(f"      https://github.com/{self.config['repo_full']}/settings/rules")
        print()
        print(f"  {Colors.YELLOW}[ ]{Colors.NC} Invite collaborators (if needed):")
        print(f"      https://github.com/{self.config['repo_full']}/settings/access")
        print()

        Logger.step("Cleanup Recommendations:")
        print("  You can safely remove the following setup scripts:")
        print("  - bootstrap.py")
        print("  - tools/pyproject_template/configure.py")
        print("  - tools/pyproject_template/setup_repo.py")
        print()

        Logger.step("You're all set!")
        print()
        repo_path = os.path.join(self.start_dir, self.config["repo_name"])
        print(f"  {Colors.GREEN}✓{Colors.NC} Repository cloned to: {repo_path}")
        print(f"  {Colors.GREEN}✓{Colors.NC} Dependencies installed")
        print(f"  {Colors.GREEN}✓{Colors.NC} Pre-commit hooks configured")
        print(f"  {Colors.GREEN}✓{Colors.NC} Code formatted and validated")
        print()
        print("  Navigate to your repository and start developing:")
        print(f"     cd {self.config['repo_name']}")
        print()

        Logger.info(
            f"Documentation: https://github.com/{self.config['repo_full']}/blob/main/README.md"
        )
        print()

    def run(self) -> None:
        """Run the complete setup process.

        Order of operations:
        1. Create GitHub repository (fail fast if there are auth/permission issues)
        2. Configure all GitHub settings (before cloning to avoid partial setup)
        3. Clone repository locally
        4. Configure local files and development environment
        """
        self.print_banner()
        self.check_requirements()
        self.gather_inputs()

        # Create repository on GitHub and configure all GitHub settings
        # BEFORE cloning to avoid partial setup if GitHub operations fail
        self.create_github_repository()
        self.configure_repository_settings()
        self.configure_branch_protection()
        self.replicate_labels()
        self.enable_github_pages()
        self.configure_codeql()

        # Now clone and configure locally
        self.clone_repository()
        self.configure_placeholders()
        self.setup_development_environment()

        self.print_manual_steps()


def main() -> None:
    """Main entry point."""
    try:
        setup = RepositorySetup()
        setup.run()
    except KeyboardInterrupt:
        print()
        Logger.warning("Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print()
        Logger.error(f"Setup failed with unexpected error: {e}")
        print()
        print("This is likely a bug in the setup script.")
        print("Please report this issue with the error details above at:")
        print("  https://github.com/endavis/pyproject-template/issues")
        print()

        # Show traceback for debugging
        import traceback

        print("Full traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("This script should not be run directly.")
    print("Please use: python manage.py")
    sys.exit(1)

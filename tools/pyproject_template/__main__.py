#!/usr/bin/env python3
"""
Unified template management script with menu-driven interface.

Usage:
    # Interactive (default)
    python -m tools.pyproject_template

    # Quick actions
    python -m tools.pyproject_template update      # Check for template updates
    python -m tools.pyproject_template configure   # Re-run configuration
    python -m tools.pyproject_template repo        # Update repository settings
    python -m tools.pyproject_template full        # Full setup (all of the above)

    # Non-interactive
    python -m tools.pyproject_template --yes --update-only
    python -m tools.pyproject_template --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tools.pyproject_template.check_template_updates import run_check_updates
from tools.pyproject_template.configure import load_defaults, run_configure
from tools.pyproject_template.settings import (
    SETTINGS_FILE,
    PreflightWarning,
    ProjectContext,
    ProjectSettings,
    SettingsManager,
    TemplateState,
    get_template_commits_since,
    get_template_latest_commit,
)
from tools.pyproject_template.utils import Colors, Logger, prompt


def print_banner() -> None:
    """Print the welcome banner."""
    print()
    print(f"{Colors.CYAN}pyproject-template{Colors.NC}")
    print()


def print_section(title: str) -> None:
    """Print a section header."""
    width = 60
    print(f"{Colors.BOLD}{'=' * width}{Colors.NC}")
    print(f"{Colors.BOLD}{title:^{width}}{Colors.NC}")
    print(f"{Colors.BOLD}{'=' * width}{Colors.NC}")
    print()


def print_warnings(warnings: list[PreflightWarning]) -> None:
    """Print preflight warnings."""
    if not warnings:
        return

    print_section("Warnings")
    for warning in warnings:
        print(f"  {Colors.YELLOW}!{Colors.NC} {warning.message}")
        if warning.suggestion:
            print(f"    {Colors.CYAN}({warning.suggestion}){Colors.NC}")
    print()


def print_settings(settings: ProjectSettings, context: ProjectContext) -> None:
    """Print detected settings."""
    print_section("Detected Settings")

    print(f"  Project name:      {settings.project_name or '(not set)'}")
    print(f"  Package name:      {settings.package_name or '(not set)'}")
    print(f"  PyPI name:         {settings.pypi_name or '(not set)'}")
    if settings.author_name or settings.author_email:
        author = f"{settings.author_name} <{settings.author_email}>"
    else:
        author = "(not set)"
    print(f"  Author:            {author}")
    if settings.github_user or settings.github_repo:
        github = f"{settings.github_user}/{settings.github_repo}"
    else:
        github = "(not set)"
    print(f"  GitHub:            {github}")
    print()

    # Context info
    if context.is_template_repo:
        print(f"  Context:           {Colors.CYAN}Template repository{Colors.NC}")
    elif context.is_existing_repo:
        print("  Context:           Existing repository")
    elif context.is_fresh_clone:
        print("  Context:           Fresh clone (needs setup)")
    else:
        print("  Context:           Not a git repository")
    print()


def print_template_status(
    template_state: TemplateState,
    latest_commit: tuple[str, str] | None,
    recent_commits: list[dict[str, str]] | None,
) -> None:
    """Print template sync status."""
    if template_state.is_synced() and template_state.commit:
        if latest_commit:
            latest_sha, _ = latest_commit
            if latest_sha[:12] == template_state.commit[:12]:
                print(
                    f"  Template status:   {Colors.GREEN}Up to date{Colors.NC} "
                    f"(synced: {template_state.commit_date})"
                )
            else:
                commits_behind = len(recent_commits) if recent_commits else "unknown"
                print(
                    f"  Template status:   {Colors.YELLOW}{commits_behind} commits behind{Colors.NC} "
                    f"(last sync: {template_state.commit_date})"
                )
                if recent_commits and len(recent_commits) > 0:
                    print()
                    print(f"  {Colors.CYAN}Recent changes:{Colors.NC}")
                    for commit in recent_commits[:5]:
                        msg = commit["message"][:50]
                        if len(commit["message"]) > 50:
                            msg += "..."
                        print(f"    - {msg}")
                    if len(recent_commits) > 5:
                        print(f"    ... and {len(recent_commits) - 5} more")
        else:
            print(f"  Template status:   Last sync: {template_state.commit_date}")
    else:
        print(f"  Template status:   {Colors.YELLOW}Never synced with template{Colors.NC}")
    print()


def get_recommended_action(
    context: ProjectContext,
    settings: ProjectSettings,
    template_state: TemplateState,
    latest_commit: tuple[str, str] | None,
) -> int | None:
    """Determine the recommended action based on context."""
    # Fresh clone needs full setup
    if context.is_fresh_clone:
        return 4  # Full setup

    # Placeholder values need configuration
    if settings.has_placeholder_values():
        return 2  # Re-run configuration

    # Existing repo with outdated template
    if template_state.is_synced() and template_state.commit and latest_commit:
        latest_sha, _ = latest_commit
        if latest_sha[:12] != template_state.commit[:12]:
            return 1  # Check for updates

    # If never synced, suggest checking updates
    if not template_state.is_synced():
        return 1  # Check for updates

    return None  # Up to date


def print_menu(recommended: int | None, dry_run: bool) -> None:
    """Print the menu options."""
    print(f"{Colors.BOLD}What would you like to do?{Colors.NC}")
    print()

    options = [
        (1, "Check for template updates"),
        (2, "Re-run configuration"),
        (3, "Update repository settings"),
        (4, "Full setup (all of the above)"),
    ]

    for num, label in options:
        rec = f" {Colors.GREEN}<- recommended{Colors.NC}" if num == recommended else ""
        print(f"  [{num}] {label}{rec}")

    print()
    print("  [e] Edit settings")
    dry_status = "on" if dry_run else "off"
    print(f"  [d] Toggle dry-run (currently: {dry_status})")
    print("  [?] Help")
    print("  [q] Quit")
    print()


def print_help() -> None:
    """Print help text for menu options."""
    print()
    print(f"  {Colors.BOLD}[1] Check for template updates{Colors.NC}")
    print("      Compare your project against the latest template and")
    print("      selectively merge improvements (workflows, configs, etc.)")
    print()
    print(f"  {Colors.BOLD}[2] Re-run configuration{Colors.NC}")
    print("      Update placeholders in all files (useful if you changed")
    print("      project name, author, etc.)")
    print()
    print(f"  {Colors.BOLD}[3] Update repository settings{Colors.NC}")
    print("      Configure GitHub repo settings, branch protection, labels")
    print("      (requires gh CLI authenticated)")
    print()
    print(f"  {Colors.BOLD}[4] Full setup{Colors.NC}")
    print("      Run all of the above in sequence")
    print()
    input("Press enter to return to menu...")


def edit_settings(manager: SettingsManager) -> None:
    """Allow user to edit settings interactively."""
    print()
    Logger.header("Edit Settings")
    print("Enter new values (press Enter to keep current value)")
    print()

    settings = manager.settings

    new_name = prompt("Project name", settings.project_name)
    if new_name:
        settings.project_name = new_name

    new_package = prompt("Package name", settings.package_name)
    if new_package:
        settings.package_name = new_package

    new_pypi = prompt("PyPI name", settings.pypi_name)
    if new_pypi:
        settings.pypi_name = new_pypi

    new_desc = prompt("Description", settings.description)
    if new_desc:
        settings.description = new_desc

    new_author = prompt("Author name", settings.author_name)
    if new_author:
        settings.author_name = new_author

    new_email = prompt("Author email", settings.author_email)
    if new_email:
        settings.author_email = new_email

    new_gh_user = prompt("GitHub user", settings.github_user)
    if new_gh_user:
        settings.github_user = new_gh_user

    new_gh_repo = prompt("GitHub repo", settings.github_repo)
    if new_gh_repo:
        settings.github_repo = new_gh_repo

    manager.save()


def run_action(action: int, manager: SettingsManager, dry_run: bool) -> int:
    """Run the selected action."""
    if action == 1:
        return action_check_updates(manager, dry_run)
    elif action == 2:
        return action_configure(manager, dry_run)
    elif action == 3:
        return action_repo_settings(manager, dry_run)
    elif action == 4:
        return action_full_setup(manager, dry_run)
    else:
        Logger.error(f"Unknown action: {action}")
        return 1


def action_check_updates(manager: SettingsManager, dry_run: bool) -> int:
    """Check for template updates."""
    Logger.header("Checking for Template Updates")

    result = run_check_updates(
        skip_changelog=True,
        keep_template=False,
        dry_run=dry_run,
    )

    if result == 0 and not dry_run:
        # Update template state with latest commit
        latest = get_template_latest_commit()
        if latest:
            commit_sha, commit_date = latest
            manager.update_template_state(commit_sha, commit_date)

    return result


def action_configure(manager: SettingsManager, dry_run: bool) -> int:
    """Re-run configuration."""
    Logger.header("Running Configuration")

    # Prepare defaults from current settings
    defaults = {
        "project_name": manager.settings.project_name,
        "package_name": manager.settings.package_name,
        "pypi_name": manager.settings.pypi_name,
        "description": manager.settings.description,
        "author_name": manager.settings.author_name,
        "author_email": manager.settings.author_email,
        "github_user": manager.settings.github_user,
    }

    # Merge with pyproject.toml defaults
    pyproject_defaults = load_defaults(Path("pyproject.toml"))
    for key, value in pyproject_defaults.items():
        if not defaults.get(key):
            defaults[key] = value

    return run_configure(
        auto=False,
        yes=False,
        dry_run=dry_run,
        defaults=defaults,
    )


def action_repo_settings(manager: SettingsManager, dry_run: bool) -> int:
    """Update repository settings."""
    Logger.header("Updating Repository Settings")

    if dry_run:
        Logger.info("Dry run: Would configure GitHub repository settings")
        Logger.info("  - Repository settings (description, features)")
        Logger.info("  - Branch protection rulesets")
        Logger.info("  - Labels")
        Logger.info("  - GitHub Pages")
        Logger.info("  - CodeQL code scanning")
        return 0

    # Import setup_repo module for repository configuration
    try:
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()
        setup.config = {
            "repo_owner": manager.settings.github_user,
            "repo_name": manager.settings.github_repo,
            "repo_full": f"{manager.settings.github_user}/{manager.settings.github_repo}",
            "description": manager.settings.description,
            "package_name": manager.settings.package_name,
            "pypi_name": manager.settings.pypi_name,
            "author_name": manager.settings.author_name,
            "author_email": manager.settings.author_email,
        }

        # Run individual configuration steps
        setup.configure_repository_settings()
        setup.configure_branch_protection()
        setup.replicate_labels()
        setup.enable_github_pages()
        setup.configure_codeql()

        Logger.success("Repository settings updated")
        return 0

    except Exception as e:
        Logger.error(f"Failed to update repository settings: {e}")
        return 1


def action_full_setup(manager: SettingsManager, dry_run: bool) -> int:
    """Run full setup (all actions in sequence)."""
    Logger.header("Running Full Setup")

    results = []

    # 1. Check for updates
    Logger.step("Step 1/3: Checking for template updates")
    results.append(action_check_updates(manager, dry_run))

    # 2. Configure
    Logger.step("Step 2/3: Running configuration")
    results.append(action_configure(manager, dry_run))

    # 3. Repository settings
    Logger.step("Step 3/3: Updating repository settings")
    results.append(action_repo_settings(manager, dry_run))

    # Summary
    print()
    print_section("Completed Actions")
    actions = ["Check for template updates", "Run configuration", "Update repository settings"]
    for action_name, result in zip(actions, results, strict=False):
        status = f"{Colors.GREEN}v{Colors.NC}" if result == 0 else f"{Colors.RED}x{Colors.NC}"
        print(f"  {status} {action_name}")
    print()

    return 0 if all(r == 0 for r in results) else 1


def interactive_menu(manager: SettingsManager, dry_run: bool = False) -> int:
    """Run the interactive menu loop."""
    while True:
        print_banner()

        # Fetch latest template info
        latest_commit = get_template_latest_commit()
        recent_commits = None
        if manager.template_state.is_synced() and manager.template_state.commit and latest_commit:
            recent_commits = get_template_commits_since(manager.template_state.commit)

        # Display information
        print_warnings(manager.warnings)
        print_settings(manager.settings, manager.context)
        print_template_status(manager.template_state, latest_commit, recent_commits)

        # Get recommended action
        recommended = get_recommended_action(
            manager.context, manager.settings, manager.template_state, latest_commit
        )

        # Show menu
        print_menu(recommended, dry_run)

        # Get user input
        try:
            choice = input("Select option: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if choice == "q":
            return 0
        elif choice == "?":
            print_help()
        elif choice == "e":
            edit_settings(manager)
        elif choice == "d":
            dry_run = not dry_run
            Logger.info(f"Dry run mode: {'enabled' if dry_run else 'disabled'}")
        elif choice in ("1", "2", "3", "4"):
            action = int(choice)
            result = run_action(action, manager, dry_run)
            if result == 0:
                Logger.success("Action completed successfully")
            else:
                Logger.error("Action failed")
            input("\nPress enter to return to menu...")
        else:
            Logger.warning(f"Unknown option: {choice}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m tools.pyproject_template",
        description="Unified template management with menu-driven interface.",
    )

    # Subcommands for quick actions
    subparsers = parser.add_subparsers(dest="command", help="Quick action commands")

    subparsers.add_parser("update", help="Check for template updates")
    subparsers.add_parser("configure", help="Re-run configuration")
    subparsers.add_parser("repo", help="Update repository settings")
    subparsers.add_parser("full", help="Full setup (all of the above)")

    # Global options
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Non-interactive mode (use detected settings, no prompts)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    parser.add_argument(
        "--update-only",
        action="store_true",
        help="Only check for updates (CI-friendly, fails if can't auto-detect)",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    # Initialize settings manager
    manager = SettingsManager(root=Path.cwd())

    # Save settings on first run to create the settings file
    if not (manager.root / SETTINGS_FILE).exists():
        manager.save()

    # Handle quick action commands
    if args.command:
        command_map = {
            "update": 1,
            "configure": 2,
            "repo": 3,
            "full": 4,
        }
        action = command_map.get(args.command)
        if action:
            return run_action(action, manager, args.dry_run)
        return 1

    # Handle --update-only (CI mode)
    if args.update_only:
        if not manager.settings.is_configured():
            Logger.error("Cannot auto-detect settings. Run interactively first.")
            return 1
        return action_check_updates(manager, args.dry_run)

    # Handle --yes (non-interactive mode)
    if args.yes:
        if not manager.settings.is_configured():
            Logger.error("Cannot run non-interactively without configured settings.")
            return 1

        # Run full setup non-interactively
        return action_full_setup(manager, args.dry_run)

    # Interactive mode
    return interactive_menu(manager, args.dry_run)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        Logger.warning("Cancelled by user")
        sys.exit(1)
    except Exception as e:
        Logger.error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

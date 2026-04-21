"""Release-related doit tasks."""

import json
import os
import re
import subprocess  # nosec B404 - subprocess is required for doit tasks
import sys
from typing import TYPE_CHECKING, Any

from doit.tools import title_with_actions
from rich.console import Console

from .base import UV_CACHE_DIR, run_streamed

if TYPE_CHECKING:
    from rich.console import Console as ConsoleType


def validate_merge_commits(console: "ConsoleType") -> bool:
    """Validate that all merge commits follow the required format.

    Returns:
        bool: True if all merge commits are valid, False otherwise.
    """
    console.print("\n[cyan]Validating merge commit format...[/cyan]")

    # Get merge commits since last tag (or all if no tags)
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
        )
        last_tag = result.stdout.strip() if result.returncode == 0 else ""
        # When no tag exists yet (first release), bound the walk to the last
        # 10 commits — matches validate_issue_links below. Walking full HEAD
        # can surface merges from unrelated pre-project history.
        range_spec = f"{last_tag}..HEAD" if last_tag else "HEAD~10..HEAD"

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

    # Pattern: <type>: <subject> (merges PR #XX, addresses #YY) or (merges PR #XX)
    merge_pattern = re.compile(
        r"^[a-f0-9]+\s+(feat|fix|refactor|docs|test|chore|ci|perf):\s.+\s"
        r"\(merges PR #\d+(?:, addresses #\d+(?:, #\d+)*)?\)$"
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
        console.print("  <type>: <subject> (merges PR #XX, addresses #YY)")
        console.print("  <type>: <subject> (merges PR #XX)")
        return False

    console.print("[green]✓ All merge commits follow required format.[/green]")
    return True


def validate_issue_links(console: "ConsoleType") -> bool:
    """Validate that commits (except docs) reference issues.

    Returns:
        bool: True if validation passes, False otherwise.
    """
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


# Version pattern covering:
#   - Production releases:       1.0.0
#   - PEP440 pre-releases:       0.1.0a0, 0.1.0b1, 0.1.0rc0, 0.1.0.dev2
#   - Semver-style pre-releases: 0.1.0-alpha.0, 0.1.0-beta.1, 0.1.0-rc.0
# The optional leading 'v' is stripped; the captured group is the bare version.
_VERSION_PATTERN = r"v?(\d+\.\d+\.\d+(?:[ab]\d+|rc\d+|\.dev\d+|-(?:alpha|beta|rc)\.\d+)?)"


def _extract_version_from_release_pr(pr_title: str, branch_name: str) -> str | None:
    """Extract a release version from a PR title or fall back to the branch name.

    Recognizes the shapes produced by ``task_release`` (and by hand):
      - PR title: ``release: v<version>``
      - Branch:   ``release/v<version>``

    The version portion may be a production release (``1.0.0``), a PEP440
    pre-release (``0.1.0a0``, ``0.1.0b1``, ``0.1.0rc0``, ``0.1.0.dev2``), or a
    semver-style pre-release (``0.1.0-alpha.0``, ``0.1.0-beta.1``,
    ``0.1.0-rc.0``).

    Args:
        pr_title: The PR title to inspect first.
        branch_name: The PR head branch name, used as a fallback.

    Returns:
        The captured version string without the leading ``v`` (e.g. ``"1.0.0"``,
        ``"0.1.0a0"``, ``"0.1.0-alpha.0"``), or ``None`` if neither input matches.
    """
    # Try the PR title first (format: "release: vX.Y.Z[suffix]").
    match = re.search(rf"release:\s*{_VERSION_PATTERN}", pr_title)
    if match:
        return match.group(1)
    # Fall back to the branch name (format: "release/vX.Y.Z[suffix]").
    match = re.search(rf"release/{_VERSION_PATTERN}", branch_name)
    if match:
        return match.group(1)
    return None


def _build_cz_get_next_cmd(increment: str, prerelease: str) -> list[str]:
    """Build the ``cz bump --get-next`` command list with optional flags.

    Pure helper: no validation, no I/O. Callers are responsible for validating
    the ``increment`` and ``prerelease`` values before invoking this helper.

    Args:
        increment: Version increment type (e.g. ``"minor"``, ``"PATCH"``).
            Uppercased before being passed to ``--increment``. Empty string
            means no ``--increment`` flag is appended.
        prerelease: Pre-release type (e.g. ``"alpha"``, ``"beta"``, ``"rc"``).
            Passed verbatim to ``--prerelease``. Empty string means no
            ``--prerelease`` flag is appended.

    Returns:
        The command list ready to hand to ``subprocess.run``.
    """
    cmd = ["uv", "run", "cz", "bump", "--get-next"]
    if increment:
        cmd.extend(["--increment", increment.upper()])
    if prerelease:
        cmd.extend(["--prerelease", prerelease])
    return cmd


def task_release(increment: str = "", prerelease: str = "") -> dict[str, Any]:
    """Create a release PR with changelog updates (PR-based release flow).

    This is the single supported release entry point. It creates a release
    branch, updates ``CHANGELOG.md``, and opens a pull request. After a
    reviewer merges the PR, run ``doit release_tag`` to tag ``main`` and
    trigger the publish workflow.

    Args:
        increment (str): Force version increment type (MAJOR, MINOR, PATCH). Auto-detects if empty.
        prerelease (str): Pre-release type (alpha, beta, rc). Empty for a production release.
            Mutually exclusive with ``increment``.
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

        # Validate prerelease value
        allowed_prerelease = {"", "alpha", "beta", "rc"}
        if prerelease not in allowed_prerelease:
            console.print(
                f"[bold red]❌ Error: Invalid prerelease value '{prerelease}'. "
                f"Allowed values: alpha, beta, rc (or empty for a production release).[/bold red]"
            )
            sys.exit(1)

        # prerelease and increment are mutually exclusive
        if prerelease and increment:
            console.print(
                "[bold red]❌ Error: --prerelease and --increment "
                "are mutually exclusive.[/bold red]"
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
            run_streamed(["git", "pull"])
            console.print("[green]✓ Git pull successful.[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ Error pulling latest changes.[/bold red]")
            sys.exit(1)

        # Governance validation
        console.print("\n[bold cyan]Running governance validations...[/bold cyan]")

        # Validate merge commit format (blocking)
        if not validate_merge_commits(console):
            console.print("\n[bold red]❌ Merge commit validation failed![/bold red]")
            console.print("[yellow]Please ensure all merge commits follow the format:[/yellow]")
            console.print("[yellow]  <type>: <subject> (merges PR #XX, addresses #YY)[/yellow]")
            sys.exit(1)

        # Validate issue links (warning only)
        validate_issue_links(console)

        console.print("[bold green]✓ Governance validations complete.[/bold green]")

        # Run all checks
        console.print("\n[cyan]Running all pre-release checks...[/cyan]")
        try:
            run_streamed(["doit", "check"])
            console.print("[green]✓ All checks passed.[/green]")
        except subprocess.CalledProcessError:
            console.print(
                "[bold red]❌ Pre-release checks failed! "
                "Please fix issues before releasing.[/bold red]"
            )
            sys.exit(1)

        # Get next version using commitizen
        console.print("\n[cyan]Determining next version...[/cyan]")
        try:
            get_next_cmd = _build_cz_get_next_cmd(increment, prerelease)
            if increment:
                console.print(f"[dim]Forcing {increment.upper()} version bump[/dim]")
            if prerelease:
                console.print(f"[dim]Pre-release type: {prerelease}[/dim]")
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
            run_streamed(
                changelog_cmd,
                env={**os.environ, "UV_CACHE_DIR": UV_CACHE_DIR},
            )
            console.print("[green]✓ CHANGELOG.md updated.[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ Failed to update changelog.[/bold red]")
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
            run_streamed(
                ["git", "commit", "-m", f"chore: update changelog for v{next_version}"],
            )
            console.print("[green]✓ Changelog committed.[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ Failed to commit changelog.[/bold red]")
            # Cleanup
            subprocess.run(["git", "checkout", "main"], capture_output=True)
            subprocess.run(["git", "branch", "-D", branch_name], capture_output=True)
            sys.exit(1)

        # Push branch
        console.print(f"\n[cyan]Pushing branch {branch_name}...[/cyan]")
        try:
            run_streamed(["git", "push", "-u", "origin", branch_name])
            console.print("[green]✓ Branch pushed.[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ Failed to push branch.[/bold red]")
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
            run_streamed(
                [
                    "gh",
                    "pr",
                    "create",
                    "--title",
                    pr_title,
                    "--body",
                    pr_body,
                ],
            )
            console.print("[green]✓ Pull request created.[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ Failed to create PR.[/bold red]")
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
            },
            {
                "name": "prerelease",
                "short": "p",
                "long": "prerelease",
                "default": "",
                "help": "Pre-release type (alpha, beta, rc). Empty for a production release.",
            },
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
            run_streamed(["git", "pull"])
            console.print("[green]✓ Git pull successful.[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ Error pulling latest changes.[/bold red]")
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

            # Extract version from PR title (format: "release: vX.Y.Z[suffix]"),
            # falling back to the branch name (format: "release/vX.Y.Z[suffix]").
            version = _extract_version_from_release_pr(pr_title, branch_name)
            if version is None:
                console.print("[bold red]❌ Could not extract version from PR.[/bold red]")
                console.print(f"[yellow]PR title: {pr_title}[/yellow]")
                console.print(f"[yellow]Branch: {branch_name}[/yellow]")
                sys.exit(1)

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
            run_streamed(["git", "push", "origin", tag_name])
            console.print(f"[green]✓ Tag {tag_name} pushed.[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ Failed to push tag.[/bold red]")
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

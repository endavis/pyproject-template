"""Git-related doit tasks."""

import os
import subprocess  # nosec B404 - subprocess is required for doit tasks
import sys
from pathlib import Path
from typing import Any

from doit.tools import title_with_actions
from rich.console import Console

from .base import install_check_or_skip, run_streamed

# Where `doit worktree` creates worktrees, relative to the main checkout. It is
# gitignored and skipped by the repo-wide test walkers. Not under tmp/, which
# `doit cleanup` empties (#854).
WORKTREES_DIR = "worktrees"


def task_commit() -> dict[str, Any]:
    """Interactive commit with commitizen (ensures conventional commit format)."""
    return {
        "actions": [
            install_check_or_skip(
                "commitizen",
                "commitizen not installed. Run: uv sync",
            )
            + "uv run cz commit"
        ],
        "title": title_with_actions,
    }


def task_bump() -> dict[str, Any]:
    """Bump version automatically based on conventional commits."""
    return {
        "actions": [
            install_check_or_skip(
                "commitizen",
                "commitizen not installed. Run: uv sync",
            )
            + "uv run cz bump"
        ],
        "title": title_with_actions,
    }


def task_changelog() -> dict[str, Any]:
    """Generate CHANGELOG from conventional commits."""
    return {
        "actions": [
            install_check_or_skip(
                "commitizen",
                "commitizen not installed. Run: uv sync",
            )
            + "uv run cz changelog"
        ],
        "title": title_with_actions,
    }


def task_pre_commit_install() -> dict[str, Any]:
    """Install pre-commit hooks.

    One action, deliberately. `.pre-commit-config.yaml` declares
    `default_install_hook_types`, so a bare `pre-commit install` installs every
    declared type — including `commit-msg`, which carries conventional-commit
    validation and the branch/issue check (#741).

    This used to enumerate `post-merge` and `post-checkout` explicitly. Those
    lines were redundant once the config declared the set, and worse than
    redundant: `commit-msg` was never added to them, so the enumeration
    described a hook set that was no longer the hook set, and the next person to
    add a type would have followed the pattern and silently changed nothing.
    The config is the single source; `tests/template/test_doit_git.py` holds the
    two to each other.
    """
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


def _main_checkout() -> Path:
    """Return the main checkout's root, also when run from a linked worktree.

    ``git worktree list`` always lists the main worktree first.
    """
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.splitlines()[0].removeprefix("worktree "))


def task_worktree() -> dict[str, Any]:
    """Create a git worktree in ``worktrees/<branch>`` with its own environment.

    The branch starts from a freshly fetched ``origin/main`` with no upstream,
    so ``doit pr`` pushes it. ``uv sync --all-extras --dev`` then builds the
    worktree's own ``.venv`` with ``VIRTUAL_ENV`` unset: an inherited
    ``VIRTUAL_ENV`` names the main checkout's environment, which a worktree
    must neither use nor change (#854).

    Examples:
        doit worktree --branch=feat/42-add-export
    """

    def create_worktree(branch: str | None = None) -> None:
        # soft_wrap leaves wrapping to the terminal. Otherwise Rich breaks lines at
        # 80 columns when output is not a tty, splitting a path in a command to
        # paste, or git's own error message.
        console = Console(soft_wrap=True)
        if not branch:
            console.print("[red]--branch is required, e.g. --branch=feat/42-add-export[/red]")
            sys.exit(1)

        # A valid branch name cannot start with "/" or contain "..", so the
        # worktree path below stays inside worktrees/.
        valid = subprocess.run(
            ["git", "check-ref-format", "--branch", branch],
            capture_output=True,
            text=True,
            check=False,
        )
        if valid.returncode != 0:
            console.print(f"[red]Not a valid branch name: {branch}[/red]")
            sys.exit(1)

        root = _main_checkout()
        path = root / WORKTREES_DIR / branch

        try:
            subprocess.run(
                ["git", "fetch", "origin", "main"],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or "").strip()
            console.print(f"[yellow]Warning: `git fetch origin main` failed: {stderr}[/yellow]")
            console.print("[yellow]Branching from the last fetched origin/main.[/yellow]")

        try:
            subprocess.run(
                ["git", "worktree", "add", "--no-track", "-b", branch, str(path), "origin/main"],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            console.print(f"[red]git worktree add failed: {(e.stderr or '').strip()}[/red]")
            sys.exit(1)
        console.print(f"[green]Created {path} on {branch}, from origin/main.[/green]")

        env = {key: value for key, value in os.environ.items() if key != "VIRTUAL_ENV"}
        # base.py defaults UV_CACHE_DIR to a relative path. Resolved here, before
        # uv runs in the worktree, it keeps pointing at this checkout's cache
        # instead of a new, empty one inside the worktree.
        if "UV_CACHE_DIR" in env:
            env["UV_CACHE_DIR"] = str(Path(env["UV_CACHE_DIR"]).resolve())
        try:
            run_streamed(["uv", "sync", "--all-extras", "--dev"], env=env, cwd=path)
        except subprocess.CalledProcessError:
            console.print("[red]uv sync failed. The worktree exists; to retry, run in it:[/red]")
            console.print("  uv sync --all-extras --dev")
            sys.exit(1)

        console.print()
        console.print("[bold]Work there through uv run, which uses the worktree's .venv:[/bold]")
        console.print(f"  cd {path}")
        console.print("  uv run doit check")
        console.print(
            "[dim]Never pass --active: it installs the worktree into the main .venv.[/dim]"
        )
        console.print("[bold]Once its PR has merged, from the main checkout:[/bold]")
        console.print(f"  git worktree remove {path}")
        console.print(f"  git branch -D {branch}  # if it still exists")

    return {
        "actions": [create_worktree],
        "params": [
            {
                "name": "branch",
                "long": "branch",
                "default": None,
                "help": "Branch to create, e.g. feat/42-add-export",
            },
        ],
        "title": title_with_actions,
    }

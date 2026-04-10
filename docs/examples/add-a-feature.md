---
title: "Add a Feature: End-to-End Walkthrough"
description: Step-by-step example of adding a module, CLI subcommand, tests, and docs to the project
audience:
  - contributors
tags:
  - examples
  - walkthrough
  - feature
  - cli
---

# Add a Feature: End-to-End Walkthrough

This guide walks through adding a hypothetical **farewell** feature from
start to finish. The feature is intentionally small -- a `farewell()` function
and a `farewell` CLI subcommand -- so the focus stays on the *workflow and
conventions* rather than the code itself.

By the end you will have touched every layer of the project: issue tracking,
branching, runtime code, tests, documentation, and the PR process.

!!! note "This is an illustrative example"
    The code snippets below are **not** committed to the repository. They show
    what you *would* write if you were adding this feature for real.

## Prerequisites

- The project is cloned and dependencies are installed (`uv sync`).
- You have read the [CLI Guide](../usage/cli.md) and understand the existing
  `greet` subcommand.
- You are familiar with [Tooling Roles and Architectural Boundaries](../development/tooling-roles.md),
  particularly the separation between runtime code and dev tooling.

---

## Step 1: Create an Issue

Every change starts with a GitHub issue. Use the `doit issue` task to create
one with the correct labels and template sections:

```bash
doit issue --type=feature --title="feat: add farewell command" \
  --body="## Problem
Users can greet but cannot say goodbye.

## Proposed Solution
Add a \`farewell(name)\` function in a new \`farewell.py\` module and expose
it as a \`farewell\` CLI subcommand."
```

Note the issue number in the output -- we will call it **#NNN** for the rest of
this guide.

## Step 2: Create a Branch

Pull the latest `main` and create a feature branch linked to the issue:

```bash
git checkout main && git pull
git checkout -b feat/NNN-add-farewell
```

Branch naming follows the convention `<type>/<issue>-<description>`.

## Step 3: Add the Core Module

Create `src/package_name/farewell.py`. The function mirrors the existing
`greet()` pattern in `core.py`:

```python
"""Farewell functionality for package_name."""


def farewell(name: str = "World") -> str:
    """Return a farewell message.

    Args:
        name: The name to bid farewell. Defaults to "World".

    Returns:
        A farewell message string.

    Examples:
        >>> farewell()
        'Goodbye, World!'
        >>> farewell("Python")
        'Goodbye, Python!'
    """
    return f"Goodbye, {name}!"
```

Key points:

- **Type hints** on the signature and return type.
- **Google-style docstring** with `Args`, `Returns`, and `Examples`.
- Pure function with no side effects -- easy to test.

## Step 4: Export from `__init__.py`

Add the new function to the package's public API in
`src/package_name/__init__.py`:

```python
"""Package Name - A short description of your package."""

from ._version import __version__
from .core import greet
from .farewell import farewell
from .logging import get_logger, setup_logging

__all__ = ["__version__", "farewell", "get_logger", "greet", "setup_logging"]
```

Keep `__all__` sorted alphabetically.

## Step 5: Add a CLI Subcommand

Extend `src/package_name/cli.py` with a `farewell` command. The CLI is a
**thin adapter** -- it delegates to the core function and handles only I/O
(printing, exit codes):

```python
from package_name.farewell import farewell as _farewell

# ... existing code ...

@main.command()
@click.option(
    "--name",
    "-n",
    default="World",
    show_default=True,
    help="Name to bid farewell.",
)
def farewell(name: str) -> None:
    """Print a farewell for NAME."""
    click.echo(_farewell(name))
```

!!! tip "Thin-adapter pattern"
    The CLI layer imports and calls `farewell()` from the core module rather
    than containing business logic itself. This keeps the logic testable
    without invoking the CLI runner. See
    [Tooling Roles](../development/tooling-roles.md) for more on this
    boundary.

## Step 6: Write Tests

Tests are created *with* the implementation, never after. You need two files:
a unit test for the core function and a CLI integration test.

### Unit tests -- `tests/test_farewell.py`

Follow the patterns in `tests/test_example.py`:

```python
"""Tests for the farewell module."""

import pytest

from package_name.farewell import farewell


def test_farewell_default() -> None:
    """farewell() with no arguments returns the default message."""
    assert farewell() == "Goodbye, World!"


def test_farewell_custom_name() -> None:
    """farewell(name) substitutes the provided name."""
    assert farewell("Python") == "Goodbye, Python!"


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Alice", "Goodbye, Alice!"),
        ("Bob", "Goodbye, Bob!"),
        ("World", "Goodbye, World!"),
    ],
)
def test_farewell_parametrized(name: str, expected: str) -> None:
    """Parametrized test covering multiple inputs."""
    assert farewell(name) == expected
```

### CLI tests -- `tests/test_cli_farewell.py`

Follow the patterns in `tests/test_cli.py`:

```python
"""Tests for the farewell CLI subcommand."""

from click.testing import CliRunner

from package_name.cli import main


def test_farewell_default_name() -> None:
    """farewell with no arguments prints the default message."""
    runner = CliRunner()
    result = runner.invoke(main, ["farewell"])
    assert result.exit_code == 0
    assert result.output == "Goodbye, World!\n"


def test_farewell_custom_name_long_option() -> None:
    """farewell --name substitutes the provided name."""
    runner = CliRunner()
    result = runner.invoke(main, ["farewell", "--name", "Python"])
    assert result.exit_code == 0
    assert result.output == "Goodbye, Python!\n"


def test_farewell_custom_name_short_option() -> None:
    """farewell -n is the short alias for --name."""
    runner = CliRunner()
    result = runner.invoke(main, ["farewell", "-n", "Python"])
    assert result.exit_code == 0
    assert result.output == "Goodbye, Python!\n"


def test_farewell_help() -> None:
    """farewell --help documents the --name option."""
    runner = CliRunner()
    result = runner.invoke(main, ["farewell", "--help"])
    assert result.exit_code == 0
    assert "--name" in result.output
```

## Step 7: Run Checks

Run the full check suite before committing:

```bash
doit check
```

This runs linting (ruff), type checking (mypy), tests (pytest), and security
scanning (bandit) in one command. Fix any failures before proceeding.

## Step 8: Update Documentation

Add the new function to the API reference page so that `mkdocstrings` picks it
up. In `docs/reference/api.md`, add a section for the farewell module:

```markdown
## Farewell

::: package_name.farewell
```

Then build the docs to make sure everything renders:

```bash
doit docs_build
```

## Step 9: Commit and Create a PR

Stage, commit (with a conventional commit message), and push:

```bash
git add .
doit commit   # interactive prompt enforces conventional format
git push -u origin feat/NNN-add-farewell
```

Then create the PR:

```bash
doit pr --title="feat: add farewell command" \
  --body="## Summary
- Add \`farewell()\` function in \`farewell.py\`
- Add \`farewell\` CLI subcommand
- Add unit and CLI tests

Addresses #NNN"
```

After CI passes and the PR is reviewed, merge with:

```bash
doit pr_merge
```

---

## Key Takeaways

1. **Issue first.** Every change, no matter how small, starts with a tracked
   issue.

2. **Branch per feature.** Never commit directly to `main`.

3. **Runtime code is separate from dev tooling.** `doit` tasks are for
   *contributors*; the user-facing CLI is built with `click` and lives in
   `src/`. See [Tooling Roles](../development/tooling-roles.md).

4. **Thin CLI adapters.** The CLI layer delegates to pure-function core
   modules. This keeps logic testable without the CLI runner.

5. **Tests ship with code.** Creating code means creating tests -- no
   exceptions. Follow existing patterns in `tests/`.

6. **`doit check` before committing.** Catches lint, type, test, and security
   issues locally before CI does.

7. **Conventional commits.** `feat:`, `fix:`, `refactor:`, `docs:`, etc.
   Messages describe *why*, not *what*.

## See Also

- [CLI Guide](../usage/cli.md) -- reference for the `click`-based CLI
- [Tooling Roles and Architectural Boundaries](../development/tooling-roles.md) --
  runtime vs dev tooling
- [API Reference](../reference/api.md) -- generated API docs
- [Contributing Guide](https://github.com/endavis/pyproject-template/blob/main/.github/CONTRIBUTING.md) --
  full development workflow
- [ADR-9014: Use click for application CLI](../template/decisions/9014-use-click-for-application-cli.md)

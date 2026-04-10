---
title: CLI Guide
description: The application's user-facing command-line interface and how to extend it
audience:
  - users
  - contributors
tags:
  - cli
  - usage
---

# CLI Guide

## Purpose

This page documents the **application's user-facing command-line
interface** — the `package-name` console script shipped by the published
package. It covers the entry point, the module layout, how to add new
subcommands, and how to test them.

This page does **not** cover `doit`, which is a contributor-only
development task runner. For `doit` tasks, see the
[Doit Tasks Reference](../development/doit-tasks-reference.md). For the
architectural rationale behind the runtime/dev split, see
[Tooling Roles and Architectural Boundaries](../development/tooling-roles.md).

## Quick reference

After installing the package, the `package-name` command is available on
your `PATH`:

```bash
$ package-name greet
Hello, World!

$ package-name greet --name Python
Hello, Python!

$ package-name greet -n Python
Hello, Python!

$ package-name --version
package_name, version 0.0.0
```

During development, prefix invocations with `uv run` to use the project
virtual environment:

```bash
uv run package-name greet --name Python
```

## Entry point and module layout

The CLI is registered in `pyproject.toml` as a console script:

```toml
[project.scripts]
package-name = "package_name.cli:main"
```

The script name on the left (`package-name`) is the hyphen-cased
distribution name. The value on the right points at the `main` function
in `src/package_name/cli.py`. When the package is installed (via `uv
sync`, `pip install`, etc.), the build backend generates an executable
shim that calls `package_name.cli.main()`.

The CLI module lives at `src/package_name/cli.py` and is a single file
for the baseline template. Larger projects may split it into a
`cli/` package with one file per subcommand group.

## How the CLI is structured

The CLI uses [click](https://click.palletsprojects.com/) as its
framework. The top-level entry point is a `click.Group` named `main`, and
subcommands attach to it via the `@main.command()` decorator:

```python
import click

from package_name.core import greet as _greet


@click.group()
@click.version_option(package_name="package_name")
def main() -> None:
    """package_name command-line interface."""


@main.command()
@click.option("--name", "-n", default="World", show_default=True, help="Name to greet.")
def greet(name: str) -> None:
    """Print a greeting for NAME."""
    click.echo(_greet(name))
```

Key properties:

- **`main` is a `click.Group`.** This is what `[project.scripts]` points
  at. It has no behavior of its own — it dispatches to subcommands.
- **`@click.version_option(package_name="package_name")`** wires up
  `--version` using the installed package metadata, so the version never
  drifts out of sync with the git tag.
- **Subcommands call into the runtime package.** The `greet` command
  delegates to `package_name.core.greet`. The CLI layer handles parsing
  and output; the core module owns the logic. This keeps the core
  testable without invoking click and makes the CLI a thin presentation
  layer.

For the rationale behind choosing click (versus `argparse` or `typer`),
see [ADR-9014: Use click for application CLI](../template/decisions/9014-use-click-for-application-cli.md).

## How to add a new subcommand

1. **Open `src/package_name/cli.py`.**
2. **Write a function decorated with `@main.command()`.** Add options
   and arguments with `@click.option` / `@click.argument`.
3. **Delegate to a function in the runtime package.** Do not put business
   logic in `cli.py` — call into `package_name.core` (or a new module)
   and use the CLI function as a thin adapter.
4. **Add tests in `tests/test_cli.py`** (see [Testing CLI commands](#testing-cli-commands)
   below).

Example: adding a `shout` subcommand that uppercases a name and greets
it loudly.

```python
# src/package_name/cli.py

@main.command()
@click.argument("name")
@click.option("--exclaim", "-e", default=1, show_default=True, help="Number of !s.")
def shout(name: str, exclaim: int) -> None:
    """Print an uppercase greeting for NAME."""
    message = _greet(name.upper())
    click.echo(message + "!" * (exclaim - 1))
```

Usage:

```bash
$ package-name shout python --exclaim 3
Hello, PYTHON!!!
```

## Testing CLI commands

Use click's in-process `CliRunner` to invoke the CLI without spawning a
subprocess. This is faster than `subprocess.run`, has no shell-quoting
pitfalls, and gives you direct access to exit codes and captured output.

```python
# tests/test_cli.py
from click.testing import CliRunner

from package_name.cli import main


def test_greet_default_name() -> None:
    """greet with no arguments prints the default greeting."""
    runner = CliRunner()
    result = runner.invoke(main, ["greet"])
    assert result.exit_code == 0
    assert result.output == "Hello, World!\n"


def test_greet_custom_name_long_option() -> None:
    """greet --name substitutes the provided name."""
    runner = CliRunner()
    result = runner.invoke(main, ["greet", "--name", "Python"])
    assert result.exit_code == 0
    assert result.output == "Hello, Python!\n"
```

What to cover for every new subcommand:

- **Happy path** with default arguments (exit code 0, expected output).
- **Each option**, long form and short form.
- **`--help`** — exit code 0 and the option text appears.
- **Error paths** — missing required arguments, invalid values. Click
  returns a non-zero exit code and writes a usage message to
  `result.output`.

## See also

- [Usage Guide](basics.md) — importing the package as a library.
- [API Reference](../reference/api.md) — full API documentation.
- [Doit Tasks Reference](../development/doit-tasks-reference.md) — the
  contributor-only task runner. Not the same thing as this page.
- [Tooling Roles and Architectural Boundaries](../development/tooling-roles.md) —
  why runtime CLI and dev tooling are kept separate.
- [ADR-9014: Use click for application CLI](../template/decisions/9014-use-click-for-application-cli.md)

- [Add a Feature End-to-End](../examples/add-a-feature.md) —
  narrative walkthrough of adding a module, CLI subcommand, tests, and docs.

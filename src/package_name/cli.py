"""Command-line interface for package_name.

This module defines the user-facing CLI for the package. It is registered
as a console script via ``[project.scripts]`` in ``pyproject.toml``:

.. code-block:: toml

    [project.scripts]
    package-name = "package_name.cli:main"

The CLI is built with `click`_ and uses a :class:`click.Group` as the top
level entry point so new subcommands can be added by decorating functions
with ``@main.command()``.

.. _click: https://click.palletsprojects.com/
"""

from __future__ import annotations

import click

from package_name.core import greet as _greet


@click.group()
@click.version_option(package_name="package_name")
def main() -> None:
    """package_name command-line interface."""


@main.command()
@click.option(
    "--name",
    "-n",
    default="World",
    show_default=True,
    help="Name to greet.",
)
def greet(name: str) -> None:
    """Print a greeting for NAME."""
    click.echo(_greet(name))

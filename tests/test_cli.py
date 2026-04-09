"""Tests for the package_name command-line interface."""

from click.testing import CliRunner

from package_name import __version__
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


def test_greet_custom_name_short_option() -> None:
    """greet -n is the short alias for --name."""
    runner = CliRunner()
    result = runner.invoke(main, ["greet", "-n", "Python"])
    assert result.exit_code == 0
    assert result.output == "Hello, Python!\n"


def test_top_level_help() -> None:
    """--help on the top-level group lists the greet subcommand."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "greet" in result.output


def test_greet_help() -> None:
    """greet --help documents the --name option without executing the command."""
    runner = CliRunner()
    result = runner.invoke(main, ["greet", "--help"])
    assert result.exit_code == 0
    assert "--name" in result.output
    assert "Hello, Python!" not in result.output


def test_version_option() -> None:
    """--version prints the installed package version."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_main_is_importable() -> None:
    """The entry-point target is importable and callable."""
    from package_name.cli import main as imported_main

    assert callable(imported_main)

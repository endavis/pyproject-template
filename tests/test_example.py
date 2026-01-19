"""Example tests for package_name."""

from pathlib import Path

import pytest

from package_name import __version__, greet


def test_version() -> None:
    """Test that version is accessible."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_greet_usage() -> None:
    """Example of testing the greet function."""
    assert greet("Test User") == "Hello, Test User!"


def test_greet_with_fixture(tmp_path: Path) -> None:
    """Example test using pytest fixture and package functionality."""
    # tmp_path is a pytest fixture that provides a temporary directory
    output_file = tmp_path / "greeting.txt"
    message = greet("File System")
    output_file.write_text(message)

    assert output_file.read_text() == "Hello, File System!"


class TestExampleClass:
    """Example test class organization."""

    def test_default_greeting(self) -> None:
        """Test method for default behavior."""
        assert greet() == "Hello, World!"

    def test_uppercase_transformation(self) -> None:
        """Test method demonstrating transformation logic."""
        message = greet("python")
        assert "Python" not in message  # simple check that logic doesn't auto-capitalize input
        assert message == "Hello, python!"


@pytest.mark.parametrize(
    "name,expected",
    [
        ("Alice", "Hello, Alice!"),
        ("Bob", "Hello, Bob!"),
        ("World", "Hello, World!"),
    ],
)
def test_greet_parametrized(name: str, expected: str) -> None:
    """Example parametrized test using package function."""
    assert greet(name) == expected

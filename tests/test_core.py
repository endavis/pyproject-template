"""Tests for core module."""

from package_name import greet


def test_greet_default() -> None:
    """Test greet with default argument."""
    assert greet() == "Hello, World!"


def test_greet_with_name() -> None:
    """Test greet with custom name."""
    assert greet("Python") == "Hello, Python!"


def test_greet_empty_string() -> None:
    """Test greet with empty string."""
    assert greet("") == "Hello, !"

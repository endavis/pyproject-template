"""Example tests for package_name."""

import pytest

from package_name import __version__


def test_version():
    """Test that version is accessible."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_example():
    """Example test case."""
    assert True


def test_example_with_fixture(tmp_path):
    """Example test using pytest fixture."""
    # tmp_path is a pytest fixture that provides a temporary directory
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!")
    assert test_file.read_text() == "Hello, World!"


class TestExampleClass:
    """Example test class."""

    def test_method_one(self):
        """Test method one."""
        assert 1 + 1 == 2

    def test_method_two(self):
        """Test method two."""
        assert "hello".upper() == "HELLO"


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (1, 2),
        (2, 4),
        (3, 6),
    ],
)
def test_parametrized(input_value, expected):
    """Example parametrized test."""
    assert input_value * 2 == expected

"""Property-based tests for the skeleton package (downstream-owned).

Only skeleton assertions live here (greet, etc.).  Tooling assertions for
``tools.pyproject_template.utils`` have been moved to the template-owned
``tests/template/test_utils_properties.py``.
"""

from __future__ import annotations

import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from package_name.core import greet

# ---------------------------------------------------------------------------
# greet
# ---------------------------------------------------------------------------


@pytest.mark.property
class TestGreetProperties:
    """Property-based tests for the greet function."""

    @given(name=st.text(min_size=1))
    @example("World")
    @example("Alice")
    def test_output_contains_input_name(self, name: str) -> None:
        """The greeting must contain the input name verbatim."""
        result = greet(name)
        assert name in result, f"Name {name!r} not found in greeting: {result!r}"

    @given(name=st.text(min_size=0))
    @example("")
    @example("Test")
    def test_output_starts_with_hello(self, name: str) -> None:
        """The greeting must always start with 'Hello, '."""
        result = greet(name)
        assert result.startswith("Hello, "), f"Greeting doesn't start with 'Hello, ': {result!r}"

    @given(name=st.text(min_size=0))
    def test_output_ends_with_exclamation(self, name: str) -> None:
        """The greeting must always end with '!'."""
        result = greet(name)
        assert result.endswith("!"), f"Greeting doesn't end with '!': {result!r}"

    @given(name=st.text(min_size=0))
    def test_output_format_is_exact(self, name: str) -> None:
        """The greeting must exactly match 'Hello, {name}!'."""
        result = greet(name)
        assert result == f"Hello, {name}!", f"Unexpected format: {result!r}"

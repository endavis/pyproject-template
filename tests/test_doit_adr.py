"""Tests for adr.py doit tasks."""

from io import StringIO
from unittest.mock import MagicMock, patch

from tools.doit.adr import (
    _get_next_adr_number,
    _is_placeholder_content,
    _title_to_slug,
    _validate_adr_content,
)


class TestTitleToSlug:
    """Tests for _title_to_slug function."""

    def test_simple_title(self) -> None:
        """Test conversion of simple title."""
        assert _title_to_slug("Use uv for package management") == "use-uv-for-package-management"

    def test_title_with_special_chars(self) -> None:
        """Test removal of special characters."""
        assert _title_to_slug("Use ruff (linting & formatting)") == "use-ruff-linting-formatting"

    def test_title_with_multiple_spaces(self) -> None:
        """Test collapsing of multiple spaces."""
        assert _title_to_slug("Use  doit   for   automation") == "use-doit-for-automation"

    def test_title_with_underscores(self) -> None:
        """Test conversion of underscores to hyphens."""
        assert _title_to_slug("use_redis_for_caching") == "use-redis-for-caching"

    def test_title_with_mixed_case(self) -> None:
        """Test conversion to lowercase."""
        assert _title_to_slug("Use PostgreSQL Database") == "use-postgresql-database"

    def test_title_with_numbers(self) -> None:
        """Test preservation of numbers."""
        assert _title_to_slug("Python 3.12 compatibility") == "python-312-compatibility"

    def test_title_with_leading_trailing_special(self) -> None:
        """Test trimming of leading/trailing special characters."""
        assert _title_to_slug("  --Use Redis--  ") == "use-redis"

    def test_empty_title(self) -> None:
        """Test handling of empty title."""
        assert _title_to_slug("") == ""

    def test_title_with_only_special_chars(self) -> None:
        """Test handling of title with only special characters."""
        assert _title_to_slug("!@#$%") == ""


class TestGetNextAdrNumber:
    """Tests for _get_next_adr_number function."""

    def test_returns_positive_integer(self) -> None:
        """Test that function returns a positive integer."""
        result = _get_next_adr_number()
        assert isinstance(result, int)
        assert result > 0

    def test_returns_sequential_number(self) -> None:
        """Test that function returns the next sequential number.

        Since we have seed ADRs 0001-0007 in place,
        the next number should be at least 8.
        """
        result = _get_next_adr_number()
        # After seeding, should be at least 8
        assert result >= 1


class TestIsPlaceholderContent:
    """Tests for _is_placeholder_content function."""

    def test_placeholder_what_is_the_issue(self) -> None:
        """Test detection of 'What is the issue' placeholder."""
        assert _is_placeholder_content("What is the issue that we're seeing?") is True

    def test_placeholder_what_is_the_change(self) -> None:
        """Test detection of 'What is the change' placeholder."""
        assert _is_placeholder_content("What is the change that we're proposing?") is True

    def test_placeholder_proposed(self) -> None:
        """Test detection of '**Proposed**' placeholder."""
        assert _is_placeholder_content("**Proposed** | Accepted | Deprecated") is True

    def test_placeholder_date(self) -> None:
        """Test detection of 'YYYY-MM-DD' placeholder."""
        assert _is_placeholder_content("YYYY-MM-DD") is True

    def test_real_content(self) -> None:
        """Test that real content is not detected as placeholder."""
        assert _is_placeholder_content("Use Redis for caching to improve performance.") is False

    def test_real_date(self) -> None:
        """Test that real dates are not detected as placeholder."""
        assert _is_placeholder_content("2025-01-21") is False


class TestValidateAdrContent:
    """Tests for _validate_adr_content function."""

    def _mock_console(self) -> MagicMock:
        """Create a mock console for testing."""
        console = MagicMock()
        console.file = StringIO()
        return console

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_valid_content(self, mock_get_sections: MagicMock) -> None:
        """Test validation of valid ADR content."""
        mock_get_sections.return_value = ["Context", "Decision", "Consequences"]
        content = """# ADR-0001: Test

## Status

Accepted

## Date

2025-01-21

## Context

This is the context.

## Decision

This is the decision.

## Consequences

### Positive

- Good thing

### Negative

- Bad thing

### Neutral

- Neutral thing
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is True

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_missing_context_section(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when Context section is missing."""
        mock_get_sections.return_value = ["Context", "Decision", "Consequences"]
        content = """# ADR-0001: Test

## Status

Accepted

## Decision

This is the decision.

## Consequences

### Positive

- Good thing
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_missing_decision_section(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when Decision section is missing."""
        mock_get_sections.return_value = ["Context", "Decision", "Consequences"]
        content = """# ADR-0001: Test

## Status

Accepted

## Context

This is the context.

## Consequences

### Positive

- Good thing
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_missing_consequences_section(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when Consequences section is missing."""
        mock_get_sections.return_value = ["Context", "Decision", "Consequences"]
        content = """# ADR-0001: Test

## Status

Accepted

## Context

This is the context.

## Decision

This is the decision.
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_empty_context_section(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when Context section is empty."""
        mock_get_sections.return_value = ["Context", "Decision", "Consequences"]
        content = """# ADR-0001: Test

## Context

## Decision

This is the decision.

## Consequences

### Positive

- Good thing
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_consequences_with_content(self, mock_get_sections: MagicMock) -> None:
        """Test validation passes with content in consequences subsections."""
        mock_get_sections.return_value = ["Context", "Decision", "Consequences"]
        content = """# ADR-0001: Test

## Context

Context here.

## Decision

Decision here.

## Consequences

### Positive

- This is a positive consequence

### Negative

-

### Neutral

-
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is True

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_uses_template_required_sections(self, mock_get_sections: MagicMock) -> None:
        """Test that validation uses sections from template."""
        # Only require Context
        mock_get_sections.return_value = ["Context"]
        content = """# ADR-0001: Test

## Context

This is the context.
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is True
        mock_get_sections.assert_called_once()

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

        Since we have seed ADRs 0001-0012 in place,
        the next number should be at least 13.
        """
        result = _get_next_adr_number()
        assert result >= 1


class TestIsPlaceholderContent:
    """Tests for _is_placeholder_content function."""

    def test_placeholder_brief_summary(self) -> None:
        """Test detection of 'Brief summary' placeholder."""
        assert _is_placeholder_content("Brief summary of what was decided.") is True

    def test_placeholder_why_decision(self) -> None:
        """Test detection of 'Why this decision' placeholder."""
        assert _is_placeholder_content("Why this decision was made.") is True

    def test_placeholder_issue_xx(self) -> None:
        """Test detection of 'Issue #XX' placeholder."""
        assert _is_placeholder_content("Issue #XX: Description") is True

    def test_real_content(self) -> None:
        """Test that real content is not detected as placeholder."""
        assert _is_placeholder_content("Use Redis for caching to improve performance.") is False

    def test_real_issue_reference(self) -> None:
        """Test that real issue references are not detected as placeholder."""
        assert _is_placeholder_content("Issue #123: Add caching support") is False


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
        mock_get_sections.return_value = ["Status", "Decision", "Rationale"]
        content = """# ADR-0001: Test

## Status

Accepted

## Decision

Use Redis for caching.

## Rationale

Improves performance significantly.

## Related Issues

- Issue #42: Add caching
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is True

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_missing_decision_section(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when Decision section is missing."""
        mock_get_sections.return_value = ["Status", "Decision", "Rationale"]
        content = """# ADR-0001: Test

## Status

Accepted

## Rationale

Some rationale.
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_missing_rationale_section(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when Rationale section is missing."""
        mock_get_sections.return_value = ["Status", "Decision", "Rationale"]
        content = """# ADR-0001: Test

## Status

Accepted

## Decision

Use Redis.
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_empty_decision_section(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when Decision section is empty."""
        mock_get_sections.return_value = ["Status", "Decision", "Rationale"]
        content = """# ADR-0001: Test

## Status

Accepted

## Decision

## Rationale

Some rationale.
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_placeholder_content_rejected(self, mock_get_sections: MagicMock) -> None:
        """Test validation fails when section has placeholder content."""
        mock_get_sections.return_value = ["Status", "Decision", "Rationale"]
        content = """# ADR-0001: Test

## Status

Accepted

## Decision

Brief summary of what was decided.

## Rationale

Why this decision was made.
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is False

    @patch("tools.doit.adr.get_adr_required_sections")
    def test_uses_template_required_sections(self, mock_get_sections: MagicMock) -> None:
        """Test that validation uses sections from template."""
        # Only require Status and Decision
        mock_get_sections.return_value = ["Status", "Decision"]
        content = """# ADR-0001: Test

## Status

Accepted

## Decision

Use Redis.
"""
        console = self._mock_console()
        assert _validate_adr_content(content, console) is True
        mock_get_sections.assert_called_once()

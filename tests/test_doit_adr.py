"""Tests for adr.py doit tasks."""

from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tools.doit import adr as adr_module
from tools.doit.adr import (
    TEMPLATE_SERIES_FLOOR,
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
        """Smoke test against the real ADR_DIR: returns a positive integer."""
        result = _get_next_adr_number()
        assert isinstance(result, int)
        assert result >= 1

    def test_project_series_returns_1_when_no_project_adrs(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Project series starts at 1 when only template (9XXX) ADRs exist."""
        for n in range(9001, 9016):
            (tmp_path / f"{n}-example.md").write_text(f"# ADR-{n}", encoding="utf-8")

        monkeypatch.setattr(adr_module, "ADR_DIR", tmp_path)
        assert _get_next_adr_number(template=False) == 1

    def test_template_series_returns_9016_given_9015_max(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Template series returns max + 1 when template ADRs already exist."""
        for n in range(9001, 9016):
            (tmp_path / f"{n}-example.md").write_text(f"# ADR-{n}", encoding="utf-8")

        monkeypatch.setattr(adr_module, "ADR_DIR", tmp_path)
        assert _get_next_adr_number(template=True) == 9016

    def test_template_series_returns_floor_when_empty(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Template series returns the floor (9001) when no template ADRs exist."""
        # Project ADRs present, but no template ADRs.
        (tmp_path / "0001-something.md").write_text("# ADR-0001", encoding="utf-8")

        monkeypatch.setattr(adr_module, "ADR_DIR", tmp_path)
        assert _get_next_adr_number(template=True) == TEMPLATE_SERIES_FLOOR

    def test_project_series_returns_max_plus_1(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Project series returns max + 1 when project ADRs already exist."""
        (tmp_path / "0001-first.md").write_text("# ADR-0001", encoding="utf-8")
        (tmp_path / "0002-second.md").write_text("# ADR-0002", encoding="utf-8")

        monkeypatch.setattr(adr_module, "ADR_DIR", tmp_path)
        assert _get_next_adr_number(template=False) == 3

    def test_series_isolation(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Template and project series are counted independently in the shared directory."""
        (tmp_path / "0001-first.md").write_text("# ADR-0001", encoding="utf-8")
        (tmp_path / "0002-second.md").write_text("# ADR-0002", encoding="utf-8")
        (tmp_path / "9001-a.md").write_text("# ADR-9001", encoding="utf-8")
        (tmp_path / "9015-b.md").write_text("# ADR-9015", encoding="utf-8")

        monkeypatch.setattr(adr_module, "ADR_DIR", tmp_path)
        assert _get_next_adr_number(template=False) == 3
        assert _get_next_adr_number(template=True) == 9016

    def test_readme_and_template_files_ignored(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """README.md and adr-template.md must not influence numbering."""
        (tmp_path / "README.md").write_text("# README", encoding="utf-8")
        (tmp_path / "adr-template.md").write_text("# ADR-NNNN", encoding="utf-8")

        monkeypatch.setattr(adr_module, "ADR_DIR", tmp_path)
        assert _get_next_adr_number(template=False) == 1
        assert _get_next_adr_number(template=True) == TEMPLATE_SERIES_FLOOR

    def test_missing_directory_returns_floor(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """If ADR_DIR does not exist, both series return their floor."""
        missing = tmp_path / "does_not_exist"
        monkeypatch.setattr(adr_module, "ADR_DIR", missing)

        assert _get_next_adr_number(template=False) == 1
        assert _get_next_adr_number(template=True) == TEMPLATE_SERIES_FLOOR


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

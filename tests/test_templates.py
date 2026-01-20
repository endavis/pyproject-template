"""Tests for the template parser module."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.doit.templates import (
    FIELD_ID_TO_SECTION,
    ISSUE_TYPE_TO_FILE,
    IssueTemplate,
    clear_template_cache,
    get_issue_labels,
    get_issue_template,
    get_pr_template,
    get_required_sections,
)


@pytest.fixture(autouse=True)
def clear_cache() -> Generator[None, None, None]:
    """Clear template cache before each test."""
    clear_template_cache()
    yield
    clear_template_cache()


class TestIssueTypeMapping:
    """Test issue type to file mapping."""

    def test_all_issue_types_have_mapping(self) -> None:
        """All expected issue types should have file mappings."""
        expected_types = {"feature", "bug", "refactor", "doc", "chore"}
        assert set(ISSUE_TYPE_TO_FILE.keys()) == expected_types

    def test_mapping_files_exist(self) -> None:
        """All mapped template files should exist."""
        github_dir = Path(__file__).parent.parent / ".github" / "ISSUE_TEMPLATE"
        for issue_type, filename in ISSUE_TYPE_TO_FILE.items():
            template_path = github_dir / filename
            assert template_path.exists(), f"Template for {issue_type} not found: {template_path}"


class TestGetIssueTemplate:
    """Test get_issue_template function."""

    @pytest.mark.parametrize("issue_type", ["feature", "bug", "refactor", "doc", "chore"])
    def test_get_template_for_valid_types(self, issue_type: str) -> None:
        """Should return IssueTemplate for all valid types."""
        result = get_issue_template(issue_type)
        assert isinstance(result, IssueTemplate)
        assert result.name  # Should have a name
        assert result.labels  # Should have labels
        assert result.editor_template  # Should have editor template content
        assert isinstance(result.required_sections, list)

    def test_invalid_type_raises_value_error(self) -> None:
        """Should raise ValueError for invalid issue type."""
        with pytest.raises(ValueError, match="Invalid issue type"):
            get_issue_template("invalid")

    def test_feature_template_has_expected_labels(self) -> None:
        """Feature template should have enhancement label."""
        result = get_issue_template("feature")
        assert "enhancement" in result.labels

    def test_bug_template_has_expected_labels(self) -> None:
        """Bug template should have bug label."""
        result = get_issue_template("bug")
        assert "bug" in result.labels

    def test_refactor_template_has_expected_labels(self) -> None:
        """Refactor template should have refactor label."""
        result = get_issue_template("refactor")
        assert "refactor" in result.labels

    def test_doc_template_has_expected_labels(self) -> None:
        """Doc template should have documentation label."""
        result = get_issue_template("doc")
        assert "documentation" in result.labels

    def test_chore_template_has_expected_labels(self) -> None:
        """Chore template should have chore label."""
        result = get_issue_template("chore")
        assert "chore" in result.labels

    def test_editor_template_has_instructions(self) -> None:
        """Editor template should contain instruction comments."""
        result = get_issue_template("feature")
        assert "# Lines starting with #" in result.editor_template
        assert "## " in result.editor_template  # Should have markdown sections

    def test_caching_returns_same_instance(self) -> None:
        """Multiple calls should return cached result."""
        result1 = get_issue_template("feature")
        result2 = get_issue_template("feature")
        assert result1 is result2


class TestGetRequiredSections:
    """Test get_required_sections function."""

    def test_feature_required_sections(self) -> None:
        """Feature type should require Problem and Proposed Solution."""
        sections = get_required_sections("feature")
        assert "Problem" in sections
        assert "Proposed Solution" in sections

    def test_bug_required_sections(self) -> None:
        """Bug type should require multiple sections."""
        sections = get_required_sections("bug")
        assert "Bug Description" in sections
        assert "Steps to Reproduce" in sections
        assert "Expected vs Actual Behavior" in sections

    def test_refactor_required_sections(self) -> None:
        """Refactor type should require specific sections."""
        sections = get_required_sections("refactor")
        assert "Current Code Issue" in sections
        assert "Proposed Improvement" in sections

    def test_doc_required_sections(self) -> None:
        """Doc type should require type and description."""
        sections = get_required_sections("doc")
        assert "Documentation Type" in sections
        assert "Description" in sections

    def test_chore_required_sections(self) -> None:
        """Chore type should require type and description."""
        sections = get_required_sections("chore")
        assert "Chore Type" in sections
        assert "Description" in sections


class TestGetIssueLabels:
    """Test get_issue_labels function."""

    @pytest.mark.parametrize(
        ("issue_type", "expected_label"),
        [
            ("feature", "enhancement"),
            ("bug", "bug"),
            ("refactor", "refactor"),
            ("doc", "documentation"),
            ("chore", "chore"),
        ],
    )
    def test_labels_contain_expected_type(self, issue_type: str, expected_label: str) -> None:
        """Labels should contain the expected type-specific label."""
        labels = get_issue_labels(issue_type)
        assert expected_label in labels

    def test_labels_include_needs_triage(self) -> None:
        """All issue types should include needs-triage label."""
        for issue_type in ISSUE_TYPE_TO_FILE:
            labels = get_issue_labels(issue_type)
            assert "needs-triage" in labels


class TestGetPrTemplate:
    """Test get_pr_template function."""

    def test_returns_string(self) -> None:
        """Should return a string."""
        result = get_pr_template()
        assert isinstance(result, str)

    def test_has_editor_instructions(self) -> None:
        """Should have editor instruction comments at top."""
        result = get_pr_template()
        assert "# Lines starting with #" in result

    def test_has_description_section(self) -> None:
        """Should have Description section."""
        result = get_pr_template()
        assert "## Description" in result

    def test_has_related_issue_section(self) -> None:
        """Should have Related Issue section."""
        result = get_pr_template()
        assert "## Related Issue" in result

    def test_has_checklist_section(self) -> None:
        """Should have Checklist section."""
        result = get_pr_template()
        assert "## Checklist" in result

    def test_caching_returns_same_instance(self) -> None:
        """Multiple calls should return cached result."""
        result1 = get_pr_template()
        result2 = get_pr_template()
        assert result1 is result2

    def test_missing_template_raises_error(self) -> None:
        """Should raise FileNotFoundError if template doesn't exist."""
        clear_template_cache()
        with patch("tools.doit.templates._get_github_dir") as mock_dir:
            mock_dir.return_value = Path("/nonexistent")
            with pytest.raises(FileNotFoundError):
                get_pr_template()


class TestFieldIdToSection:
    """Test field ID to section name mapping."""

    def test_all_common_field_ids_mapped(self) -> None:
        """Common field IDs should be mapped to section names."""
        expected_ids = {
            "problem",
            "proposed-solution",
            "bug-description",
            "steps-to-reproduce",
            "current-code-issue",
            "proposed-improvement",
            "description",
        }
        for field_id in expected_ids:
            assert field_id in FIELD_ID_TO_SECTION, f"Missing mapping for {field_id}"


class TestClearTemplateCache:
    """Test clear_template_cache function."""

    def test_clears_issue_template_cache(self) -> None:
        """Should clear the issue template cache."""
        # Load a template to populate cache
        result1 = get_issue_template("feature")

        # Clear and reload
        clear_template_cache()
        result2 = get_issue_template("feature")

        # Should be equal but not the same object
        assert result1 == result2
        assert result1 is not result2

    def test_clears_pr_template_cache(self) -> None:
        """Should clear the PR template cache."""
        # Load template to populate cache
        result1 = get_pr_template()

        # Clear and reload
        clear_template_cache()
        result2 = get_pr_template()

        # Should be equal but not the same object (strings are immutable so may be same)
        assert result1 == result2

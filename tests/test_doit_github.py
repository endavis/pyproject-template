"""Tests for github.py doit tasks."""

from tools.doit.github import _extract_linked_issues, _format_merge_subject


class TestExtractLinkedIssues:
    """Tests for _extract_linked_issues function."""

    def test_addresses_issue(self) -> None:
        """Test extraction of 'Addresses #XX' pattern."""
        body = "Addresses #123"
        result = _extract_linked_issues(body)
        assert result == ["123"]

    def test_addresses_lowercase(self) -> None:
        """Test extraction of lowercase 'addresses #XX' pattern."""
        body = "addresses #456"
        result = _extract_linked_issues(body)
        assert result == ["456"]

    def test_addresses_uppercase(self) -> None:
        """Test extraction of uppercase 'ADDRESSES #XX' pattern."""
        body = "ADDRESSES #789"
        result = _extract_linked_issues(body)
        assert result == ["789"]

    def test_multiple_addresses(self) -> None:
        """Test extraction of multiple addresses patterns."""
        body = "Addresses #123\nAddresses #456"
        result = _extract_linked_issues(body)
        assert result == ["123", "456"]

    def test_duplicate_issues(self) -> None:
        """Test that duplicate issues are removed."""
        body = "Addresses #123\nAlso addresses #123"
        result = _extract_linked_issues(body)
        assert result == ["123"]

    def test_no_issues(self) -> None:
        """Test handling of body with no issues."""
        body = "This PR adds a new feature"
        result = _extract_linked_issues(body)
        assert result == []

    def test_issue_in_code_block_still_matched(self) -> None:
        """Test that issues in code blocks are still matched (by design)."""
        body = "```\nAddresses #123\n```"
        result = _extract_linked_issues(body)
        assert result == ["123"]

    def test_old_closes_keyword_not_matched(self) -> None:
        """Test that old 'Closes' keyword is not matched."""
        body = "Closes #123"
        result = _extract_linked_issues(body)
        assert result == []

    def test_old_fixes_keyword_not_matched(self) -> None:
        """Test that old 'Fixes' keyword is not matched."""
        body = "Fixes #456"
        result = _extract_linked_issues(body)
        assert result == []

    def test_old_part_of_keyword_not_matched(self) -> None:
        """Test that old 'Part of' keyword is not matched."""
        body = "Part of #101"
        result = _extract_linked_issues(body)
        assert result == []


class TestFormatMergeSubject:
    """Tests for _format_merge_subject function."""

    def test_with_single_issue(self) -> None:
        """Test formatting with a single addressed issue."""
        result = _format_merge_subject("feat: add feature", 18, ["42"])
        assert result == "feat: add feature (merges PR #18, addresses #42)"

    def test_with_multiple_issues(self) -> None:
        """Test formatting with multiple addressed issues."""
        result = _format_merge_subject("fix: bug fix", 23, ["19", "20"])
        assert result == "fix: bug fix (merges PR #23, addresses #19, #20)"

    def test_without_issues(self) -> None:
        """Test formatting without linked issues."""
        result = _format_merge_subject("docs: update readme", 29, [])
        assert result == "docs: update readme (merges PR #29)"

    def test_with_scope(self) -> None:
        """Test formatting with scoped title."""
        result = _format_merge_subject("feat(api): add endpoint", 50, ["100"])
        assert result == "feat(api): add endpoint (merges PR #50, addresses #100)"

    def test_preserves_title_exactly(self) -> None:
        """Test that PR title is preserved exactly."""
        title = "refactor: simplify complex logic"
        result = _format_merge_subject(title, 99, ["55"])
        assert result.startswith(title)

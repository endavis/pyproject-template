"""Tests for github.py doit tasks."""

from tools.doit.github import _extract_linked_issues, _format_merge_subject


class TestExtractLinkedIssues:
    """Tests for _extract_linked_issues function."""

    def test_closes_issue(self) -> None:
        """Test extraction of 'Closes #XX' pattern."""
        body = "This PR closes #123"
        assert _extract_linked_issues(body) == ["123"]

    def test_fixes_issue(self) -> None:
        """Test extraction of 'Fixes #XX' pattern."""
        body = "This PR fixes #456"
        assert _extract_linked_issues(body) == ["456"]

    def test_resolves_issue(self) -> None:
        """Test extraction of 'Resolves #XX' pattern."""
        body = "This PR resolves #789"
        assert _extract_linked_issues(body) == ["789"]

    def test_part_of_issue(self) -> None:
        """Test extraction of 'Part of #XX' pattern."""
        body = "Part of #101"
        assert _extract_linked_issues(body) == ["101"]

    def test_multiple_issues(self) -> None:
        """Test extraction of multiple issues."""
        body = "Closes #123\nFixes #456\nPart of #789"
        assert _extract_linked_issues(body) == ["123", "456", "789"]

    def test_duplicate_issues(self) -> None:
        """Test that duplicate issues are removed."""
        body = "Closes #123\nAlso closes #123"
        assert _extract_linked_issues(body) == ["123"]

    def test_case_insensitive(self) -> None:
        """Test that matching is case insensitive."""
        body = "CLOSES #123\nfixes #456\nResolves #789"
        assert _extract_linked_issues(body) == ["123", "456", "789"]

    def test_no_issues(self) -> None:
        """Test handling of body with no issues."""
        body = "This PR adds a new feature"
        assert _extract_linked_issues(body) == []

    def test_issue_in_code_block_still_matched(self) -> None:
        """Test that issues in code blocks are still matched (by design)."""
        body = "```\nCloses #123\n```"
        # Note: This is a design decision - we match anywhere in body
        assert _extract_linked_issues(body) == ["123"]

    def test_closed_variant(self) -> None:
        """Test 'Closed' variant."""
        body = "Closed #123"
        assert _extract_linked_issues(body) == ["123"]

    def test_fixed_variant(self) -> None:
        """Test 'Fixed' variant."""
        body = "Fixed #123"
        assert _extract_linked_issues(body) == ["123"]


class TestFormatMergeSubject:
    """Tests for _format_merge_subject function."""

    def test_with_single_issue(self) -> None:
        """Test formatting with a single linked issue."""
        result = _format_merge_subject("feat: add feature", 18, ["42"])
        assert result == "feat: add feature (merges PR #18, closes #42)"

    def test_with_multiple_issues(self) -> None:
        """Test formatting with multiple linked issues."""
        result = _format_merge_subject("fix: bug fix", 23, ["19", "20"])
        assert result == "fix: bug fix (merges PR #23, closes #19, #20)"

    def test_without_issues(self) -> None:
        """Test formatting without linked issues."""
        result = _format_merge_subject("docs: update readme", 29, [])
        assert result == "docs: update readme (merges PR #29)"

    def test_with_scope(self) -> None:
        """Test formatting with scoped title."""
        result = _format_merge_subject("feat(api): add endpoint", 50, ["100"])
        assert result == "feat(api): add endpoint (merges PR #50, closes #100)"

    def test_preserves_title_exactly(self) -> None:
        """Test that PR title is preserved exactly."""
        title = "refactor: simplify complex logic"
        result = _format_merge_subject(title, 99, ["55"])
        assert result.startswith(title)

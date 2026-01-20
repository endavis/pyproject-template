"""Tests for github.py doit tasks."""

from tools.doit.github import _extract_linked_issues, _format_merge_subject


class TestExtractLinkedIssues:
    """Tests for _extract_linked_issues function."""

    def test_closes_issue(self) -> None:
        """Test extraction of 'Closes #XX' pattern."""
        body = "This PR closes #123"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123"], "part_of": []}

    def test_fixes_issue(self) -> None:
        """Test extraction of 'Fixes #XX' pattern."""
        body = "This PR fixes #456"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["456"], "part_of": []}

    def test_resolves_issue(self) -> None:
        """Test extraction of 'Resolves #XX' pattern."""
        body = "This PR resolves #789"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["789"], "part_of": []}

    def test_part_of_issue(self) -> None:
        """Test extraction of 'Part of #XX' pattern."""
        body = "Part of #101"
        result = _extract_linked_issues(body)
        assert result == {"closes": [], "part_of": ["101"]}

    def test_multiple_closes_issues(self) -> None:
        """Test extraction of multiple closes issues."""
        body = "Closes #123\nFixes #456"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123", "456"], "part_of": []}

    def test_mixed_closes_and_part_of(self) -> None:
        """Test extraction of mixed closes and part of issues."""
        body = "Closes #123\nPart of #789"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123"], "part_of": ["789"]}

    def test_duplicate_issues(self) -> None:
        """Test that duplicate issues are removed."""
        body = "Closes #123\nAlso closes #123"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123"], "part_of": []}

    def test_case_insensitive(self) -> None:
        """Test that matching is case insensitive."""
        body = "CLOSES #123\nfixes #456\nPART OF #789"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123", "456"], "part_of": ["789"]}

    def test_no_issues(self) -> None:
        """Test handling of body with no issues."""
        body = "This PR adds a new feature"
        result = _extract_linked_issues(body)
        assert result == {"closes": [], "part_of": []}

    def test_issue_in_code_block_still_matched(self) -> None:
        """Test that issues in code blocks are still matched (by design)."""
        body = "```\nCloses #123\n```"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123"], "part_of": []}

    def test_closed_variant(self) -> None:
        """Test 'Closed' variant."""
        body = "Closed #123"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123"], "part_of": []}

    def test_fixed_variant(self) -> None:
        """Test 'Fixed' variant."""
        body = "Fixed #123"
        result = _extract_linked_issues(body)
        assert result == {"closes": ["123"], "part_of": []}


class TestFormatMergeSubject:
    """Tests for _format_merge_subject function."""

    def test_with_single_closes_issue(self) -> None:
        """Test formatting with a single closes issue."""
        issues = {"closes": ["42"], "part_of": []}
        result = _format_merge_subject("feat: add feature", 18, issues)
        assert result == "feat: add feature (merges PR #18, closes #42)"

    def test_with_multiple_closes_issues(self) -> None:
        """Test formatting with multiple closes issues."""
        issues = {"closes": ["19", "20"], "part_of": []}
        result = _format_merge_subject("fix: bug fix", 23, issues)
        assert result == "fix: bug fix (merges PR #23, closes #19, #20)"

    def test_without_issues(self) -> None:
        """Test formatting without linked issues."""
        issues: dict[str, list[str]] = {"closes": [], "part_of": []}
        result = _format_merge_subject("docs: update readme", 29, issues)
        assert result == "docs: update readme (merges PR #29)"

    def test_with_part_of_issue(self) -> None:
        """Test formatting with part of issue."""
        issues = {"closes": [], "part_of": ["100"]}
        result = _format_merge_subject("feat: add step 1", 50, issues)
        assert result == "feat: add step 1 (merges PR #50, part of #100)"

    def test_with_multiple_part_of_issues(self) -> None:
        """Test formatting with multiple part of issues."""
        issues = {"closes": [], "part_of": ["100", "101"]}
        result = _format_merge_subject("feat: add step 1", 50, issues)
        assert result == "feat: add step 1 (merges PR #50, part of #100, #101)"

    def test_with_closes_and_part_of(self) -> None:
        """Test formatting with both closes and part of issues."""
        issues = {"closes": ["42"], "part_of": ["100"]}
        result = _format_merge_subject("feat: complete feature", 60, issues)
        assert result == "feat: complete feature (merges PR #60, closes #42, part of #100)"

    def test_with_scope(self) -> None:
        """Test formatting with scoped title."""
        issues = {"closes": ["100"], "part_of": []}
        result = _format_merge_subject("feat(api): add endpoint", 50, issues)
        assert result == "feat(api): add endpoint (merges PR #50, closes #100)"

    def test_preserves_title_exactly(self) -> None:
        """Test that PR title is preserved exactly."""
        title = "refactor: simplify complex logic"
        issues = {"closes": ["55"], "part_of": []}
        result = _format_merge_subject(title, 99, issues)
        assert result.startswith(title)

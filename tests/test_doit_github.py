"""Tests for github.py doit tasks."""

import io
import subprocess
from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console

from tools.doit.github import (
    _check_branch_up_to_date,
    _close_linked_issues,
    _ensure_branch_pushed,
    _extract_linked_issues,
    _format_merge_subject,
)


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


class TestCloseLinkedIssues:
    """Tests for _close_linked_issues helper."""

    def test_closes_single_linked_issue(self) -> None:
        """Single issue results in one gh issue close invocation."""
        console = Console()
        with patch("tools.doit.github.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            _close_linked_issues(["123"], 45, console)

        assert mock_run.call_count == 1
        args, kwargs = mock_run.call_args
        assert args[0] == [
            "gh",
            "issue",
            "close",
            "123",
            "--comment",
            "Addressed in PR #45",
        ]
        assert kwargs["check"] is True
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True

    def test_closes_multiple_linked_issues(self) -> None:
        """Multiple issues result in multiple calls in order."""
        console = Console()
        with patch("tools.doit.github.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            _close_linked_issues(["10", "20", "30"], 7, console)

        assert mock_run.call_count == 3
        called_issues = [call.args[0][3] for call in mock_run.call_args_list]
        assert called_issues == ["10", "20", "30"]

    def test_no_issues_is_noop(self) -> None:
        """Empty issue list results in no subprocess calls."""
        console = Console()
        with patch("tools.doit.github.subprocess.run") as mock_run:
            _close_linked_issues([], 99, console)

        mock_run.assert_not_called()

    def test_partial_failure_continues(self) -> None:
        """A failure on one issue does not stop subsequent closes."""
        console = Console()

        def side_effect(cmd: list[str], *_args: object, **_kwargs: object) -> MagicMock:
            issue = cmd[3]
            if issue == "20":
                raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="boom")
            return MagicMock(returncode=0, stdout="", stderr="")

        with patch("tools.doit.github.subprocess.run", side_effect=side_effect) as mock_run:
            # Should not raise.
            _close_linked_issues(["10", "20", "30"], 7, console)

        assert mock_run.call_count == 3
        called_issues = [call.args[0][3] for call in mock_run.call_args_list]
        assert called_issues == ["10", "20", "30"]

    def test_close_comment_format(self) -> None:
        """The close comment must be exactly 'Addressed in PR #<n>'."""
        console = Console()
        with patch("tools.doit.github.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            _close_linked_issues(["5"], 123, console)

        cmd = mock_run.call_args.args[0]
        assert cmd[4] == "--comment"
        assert cmd[5] == "Addressed in PR #123"


class TestCheckBranchUpToDate:
    """Tests for _check_branch_up_to_date helper."""

    @staticmethod
    def _make_console() -> Console:
        return Console(file=io.StringIO(), width=200)

    def test_up_to_date_branch_passes(self) -> None:
        """rev-list --count == 0 → helper returns cleanly."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "fetch"]:
                return MagicMock(returncode=0, stdout="", stderr="")
            if cmd[:3] == ["git", "rev-list", "--count"]:
                return MagicMock(returncode=0, stdout="0\n", stderr="")
            raise AssertionError(f"unexpected cmd: {cmd}")

        with patch("tools.doit.github.subprocess.run", side_effect=side_effect):
            _check_branch_up_to_date("feat/x", console)

        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "up to date" in output.lower()

    def test_behind_branch_aborts(self) -> None:
        """rev-list --count > 0 → SystemExit(1) with remediation message."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "fetch"]:
                return MagicMock(returncode=0, stdout="", stderr="")
            if cmd[:3] == ["git", "rev-list", "--count"]:
                return MagicMock(returncode=0, stdout="3\n", stderr="")
            if cmd[:2] == ["git", "log"]:
                return MagicMock(returncode=0, stdout="abc1 one\n", stderr="")
            raise AssertionError(f"unexpected cmd: {cmd}")

        with (
            patch("tools.doit.github.subprocess.run", side_effect=side_effect),
            pytest.raises(SystemExit) as excinfo,
        ):
            _check_branch_up_to_date("feat/x", console)

        assert excinfo.value.code == 1
        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "3 commit" in output
        assert "git rebase origin/main" in output
        assert "feat/x" in output

    def test_fetch_failure_warns_and_proceeds(self) -> None:
        """git fetch failure → warning printed, helper returns."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "fetch"]:
                raise subprocess.CalledProcessError(
                    returncode=128, cmd=cmd, stderr="could not resolve host"
                )
            raise AssertionError(f"unexpected cmd after fetch failed: {cmd}")

        with patch("tools.doit.github.subprocess.run", side_effect=side_effect):
            _check_branch_up_to_date("feat/x", console)

        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "warning" in output.lower()
        assert "could not resolve host" in output

    def test_behind_branch_lists_missing_commits(self) -> None:
        """Missing commit SHAs from `git log` appear in the output."""
        console = self._make_console()

        log_out = "abc1234 feat: one\ndef5678 fix: two\n"

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "fetch"]:
                return MagicMock(returncode=0, stdout="", stderr="")
            if cmd[:3] == ["git", "rev-list", "--count"]:
                return MagicMock(returncode=0, stdout="2\n", stderr="")
            if cmd[:2] == ["git", "log"]:
                return MagicMock(returncode=0, stdout=log_out, stderr="")
            raise AssertionError(f"unexpected cmd: {cmd}")

        with (
            patch("tools.doit.github.subprocess.run", side_effect=side_effect),
            pytest.raises(SystemExit),
        ):
            _check_branch_up_to_date("feat/x", console)

        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "abc1234" in output
        assert "def5678" in output


class TestEnsureBranchPushed:
    """Tests for _ensure_branch_pushed helper."""

    @staticmethod
    def _make_console() -> Console:
        return Console(file=io.StringIO(), width=200)

    def test_existing_upstream_is_noop(self) -> None:
        """rev-parse @{u} succeeds → no push, helper returns."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "rev-parse"]:
                return MagicMock(returncode=0, stdout="origin/feat/x\n", stderr="")
            raise AssertionError(f"unexpected cmd: {cmd}")

        with patch("tools.doit.github.subprocess.run", side_effect=side_effect) as run:
            _ensure_branch_pushed("feat/x", console, no_push=False)

        assert run.call_count == 1

    def test_no_upstream_pushes(self) -> None:
        """rev-parse @{u} fails → git push -u origin is called."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "rev-parse"]:
                raise subprocess.CalledProcessError(
                    returncode=128, cmd=cmd, stderr="no upstream configured"
                )
            if cmd[:3] == ["git", "push", "-u"]:
                return MagicMock(returncode=0, stdout="", stderr="")
            raise AssertionError(f"unexpected cmd: {cmd}")

        with patch("tools.doit.github.subprocess.run", side_effect=side_effect) as run:
            _ensure_branch_pushed("feat/x", console, no_push=False)

        assert run.call_count == 2
        push_cmd = run.call_args_list[1].args[0]
        assert push_cmd == ["git", "push", "-u", "origin", "feat/x"]

    def test_push_failure_aborts(self) -> None:
        """rev-parse @{u} fails and git push fails → SystemExit(1)."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "rev-parse"]:
                raise subprocess.CalledProcessError(returncode=128, cmd=cmd, stderr="no upstream")
            if cmd[:3] == ["git", "push", "-u"]:
                raise subprocess.CalledProcessError(
                    returncode=1, cmd=cmd, stderr="remote rejected: protected branch"
                )
            raise AssertionError(f"unexpected cmd: {cmd}")

        with (
            patch("tools.doit.github.subprocess.run", side_effect=side_effect),
            pytest.raises(SystemExit) as excinfo,
        ):
            _ensure_branch_pushed("feat/x", console, no_push=False)

        assert excinfo.value.code == 1
        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "Failed to push" in output
        assert "remote rejected" in output

    def test_no_push_flag_and_no_upstream_aborts(self) -> None:
        """no_push=True with missing upstream → SystemExit(1), no push."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "rev-parse"]:
                raise subprocess.CalledProcessError(returncode=128, cmd=cmd, stderr="no upstream")
            raise AssertionError(f"unexpected cmd: {cmd} (push should not run)")

        with (
            patch("tools.doit.github.subprocess.run", side_effect=side_effect) as run,
            pytest.raises(SystemExit) as excinfo,
        ):
            _ensure_branch_pushed("feat/x", console, no_push=True)

        assert excinfo.value.code == 1
        assert run.call_count == 1
        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "no upstream" in output.lower()
        assert "--no-push" in output

    def test_no_push_flag_with_upstream_passes(self) -> None:
        """no_push=True with an upstream → returns, no push."""
        console = self._make_console()

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            if cmd[:2] == ["git", "rev-parse"]:
                return MagicMock(returncode=0, stdout="origin/feat/x\n", stderr="")
            raise AssertionError(f"unexpected cmd: {cmd}")

        with patch("tools.doit.github.subprocess.run", side_effect=side_effect) as run:
            _ensure_branch_pushed("feat/x", console, no_push=True)

        assert run.call_count == 1

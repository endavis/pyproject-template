"""Tests for github.py doit tasks."""

import io
import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from rich.console import Console

from tools.doit.github import (
    _PR_TITLE_PATTERN,
    _check_branch_up_to_date,
    _close_linked_issues,
    _ensure_branch_pushed,
    _extract_linked_issues,
    _fetch_github_labels,
    _format_merge_subject,
    _load_labels_file,
    _reconcile_labels,
    task_labels_sync,
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

    def test_closes_single_linked_issue(self, mock_subprocess: MagicMock) -> None:
        """Single issue results in one gh issue close invocation."""
        console = Console()
        mock_subprocess.register({("gh", "issue", "close"): {}})
        _close_linked_issues(["123"], 45, console)

        assert mock_subprocess.call_count == 1
        args, kwargs = mock_subprocess.call_args
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

    def test_closes_multiple_linked_issues(self, mock_subprocess: MagicMock) -> None:
        """Multiple issues result in multiple calls in order."""
        console = Console()
        mock_subprocess.register({("gh", "issue", "close"): {}})
        _close_linked_issues(["10", "20", "30"], 7, console)

        assert mock_subprocess.call_count == 3
        called_issues = [call.args[0][3] for call in mock_subprocess.call_args_list]
        assert called_issues == ["10", "20", "30"]

    def test_no_issues_is_noop(self, mock_subprocess: MagicMock) -> None:
        """Empty issue list results in no subprocess calls."""
        console = Console()
        _close_linked_issues([], 99, console)

        mock_subprocess.assert_not_called()

    def test_partial_failure_continues(self, mock_subprocess: MagicMock) -> None:
        """A failure on one issue does not stop subsequent closes."""
        console = Console()

        def spec(cmd: list[str]) -> MagicMock | BaseException:
            if cmd[3] == "20":
                return subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="boom")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_subprocess.register({("gh", "issue", "close"): spec})
        # Should not raise.
        _close_linked_issues(["10", "20", "30"], 7, console)

        assert mock_subprocess.call_count == 3
        called_issues = [call.args[0][3] for call in mock_subprocess.call_args_list]
        assert called_issues == ["10", "20", "30"]

    def test_close_comment_format(self, mock_subprocess: MagicMock) -> None:
        """The close comment must be exactly 'Addressed in PR #<n>'."""
        console = Console()
        mock_subprocess.register({("gh", "issue", "close"): {}})
        _close_linked_issues(["5"], 123, console)

        cmd = mock_subprocess.call_args.args[0]
        assert cmd[4] == "--comment"
        assert cmd[5] == "Addressed in PR #123"


class TestCheckBranchUpToDate:
    """Tests for _check_branch_up_to_date helper."""

    @staticmethod
    def _make_console() -> Console:
        return Console(file=io.StringIO(), width=200)

    def test_up_to_date_branch_passes(self, mock_subprocess: MagicMock) -> None:
        """rev-list --count == 0 → helper returns cleanly."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "rev-list", "--count"): {"stdout": "0\n"},
                ("git", "fetch"): {},
            }
        )
        _check_branch_up_to_date("feat/x", console)

        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "up to date" in output.lower()

    def test_behind_branch_aborts(self, mock_subprocess: MagicMock) -> None:
        """rev-list --count > 0 → SystemExit(1) with remediation message."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "rev-list", "--count"): {"stdout": "3\n"},
                ("git", "fetch"): {},
                ("git", "log"): {"stdout": "abc1 one\n"},
            }
        )

        with pytest.raises(SystemExit) as excinfo:
            _check_branch_up_to_date("feat/x", console)

        assert excinfo.value.code == 1
        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "3 commit" in output
        assert "git rebase origin/main" in output
        assert "feat/x" in output

    def test_fetch_failure_warns_and_proceeds(self, mock_subprocess: MagicMock) -> None:
        """git fetch failure → warning printed, helper returns."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "fetch"): subprocess.CalledProcessError(
                    returncode=128, cmd=["git", "fetch"], stderr="could not resolve host"
                ),
            }
        )
        _check_branch_up_to_date("feat/x", console)

        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "warning" in output.lower()
        assert "could not resolve host" in output

    def test_behind_branch_lists_missing_commits(self, mock_subprocess: MagicMock) -> None:
        """Missing commit SHAs from `git log` appear in the output."""
        console = self._make_console()
        log_out = "abc1234 feat: one\ndef5678 fix: two\n"
        mock_subprocess.register(
            {
                ("git", "rev-list", "--count"): {"stdout": "2\n"},
                ("git", "fetch"): {},
                ("git", "log"): {"stdout": log_out},
            }
        )

        with pytest.raises(SystemExit):
            _check_branch_up_to_date("feat/x", console)

        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "abc1234" in output
        assert "def5678" in output


class TestEnsureBranchPushed:
    """Tests for _ensure_branch_pushed helper."""

    @staticmethod
    def _make_console() -> Console:
        return Console(file=io.StringIO(), width=200)

    def test_existing_upstream_is_noop(self, mock_subprocess: MagicMock) -> None:
        """rev-parse @{u} succeeds → no push, helper returns."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "rev-parse"): {"stdout": "origin/feat/x\n"},
            }
        )
        _ensure_branch_pushed("feat/x", console, no_push=False)

        assert mock_subprocess.call_count == 1

    def test_no_upstream_pushes(self, mock_subprocess: MagicMock) -> None:
        """rev-parse @{u} fails → git push -u origin is called."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "rev-parse"): subprocess.CalledProcessError(
                    returncode=128, cmd=["git", "rev-parse"], stderr="no upstream configured"
                ),
                ("git", "push", "-u"): {},
            }
        )
        _ensure_branch_pushed("feat/x", console, no_push=False)

        assert mock_subprocess.call_count == 2
        push_cmd = mock_subprocess.call_args_list[1].args[0]
        assert push_cmd == ["git", "push", "-u", "origin", "feat/x"]

    def test_push_failure_aborts(self, mock_subprocess: MagicMock) -> None:
        """rev-parse @{u} fails and git push fails → SystemExit(1)."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "rev-parse"): subprocess.CalledProcessError(
                    returncode=128, cmd=["git", "rev-parse"], stderr="no upstream"
                ),
                ("git", "push", "-u"): subprocess.CalledProcessError(
                    returncode=1,
                    cmd=["git", "push", "-u"],
                    stderr="remote rejected: protected branch",
                ),
            }
        )

        with pytest.raises(SystemExit) as excinfo:
            _ensure_branch_pushed("feat/x", console, no_push=False)

        assert excinfo.value.code == 1
        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "Failed to push" in output
        assert "remote rejected" in output

    def test_no_push_flag_and_no_upstream_aborts(self, mock_subprocess: MagicMock) -> None:
        """no_push=True with missing upstream → SystemExit(1), no push."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "rev-parse"): subprocess.CalledProcessError(
                    returncode=128, cmd=["git", "rev-parse"], stderr="no upstream"
                ),
            }
        )

        with pytest.raises(SystemExit) as excinfo:
            _ensure_branch_pushed("feat/x", console, no_push=True)

        assert excinfo.value.code == 1
        assert mock_subprocess.call_count == 1
        output = console.file.getvalue()  # type: ignore[attr-defined]
        assert "no upstream" in output.lower()
        assert "--no-push" in output

    def test_no_push_flag_with_upstream_passes(self, mock_subprocess: MagicMock) -> None:
        """no_push=True with an upstream → returns, no push."""
        console = self._make_console()
        mock_subprocess.register(
            {
                ("git", "rev-parse"): {"stdout": "origin/feat/x\n"},
            }
        )
        _ensure_branch_pushed("feat/x", console, no_push=True)

        assert mock_subprocess.call_count == 1


class TestLabelsSync:
    """Tests for the ``labels_sync`` doit task and its helpers."""

    @staticmethod
    def _make_console() -> Console:
        return Console(file=io.StringIO(), width=200)

    @staticmethod
    def _labels_file(tmp_path: Path, body: str) -> Path:
        path = tmp_path / "labels.yml"
        path.write_text(body)
        return path

    @staticmethod
    def _register_list(mock_subprocess: MagicMock, current: list[dict[str, str]]) -> None:
        """Wire `gh label list` to return ``current`` as JSON."""
        mock_subprocess.register({("gh", "label", "list"): {"stdout": json.dumps(current)}})

    def _run_task(
        self,
        dry_run: bool = False,
        prune: bool = False,
        file: str = "",
    ) -> None:
        action = task_labels_sync()["actions"][0]
        action(dry_run=dry_run, prune=prune, file=file)

    def test_creates_missing_labels(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """File has 'foo', GH has none → one gh label create call."""
        labels_file = self._labels_file(
            tmp_path,
            "- name: foo\n  color: aaa111\n  description: Foo label\n",
        )
        self._register_list(mock_subprocess, [])
        mock_subprocess.register({("gh", "label", "create"): {}})

        self._run_task(file=str(labels_file))

        create_calls = [
            c for c in mock_subprocess.call_args_list if c.args[0][:3] == ["gh", "label", "create"]
        ]
        assert len(create_calls) == 1
        assert create_calls[0].args[0] == [
            "gh",
            "label",
            "create",
            "foo",
            "--color",
            "aaa111",
            "--description",
            "Foo label",
        ]

    def test_updates_mismatched_labels(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """File has 'foo' color aaa111, GH has color bbb222 → one gh label edit call."""
        labels_file = self._labels_file(
            tmp_path,
            "- name: foo\n  color: aaa111\n  description: Foo label\n",
        )
        self._register_list(
            mock_subprocess,
            [{"name": "foo", "color": "bbb222", "description": "Foo label"}],
        )
        mock_subprocess.register({("gh", "label", "edit"): {}})

        self._run_task(file=str(labels_file))

        edit_calls = [
            c for c in mock_subprocess.call_args_list if c.args[0][:3] == ["gh", "label", "edit"]
        ]
        assert len(edit_calls) == 1
        assert edit_calls[0].args[0] == [
            "gh",
            "label",
            "edit",
            "foo",
            "--color",
            "aaa111",
            "--description",
            "Foo label",
        ]

    def test_no_change_when_match(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """File and GH identical → no mutating calls."""
        labels_file = self._labels_file(
            tmp_path,
            "- name: foo\n  color: aaa111\n  description: Foo label\n",
        )
        self._register_list(
            mock_subprocess,
            [{"name": "foo", "color": "aaa111", "description": "Foo label"}],
        )

        self._run_task(file=str(labels_file))

        mutating = [
            c
            for c in mock_subprocess.call_args_list
            if c.args[0][:3]
            in (["gh", "label", "create"], ["gh", "label", "edit"], ["gh", "label", "delete"])
        ]
        assert mutating == []

    def test_prune_deletes_extras(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """With --prune, GH has a label not in file → gh label delete is called."""
        labels_file = self._labels_file(
            tmp_path,
            "- name: foo\n  color: aaa111\n  description: Foo label\n",
        )
        self._register_list(
            mock_subprocess,
            [
                {"name": "foo", "color": "aaa111", "description": "Foo label"},
                {"name": "old-label", "color": "cccccc", "description": "legacy"},
            ],
        )
        mock_subprocess.register({("gh", "label", "delete"): {}})

        self._run_task(file=str(labels_file), prune=True)

        delete_calls = [
            c for c in mock_subprocess.call_args_list if c.args[0][:3] == ["gh", "label", "delete"]
        ]
        assert len(delete_calls) == 1
        assert delete_calls[0].args[0] == ["gh", "label", "delete", "old-label", "--yes"]

    def test_no_prune_by_default(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """GH has extra label, no --prune → no delete call; extra is reported as skipped."""
        labels_file = self._labels_file(
            tmp_path,
            "- name: foo\n  color: aaa111\n  description: Foo label\n",
        )
        self._register_list(
            mock_subprocess,
            [
                {"name": "foo", "color": "aaa111", "description": "Foo label"},
                {"name": "old-label", "color": "cccccc", "description": "legacy"},
            ],
        )

        self._run_task(file=str(labels_file))

        delete_calls = [
            c for c in mock_subprocess.call_args_list if c.args[0][:3] == ["gh", "label", "delete"]
        ]
        assert delete_calls == []

    def test_dry_run_makes_no_mutations(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """With --dry-run, only gh label list is called; no create/edit/delete."""
        labels_file = self._labels_file(
            tmp_path,
            "- name: foo\n  color: aaa111\n  description: Foo label\n"
            "- name: bar\n  color: bbb222\n  description: Bar label\n",
        )
        self._register_list(
            mock_subprocess,
            [
                {"name": "bar", "color": "999999", "description": "Bar label"},
                {"name": "legacy", "color": "cccccc", "description": "to prune"},
            ],
        )

        self._run_task(file=str(labels_file), prune=True, dry_run=True)

        mutating = [
            c
            for c in mock_subprocess.call_args_list
            if c.args[0][:3]
            in (["gh", "label", "create"], ["gh", "label", "edit"], ["gh", "label", "delete"])
        ]
        assert mutating == []

    def test_malformed_yaml_raises_clear_error(
        self, tmp_path: Path, mock_subprocess: MagicMock
    ) -> None:
        """Entry without a 'name' field → SystemExit(1) naming the offending entry."""
        labels_file = self._labels_file(tmp_path, "- color: red\n")

        with pytest.raises(SystemExit) as excinfo:
            self._run_task(file=str(labels_file))

        assert excinfo.value.code == 1
        mock_subprocess.assert_not_called()

    def test_missing_file_raises(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """--file pointing at a nonexistent path → SystemExit(1)."""
        missing = tmp_path / "does-not-exist.yml"

        with pytest.raises(SystemExit) as excinfo:
            self._run_task(file=str(missing))

        assert excinfo.value.code == 1
        mock_subprocess.assert_not_called()

    def test_color_comparison_case_insensitive(
        self, tmp_path: Path, mock_subprocess: MagicMock
    ) -> None:
        """File 'FBCA04', GH 'fbca04' → no update."""
        labels_file = self._labels_file(
            tmp_path,
            "- name: needs-triage\n  color: FBCA04\n  description: triage\n",
        )
        self._register_list(
            mock_subprocess,
            [{"name": "needs-triage", "color": "fbca04", "description": "triage"}],
        )

        self._run_task(file=str(labels_file))

        mutating = [
            c
            for c in mock_subprocess.call_args_list
            if c.args[0][:3]
            in (["gh", "label", "create"], ["gh", "label", "edit"], ["gh", "label", "delete"])
        ]
        assert mutating == []

    def test_empty_description_handled(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """File entry with empty description → create call uses --description ''."""
        labels_file = self._labels_file(
            tmp_path,
            '- name: foo\n  color: aaa111\n  description: ""\n',
        )
        self._register_list(mock_subprocess, [])
        mock_subprocess.register({("gh", "label", "create"): {}})

        self._run_task(file=str(labels_file))

        create_calls = [
            c for c in mock_subprocess.call_args_list if c.args[0][:3] == ["gh", "label", "create"]
        ]
        assert len(create_calls) == 1
        cmd = create_calls[0].args[0]
        assert cmd[-2:] == ["--description", ""]

    def test_summary_counts_correct(self, tmp_path: Path, mock_subprocess: MagicMock) -> None:
        """Mixed scenario (create + update + no-change + skipped) → counters correct."""
        labels_file = self._labels_file(
            tmp_path,
            "\n".join(
                [
                    "- name: new-one",
                    "  color: aaa111",
                    "  description: new",
                    "- name: updated",
                    "  color: bbb222",
                    "  description: updated desc",
                    "- name: same",
                    "  color: cccccc",
                    "  description: same",
                    "",
                ]
            ),
        )
        self._register_list(
            mock_subprocess,
            [
                {"name": "updated", "color": "999999", "description": "old"},
                {"name": "same", "color": "cccccc", "description": "same"},
                {"name": "extra", "color": "111111", "description": "extra"},
            ],
        )
        mock_subprocess.register(
            {
                ("gh", "label", "create"): {},
                ("gh", "label", "edit"): {},
            }
        )

        counters = _reconcile_labels(
            _load_labels_file(labels_file, self._make_console()),
            _fetch_github_labels(self._make_console()),
            prune=False,
            dry_run=False,
            console=self._make_console(),
        )

        assert counters["created"] == 1
        assert counters["updated"] == 1
        assert counters["unchanged"] == 1
        assert counters["deleted"] == 0
        assert counters["skipped"] == 1

    def test_labels_file_parses(self) -> None:
        """The actual .github/labels.yml parses and has non-empty entries."""
        repo_labels = Path(__file__).resolve().parent.parent / ".github" / "labels.yml"
        assert repo_labels.exists(), f"{repo_labels} is missing"

        entries = _load_labels_file(repo_labels, self._make_console())
        assert entries, "labels.yml should not be empty"

        names = {entry["name"] for entry in entries}
        # Two labels the issue highlighted as missing on the repo must be present.
        assert "automerge-blocked" in names
        assert "do-not-merge" in names
        # Every entry must have a 6-char hex color.
        for entry in entries:
            assert len(entry["color"]) == 6, f"bad color for {entry['name']}: {entry['color']!r}"


class TestPrTitlePattern:
    """Tests for ``_PR_TITLE_PATTERN`` (issue #655).

    The pattern gates whether ``doit pr_merge`` accepts a PR title. All eight
    standard conventional-commit types must pass; ``release`` must pass too
    (machine-generated by ``doit release``) so the release PR can be merged
    via the standard flow. Arbitrary titles must be rejected.
    """

    @pytest.mark.parametrize(
        "title",
        [
            "feat: add thing",
            "fix: bug fix",
            "refactor: restructure",
            "docs: update",
            "test: add case",
            "chore: bump dep",
            "ci: add workflow",
            "perf: speed it up",
            "release: v0.1.0a0",
            "release: v1.2.3",
            "release: v0.1.0-alpha.0",
            "fix(api): scope ok",
            "release(hotfix): v1.2.3",
        ],
    )
    def test_valid_titles_match(self, title: str) -> None:
        assert _PR_TITLE_PATTERN.match(title), f"should match: {title!r}"

    @pytest.mark.parametrize(
        "title",
        [
            "no type prefix",
            "Release: wrong case",
            "feat add colon",
            "bump: wrong type",
            "release v0.1.0a0",  # missing colon
            "",
        ],
    )
    def test_invalid_titles_reject(self, title: str) -> None:
        assert not _PR_TITLE_PATTERN.match(title), f"should not match: {title!r}"

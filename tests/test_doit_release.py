"""Tests for helpers in tools.doit.base and tools.doit.release.

``run_streamed`` / ``run_teed`` back the live-streaming output changes for
the release tasks (issue #631). ``_extract_version_from_release_pr`` is the
version-parsing helper factored out of ``task_release_tag`` to support
PEP440 and semver-style pre-release suffixes (issue #632 Phase A).
``_build_cz_get_next_cmd`` is the command-list builder factored out of
``task_release`` so ``--prerelease`` can be threaded through to
``cz bump --get-next`` (issue #632 Phase B). The task functions themselves
(``task_release``, etc.) have no existing test coverage and are out of scope
per the plan.
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest
from rich.console import Console

from tools.doit.base import run_streamed, run_teed
from tools.doit.release import (
    _build_cz_get_next_cmd,
    _extract_next_version_from_cz_output,
    _extract_version_from_release_pr,
    _repo_has_version_tags,
    validate_merge_commits,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from _pytest.monkeypatch import MonkeyPatch


class TestRunStreamed:
    """Tests for ``run_streamed``."""

    def test_success_returns_none(self) -> None:
        """A zero-exit command returns ``None`` and does not raise."""
        result = run_streamed([sys.executable, "-c", "print('hi')"])
        assert result is None

    def test_failure_with_check_true_raises(self) -> None:
        """Non-zero exit with ``check=True`` raises ``CalledProcessError``."""
        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            run_streamed([sys.executable, "-c", "import sys; sys.exit(2)"])
        assert excinfo.value.returncode == 2

    def test_failure_with_check_false_does_not_raise(self) -> None:
        """Non-zero exit with ``check=False`` returns without raising."""
        # Must not raise.
        result = run_streamed(
            [sys.executable, "-c", "import sys; sys.exit(3)"],
            check=False,
        )
        assert result is None

    def test_env_is_threaded_through(self, capfd: pytest.CaptureFixture[str]) -> None:
        """The ``env`` mapping is forwarded to the child process."""
        # Use a sentinel env var the child will echo to stdout.
        run_streamed(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('RUN_STREAMED_TEST', ''))",
            ],
            env={"RUN_STREAMED_TEST": "threaded-value"},
        )
        out = capfd.readouterr().out
        assert "threaded-value" in out

    def test_empty_env_isolates_child(self, capfd: pytest.CaptureFixture[str]) -> None:
        """Passing a tightly-scoped env actually replaces (not extends) the parent env."""
        # A var the parent likely has — confirm the child doesn't see it when
        # we pass a minimal env. We still need PATH for the interpreter lookup
        # on some platforms; use the interpreter's absolute path to avoid that.
        run_streamed(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('PATH', 'NO_PATH'))",
            ],
            env={"OTHER": "x"},
        )
        out = capfd.readouterr().out
        assert "NO_PATH" in out

    def test_pythonunbuffered_is_set_by_default(self, capfd: pytest.CaptureFixture[str]) -> None:
        """``PYTHONUNBUFFERED=1`` is injected into the child env so Python
        descendants flush stdout line-by-line to pipes, not on process exit."""
        run_streamed(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('PYTHONUNBUFFERED', 'unset'))",
            ]
        )
        assert capfd.readouterr().out.strip() == "1"


class TestRunTeed:
    """Tests for ``run_teed``."""

    def test_streams_and_captures_stdout(self, monkeypatch: MonkeyPatch) -> None:
        """Each line of stdout is both written live and captured in the buffer.

        The child deliberately does NOT call ``sys.stdout.flush()`` — real
        tools (cz, pytest, mypy) don't, and an earlier version of this test
        did which masked a PYTHONUNBUFFERED bug. We rely on the helper's
        ``PYTHONUNBUFFERED=1`` env override for the child to line-buffer.
        """
        fake_stdout = io.StringIO()
        monkeypatch.setattr(sys, "stdout", fake_stdout)

        result = run_teed(
            [
                sys.executable,
                "-c",
                "for i in (1, 2, 3):\n    print(i)\n",
            ]
        )

        streamed = fake_stdout.getvalue()
        # All three lines must appear in the live-streamed output.
        assert "1\n" in streamed
        assert "2\n" in streamed
        assert "3\n" in streamed
        # And also in the returned captured stdout.
        assert result.stdout == "1\n2\n3\n"
        assert result.stderr == ""
        assert result.returncode == 0

    def test_stderr_merges_into_stdout(self, monkeypatch: MonkeyPatch) -> None:
        """Content written to stderr is captured in ``.stdout`` (merged stream)."""
        fake_stdout = io.StringIO()
        monkeypatch.setattr(sys, "stdout", fake_stdout)

        result = run_teed(
            [
                sys.executable,
                "-c",
                "import sys; sys.stderr.write('err-line\\n'); sys.stderr.flush()",
            ]
        )

        assert "err-line" in result.stdout
        assert "err-line" in fake_stdout.getvalue()
        assert result.stderr == ""
        assert result.returncode == 0

    def test_returncode_reflects_success(self, monkeypatch: MonkeyPatch) -> None:
        """A zero-exit command returns a ``CompletedProcess`` with ``returncode=0``."""
        monkeypatch.setattr(sys, "stdout", io.StringIO())
        result = run_teed([sys.executable, "-c", "print('ok')"])
        assert result.returncode == 0
        assert "ok" in result.stdout

    def test_failure_with_check_true_raises_with_stdout(self, monkeypatch: MonkeyPatch) -> None:
        """Non-zero exit under ``check=True`` raises with captured ``stdout``.

        This preserves the old error-path semantics — callers that logged
        ``e.stdout`` still see output even though live streaming already
        showed it to the user.
        """
        monkeypatch.setattr(sys, "stdout", io.StringIO())

        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            run_teed(
                [
                    sys.executable,
                    "-c",
                    "import sys; print('partial output'); sys.exit(5)",
                ]
            )

        err = excinfo.value
        assert err.returncode == 5
        assert err.stdout is not None
        assert "partial output" in err.stdout

    def test_failure_with_check_false_returns_completedprocess(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        """Non-zero exit under ``check=False`` returns a ``CompletedProcess``."""
        monkeypatch.setattr(sys, "stdout", io.StringIO())

        result = run_teed(
            [
                sys.executable,
                "-c",
                "import sys; print('still captured'); sys.exit(7)",
            ],
            check=False,
        )

        assert result.returncode == 7
        assert "still captured" in result.stdout
        assert result.stderr == ""

    def test_env_is_threaded_through(self, monkeypatch: MonkeyPatch) -> None:
        """The ``env`` mapping is forwarded to the child process."""
        monkeypatch.setattr(sys, "stdout", io.StringIO())

        result = run_teed(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('RUN_TEED_TEST', ''))",
            ],
            env={"RUN_TEED_TEST": "teed-value"},
        )

        assert "teed-value" in result.stdout

    def test_cwd_is_threaded_through(self, monkeypatch: MonkeyPatch, tmp_path: object) -> None:
        """The ``cwd`` parameter is forwarded to the child process."""
        monkeypatch.setattr(sys, "stdout", io.StringIO())

        # tmp_path is a pathlib.Path fixture; reify to str for the child.
        from pathlib import Path

        assert isinstance(tmp_path, Path)
        result = run_teed(
            [sys.executable, "-c", "import os; print(os.getcwd())"],
            cwd=str(tmp_path),
        )

        # getcwd() in the child should resolve to tmp_path.
        captured = result.stdout.strip()
        assert Path(captured).resolve() == tmp_path.resolve()

    def test_pythonunbuffered_is_set_by_default(self, monkeypatch: MonkeyPatch) -> None:
        """``PYTHONUNBUFFERED=1`` is injected into the child env so Python
        descendants flush stdout line-by-line to pipes, not on process exit."""
        monkeypatch.setattr(sys, "stdout", io.StringIO())
        result = run_teed(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('PYTHONUNBUFFERED', 'unset'))",
            ]
        )
        assert result.stdout.strip() == "1"

    def test_pythonunbuffered_caller_override_respected(self, monkeypatch: MonkeyPatch) -> None:
        """A caller-supplied ``PYTHONUNBUFFERED`` wins; the helper only
        provides it as a default."""
        monkeypatch.setattr(sys, "stdout", io.StringIO())
        result = run_teed(
            [
                sys.executable,
                "-c",
                "import os; print(os.environ.get('PYTHONUNBUFFERED', 'unset'))",
            ],
            env={**os.environ, "PYTHONUNBUFFERED": "0"},
        )
        assert result.stdout.strip() == "0"

    def test_streams_line_by_line_without_child_flush(self, monkeypatch: MonkeyPatch) -> None:
        """Regression test for PR #633 review Issue 2: a Python child that
        does NOT call ``sys.stdout.flush()`` after each print (which is what
        real tools do) still delivers lines to the parent as they are
        printed — not batched at process exit — thanks to
        ``PYTHONUNBUFFERED=1``. Without that env override, all three writes
        would arrive together at ~0.45s when the child terminates.
        """
        import time

        received: list[tuple[float, str]] = []
        start = time.monotonic()

        class TimestampingStdout:
            def write(self, s: str) -> int:
                received.append((time.monotonic() - start, s))
                return len(s)

            def flush(self) -> None:
                pass

        monkeypatch.setattr(sys, "stdout", TimestampingStdout())

        # Child prints 3 lines with 150ms gaps. Total runtime ~0.45s. No flush.
        run_teed(
            [
                sys.executable,
                "-c",
                "import time\nfor i in (1, 2, 3):\n    print(i)\n    time.sleep(0.15)\n",
            ]
        )

        content_writes = [(t, s) for t, s in received if s.strip()]
        assert len(content_writes) >= 3, f"expected >=3 content writes, got {content_writes}"

        first_write_time = content_writes[0][0]
        # Generous threshold: first line should arrive by ~0.15s under live
        # streaming; child's full runtime is ~0.45s. 0.3s gives margin for
        # slow CI without masking a regression where everything arrives at
        # process exit.
        assert first_write_time < 0.3, (
            f"first content write at {first_write_time:.3f}s "
            f"(child runs ~0.45s). Output appears buffered — "
            f"regression of PR #633 review Issue 2 fix (PYTHONUNBUFFERED)."
        )

    def test_raising_write_triggers_child_cleanup(self, monkeypatch: MonkeyPatch) -> None:
        """Regression test for PR #633 review Issue 1: if the stdout-write
        loop raises, the helper still calls ``process.kill()`` and
        ``wait()`` so the child is reaped and the pipe is closed — no
        lingering child, no deadlock on a full pipe."""

        class FailingStdout:
            def write(self, s: str) -> int:
                raise OSError(f"broken stdout (refused {len(s)} chars)")

            def flush(self) -> None:
                pass

        monkeypatch.setattr(sys, "stdout", FailingStdout())

        # The child prints a line; our write will raise on the first line.
        # Primary assertion: the exception propagates out (rather than the
        # helper swallowing it and hanging on wait()).
        with pytest.raises(OSError, match="broken stdout"):
            run_teed([sys.executable, "-c", "print('hi')"])


class TestExtractVersionFromReleasePR:
    """Tests for ``_extract_version_from_release_pr``.

    Covers the PR-title / branch-name shapes produced by ``task_release``
    (and the shapes a maintainer might hand-write), including PEP440 and
    semver-style pre-release suffixes that the previous regex in
    ``task_release_tag`` rejected (issue #632).
    """

    @pytest.mark.parametrize(
        ("pr_title", "expected"),
        [
            # Production release (what was already supported before #632).
            ("release: v1.0.0", "1.0.0"),
            # PEP440 pre-release shapes (cz bump --prerelease output).
            ("release: v0.1.0a0", "0.1.0a0"),
            ("release: v0.2.0b1", "0.2.0b1"),
            ("release: v1.5.0rc0", "1.5.0rc0"),
            ("release: v0.1.0.dev2", "0.1.0.dev2"),
            # Semver-style pre-release shapes (hand-written / alternate tooling).
            ("release: v0.1.0-alpha.0", "0.1.0-alpha.0"),
            ("release: v0.1.0-beta.1", "0.1.0-beta.1"),
            ("release: v0.1.0-rc.0", "0.1.0-rc.0"),
        ],
    )
    def test_extracts_from_pr_title(self, pr_title: str, expected: str) -> None:
        """The PR title is the primary source; the captured group is the bare version."""
        # Branch name is deliberately unrelated so the title match is the only
        # thing that can succeed.
        assert _extract_version_from_release_pr(pr_title, "unrelated/branch") == expected

    def test_falls_back_to_branch_name(self) -> None:
        """When the PR title doesn't match, the branch name is consulted."""
        assert _extract_version_from_release_pr("unrelated: fix", "release/v0.1.0a0") == "0.1.0a0"

    def test_returns_none_when_neither_matches(self) -> None:
        """Neither input matches -> ``None`` (caller handles the error path)."""
        assert _extract_version_from_release_pr("fix: bug", "fix/123-thing") is None

    def test_returns_none_for_non_numeric_version(self) -> None:
        """``release: vX.Y.Z`` with literal letters must not match — the regex
        requires digits."""
        assert _extract_version_from_release_pr("release: vX.Y.Z", "release/vX.Y.Z") is None


class TestBuildCzGetNextCmd:
    """Tests for ``_build_cz_get_next_cmd``.

    The helper is a pure command-list builder: no validation, no I/O. These
    tests pin the flag ordering, the uppercasing of ``--increment``, and the
    verbatim pass-through of ``--prerelease`` (issue #632 Phase B).
    """

    @pytest.mark.parametrize(
        ("increment", "prerelease", "expected"),
        [
            # No flags: base command only.
            ("", "", ["uv", "run", "cz", "bump", "--get-next", "--yes"]),
            # Increment alone (lowercase input is uppercased).
            (
                "minor",
                "",
                ["uv", "run", "cz", "bump", "--get-next", "--yes", "--increment", "MINOR"],
            ),
            # Increment alone (already uppercase stays uppercase).
            (
                "PATCH",
                "",
                ["uv", "run", "cz", "bump", "--get-next", "--yes", "--increment", "PATCH"],
            ),
            # Prerelease alone: alpha.
            (
                "",
                "alpha",
                ["uv", "run", "cz", "bump", "--get-next", "--yes", "--prerelease", "alpha"],
            ),
            # Prerelease alone: beta.
            (
                "",
                "beta",
                ["uv", "run", "cz", "bump", "--get-next", "--yes", "--prerelease", "beta"],
            ),
            # Prerelease alone: rc.
            (
                "",
                "rc",
                ["uv", "run", "cz", "bump", "--get-next", "--yes", "--prerelease", "rc"],
            ),
            # Both set: helper does NOT validate; the task is responsible for
            # rejecting this combination. Helper just emits both flags in
            # increment-then-prerelease order.
            (
                "minor",
                "alpha",
                [
                    "uv",
                    "run",
                    "cz",
                    "bump",
                    "--get-next",
                    "--yes",
                    "--increment",
                    "MINOR",
                    "--prerelease",
                    "alpha",
                ],
            ),
        ],
    )
    def test_builds_expected_command(
        self, increment: str, prerelease: str, expected: list[str]
    ) -> None:
        """The emitted list matches the expected base + flags in order."""
        assert _build_cz_get_next_cmd(increment, prerelease) == expected


class TestValidateMergeCommits:
    """Tests for ``validate_merge_commits`` (issue #639).

    The helper shells out to ``git describe`` and ``git log --merges``; the
    tests monkeypatch ``subprocess.run`` inside ``tools.doit.release`` so the
    git calls return canned results and the ``range_spec`` argument to the
    second call can be asserted on.
    """

    @staticmethod
    def _silent_console() -> Console:
        return Console(file=io.StringIO(), force_terminal=False)

    @staticmethod
    def _fake_run(
        describe_returncode: int,
        describe_stdout: str,
        log_stdout: str,
    ) -> tuple[list[list[str]], object]:
        """Build a fake ``subprocess.run`` that captures calls.

        Returns ``(captured_calls, fake_run)``. The first git-describe call
        yields a ``CompletedProcess`` with the given ``describe_returncode``
        and ``describe_stdout``; the second git-log call yields ``log_stdout``
        with returncode 0. ``captured_calls`` is appended to on each call.
        """
        calls: list[list[str]] = []

        def fake(
            cmd: list[str],
            *_args: object,
            **_kwargs: object,
        ) -> subprocess.CompletedProcess[str]:
            calls.append(cmd)
            if "describe" in cmd:
                return subprocess.CompletedProcess(
                    args=cmd, returncode=describe_returncode, stdout=describe_stdout, stderr=""
                )
            return subprocess.CompletedProcess(args=cmd, returncode=0, stdout=log_stdout, stderr="")

        return calls, fake

    def test_no_tags_falls_back_to_last_10_commits(self, monkeypatch: MonkeyPatch) -> None:
        """When ``git describe`` fails (no tags), range_spec is ``HEAD~10..HEAD``.

        Regression test for #639: the previous fallback was ``HEAD``, which
        walked full history and surfaced merges from unrelated pre-project
        ancestors on any fresh repo.
        """
        calls, fake = self._fake_run(describe_returncode=128, describe_stdout="", log_stdout="")
        monkeypatch.setattr("tools.doit.release.subprocess.run", fake)

        assert validate_merge_commits(self._silent_console()) is True

        log_cmds = [c for c in calls if "log" in c]
        assert len(log_cmds) == 1
        assert log_cmds[0][-1] == "HEAD~10..HEAD"

    def test_with_tag_uses_tag_range(self, monkeypatch: MonkeyPatch) -> None:
        """When a tag exists, range_spec is ``<last_tag>..HEAD``."""
        calls, fake = self._fake_run(
            describe_returncode=0, describe_stdout="v0.1.0\n", log_stdout=""
        )
        monkeypatch.setattr("tools.doit.release.subprocess.run", fake)

        assert validate_merge_commits(self._silent_console()) is True

        log_cmds = [c for c in calls if "log" in c]
        assert len(log_cmds) == 1
        assert log_cmds[0][-1] == "v0.1.0..HEAD"

    def test_valid_merge_commit_passes(self, monkeypatch: MonkeyPatch) -> None:
        """A merge commit matching the convention returns True."""
        _, fake = self._fake_run(
            describe_returncode=0,
            describe_stdout="v0.1.0\n",
            log_stdout="abc1234 fix: handle null (merges PR #42, addresses #41)",
        )
        monkeypatch.setattr("tools.doit.release.subprocess.run", fake)

        assert validate_merge_commits(self._silent_console()) is True

    def test_invalid_merge_commit_fails(self, monkeypatch: MonkeyPatch) -> None:
        """A merge commit not matching the convention returns False."""
        _, fake = self._fake_run(
            describe_returncode=0,
            describe_stdout="v0.1.0\n",
            log_stdout="abc1234 Merge branch 'master' of https://example.com/repo",
        )
        monkeypatch.setattr("tools.doit.release.subprocess.run", fake)

        assert validate_merge_commits(self._silent_console()) is False


class TestExtractNextVersionFromCzOutput:
    """Tests for ``_extract_next_version_from_cz_output`` (issue #641).

    Scans the captured stdout of ``cz bump --get-next --yes`` and returns
    the last line that matches a semver-ish version pattern. Must tolerate
    leading diagnostic noise (on a tagless repo, cz prints a multi-line
    "No tag matching configuration could be found" block before emitting
    the version) and reject strings that merely contain a version substring.
    """

    @pytest.mark.parametrize(
        ("stdout", "expected"),
        [
            # Clean production-release output.
            ("1.2.3\n", "1.2.3"),
            # Clean pre-release output (PEP440).
            ("0.1.0a0\n", "0.1.0a0"),
            ("0.1.0b1\n", "0.1.0b1"),
            ("0.1.0rc0\n", "0.1.0rc0"),
            # Clean pre-release output (semver style).
            ("0.1.0-alpha.0\n", "0.1.0-alpha.0"),
            # Leading 'v' accepted and stripped.
            ("v0.2.0\n", "0.2.0"),
            # Tagless-repo case: diagnostic noise precedes the version.
            # Regression case that this helper exists to fix.
            (
                "No tag matching configuration could be found.\n"
                "Possible causes:\n"
                "- version in configuration is not the current version\n"
                "- tag_format or legacy_tag_formats is missing\n"
                "\n"
                "0.1.0a0\n",
                "0.1.0a0",
            ),
            # Trailing blank lines are ignored; the version is still found.
            ("0.1.0\n\n\n", "0.1.0"),
        ],
    )
    def test_returns_trailing_version_line(self, stdout: str, expected: str) -> None:
        assert _extract_next_version_from_cz_output(stdout) == expected

    def test_returns_none_when_no_version_line(self) -> None:
        """Output with zero version-shaped lines returns ``None``."""
        assert _extract_next_version_from_cz_output("totally unrelated output\n") is None

    def test_rejects_line_that_only_contains_a_version_substring(self) -> None:
        """The pattern is anchored to the whole line.

        A diagnostic line like ``"error at 1.2.3 somewhere"`` must not
        be mistaken for the version output.
        """
        stdout = "something broke near 1.2.3 in the build\n"
        assert _extract_next_version_from_cz_output(stdout) is None

    def test_returns_last_version_when_multiple(self) -> None:
        """When multiple version-shaped lines are present, take the last.

        cz may print intermediate version hints in diagnostic output; the
        trailing line is the authoritative one.
        """
        stdout = "0.0.1\n0.0.2\n0.0.3\n"
        assert _extract_next_version_from_cz_output(stdout) == "0.0.3"


class TestRepoHasVersionTags:
    """Tests for ``_repo_has_version_tags`` (issue #448).

    The helper shells out to ``git tag --list v*``. These tests monkeypatch
    ``subprocess.run`` inside ``tools.doit.release`` so the git call returns
    canned stdout.
    """

    @staticmethod
    def _fake_tag_list(
        stdout: str, returncode: int = 0
    ) -> Callable[..., subprocess.CompletedProcess[str]]:
        def fake(
            cmd: list[str],
            *_args: object,
            **_kwargs: object,
        ) -> subprocess.CompletedProcess[str]:
            assert cmd[:3] == ["git", "tag", "--list"]
            return subprocess.CompletedProcess(
                args=cmd, returncode=returncode, stdout=stdout, stderr=""
            )

        return fake

    def test_no_tags_returns_false(self, monkeypatch: MonkeyPatch) -> None:
        """Empty ``git tag --list v*`` output → no tags → ``False``."""
        monkeypatch.setattr("tools.doit.release.subprocess.run", self._fake_tag_list(""))
        assert _repo_has_version_tags() is False

    def test_whitespace_only_returns_false(self, monkeypatch: MonkeyPatch) -> None:
        """Whitespace-only output counts as no tags."""
        monkeypatch.setattr("tools.doit.release.subprocess.run", self._fake_tag_list("\n\n  \n"))
        assert _repo_has_version_tags() is False

    def test_one_tag_returns_true(self, monkeypatch: MonkeyPatch) -> None:
        """A single ``v*`` tag present → ``True``."""
        monkeypatch.setattr("tools.doit.release.subprocess.run", self._fake_tag_list("v0.0.0\n"))
        assert _repo_has_version_tags() is True

    def test_multiple_tags_returns_true(self, monkeypatch: MonkeyPatch) -> None:
        """Multiple ``v*`` tags present → ``True``."""
        monkeypatch.setattr(
            "tools.doit.release.subprocess.run",
            self._fake_tag_list("v0.0.0\nv0.1.0a0\nv0.1.0\n"),
        )
        assert _repo_has_version_tags() is True


class TestTaskReleaseActionSignature:
    """Regression tests for ``task_release`` CLI-param wiring (issue #650).

    doit's ``params`` parsing populates values for the **action function**,
    not the outer task-creator function. If the action doesn't accept the
    param names as kwargs, doit silently drops the CLI values and the action
    runs with closure-captured defaults. These tests pin the action signature
    so a future refactor can't re-introduce the silent drop.
    """

    def test_action_accepts_params(self) -> None:
        """The first action must accept ``increment`` and ``prerelease`` kwargs."""
        import inspect

        from tools.doit.release import task_release

        result = task_release()
        actions = result["actions"]
        assert actions, "task_release must return at least one action"
        action = actions[0]
        sig = inspect.signature(action)
        assert "increment" in sig.parameters, (
            "create_release_pr must accept 'increment' for --increment CLI flag to reach it"
        )
        assert "prerelease" in sig.parameters, (
            "create_release_pr must accept 'prerelease' for --prerelease CLI flag to reach it"
        )

    def test_params_names_match_action_signature(self) -> None:
        """Every ``params[n]['name']`` must be a parameter of the action function.

        Without this match, doit's parsed CLI values can't reach the action.
        """
        import inspect

        from tools.doit.release import task_release

        result = task_release()
        action = result["actions"][0]
        sig_params = set(inspect.signature(action).parameters)
        cli_param_names = {p["name"] for p in result["params"]}
        missing = cli_param_names - sig_params
        assert not missing, (
            f"params names {missing} have no matching kwarg in the action signature; "
            "doit will silently drop their CLI values"
        )


class TestReleaseTagGhSearch:
    """Regression test for ``task_release_tag``'s gh pr list search (issue #657).

    GitHub's search parses ``release: v in:title`` with the colon as a
    qualifier separator (like ``head:``, ``author:``), returning zero results
    for literal title substrings containing colons. ``head:release/`` is
    GitHub's intended syntax and matches the head-branch naming convention
    ``doit release`` uses for release branches.
    """

    def test_gh_search_uses_head_prefix_not_title_colon_substring(self) -> None:
        """Source must use head:release/ and not the broken title-colon search."""
        import pathlib

        # Windows read_text() defaults to cp1252 which can't decode non-ASCII
        # characters like ❌ in release.py's error banners — always specify utf-8.
        src = pathlib.Path("tools/doit/release.py").read_text(encoding="utf-8")
        assert "release: v in:title" not in src, (
            "The broken colon-in-search pattern returns zero results from gh "
            "pr list and must not recur"
        )
        assert '"head:release/"' in src, (
            "task_release_tag must use head:release/ to find merged release PRs"
        )

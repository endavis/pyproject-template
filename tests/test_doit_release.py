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
    _extract_version_from_release_pr,
    validate_merge_commits,
)

if TYPE_CHECKING:
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
            ("", "", ["uv", "run", "cz", "bump", "--get-next"]),
            # Increment alone (lowercase input is uppercased).
            (
                "minor",
                "",
                ["uv", "run", "cz", "bump", "--get-next", "--increment", "MINOR"],
            ),
            # Increment alone (already uppercase stays uppercase).
            (
                "PATCH",
                "",
                ["uv", "run", "cz", "bump", "--get-next", "--increment", "PATCH"],
            ),
            # Prerelease alone: alpha.
            (
                "",
                "alpha",
                ["uv", "run", "cz", "bump", "--get-next", "--prerelease", "alpha"],
            ),
            # Prerelease alone: beta.
            (
                "",
                "beta",
                ["uv", "run", "cz", "bump", "--get-next", "--prerelease", "beta"],
            ),
            # Prerelease alone: rc.
            (
                "",
                "rc",
                ["uv", "run", "cz", "bump", "--get-next", "--prerelease", "rc"],
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

"""Tests for tools/doit/git.py task wiring.

Verifies that ``task_commit``, ``task_bump``, and ``task_changelog`` gate
their ``cz`` invocations on ``uv pip show commitizen`` (via
``install_check_or_skip``) so real failures — pre-commit hook rejections,
tag/version bump failures, changelog generation failures — propagate
instead of being swallowed by the legacy ``|| echo 'not installed'`` pattern.

Addresses issue #527. ``TestWorktree`` covers ``doit worktree`` (#854).
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Iterator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from tools.doit.git import (
    _main_checkout,
    task_bump,
    task_changelog,
    task_commit,
    task_pre_commit_install,
    task_worktree,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestGitTaskGates:
    """Each git task gates ``cz`` via ``uv pip show commitizen``.

    The package name is ``commitizen`` (CLI is ``cz``). All three tasks
    share the same gating package; the underlying ``cz`` subcommand differs.
    """

    def test_commit_gates_on_commitizen_package(self) -> None:
        action = task_commit()["actions"][0]
        assert isinstance(action, str)
        assert "uv pip show commitizen" in action
        assert "commitizen not installed. Run: uv sync" in action
        assert "uv run cz commit" in action
        # Bug-fix invariant: the bare-swallow pattern must be gone.
        assert "|| echo 'commitizen not installed" not in action

    def test_bump_gates_on_commitizen_package(self) -> None:
        action = task_bump()["actions"][0]
        assert isinstance(action, str)
        assert "uv pip show commitizen" in action
        assert "commitizen not installed. Run: uv sync" in action
        assert "uv run cz bump" in action
        assert "|| echo 'commitizen not installed" not in action

    def test_changelog_gates_on_commitizen_package(self) -> None:
        action = task_changelog()["actions"][0]
        assert isinstance(action, str)
        assert "uv pip show commitizen" in action
        assert "commitizen not installed. Run: uv sync" in action
        assert "uv run cz changelog" in action
        assert "|| echo 'commitizen not installed" not in action


class TestPreCommitInstall:
    """`pre_commit_install` and the config must agree on the hook set (#749 D1).

    The task installs whatever `default_install_hook_types` declares. That is the
    right design — one source for the set — but it couples two files silently:
    remove the declaration and the task keeps passing while `commit-msg` stops
    being installed, which is the #741 failure exactly. These tests hold the two
    together.
    """

    @staticmethod
    def _declared_hook_types() -> list[str]:
        config = yaml.safe_load((REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
        return list(config.get("default_install_hook_types") or [])

    def test_task_delegates_the_hook_set_to_the_config(self) -> None:
        """A single bare install, so the config decides which types are installed."""
        actions = task_pre_commit_install()["actions"]
        assert actions == ["uv run pre-commit install"], (
            "Enumerating --hook-type here re-creates the bug this fixed: the list "
            "drifts from `default_install_hook_types` and describes a hook set that "
            "is no longer the hook set."
        )

    def test_config_declares_the_hook_types_the_task_relies_on(self) -> None:
        """The bare install is only sufficient while the config declares the set."""
        declared = self._declared_hook_types()
        assert declared, (
            "`default_install_hook_types` is gone from .pre-commit-config.yaml, so "
            "`pre-commit install` now installs only `pre-commit` and every other hook "
            "type stops running. Restore it, or make the task enumerate the set again."
        )

    def test_commit_msg_is_among_them(self) -> None:
        """`commit-msg` carries conventional commits and the branch/issue check."""
        assert "commit-msg" in self._declared_hook_types(), (
            "Without `commit-msg`, neither conventional-commit validation nor the "
            "commit/branch issue check runs -- silently, because a hook that was "
            "never installed cannot fail (#741)."
        )


def _fake_git(
    fail: dict[str, subprocess.CalledProcessError] | None = None, valid_name: bool = True
) -> Callable[..., MagicMock]:
    """Stand in for ``subprocess.run``; *fail* maps a git subcommand to the error it raises."""

    def run(cmd: list[str], **_kwargs: object) -> MagicMock:
        if fail and cmd[1] in fail:
            raise fail[cmd[1]]
        ok = valid_name or cmd[1] != "check-ref-format"
        return MagicMock(returncode=0 if ok else 1, stdout="", stderr="")

    return run


class TestWorktree:
    """`doit worktree` — a checkout with its own environment (#854)."""

    BRANCH = "feat/42-add-export"

    @pytest.fixture
    def mocks(self, tmp_path: Path) -> Iterator[tuple[MagicMock, MagicMock]]:
        """Patch git (``subprocess.run``) and ``uv sync`` (``run_streamed``)."""
        with (
            patch("tools.doit.git._main_checkout", return_value=tmp_path),
            patch("tools.doit.git.subprocess.run", side_effect=_fake_git()) as mock_run,
            patch("tools.doit.git.run_streamed") as mock_sync,
        ):
            yield mock_run, mock_sync

    @staticmethod
    def _create(branch: str | None) -> None:
        action: Callable[..., None] = task_worktree()["actions"][0]
        action(branch=branch)

    @staticmethod
    def _cmds(mock_run: MagicMock) -> list[list[str]]:
        return [call.args[0] for call in mock_run.call_args_list]

    def test_branches_from_a_fresh_origin_main_without_tracking(
        self, mocks: tuple[MagicMock, MagicMock], tmp_path: Path
    ) -> None:
        """No upstream, so `doit pr` pushes the branch rather than trusting origin/main."""
        mock_run, _ = mocks
        self._create(self.BRANCH)

        cmds = self._cmds(mock_run)
        fetch = ["git", "fetch", "origin", "main"]
        path = str(tmp_path / "worktrees" / self.BRANCH)
        add = ["git", "worktree", "add", "--no-track", "-b", self.BRANCH, path, "origin/main"]
        assert cmds.index(fetch) < cmds.index(add)

    def test_syncs_its_own_environment_without_virtual_env(
        self,
        mocks: tuple[MagicMock, MagicMock],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """An inherited VIRTUAL_ENV names the main checkout's .venv; the sync must not see it."""
        _, mock_sync = mocks
        monkeypatch.setenv("VIRTUAL_ENV", "/main/.venv")
        monkeypatch.setenv("UV_CACHE_DIR", "/shared/uv-cache")
        self._create(self.BRANCH)

        mock_sync.assert_called_once()
        assert mock_sync.call_args.args[0] == ["uv", "sync", "--all-extras", "--dev"]
        assert mock_sync.call_args.kwargs["cwd"] == tmp_path / "worktrees" / self.BRANCH
        env = mock_sync.call_args.kwargs["env"]
        assert "VIRTUAL_ENV" not in env
        assert env["UV_CACHE_DIR"] == "/shared/uv-cache"

    def test_a_relative_uv_cache_stays_this_checkouts_cache(
        self,
        mocks: tuple[MagicMock, MagicMock],
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """base.py's relative default would otherwise resolve inside the new worktree."""
        _, mock_sync = mocks
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("UV_CACHE_DIR", "tmp/.uv_cache")
        self._create(self.BRANCH)

        env = mock_sync.call_args.kwargs["env"]
        assert env["UV_CACHE_DIR"] == str((tmp_path / "tmp" / ".uv_cache").resolve())

    def test_prints_how_to_work_there_and_how_to_remove_it(
        self,
        mocks: tuple[MagicMock, MagicMock],
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        self._create(self.BRANCH)

        out = capsys.readouterr().out
        path = tmp_path / "worktrees" / self.BRANCH
        assert f"cd {path}" in out
        assert "uv run doit check" in out
        assert "Never pass --active" in out
        assert f"git worktree remove {path}" in out

    def test_requires_a_branch(self, mocks: tuple[MagicMock, MagicMock]) -> None:
        mock_run, mock_sync = mocks
        with pytest.raises(SystemExit) as exc:
            self._create(None)

        assert exc.value.code == 1
        mock_run.assert_not_called()
        mock_sync.assert_not_called()

    def test_refuses_an_invalid_branch_name(self, mocks: tuple[MagicMock, MagicMock]) -> None:
        """The name becomes a path under worktrees/, so it is checked before anything runs."""
        mock_run, mock_sync = mocks
        mock_run.side_effect = _fake_git(valid_name=False)
        with pytest.raises(SystemExit) as exc:
            self._create("feat/bad name")

        assert exc.value.code == 1
        assert [cmd[1] for cmd in self._cmds(mock_run)] == ["check-ref-format"]
        mock_sync.assert_not_called()

    @pytest.mark.parametrize("name", ["../escape", "/tmp/escape", "feat/../../escape"])
    def test_git_rejects_names_that_would_leave_worktrees_dir(self, name: str) -> None:
        """The path check relies on git refusing these; pin that with the real git."""
        result = subprocess.run(
            ["git", "check-ref-format", "--branch", name],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode != 0

    def test_fetch_failure_warns_and_still_creates(
        self, mocks: tuple[MagicMock, MagicMock], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Offline, the last fetched origin/main is still a sound base; `doit pr` checks later."""
        mock_run, mock_sync = mocks
        error = subprocess.CalledProcessError(128, ["git"], stderr="could not resolve host")
        mock_run.side_effect = _fake_git(fail={"fetch": error})
        self._create(self.BRANCH)

        assert "worktree" in [cmd[1] for cmd in self._cmds(mock_run)]
        mock_sync.assert_called_once()
        assert "could not resolve host" in capsys.readouterr().out

    def test_worktree_add_failure_exits_before_syncing(
        self, mocks: tuple[MagicMock, MagicMock], capsys: pytest.CaptureFixture[str]
    ) -> None:
        mock_run, mock_sync = mocks
        error = subprocess.CalledProcessError(
            128, ["git"], stderr="fatal: a branch named 'feat/42-add-export' already exists"
        )
        mock_run.side_effect = _fake_git(fail={"worktree": error})
        with pytest.raises(SystemExit) as exc:
            self._create(self.BRANCH)

        assert exc.value.code == 1
        mock_sync.assert_not_called()
        assert "already exists" in capsys.readouterr().out

    def test_sync_failure_exits_and_keeps_the_worktree(
        self, mocks: tuple[MagicMock, MagicMock], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """No silent revert: the worktree stays, with the command to retry."""
        mock_run, mock_sync = mocks
        mock_sync.side_effect = subprocess.CalledProcessError(1, ["uv"])
        with pytest.raises(SystemExit) as exc:
            self._create(self.BRANCH)

        assert exc.value.code == 1
        assert ["git", "worktree", "remove"] not in [cmd[:3] for cmd in self._cmds(mock_run)]
        assert "uv sync --all-extras --dev" in capsys.readouterr().out


def test_main_checkout_is_the_first_listed_worktree() -> None:
    """Run from a linked worktree, `doit worktree` still creates beside the main checkout."""
    porcelain = (
        "worktree /src/project\nHEAD abc\nbranch refs/heads/main\n\n"
        "worktree /src/project/worktrees/feat/1-x\nHEAD def\nbranch refs/heads/feat/1-x\n"
    )
    with patch("tools.doit.git.subprocess.run", return_value=MagicMock(stdout=porcelain)):
        assert _main_checkout() == Path("/src/project")


def test_worktrees_directory_is_gitignored() -> None:
    """A worktree inside the repository must never show as untracked, or be committed."""
    result = subprocess.run(
        ["git", "check-ignore", "-q", "worktrees/feat/42-add-export/pyproject.toml"],
        cwd=REPO_ROOT,
        check=False,
    )
    assert result.returncode == 0

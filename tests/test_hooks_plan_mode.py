"""Tests for the plan-mode PostToolUse hooks."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOKS_DIR = REPO_ROOT / "tools" / "hooks" / "ai"
ENTER_HOOK = HOOKS_DIR / "plan-mode-enter.py"
EXIT_HOOK = HOOKS_DIR / "plan-mode-exit.py"


def _run_hook(
    hook_path: Path,
    project_dir: Path,
    stdin_payload: str,
) -> subprocess.CompletedProcess[str]:
    """Invoke a hook script as Claude Code would."""
    env = {
        "CLAUDE_PROJECT_DIR": str(project_dir),
        "PATH": os.environ["PATH"],
    }
    # Preserve Python env bits so interpreter can find stdlib in venvs.
    for key in ("PYTHONPATH", "VIRTUAL_ENV", "HOME"):
        if key in os.environ:
            env[key] = os.environ[key]

    return subprocess.run(
        [sys.executable, str(hook_path)],
        input=stdin_payload,
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
        check=False,
    )


def _state_file(project_dir: Path) -> Path:
    return project_dir / ".claude" / ".plan-mode-state"


@pytest.fixture
def payload() -> str:
    """Minimal plausible PostToolUse JSON payload."""
    return json.dumps(
        {
            "tool_name": "EnterPlanMode",
            "tool_input": {"plan": "do stuff"},
            "tool_response": {},
        }
    )


class TestEnterHook:
    def test_writes_active(self, tmp_path: Path, payload: str) -> None:
        result = _run_hook(ENTER_HOOK, tmp_path, payload)
        assert result.returncode == 0, result.stderr
        state = _state_file(tmp_path)
        assert state.exists()
        assert state.read_bytes() == b"active"

    def test_overwrites_existing_inactive(self, tmp_path: Path, payload: str) -> None:
        state = _state_file(tmp_path)
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("inactive")

        result = _run_hook(ENTER_HOOK, tmp_path, payload)
        assert result.returncode == 0, result.stderr
        assert state.read_bytes() == b"active"

    def test_creates_claude_dir_if_missing(self, tmp_path: Path, payload: str) -> None:
        # tmp_path has no .claude/ subdir
        assert not (tmp_path / ".claude").exists()
        result = _run_hook(ENTER_HOOK, tmp_path, payload)
        assert result.returncode == 0, result.stderr
        assert _state_file(tmp_path).read_bytes() == b"active"

    def test_malformed_json_stdin_exits_zero(self, tmp_path: Path) -> None:
        result = _run_hook(ENTER_HOOK, tmp_path, "not valid json {{{")
        assert result.returncode == 0, result.stderr
        # Even with bad JSON, the hook still writes state (it ignores the payload).
        assert _state_file(tmp_path).read_bytes() == b"active"

    def test_empty_stdin_exits_zero(self, tmp_path: Path) -> None:
        result = _run_hook(ENTER_HOOK, tmp_path, "")
        assert result.returncode == 0, result.stderr
        assert _state_file(tmp_path).read_bytes() == b"active"

    def test_no_trailing_newline(self, tmp_path: Path, payload: str) -> None:
        _run_hook(ENTER_HOOK, tmp_path, payload)
        content = _state_file(tmp_path).read_bytes()
        assert not content.endswith(b"\n")
        assert content == b"active"


class TestExitHook:
    def test_writes_inactive(self, tmp_path: Path, payload: str) -> None:
        result = _run_hook(EXIT_HOOK, tmp_path, payload)
        assert result.returncode == 0, result.stderr
        state = _state_file(tmp_path)
        assert state.exists()
        assert state.read_bytes() == b"inactive"

    def test_overwrites_existing_active(self, tmp_path: Path, payload: str) -> None:
        state = _state_file(tmp_path)
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("active")

        result = _run_hook(EXIT_HOOK, tmp_path, payload)
        assert result.returncode == 0, result.stderr
        assert state.read_bytes() == b"inactive"

    def test_creates_claude_dir_if_missing(self, tmp_path: Path, payload: str) -> None:
        assert not (tmp_path / ".claude").exists()
        result = _run_hook(EXIT_HOOK, tmp_path, payload)
        assert result.returncode == 0, result.stderr
        assert _state_file(tmp_path).read_bytes() == b"inactive"

    def test_malformed_json_stdin_exits_zero(self, tmp_path: Path) -> None:
        result = _run_hook(EXIT_HOOK, tmp_path, "{ bad json")
        assert result.returncode == 0, result.stderr
        assert _state_file(tmp_path).read_bytes() == b"inactive"

    def test_no_trailing_newline(self, tmp_path: Path, payload: str) -> None:
        _run_hook(EXIT_HOOK, tmp_path, payload)
        content = _state_file(tmp_path).read_bytes()
        assert not content.endswith(b"\n")
        assert content == b"inactive"


class TestRoundTrip:
    def test_enter_then_exit(self, tmp_path: Path, payload: str) -> None:
        _run_hook(ENTER_HOOK, tmp_path, payload)
        assert _state_file(tmp_path).read_bytes() == b"active"

        _run_hook(EXIT_HOOK, tmp_path, payload)
        assert _state_file(tmp_path).read_bytes() == b"inactive"

        _run_hook(ENTER_HOOK, tmp_path, payload)
        assert _state_file(tmp_path).read_bytes() == b"active"

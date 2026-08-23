"""Tests for the ``block-dangerous-commands`` PreToolUse hook.

The hook script lives at ``tools/hooks/ai/block-dangerous-commands.py``. Its
filename contains hyphens, so it isn't directly importable as a module — we
load it via ``importlib`` and invoke ``main()`` directly with a stubbed stdin.

Pattern mirrors ``tests/test_bash_ban_raw_tools.py``.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import types
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator

HOOK_PATH = (
    Path(__file__).resolve().parents[1] / "tools" / "hooks" / "ai" / "block-dangerous-commands.py"
)


def _load_hook() -> types.ModuleType:
    """Load the hook script as a fresh module instance."""
    spec = importlib.util.spec_from_file_location("block_dangerous_commands", HOOK_PATH)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise RuntimeError(f"could not load hook from {HOOK_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def hook() -> Iterator[types.ModuleType]:
    """Load a fresh copy of the hook module for each test."""
    module = _load_hook()
    sys.modules["block_dangerous_commands"] = module
    try:
        yield module
    finally:
        sys.modules.pop("block_dangerous_commands", None)


def _set_stdin(monkeypatch: pytest.MonkeyPatch, payload: str) -> None:
    """Replace ``sys.stdin`` with a StringIO containing *payload*."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))


def _bash_payload(command: str) -> str:
    """Build a Claude/Gemini/Codex Bash tool payload."""
    return json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})


def _run(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    *,
    branch: str = "feature/test",
) -> int:
    """Run the hook for *command* and return its exit code.

    ``get_current_branch`` is monkeypatched to return *branch* so tests are
    deterministic regardless of the actual checkout state (TRAP 2 from the plan).
    """
    monkeypatch.setattr(hook, "get_current_branch", lambda: branch)
    _set_stdin(monkeypatch, _bash_payload(command))
    # ``main()`` returns its exit code rather than calling ``sys.exit()``, so
    # call it directly. ``int()`` narrows the module attribute's ``Any`` type
    # for mypy's ``warn_return_any``.
    return int(hook.main())


# ---------------------------------------------------------------------------
# Must-block cases — all currently ALLOWED before this fix
# ---------------------------------------------------------------------------


def test_block_push_force_refspec_head_main(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push --force origin HEAD:main`` is blocked."""
    assert _run(hook, monkeypatch, "git push --force origin HEAD:main") == 2


def test_block_push_plus_main(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push origin +main`` is blocked ('+' prefix is force-push marker)."""
    assert _run(hook, monkeypatch, "git push origin +main") == 2


def test_block_push_with_git_global_dir_option(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git -C . push --force origin main`` is blocked despite global -C option."""
    assert _run(hook, monkeypatch, "git -C . push --force origin main") == 2


def test_block_push_with_git_global_dash_c(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git -c core.pager=cat push --force origin main`` is blocked."""
    assert _run(hook, monkeypatch, "git -c core.pager=cat push --force origin main") == 2


def test_block_push_with_git_global_git_dir(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git --git-dir=.git push --force origin main`` is blocked."""
    assert _run(hook, monkeypatch, "git --git-dir=.git push --force origin main") == 2


def test_block_push_force_with_lease_eq_form(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push --force-with-lease=main origin HEAD:main`` is blocked.

    The ``=<ref>`` form of ``--force-with-lease`` must be recognised as a
    force flag (prefix-aware matching).
    """
    assert _run(hook, monkeypatch, "git push --force-with-lease=main origin HEAD:main") == 2


def test_block_bash_c_push_force(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``bash -c "git push --force origin main"`` is blocked via payload unwrap."""
    assert _run(hook, monkeypatch, 'bash -c "git push --force origin main"') == 2


def test_block_sh_c_push_force(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``sh -c "git push --force origin main"`` is blocked via payload unwrap."""
    assert _run(hook, monkeypatch, 'sh -c "git push --force origin main"') == 2


def test_block_eval_push_force(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``eval "git push --force origin main"`` is blocked via eval unwrap."""
    assert _run(hook, monkeypatch, 'eval "git push --force origin main"') == 2


def test_block_branch_delete_with_git_global_dir(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git -C . branch -D main`` is blocked despite global -C option."""
    assert _run(hook, monkeypatch, "git -C . branch -D main") == 2


def test_block_bash_c_branch_delete(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``bash -c "git branch -D main"`` is blocked via payload unwrap."""
    assert _run(hook, monkeypatch, 'bash -c "git branch -D main"') == 2


def test_block_bash_c_gh_pr_merge_admin(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``bash -c "gh pr merge 1 --admin"`` is blocked — proves unwrap reaches non-git checks."""
    assert _run(hook, monkeypatch, 'bash -c "gh pr merge 1 --admin"') == 2


# ---------------------------------------------------------------------------
# Must-stay-ALLOWED guards
# ---------------------------------------------------------------------------


def test_allow_push_refspec_main_to_feature(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push origin main:feature`` is allowed (destination is 'feature')."""
    assert _run(hook, monkeypatch, "git push origin main:feature") == 0


def test_allow_push_refspec_head_to_refs_feature(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push origin HEAD:refs/heads/feature`` is allowed (destination is 'feature')."""
    assert _run(hook, monkeypatch, "git push origin HEAD:refs/heads/feature") == 0


def test_allow_push_feature_branch(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push origin feature`` is allowed."""
    assert _run(hook, monkeypatch, "git push origin feature") == 0


def test_allow_force_push_feature_branch(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push --force origin feat/my-feature`` is allowed (existing regression guard)."""
    assert _run(hook, monkeypatch, "git push --force origin feat/my-feature") == 0


def test_allow_bash_c_echo_main(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``bash -c "echo main"`` is allowed — unwrap must not over-block."""
    assert _run(hook, monkeypatch, 'bash -c "echo main"') == 0


def test_allow_git_global_dir_push_feature(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git -C /other/repo push origin feature`` is allowed."""
    assert _run(hook, monkeypatch, "git -C /other/repo push origin feature") == 0


# ---------------------------------------------------------------------------
# Message-correctness: deletion refspec must keep its own reason string
# ---------------------------------------------------------------------------


def test_delete_refspec_colon_main_reports_deletion_reason(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """``git push origin :main`` must be blocked with the *deletion* reason, not push reason.

    This guards the ordering hazard documented in the plan: check_push_to_protected
    runs before check_delete_protected_branch. The colon-prefixed token must be
    skipped by the push check so the delete check owns it and reports the correct
    reason.
    """
    monkeypatch.setattr(hook, "get_current_branch", lambda: "feature/test")
    _set_stdin(monkeypatch, _bash_payload("git push origin :main"))
    with pytest.raises(SystemExit) as exc_info:
        sys.exit(hook.main())

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "Deleting protected remote branch 'main'" in captured.err


# ---------------------------------------------------------------------------
# Existing regression: force-with-lease without "=" still blocked
# ---------------------------------------------------------------------------


def test_block_push_force_with_lease_plain(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``git push --force-with-lease origin main`` (no ``=``) is still blocked."""
    assert _run(hook, monkeypatch, "git push --force-with-lease origin main") == 2


# ---------------------------------------------------------------------------
# Determinism: bare push on protected branch is blocked only when on that branch
# ---------------------------------------------------------------------------


def test_bare_push_blocked_when_on_main(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bare ``git push`` is blocked when current branch is main."""
    assert _run(hook, monkeypatch, "git push", branch="main") == 2


def test_bare_push_allowed_when_on_feature(
    hook: types.ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bare ``git push`` with no explicit branch is allowed on a feature branch.

    (Force push without explicit branch is still blocked separately — this checks
    plain push only.)
    """
    # A bare "git push" with no force flag on a feature branch is allowed
    assert _run(hook, monkeypatch, "git push", branch="feature/my-work") == 0

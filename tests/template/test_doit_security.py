"""Tests for tools/doit/security.py ``task_security`` wiring around ``bootstrap.py``.

Verifies that the security task (bandit) includes ``bootstrap.py`` when it
exists at the cwd (template repo) and excludes it when it has been removed
(spawned consumer project). Addresses issue #469.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.doit.security import task_security


def _touch(tmp_path: Path, rel: str) -> Path:
    """Create ``rel`` under ``tmp_path`` and return the absolute path."""
    target = tmp_path / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("", encoding="utf-8")
    return target


class TestTaskSecurity:
    """``task_security`` includes bootstrap.py iff it exists at cwd."""

    def test_includes_bootstrap_py_when_present(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "bootstrap.py")

        task = task_security()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert " bootstrap.py" in action
        # The shell-level fallback messaging is still in place.
        assert "bandit not installed" in action

    def test_excludes_bootstrap_py_when_absent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)

        task = task_security()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert "bootstrap.py" not in action
        # The bandit invocation is still present.
        assert "bandit" in action
        assert "src/" in action
        assert "tools/" in action

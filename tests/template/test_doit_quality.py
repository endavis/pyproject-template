"""Tests for tools/doit/quality.py task wiring around ``bootstrap.py``.

These tests verify that the code-quality tasks include ``bootstrap.py`` when
it exists at the cwd (template repo) and exclude it when it has been removed
(spawned consumer project). Addresses issue #469.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.doit.quality import (
    task_format,
    task_format_check,
    task_lint,
    task_type_check,
)


def _touch(tmp_path: Path, rel: str) -> Path:
    """Create ``rel`` under ``tmp_path`` and return the absolute path."""
    target = tmp_path / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("", encoding="utf-8")
    return target


class TestTaskLint:
    """``task_lint`` includes bootstrap.py iff it exists at cwd."""

    def test_includes_bootstrap_py_when_present(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "bootstrap.py")

        task = task_lint()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert " bootstrap.py" in action

    def test_excludes_bootstrap_py_when_absent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)

        task = task_lint()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert "bootstrap.py" not in action
        # Sanity check: the ruff invocation is still present.
        assert "ruff check" in action


class TestTaskFormat:
    """``task_format`` has two actions (format + check --fix); both must behave the same."""

    def test_both_actions_include_bootstrap_py_when_present(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "bootstrap.py")

        task = task_format()
        for action in task["actions"]:
            assert isinstance(action, str)
            assert " bootstrap.py" in action

    def test_both_actions_exclude_bootstrap_py_when_absent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)

        task = task_format()
        for action in task["actions"]:
            assert isinstance(action, str)
            assert "bootstrap.py" not in action


class TestTaskFormatCheck:
    """``task_format_check`` runs ``ruff format --check``."""

    def test_includes_bootstrap_py_when_present(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "bootstrap.py")

        task = task_format_check()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert " bootstrap.py" in action

    def test_excludes_bootstrap_py_when_absent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)

        task = task_format_check()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert "bootstrap.py" not in action
        assert "ruff format --check" in action


class TestTaskTypeCheck:
    """``task_type_check`` runs ``mypy``."""

    def test_includes_bootstrap_py_when_present(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "bootstrap.py")

        task = task_type_check()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert " bootstrap.py" in action

    def test_excludes_bootstrap_py_when_absent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)

        task = task_type_check()
        action = task["actions"][0]
        assert isinstance(action, str)
        assert "bootstrap.py" not in action
        assert "mypy" in action

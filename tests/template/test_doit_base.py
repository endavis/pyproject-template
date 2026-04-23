"""Tests for tools/doit/base.py helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.doit.base import optional_root_files


def _touch(tmp_path: Path, rel: str) -> Path:
    """Create ``rel`` under ``tmp_path`` and return the absolute path."""
    target = tmp_path / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("", encoding="utf-8")
    return target


class TestOptionalRootFiles:
    """Tests for the ``optional_root_files`` helper."""

    def test_empty_input_returns_empty_string(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """No names -> empty string (safe to concatenate)."""
        monkeypatch.chdir(tmp_path)
        assert optional_root_files() == ""

    def test_missing_file_returns_empty_string(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Absent candidate -> empty string."""
        monkeypatch.chdir(tmp_path)
        assert optional_root_files("bootstrap.py") == ""

    def test_present_file_returns_space_prefixed_name(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Existing file -> ``' bootstrap.py'`` (single leading space)."""
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "bootstrap.py")

        result = optional_root_files("bootstrap.py")
        assert result == " bootstrap.py"
        # Exactly one leading space.
        assert result.startswith(" ")
        assert not result.startswith("  ")

    def test_two_present_files_preserve_argument_order(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Multiple present names -> argument order preserved, single space separators."""
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "a.py")
        _touch(tmp_path, "b.py")

        assert optional_root_files("a.py", "b.py") == " a.py b.py"
        # Swapping the argument order swaps the output order too.
        assert optional_root_files("b.py", "a.py") == " b.py a.py"

    def test_mix_of_present_and_absent_filters_out_missing(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Only the present names survive; missing ones are silently skipped."""
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "a.py")

        assert optional_root_files("a.py", "missing.py") == " a.py"
        assert optional_root_files("missing.py", "a.py") == " a.py"

    def test_single_leading_space_and_separator(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Output uses exactly one leading space and one separator between names."""
        monkeypatch.chdir(tmp_path)
        _touch(tmp_path, "x.py")
        _touch(tmp_path, "y.py")

        result = optional_root_files("x.py", "y.py")
        # No double-spaces anywhere in the output.
        assert "  " not in result
        # Exactly two names separated by exactly one space.
        assert result == " x.py y.py"

    def test_directory_with_matching_name_is_not_treated_as_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A directory named ``bootstrap.py`` must not satisfy the is_file() guard."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "bootstrap.py").mkdir()

        assert optional_root_files("bootstrap.py") == ""

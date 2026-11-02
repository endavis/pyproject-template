"""The configurator points migrating users at the steps it does not do (#1180)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.pyproject_template import configure


def test_print_migration_next_steps_names_cleanup(capsys: pytest.CaptureFixture[str]) -> None:
    configure.print_migration_next_steps()
    out = capsys.readouterr().out
    for needle in (
        "tests/test_cli.py",
        "tests/template/test_properties.py",
        "pytest_add_cli_args_test_selection",
        "tests/conftest.py",
        "_hermetic_path",
        "tests/test_documented_paths.py",
        "docs/template/migration.md",
    ):
        assert needle in out


def test_find_backup_gates_the_pointers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert configure.find_backup_pyproject() is None
    backup = tmp_path / "tmp" / "template-migration-backup-1"
    backup.mkdir(parents=True)
    (backup / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    assert configure.find_backup_pyproject() is not None

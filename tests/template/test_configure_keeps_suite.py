"""configure.py must not delete itself (#1178).

``tools/pyproject_template/__init__.py`` and ``manage.py`` import ``configure``,
so removing it at the end of a run left the rest of the suite broken with an
``ImportError``. ``configure.py`` is shed by cleanup instead.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_run_configure_never_unlinks_configure_py(tmp_path: Path) -> None:
    """run_configure must not try to remove its own source file."""
    from unittest.mock import patch

    from tools.pyproject_template.configure import run_configure

    (tmp_path / "pyproject.toml").write_text('[project]\nname = "test"', encoding="utf-8")
    (tmp_path / "src" / "test_pkg").mkdir(parents=True)
    (tmp_path / "src" / "test_pkg" / "__init__.py").write_text("", encoding="utf-8")

    real_unlink = Path.unlink
    attempted: list[Path] = []

    def _spy(self: Path, *args: object, **kwargs: object) -> None:
        if self.name == "configure.py":
            attempted.append(self)
            return  # never let a regression delete the real file
        real_unlink(self, *args, **kwargs)  # type: ignore[arg-type]

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        with patch.object(Path, "unlink", _spy):
            result = run_configure(
                auto=True,
                yes=True,
                defaults={
                    "project_name": "Test Project",
                    "package_name": "test_pkg",
                    "pypi_name": "test-pkg",
                    "description": "A test project",
                    "author_name": "Test Author",
                    "author_email": "test@example.com",
                    "github_user": "testuser",
                },
            )
    finally:
        os.chdir(old_cwd)

    assert result == 0
    assert attempted == []
    assert (REPO_ROOT / "tools" / "pyproject_template" / "configure.py").is_file()

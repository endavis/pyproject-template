"""Configuring a project resets CHANGELOG.md to an empty ``[Unreleased]`` (#1315).

Release sections copied from the template would survive
``cz changelog --incremental`` into the project's first generated release.
Template-owned: it targets code the wizards shed.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tools.pyproject_template.utils import CHANGELOG_RESET_CONTENT, reset_changelog

REPO_ROOT = Path(__file__).resolve().parents[2]

TEMPLATE_HISTORY = (
    "# Changelog\n\n## [Unreleased]\n\n"
    "## v1.0.0 (2026-01-01)\n\n### Feat\n\n- template feature\n\n"
    "## v0.1.0 (2025-12-01)\n\n- older template change\n"
)


def _assert_reset(root: Path) -> None:
    text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert text == CHANGELOG_RESET_CONTENT
    assert text.rstrip().endswith("## [Unreleased]")
    assert "v1.0.0" not in text
    assert "v0.1.0" not in text


def test_reset_drops_release_sections(tmp_path: Path) -> None:
    """Release sections are replaced by the header and an empty Unreleased."""
    (tmp_path / "CHANGELOG.md").write_text(TEMPLATE_HISTORY, encoding="utf-8")
    reset_changelog(tmp_path)
    _assert_reset(tmp_path)


def test_reset_creates_missing_changelog(tmp_path: Path) -> None:
    """A project without CHANGELOG.md gets one."""
    reset_changelog(tmp_path)
    _assert_reset(tmp_path)


def test_configure_resets_template_history(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """``configure.py`` gives a new project an empty changelog, not the template's."""
    from tools.pyproject_template.configure import run_configure

    for rel in ("pyproject.toml", "mkdocs.yml", "README.template.md", "README.md"):
        shutil.copy(REPO_ROOT / rel, tmp_path / rel)
    (tmp_path / "src" / "package_name").mkdir(parents=True)
    (tmp_path / "src" / "package_name" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(TEMPLATE_HISTORY, encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    defaults = {
        "project_name": "My Tool",
        "package_name": "mytool",
        "pypi_name": "my-tool",
        "description": "A tool",
        "author_name": "Test Author",
        "author_email": "author@real.example",
        "github_user": "example-user",
        "github_repo": "my-tool",
    }
    with patch("tools.pyproject_template.configure.get_git_config", return_value=""):
        assert run_configure(auto=True, yes=True, defaults=defaults) == 0

    _assert_reset(tmp_path)


def test_setup_repo_resets_template_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``setup_repo.py`` gives a new project an empty changelog, not the template's."""
    from tools.pyproject_template.setup_repo import RepositorySetup

    (tmp_path / "CHANGELOG.md").write_text(TEMPLATE_HISTORY, encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    setup = RepositorySetup()
    setup.config = {
        "repo_owner": "testuser",
        "repo_name": "Test Project",
        "package_name": "test_pkg",
        "pypi_name": "test-pkg",
        "description": "A test project",
        "author_name": "Test Author",
        "author_email": "test@example.com",
    }
    with patch("tools.pyproject_template.setup_repo.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        setup.configure_placeholders()

    _assert_reset(tmp_path)

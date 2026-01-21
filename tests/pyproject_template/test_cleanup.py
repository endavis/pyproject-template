"""Tests for cleanup.py template file cleanup functionality."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest


class TestCleanupMode:
    """Tests for CleanupMode enum."""

    def test_cleanup_mode_values(self) -> None:
        """Test that CleanupMode has expected values."""
        from tools.pyproject_template.cleanup import CleanupMode

        assert CleanupMode.SETUP_ONLY.value == "setup"
        assert CleanupMode.ALL.value == "all"


class TestGetFilesToDelete:
    """Tests for get_files_to_delete function."""

    def test_get_files_setup_only(self, tmp_path: Path) -> None:
        """Test get_files_to_delete returns setup files for SETUP_ONLY mode."""
        from tools.pyproject_template.cleanup import CleanupMode, get_files_to_delete

        # Create some setup files
        (tmp_path / "bootstrap.py").touch()
        tools_dir = tmp_path / "tools" / "pyproject_template"
        tools_dir.mkdir(parents=True)
        (tools_dir / "setup_repo.py").touch()
        (tools_dir / "migrate_existing_project.py").touch()
        # This one should NOT be deleted in SETUP_ONLY mode
        (tools_dir / "manage.py").touch()

        files = get_files_to_delete(CleanupMode.SETUP_ONLY, tmp_path)

        file_names = [f.name for f in files]
        assert "bootstrap.py" in file_names
        assert "setup_repo.py" in file_names
        assert "migrate_existing_project.py" in file_names
        assert "manage.py" not in file_names

    def test_get_files_all(self, tmp_path: Path) -> None:
        """Test get_files_to_delete returns all template files for ALL mode."""
        from tools.pyproject_template.cleanup import CleanupMode, get_files_to_delete

        # Create template files
        (tmp_path / "bootstrap.py").touch()
        tools_dir = tmp_path / "tools" / "pyproject_template"
        tools_dir.mkdir(parents=True)
        (tools_dir / "setup_repo.py").touch()
        (tools_dir / "manage.py").touch()
        (tools_dir / "cleanup.py").touch()

        files = get_files_to_delete(CleanupMode.ALL, tmp_path)

        file_names = [f.name for f in files]
        assert "bootstrap.py" in file_names
        assert "setup_repo.py" in file_names
        assert "manage.py" in file_names
        assert "cleanup.py" in file_names

    def test_get_files_nonexistent(self, tmp_path: Path) -> None:
        """Test get_files_to_delete returns empty list when no files exist."""
        from tools.pyproject_template.cleanup import CleanupMode, get_files_to_delete

        files = get_files_to_delete(CleanupMode.SETUP_ONLY, tmp_path)
        assert files == []


class TestGetDirsToDelete:
    """Tests for get_dirs_to_delete function."""

    def test_get_dirs_setup_only(self, tmp_path: Path) -> None:
        """Test get_dirs_to_delete returns empty for SETUP_ONLY mode."""
        from tools.pyproject_template.cleanup import CleanupMode, get_dirs_to_delete

        # Create directories
        (tmp_path / "tools" / "pyproject_template").mkdir(parents=True)

        dirs = get_dirs_to_delete(CleanupMode.SETUP_ONLY, tmp_path)
        assert dirs == []

    def test_get_dirs_all(self, tmp_path: Path) -> None:
        """Test get_dirs_to_delete returns directories for ALL mode."""
        from tools.pyproject_template.cleanup import CleanupMode, get_dirs_to_delete

        # Create directories
        (tmp_path / "tools" / "pyproject_template").mkdir(parents=True)
        (tmp_path / "docs" / "template").mkdir(parents=True)
        (tmp_path / ".config" / "pyproject_template").mkdir(parents=True)

        dirs = get_dirs_to_delete(CleanupMode.ALL, tmp_path)

        dir_names = [d.name for d in dirs]
        assert "pyproject_template" in dir_names


class TestUpdateMkdocsNav:
    """Tests for update_mkdocs_nav function."""

    def test_update_mkdocs_nav_removes_template_section(self, tmp_path: Path) -> None:
        """Test that Template section is removed from mkdocs.yml."""
        from tools.pyproject_template.cleanup import update_mkdocs_nav

        mkdocs_content = """\
nav:
  - Home: index.md
  - Template:
      - Overview: template/index.md
      - Manager: template/manage.md
  - Development:
      - Setup: development/setup.md
"""
        mkdocs_file = tmp_path / "mkdocs.yml"
        mkdocs_file.write_text(mkdocs_content)

        result = update_mkdocs_nav(tmp_path, dry_run=False)

        assert result is True
        new_content = mkdocs_file.read_text()
        assert "Template:" not in new_content
        assert "template/index.md" not in new_content
        assert "Development:" in new_content

    def test_update_mkdocs_nav_no_template_section(self, tmp_path: Path) -> None:
        """Test update_mkdocs_nav when no Template section exists."""
        from tools.pyproject_template.cleanup import update_mkdocs_nav

        mkdocs_content = """\
nav:
  - Home: index.md
  - Development:
      - Setup: development/setup.md
"""
        mkdocs_file = tmp_path / "mkdocs.yml"
        mkdocs_file.write_text(mkdocs_content)

        result = update_mkdocs_nav(tmp_path, dry_run=False)
        assert result is False

    def test_update_mkdocs_nav_dry_run(self, tmp_path: Path) -> None:
        """Test update_mkdocs_nav dry run doesn't modify file."""
        from tools.pyproject_template.cleanup import update_mkdocs_nav

        mkdocs_content = """\
nav:
  - Home: index.md
  - Template:
      - Overview: template/index.md
"""
        mkdocs_file = tmp_path / "mkdocs.yml"
        mkdocs_file.write_text(mkdocs_content)

        result = update_mkdocs_nav(tmp_path, dry_run=True)

        assert result is True
        # Content should be unchanged
        assert mkdocs_file.read_text() == mkdocs_content

    def test_update_mkdocs_nav_no_file(self, tmp_path: Path) -> None:
        """Test update_mkdocs_nav when mkdocs.yml doesn't exist."""
        from tools.pyproject_template.cleanup import update_mkdocs_nav

        result = update_mkdocs_nav(tmp_path, dry_run=False)
        assert result is False


class TestCleanupTemplateFiles:
    """Tests for cleanup_template_files function."""

    def test_cleanup_setup_only(self, tmp_path: Path) -> None:
        """Test cleanup in SETUP_ONLY mode deletes only setup files."""
        from tools.pyproject_template.cleanup import (
            CleanupMode,
            cleanup_template_files,
        )

        # Create files
        (tmp_path / "bootstrap.py").touch()
        tools_dir = tmp_path / "tools" / "pyproject_template"
        tools_dir.mkdir(parents=True)
        (tools_dir / "setup_repo.py").touch()
        (tools_dir / "manage.py").touch()  # Should NOT be deleted

        result = cleanup_template_files(CleanupMode.SETUP_ONLY, tmp_path)

        assert not (tmp_path / "bootstrap.py").exists()
        assert not (tools_dir / "setup_repo.py").exists()
        assert (tools_dir / "manage.py").exists()  # Should still exist
        assert len(result.deleted_files) >= 2
        assert len(result.deleted_dirs) == 0

    def test_cleanup_all(self, tmp_path: Path) -> None:
        """Test cleanup in ALL mode deletes all template files and directories."""
        from tools.pyproject_template.cleanup import (
            CleanupMode,
            cleanup_template_files,
        )

        # Create files and directories
        (tmp_path / "bootstrap.py").touch()
        tools_dir = tmp_path / "tools" / "pyproject_template"
        tools_dir.mkdir(parents=True)
        (tools_dir / "setup_repo.py").touch()
        (tools_dir / "manage.py").touch()
        (tools_dir / "__init__.py").touch()

        # Create mkdocs.yml with Template section
        mkdocs_content = """\
nav:
  - Home: index.md
  - Template:
      - Overview: template/index.md
"""
        (tmp_path / "mkdocs.yml").write_text(mkdocs_content)

        result = cleanup_template_files(CleanupMode.ALL, tmp_path)

        assert not (tmp_path / "bootstrap.py").exists()
        assert not tools_dir.exists()
        assert result.mkdocs_updated is True

    def test_cleanup_dry_run(self, tmp_path: Path) -> None:
        """Test cleanup dry run doesn't delete files."""
        from tools.pyproject_template.cleanup import (
            CleanupMode,
            cleanup_template_files,
        )

        # Create files
        bootstrap = tmp_path / "bootstrap.py"
        bootstrap.touch()

        result = cleanup_template_files(CleanupMode.SETUP_ONLY, tmp_path, dry_run=True)

        # File should still exist
        assert bootstrap.exists()
        # But should be in the list of files that would be deleted
        assert any(f.name == "bootstrap.py" for f in result.deleted_files)

    def test_cleanup_no_files(self, tmp_path: Path) -> None:
        """Test cleanup when no template files exist."""
        from tools.pyproject_template.cleanup import (
            CleanupMode,
            cleanup_template_files,
        )

        result = cleanup_template_files(CleanupMode.SETUP_ONLY, tmp_path)

        assert result.deleted_files == []
        assert result.deleted_dirs == []
        assert result.failed == []


class TestPromptCleanup:
    """Tests for prompt_cleanup function."""

    def test_prompt_cleanup_setup_only(self) -> None:
        """Test prompt_cleanup returns SETUP_ONLY for choice 1."""
        from tools.pyproject_template.cleanup import CleanupMode, prompt_cleanup

        with patch("builtins.input", return_value="1"):
            result = prompt_cleanup()
            assert result == CleanupMode.SETUP_ONLY

    def test_prompt_cleanup_all(self) -> None:
        """Test prompt_cleanup returns ALL for choice 2."""
        from tools.pyproject_template.cleanup import CleanupMode, prompt_cleanup

        with patch("builtins.input", return_value="2"):
            result = prompt_cleanup()
            assert result == CleanupMode.ALL

    def test_prompt_cleanup_keep(self) -> None:
        """Test prompt_cleanup returns None for choice 3."""
        from tools.pyproject_template.cleanup import prompt_cleanup

        with patch("builtins.input", return_value="3"):
            result = prompt_cleanup()
            assert result is None

    def test_prompt_cleanup_invalid_then_valid(self) -> None:
        """Test prompt_cleanup handles invalid input then valid."""
        from tools.pyproject_template.cleanup import CleanupMode, prompt_cleanup

        with patch("builtins.input", side_effect=["invalid", "1"]):
            result = prompt_cleanup()
            assert result == CleanupMode.SETUP_ONLY

    def test_prompt_cleanup_keyboard_interrupt(self) -> None:
        """Test prompt_cleanup handles keyboard interrupt."""
        from tools.pyproject_template.cleanup import prompt_cleanup

        with patch("builtins.input", side_effect=KeyboardInterrupt):
            result = prompt_cleanup()
            assert result is None


class TestMain:
    """Tests for main entry point."""

    def test_main_setup_flag(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main with --setup flag."""
        from tools.pyproject_template.cleanup import main

        monkeypatch.chdir(tmp_path)

        # Create a file to delete
        (tmp_path / "bootstrap.py").touch()

        with patch("sys.argv", ["cleanup.py", "--setup"]):
            result = main()
            assert result == 0

    def test_main_dry_run(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main with --dry-run flag."""
        from tools.pyproject_template.cleanup import main

        monkeypatch.chdir(tmp_path)

        # Create a file
        bootstrap = tmp_path / "bootstrap.py"
        bootstrap.touch()

        with patch("sys.argv", ["cleanup.py", "--setup", "--dry-run"]):
            result = main()
            assert result == 0
            assert bootstrap.exists()  # Should not be deleted

    def test_main_conflicting_flags(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main with conflicting --setup and --all flags."""
        from tools.pyproject_template.cleanup import main

        monkeypatch.chdir(tmp_path)

        with patch("sys.argv", ["cleanup.py", "--setup", "--all"]):
            result = main()
            assert result == 1

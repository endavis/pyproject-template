"""Tests for install.py doit tasks."""

from tools.doit.install import task_install, task_install_dev


class TestTaskInstall:
    """Tests for task_install function."""

    def test_returns_valid_doit_task(self) -> None:
        """Test that task_install returns a valid doit task dict."""
        result = task_install()
        assert isinstance(result, dict)
        assert "actions" in result
        assert "title" in result

    def test_actions_contain_uv_sync(self) -> None:
        """Test that actions include uv sync."""
        result = task_install()
        assert "uv sync" in result["actions"]


class TestTaskInstallDev:
    """Tests for task_install_dev function."""

    def test_returns_valid_doit_task(self) -> None:
        """Test that task_install_dev returns a valid doit task dict."""
        result = task_install_dev()
        assert isinstance(result, dict)
        assert "actions" in result
        assert "title" in result

    def test_actions_contain_uv_sync_all_extras(self) -> None:
        """Test that actions include uv sync with all extras and dev."""
        result = task_install_dev()
        assert "uv sync --all-extras --dev" in result["actions"]

    def test_actions_contain_assume_unchanged(self) -> None:
        """Test that actions include git update-index --assume-unchanged for _version.py."""
        result = task_install_dev()
        expected = "git update-index --assume-unchanged src/package_name/_version.py"
        assert expected in result["actions"]

    def test_uv_sync_runs_before_assume_unchanged(self) -> None:
        """Test that uv sync runs before git update-index."""
        result = task_install_dev()
        actions = result["actions"]
        sync_idx = actions.index("uv sync --all-extras --dev")
        assume_idx = actions.index(
            "git update-index --assume-unchanged src/package_name/_version.py"
        )
        assert sync_idx < assume_idx

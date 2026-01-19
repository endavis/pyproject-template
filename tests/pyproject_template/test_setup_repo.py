"""Tests for setup_repo.py repository setup functionality."""

from __future__ import annotations

from unittest.mock import patch

import pytest


class TestRepositorySetup:
    """Tests for RepositorySetup class."""

    def test_init_creates_empty_config(self) -> None:
        """Test that __init__ creates empty config dict."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()
        assert setup.config == {}
        assert setup.start_dir is not None

    def test_template_full_is_set(self) -> None:
        """Test that TEMPLATE_FULL is set from utils."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        assert RepositorySetup.TEMPLATE_FULL == "endavis/pyproject-template"

    def test_print_banner_outputs_text(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that print_banner outputs the welcome message."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()
        setup.print_banner()

        captured = capsys.readouterr()
        assert "Python Project Template" in captured.out
        assert "Repository Setup" in captured.out

    def test_check_requirements_fails_without_git(self) -> None:
        """Test that check_requirements exits if git is not installed."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        with (
            patch("tools.pyproject_template.setup_repo.command_exists", return_value=False),
            pytest.raises(SystemExit),
        ):
            setup.check_requirements()

    def test_check_requirements_fails_without_gh(self) -> None:
        """Test that check_requirements exits if gh CLI is not installed."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        def mock_command_exists(cmd: str) -> bool:
            return cmd == "git"  # git exists, gh doesn't

        with (
            patch(
                "tools.pyproject_template.setup_repo.command_exists",
                side_effect=mock_command_exists,
            ),
            pytest.raises(SystemExit),
        ):
            setup.check_requirements()

    def test_check_requirements_fails_without_gh_auth(self) -> None:
        """Test that check_requirements exits if gh is not authenticated."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        with (
            patch("tools.pyproject_template.setup_repo.command_exists", return_value=True),
            patch(
                "tools.pyproject_template.setup_repo.GitHubCLI.is_authenticated",
                return_value=False,
            ),
            pytest.raises(SystemExit),
        ):
            setup.check_requirements()

    def test_check_requirements_passes_with_all_requirements(self) -> None:
        """Test that check_requirements passes when all requirements met."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        with (
            patch("tools.pyproject_template.setup_repo.command_exists", return_value=True),
            patch(
                "tools.pyproject_template.setup_repo.GitHubCLI.is_authenticated",
                return_value=True,
            ),
            patch.object(setup, "_check_token_permissions"),
        ):
            # Should not raise
            setup.check_requirements()

    def test_gather_inputs_with_git_config(self) -> None:
        """Test that gather_inputs uses git config values as defaults."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        def mock_get_git_config(key: str, default: str = "") -> str:
            configs = {
                "user.name": "Test User",
                "user.email": "test@example.com",
            }
            return configs.get(key, default)

        def mock_prompt(_question: str, default: str = "") -> str:
            # Return defaults for all prompts
            return default if default else "test_value"

        # Track calls to prompt_confirm to return appropriate values
        confirm_calls = []

        def mock_prompt_confirm(_question: str, default: bool = False) -> bool:
            confirm_calls.append(True)
            if len(confirm_calls) == 1:
                return False  # "Create in organization?" -> No
            if len(confirm_calls) == 2:
                return True  # "Make repository public?" -> Yes
            return True  # "Proceed with these settings?" -> Yes

        mock_api_response = {"login": "testuser"}

        with (
            patch(
                "tools.pyproject_template.setup_repo.get_git_config",
                side_effect=mock_get_git_config,
            ),
            patch(
                "tools.pyproject_template.setup_repo.prompt",
                side_effect=mock_prompt,
            ),
            patch(
                "tools.pyproject_template.setup_repo.prompt_confirm",
                side_effect=mock_prompt_confirm,
            ),
            patch(
                "tools.pyproject_template.setup_repo.GitHubCLI.api",
                return_value=mock_api_response,
            ),
        ):
            setup.gather_inputs()

            assert setup.config["author_name"] == "Test User"
            assert setup.config["author_email"] == "test@example.com"
            assert setup.config["repo_owner"] == "testuser"

"""Tests for setup_repo.py repository setup functionality."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

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


class TestCleanupTemplateSuite:
    """Tests for RepositorySetup.cleanup_template_suite().

    These tests cover the auto-removal of the template management suite
    from spawned consumer projects (issue #465). They mock
    ``cleanup_template_files`` and ``subprocess.run`` so no real filesystem
    or git effects occur.
    """

    def _make_cleanup_result(
        self,
        *,
        deleted_files: list[Path] | None = None,
        deleted_dirs: list[Path] | None = None,
    ) -> MagicMock:
        """Build a CleanupResult-compatible mock.

        ``cleanup_template_files`` returns a ``CleanupResult`` (NamedTuple).
        Only ``deleted_files`` and ``deleted_dirs`` are consulted by
        ``cleanup_template_suite``; supplying a MagicMock with those
        attributes is sufficient.
        """
        result = MagicMock()
        result.deleted_files = deleted_files or []
        result.deleted_dirs = deleted_dirs or []
        result.failed = []
        result.mkdocs_updated = False
        return result

    def test_cleanup_invokes_cleanup_template_files_with_all_mode(self) -> None:
        """cleanup_template_suite() passes CleanupMode.ALL to cleanup_template_files."""
        from tools.pyproject_template.setup_repo import CleanupMode, RepositorySetup

        setup = RepositorySetup()

        # Simulate at least one deleted file so the git path is exercised.
        fake_result = self._make_cleanup_result(deleted_files=[Path("bootstrap.py")])

        with (
            patch(
                "tools.pyproject_template.setup_repo.cleanup_template_files",
                return_value=fake_result,
            ) as mock_cleanup,
            patch("tools.pyproject_template.setup_repo.subprocess.run"),
        ):
            setup.cleanup_template_suite()

        # Assert it was called exactly once with CleanupMode.ALL.
        mock_cleanup.assert_called_once()
        _, kwargs = mock_cleanup.call_args
        args = mock_cleanup.call_args.args
        assert args[0] == CleanupMode.ALL
        # root is passed as a keyword argument.
        assert "root" in kwargs

    def test_cleanup_uses_current_working_directory_as_root(self) -> None:
        """cleanup_template_suite() passes Path.cwd() as the root."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        fake_result = self._make_cleanup_result(deleted_files=[Path("bootstrap.py")])

        with (
            patch(
                "tools.pyproject_template.setup_repo.cleanup_template_files",
                return_value=fake_result,
            ) as mock_cleanup,
            patch("tools.pyproject_template.setup_repo.subprocess.run"),
        ):
            setup.cleanup_template_suite()

        _, kwargs = mock_cleanup.call_args
        assert kwargs["root"] == Path.cwd()

    def test_cleanup_commits_and_pushes_after_successful_cleanup(self) -> None:
        """After deletions, cleanup_template_suite() stages, commits, and pushes."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        fake_result = self._make_cleanup_result(
            deleted_files=[Path("bootstrap.py")],
            deleted_dirs=[Path("tools/pyproject_template")],
        )

        with (
            patch(
                "tools.pyproject_template.setup_repo.cleanup_template_files",
                return_value=fake_result,
            ),
            patch("tools.pyproject_template.setup_repo.subprocess.run") as mock_run,
        ):
            setup.cleanup_template_suite()

        # Collect the first positional argument (the command list) for each call.
        commands = [call.args[0] for call in mock_run.call_args_list]

        # Verify add -A was called.
        assert any(cmd[:2] == ["git", "add"] and "-A" in cmd for cmd in commands), (
            f"Expected 'git add -A' in commands, got: {commands}"
        )

        # Verify commit --no-verify was called with the expected subject.
        commit_calls = [
            cmd for cmd in commands if len(cmd) >= 3 and cmd[0] == "git" and cmd[1] == "commit"
        ]
        assert commit_calls, f"Expected 'git commit' call, got: {commands}"
        commit_cmd = commit_calls[0]
        assert "--no-verify" in commit_cmd
        # The commit message is the argument after -m.
        assert "-m" in commit_cmd
        msg_index = commit_cmd.index("-m") + 1
        assert "chore: remove template management suite" in commit_cmd[msg_index]

        # Verify push was called.
        assert ["git", "push"] in commands, f"Expected 'git push' in commands, got: {commands}"

    def test_cleanup_skips_commit_when_nothing_was_deleted(self) -> None:
        """cleanup_template_suite() does not commit when no files were deleted.

        Guards against an empty git commit when a consumer re-runs setup on a
        project that has already been cleaned.
        """
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        # No deletions performed.
        fake_result = self._make_cleanup_result()

        with (
            patch(
                "tools.pyproject_template.setup_repo.cleanup_template_files",
                return_value=fake_result,
            ),
            patch("tools.pyproject_template.setup_repo.subprocess.run") as mock_run,
        ):
            setup.cleanup_template_suite()

        # No git subprocess calls should have been made.
        assert mock_run.call_count == 0

    def test_cleanup_logs_warning_and_does_not_raise_on_failure(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """cleanup_template_suite() swallows exceptions rather than re-raising.

        A cleanup failure must not block the user from using their freshly
        spawned repository, so the method must log a warning and return
        normally.
        """
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        with (
            patch(
                "tools.pyproject_template.setup_repo.cleanup_template_files",
                side_effect=OSError("permission denied"),
            ),
            patch("tools.pyproject_template.setup_repo.subprocess.run"),
        ):
            # Must not raise.
            setup.cleanup_template_suite()

        captured = capsys.readouterr()
        combined = captured.out + captured.err
        # Warning text should surface the exception.
        assert "Template suite cleanup failed" in combined
        assert "permission denied" in combined

    def test_cleanup_logs_warning_when_git_commit_fails(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """cleanup_template_suite() handles subprocess failures defensively."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        fake_result = self._make_cleanup_result(deleted_files=[Path("bootstrap.py")])

        def mock_run(cmd: list[str], **_kwargs: object) -> object:
            if len(cmd) >= 2 and cmd[0] == "git" and cmd[1] == "commit":
                raise subprocess.CalledProcessError(1, cmd, b"", b"hook rejected")
            return MagicMock(returncode=0)

        with (
            patch(
                "tools.pyproject_template.setup_repo.cleanup_template_files",
                return_value=fake_result,
            ),
            patch("tools.pyproject_template.setup_repo.subprocess.run", side_effect=mock_run),
        ):
            # Must not raise.
            setup.cleanup_template_suite()

        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "Template suite cleanup failed" in combined


class TestRunOrder:
    """Tests for RepositorySetup.run() ordering.

    The critical ordering requirement introduced by issue #465 is that
    ``cleanup_template_suite`` must run AFTER the development environment
    is set up (so ``doit check`` still has the template tests available)
    and BEFORE the manual steps are printed (so the printed summary
    reflects the cleaned tree).
    """

    def test_run_invokes_cleanup_between_env_setup_and_manual_steps(self) -> None:
        """run() calls cleanup_template_suite() between env-setup and manual-steps."""
        from tools.pyproject_template.setup_repo import RepositorySetup

        setup = RepositorySetup()

        # Track the order that the orchestration methods are called.
        call_order: list[str] = []

        def make_tracker(name: str) -> object:
            def _tracked(*_args: object, **_kwargs: object) -> None:
                call_order.append(name)

            return _tracked

        # Patch every orchestration step on the instance. We use
        # ``patch.object`` so each MagicMock records on the ``setup``
        # instance without polluting other tests.
        with (
            patch.object(setup, "print_banner", side_effect=make_tracker("print_banner")),
            patch.object(
                setup, "check_requirements", side_effect=make_tracker("check_requirements")
            ),
            patch.object(setup, "gather_inputs", side_effect=make_tracker("gather_inputs")),
            patch.object(
                setup,
                "create_github_repository",
                side_effect=make_tracker("create_github_repository"),
            ),
            patch.object(
                setup,
                "configure_repository_settings",
                side_effect=make_tracker("configure_repository_settings"),
            ),
            patch.object(
                setup,
                "configure_branch_protection",
                side_effect=make_tracker("configure_branch_protection"),
            ),
            patch.object(setup, "replicate_labels", side_effect=make_tracker("replicate_labels")),
            patch.object(
                setup, "enable_github_pages", side_effect=make_tracker("enable_github_pages")
            ),
            patch.object(setup, "clone_repository", side_effect=make_tracker("clone_repository")),
            patch.object(
                setup,
                "configure_placeholders",
                side_effect=make_tracker("configure_placeholders"),
            ),
            patch.object(
                setup,
                "setup_development_environment",
                side_effect=make_tracker("setup_development_environment"),
            ),
            patch.object(
                setup,
                "cleanup_template_suite",
                side_effect=make_tracker("cleanup_template_suite"),
            ),
            patch.object(
                setup, "print_manual_steps", side_effect=make_tracker("print_manual_steps")
            ),
        ):
            setup.run()

        # cleanup_template_suite must appear after setup_development_environment
        # and before print_manual_steps.
        assert "setup_development_environment" in call_order
        assert "cleanup_template_suite" in call_order
        assert "print_manual_steps" in call_order

        env_idx = call_order.index("setup_development_environment")
        cleanup_idx = call_order.index("cleanup_template_suite")
        manual_idx = call_order.index("print_manual_steps")

        assert env_idx < cleanup_idx < manual_idx, (
            f"Expected setup_development_environment < cleanup_template_suite < "
            f"print_manual_steps, got order: {call_order}"
        )

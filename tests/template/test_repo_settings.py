"""Tests for repo_settings.py repository settings functionality."""

from __future__ import annotations

import sys
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess
from unittest.mock import patch

import pytest


class TestCheckAdminAccess:
    """Tests for check_admin_access (#1034)."""

    def test_true_when_token_has_admin(self) -> None:
        from tools.pyproject_template.repo_settings import check_admin_access

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            return_value={"permissions": {"admin": True}},
        ):
            assert check_admin_access("user/repo") is True

    def test_false_when_token_lacks_admin(self, capsys: pytest.CaptureFixture[str]) -> None:
        from tools.pyproject_template.repo_settings import check_admin_access

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            return_value={"permissions": {"admin": False}},
        ):
            assert check_admin_access("user/repo") is False

        err = capsys.readouterr().err
        assert "Administration" in err

    def test_false_when_permissions_missing(self) -> None:
        from tools.pyproject_template.repo_settings import check_admin_access

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            return_value={},
        ):
            assert check_admin_access("user/repo") is False

    def test_false_on_api_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        from tools.pyproject_template.repo_settings import check_admin_access

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=CalledProcessError(1, "gh", stderr="HTTP 404: Not Found"),
        ):
            assert check_admin_access("user/repo") is False

        assert "Could not read repository settings" in capsys.readouterr().err


class TestDisableCodeqlDefaultSetup:
    """Tests for disable_codeql_default_setup (#1034)."""

    def test_configured_sends_patch(self) -> None:
        from tools.pyproject_template.repo_settings import disable_codeql_default_setup

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=[{"state": "configured"}, None],
        ) as mock_api:
            assert disable_codeql_default_setup("user/repo") is True

        assert mock_api.call_count == 2
        patch_call = mock_api.call_args_list[1]
        assert patch_call.kwargs.get("method") == "PATCH"
        assert patch_call.kwargs.get("data") == {"state": "not-configured"}

    def test_not_configured_sends_no_patch(self) -> None:
        from tools.pyproject_template.repo_settings import disable_codeql_default_setup

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            return_value={"state": "not-configured"},
        ) as mock_api:
            assert disable_codeql_default_setup("user/repo") is True

        assert mock_api.call_count == 1

    def test_get_403_warns_with_all_causes_and_no_security_events_mention(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        from tools.pyproject_template.repo_settings import disable_codeql_default_setup

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=CalledProcessError(1, "gh", stderr="HTTP 403: Forbidden"),
        ):
            assert disable_codeql_default_setup("user/repo") is False

        out = capsys.readouterr().out
        assert "Administration permission" in out
        assert "Advanced Security" in out
        assert "archived" in out
        assert "security_events" not in out

    def test_patch_403_warns(self, capsys: pytest.CaptureFixture[str]) -> None:
        from tools.pyproject_template.repo_settings import disable_codeql_default_setup

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=[
                {"state": "configured"},
                CalledProcessError(1, "gh", stderr="HTTP 403: Forbidden"),
            ],
        ):
            assert disable_codeql_default_setup("user/repo") is False

        out = capsys.readouterr().out
        assert "Administration permission" in out
        assert "Advanced Security" in out
        assert "archived" in out
        assert "security_events" not in out

    def test_non_403_get_failure_warns_without_the_403_causes(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        from tools.pyproject_template.repo_settings import disable_codeql_default_setup

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=CalledProcessError(1, "gh", stderr="HTTP 500: Internal Server Error"),
        ):
            assert disable_codeql_default_setup("user/repo") is False

        out = capsys.readouterr().out
        assert "Failed to check CodeQL default setup" in out


class TestConfigureRepositorySettings:
    """Tests for configure_repository_settings function."""

    def test_configure_repository_settings_success(self) -> None:
        """Test successful repository settings configuration."""
        from tools.pyproject_template.repo_settings import configure_repository_settings

        mock_template_settings = {
            "description": "Template description",
            "has_issues": True,
            "has_wiki": False,
            "allow_squash_merge": True,
            # Read-only fields that should be filtered
            "id": 123,
            "node_id": "abc",
            "full_name": "old/name",
        }

        mock_owner_info = {"type": "User"}

        with (
            patch(
                "tools.pyproject_template.repo_settings.GitHubCLI.api",
                side_effect=[mock_template_settings, mock_owner_info, None],
            ) as mock_api,
        ):
            result = configure_repository_settings(
                repo_full="user/repo",
                description="New description",
                visibility="public",
            )

            assert result is True
            # Verify API was called correctly
            assert mock_api.call_count == 3

    def test_configure_repository_settings_failure(self) -> None:
        """Test repository settings configuration handles failure."""
        from subprocess import CalledProcessError

        from tools.pyproject_template.repo_settings import configure_repository_settings

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=CalledProcessError(1, "gh", stderr="Error"),
        ):
            result = configure_repository_settings(
                repo_full="user/repo",
                description="Description",
            )

            assert result is False


class TestConfigureBranchProtection:
    """Tests for configure_branch_protection function."""

    def test_configure_branch_protection_creates_new_ruleset(self) -> None:
        """Test creating a new ruleset when none exists."""
        from tools.pyproject_template.repo_settings import configure_branch_protection

        mock_template_rulesets = [{"id": 1, "name": "main-protection"}]
        mock_existing_rulesets: list[dict[str, object]] = []  # No existing rulesets
        mock_full_ruleset = {
            "id": 1,
            "name": "main-protection",
            "target": "branch",
            "enforcement": "active",
            "bypass_actors": [],
            "conditions": {},
            "rules": [],
        }

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=[
                mock_template_rulesets,  # GET template rulesets
                mock_existing_rulesets,  # GET existing rulesets in target repo
                mock_full_ruleset,  # GET full ruleset details
                None,  # POST new ruleset
            ],
        ) as mock_api:
            result = configure_branch_protection(repo_full="user/repo")
            assert result is True
            # Verify POST was used (4th call)
            assert mock_api.call_count == 4
            last_call = mock_api.call_args_list[3]
            assert last_call.kwargs.get("method") == "POST"
            assert "rulesets" in last_call.args[0]
            assert "rulesets/" not in last_call.args[0]  # No ID in URL for POST

    def test_configure_branch_protection_updates_existing_ruleset(self) -> None:
        """Test updating an existing ruleset instead of creating a duplicate."""
        from tools.pyproject_template.repo_settings import configure_branch_protection

        mock_template_rulesets = [{"id": 1, "name": "main-protection"}]
        mock_existing_rulesets = [{"id": 99, "name": "main-protection"}]  # Already exists
        mock_full_ruleset = {
            "id": 1,
            "name": "main-protection",
            "target": "branch",
            "enforcement": "active",
            "bypass_actors": [],
            "conditions": {},
            "rules": [],
        }

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=[
                mock_template_rulesets,  # GET template rulesets
                mock_existing_rulesets,  # GET existing rulesets in target repo
                mock_full_ruleset,  # GET full ruleset details
                None,  # PUT existing ruleset
            ],
        ) as mock_api:
            result = configure_branch_protection(repo_full="user/repo")
            assert result is True
            # Verify PUT was used with correct ID (4th call)
            assert mock_api.call_count == 4
            last_call = mock_api.call_args_list[3]
            assert last_call.kwargs.get("method") == "PUT"
            assert "rulesets/99" in last_call.args[0]  # Uses existing ID

    def test_configure_branch_protection_no_rulesets(self) -> None:
        """Test branch protection when template has no rulesets."""
        from tools.pyproject_template.repo_settings import configure_branch_protection

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            return_value=[],
        ):
            result = configure_branch_protection(repo_full="user/repo")
            assert result is True  # No rulesets is not a failure

    def test_configure_branch_protection_matches_differently_named_ruleset_by_conditions(
        self,
    ) -> None:
        """A differently-named ruleset covering ~DEFAULT_BRANCH is updated, not duplicated (#1034).

        Reported in #1034: bastproxy's ruleset is named 'main', the template's is 'main branch',
        both targeting the same branch via ~DEFAULT_BRANCH. Matching by name alone would create
        a duplicate; this must PUT the existing one instead, keeping its own name.
        """
        from tools.pyproject_template.repo_settings import configure_branch_protection

        mock_template_rulesets = [{"id": 1, "name": "main branch"}]
        mock_existing_rulesets = [{"id": 99, "name": "main", "target": "branch"}]
        mock_full_template_ruleset = {
            "id": 1,
            "name": "main branch",
            "target": "branch",
            "enforcement": "active",
            "bypass_actors": [],
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "rules": [],
        }
        mock_full_existing_ruleset = {
            "id": 99,
            "name": "main",
            "target": "branch",
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        }

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=[
                mock_template_rulesets,  # GET template rulesets
                mock_existing_rulesets,  # GET existing rulesets in target repo
                mock_full_template_ruleset,  # GET full template ruleset details
                mock_full_existing_ruleset,  # GET full existing ruleset details (match check)
                None,  # PUT existing ruleset
            ],
        ) as mock_api:
            result = configure_branch_protection(repo_full="user/repo")
            assert result is True
            assert mock_api.call_count == 5
            put_call = mock_api.call_args_list[4]
            assert put_call.kwargs.get("method") == "PUT"
            assert "rulesets/99" in put_call.args[0]
            # The existing ruleset's own name is kept, not renamed to the template's.
            assert put_call.kwargs["data"]["name"] == "main"

    def test_configure_branch_protection_does_not_match_unrelated_ruleset(self) -> None:
        """A ruleset with a different name/target and no ~DEFAULT_BRANCH condition isn't matched."""
        from tools.pyproject_template.repo_settings import configure_branch_protection

        mock_template_rulesets = [{"id": 1, "name": "main branch"}]
        mock_existing_rulesets = [{"id": 99, "name": "tag-protection", "target": "tag"}]
        mock_full_template_ruleset = {
            "id": 1,
            "name": "main branch",
            "target": "branch",
            "enforcement": "active",
            "bypass_actors": [],
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "rules": [],
        }

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=[
                mock_template_rulesets,
                mock_existing_rulesets,
                mock_full_template_ruleset,
                None,  # POST new ruleset (no full fetch of 'tag-protection': target mismatch)
            ],
        ) as mock_api:
            result = configure_branch_protection(repo_full="user/repo")
            assert result is True
            assert mock_api.call_count == 4
            post_call = mock_api.call_args_list[3]
            assert post_call.kwargs.get("method") == "POST"
            assert "rulesets/" not in post_call.args[0]


class TestReplicateLabels:
    """Tests for replicate_labels function."""

    def test_replicate_labels_success(self) -> None:
        """Test successful label replication."""
        from tools.pyproject_template.repo_settings import replicate_labels

        mock_labels = [
            {"name": "bug", "color": "d73a4a", "description": "Bug report"},
            {"name": "enhancement", "color": "a2eeef", "description": "New feature"},
        ]

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=[mock_labels, None, None],
        ):
            result = replicate_labels(repo_full="user/repo")
            assert result is True

    def test_replicate_labels_empty(self) -> None:
        """Test label replication when template has no labels."""
        from tools.pyproject_template.repo_settings import replicate_labels

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            return_value=[],
        ):
            result = replicate_labels(repo_full="user/repo")
            assert result is False


class TestSyncLabelsFromFile:
    """Tests for sync_labels_from_file, the create+update replacement for replicate_labels."""

    @pytest.fixture
    def labels_file(self, tmp_path: Path) -> str:
        path = tmp_path / "labels.yml"
        path.write_text("- name: bug\n  color: d73a4a\n", encoding="utf-8")
        return str(path)

    def test_runs_doit_labels_sync_against_the_target_repo(self, labels_file: str) -> None:
        from tools.pyproject_template.repo_settings import sync_labels_from_file

        with (
            patch("tools.pyproject_template.repo_settings.shutil.which", return_value="/bin/uv"),
            patch(
                "tools.pyproject_template.repo_settings.subprocess.run",
                return_value=CompletedProcess([], 0),
            ) as mock_run,
        ):
            assert sync_labels_from_file("user/repo", file=labels_file) is True

        args, kwargs = mock_run.call_args
        assert args[0] == ["uv", "run", "doit", "labels_sync", f"--file={labels_file}"]
        assert kwargs["env"]["GH_REPO"] == "user/repo"

    def test_returns_false_when_labels_sync_fails(self, labels_file: str) -> None:
        from tools.pyproject_template.repo_settings import sync_labels_from_file

        with (
            patch("tools.pyproject_template.repo_settings.shutil.which", return_value="/bin/uv"),
            patch(
                "tools.pyproject_template.repo_settings.subprocess.run",
                return_value=CompletedProcess([], 1),
            ),
            patch("tools.pyproject_template.repo_settings.replicate_labels") as mock_replicate,
        ):
            assert sync_labels_from_file("user/repo", file=labels_file) is False
        mock_replicate.assert_not_called()

    def test_falls_back_when_uv_is_missing(self, labels_file: str) -> None:
        from tools.pyproject_template.repo_settings import sync_labels_from_file

        with (
            patch("tools.pyproject_template.repo_settings.shutil.which", return_value=None),
            patch("tools.pyproject_template.repo_settings.subprocess.run") as mock_run,
            patch(
                "tools.pyproject_template.repo_settings.replicate_labels", return_value=True
            ) as mock_replicate,
        ):
            assert sync_labels_from_file("user/repo", file=labels_file) is True
        mock_run.assert_not_called()
        mock_replicate.assert_called_once_with("user/repo")

    def test_falls_back_when_labels_file_is_missing(self, tmp_path: Path) -> None:
        """A bootstrap-only checkout has no .github/labels.yml."""
        from tools.pyproject_template.repo_settings import sync_labels_from_file

        with (
            patch("tools.pyproject_template.repo_settings.shutil.which", return_value="/bin/uv"),
            patch("tools.pyproject_template.repo_settings.subprocess.run") as mock_run,
            patch(
                "tools.pyproject_template.repo_settings.replicate_labels", return_value=False
            ) as mock_replicate,
        ):
            assert sync_labels_from_file("user/repo", file=str(tmp_path / "none.yml")) is False
        mock_run.assert_not_called()
        mock_replicate.assert_called_once_with("user/repo")

    def test_module_imports_no_third_party_packages(self) -> None:
        """manage.py runs under a bare interpreter, so this module must stay stdlib-only."""
        import ast

        from tools.pyproject_template import repo_settings

        source = Path(repo_settings.__file__).read_text(encoding="utf-8")
        roots = {
            (node.module or "").split(".")[0]
            if isinstance(node, ast.ImportFrom)
            else alias.name.split(".")[0]
            for node in ast.walk(ast.parse(source))
            if isinstance(node, (ast.Import, ast.ImportFrom)) and getattr(node, "level", 0) == 0
            for alias in node.names
        }
        assert roots <= set(sys.stdlib_module_names) | {"utils"}


class TestEnableGithubPages:
    """Tests for enable_github_pages function."""

    def test_enable_github_pages_success(self) -> None:
        """Test successful GitHub Pages enablement."""
        from tools.pyproject_template.repo_settings import enable_github_pages

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            return_value=None,
        ):
            result = enable_github_pages(repo_full="user/repo")
            assert result is True

    def test_enable_github_pages_no_branch(self) -> None:
        """Test GitHub Pages when gh-pages branch doesn't exist."""
        from subprocess import CalledProcessError

        from tools.pyproject_template.repo_settings import enable_github_pages

        with patch(
            "tools.pyproject_template.repo_settings.GitHubCLI.api",
            side_effect=CalledProcessError(1, "gh"),
        ):
            result = enable_github_pages(repo_full="user/repo")
            assert result is False


class TestUpdateAllRepoSettings:
    """Tests for update_all_repo_settings convenience function.

    CodeQL default setup is checked by :func:`disable_codeql_default_setup`, not
    skipped: CodeQL scanning itself still runs from the committed
    ``.github/workflows/codeql.yml`` workflow file the template generator copies
    into every new repository, but a repo that synced the template after already
    using GitHub's own CodeQL default setup needs that switched off too (#431, #1034).
    """

    def test_update_all_repo_settings_success(self) -> None:
        """Test that update_all_repo_settings calls all configuration functions, in order."""
        from tools.pyproject_template.repo_settings import update_all_repo_settings

        with (
            patch(
                "tools.pyproject_template.repo_settings.check_admin_access",
                return_value=True,
            ) as mock_admin,
            patch(
                "tools.pyproject_template.repo_settings.configure_repository_settings",
                return_value=True,
            ) as mock_repo,
            patch(
                "tools.pyproject_template.repo_settings.configure_branch_protection",
                return_value=True,
            ) as mock_branch,
            patch(
                "tools.pyproject_template.repo_settings.disable_codeql_default_setup",
                return_value=True,
            ) as mock_codeql,
            patch(
                "tools.pyproject_template.repo_settings.sync_labels_from_file",
                return_value=True,
            ) as mock_labels,
            patch(
                "tools.pyproject_template.repo_settings.enable_github_pages",
                return_value=True,
            ) as mock_pages,
        ):
            result = update_all_repo_settings(
                repo_full="user/repo",
                description="Description",
            )

            assert result is True
            mock_admin.assert_called_once()
            mock_repo.assert_called_once()
            mock_branch.assert_called_once()
            mock_codeql.assert_called_once()
            mock_labels.assert_called_once()
            mock_pages.assert_called_once()

    def test_update_all_repo_settings_partial_failure(self) -> None:
        """Test that update_all_repo_settings returns False if any step fails."""
        from tools.pyproject_template.repo_settings import update_all_repo_settings

        with (
            patch(
                "tools.pyproject_template.repo_settings.check_admin_access",
                return_value=True,
            ),
            patch(
                "tools.pyproject_template.repo_settings.configure_repository_settings",
                return_value=True,
            ),
            patch(
                "tools.pyproject_template.repo_settings.configure_branch_protection",
                return_value=False,  # This one fails
            ),
            patch(
                "tools.pyproject_template.repo_settings.disable_codeql_default_setup",
                return_value=True,
            ),
            patch(
                "tools.pyproject_template.repo_settings.sync_labels_from_file",
                return_value=True,
            ),
            patch(
                "tools.pyproject_template.repo_settings.enable_github_pages",
                return_value=True,
            ),
        ):
            result = update_all_repo_settings(
                repo_full="user/repo",
                description="Description",
            )

            assert result is False

    def test_update_all_repo_settings_stops_when_admin_check_fails(self) -> None:
        """A failed admin check returns False before any other step runs (#1034)."""
        from tools.pyproject_template.repo_settings import update_all_repo_settings

        with (
            patch(
                "tools.pyproject_template.repo_settings.check_admin_access",
                return_value=False,
            ) as mock_admin,
            patch(
                "tools.pyproject_template.repo_settings.configure_repository_settings",
            ) as mock_repo,
            patch(
                "tools.pyproject_template.repo_settings.configure_branch_protection",
            ) as mock_branch,
            patch(
                "tools.pyproject_template.repo_settings.disable_codeql_default_setup",
            ) as mock_codeql,
            patch(
                "tools.pyproject_template.repo_settings.sync_labels_from_file",
            ) as mock_labels,
            patch(
                "tools.pyproject_template.repo_settings.enable_github_pages",
            ) as mock_pages,
        ):
            result = update_all_repo_settings(
                repo_full="user/repo",
                description="Description",
            )

            assert result is False
            mock_admin.assert_called_once()
            mock_repo.assert_not_called()
            mock_branch.assert_not_called()
            mock_codeql.assert_not_called()
            mock_labels.assert_not_called()
            mock_pages.assert_not_called()

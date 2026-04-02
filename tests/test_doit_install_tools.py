"""Tests for install_tools.py reusable tool installation framework."""

import json
import subprocess  # nosec B404 - needed for CompletedProcess in tests
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tools.doit.install_tools import (
    create_install_task,
    download_github_release_binary,
    get_install_dir,
    get_latest_github_release,
    install_tool,
)


class TestGetLatestGithubRelease:
    """Tests for get_latest_github_release function."""

    @patch("tools.doit.install_tools.urllib.request.urlopen")
    @patch("tools.doit.install_tools.urllib.request.Request")
    def test_returns_version_without_v_prefix(
        self, mock_request_cls: MagicMock, mock_urlopen: MagicMock
    ) -> None:
        """Test that leading 'v' is stripped from tag_name."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"tag_name": "v2.34.0"}).encode()
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = get_latest_github_release("direnv/direnv")

        assert result == "2.34.0"

    @patch("tools.doit.install_tools.urllib.request.urlopen")
    @patch("tools.doit.install_tools.urllib.request.Request")
    def test_returns_version_without_v_when_no_prefix(
        self, mock_request_cls: MagicMock, mock_urlopen: MagicMock
    ) -> None:
        """Test version returned as-is when no 'v' prefix."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"tag_name": "2.34.0"}).encode()
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        result = get_latest_github_release("owner/repo")

        assert result == "2.34.0"

    @patch.dict("os.environ", {"GITHUB_TOKEN": "test-token"})
    @patch("tools.doit.install_tools.urllib.request.urlopen")
    @patch("tools.doit.install_tools.urllib.request.Request")
    def test_adds_auth_header_when_token_present(
        self, mock_request_cls: MagicMock, mock_urlopen: MagicMock
    ) -> None:
        """Test that GITHUB_TOKEN is used for Authorization header."""
        mock_request_instance = MagicMock()
        mock_request_cls.return_value = mock_request_instance

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"tag_name": "v1.0.0"}).encode()
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        get_latest_github_release("owner/repo")

        mock_request_instance.add_header.assert_called_once_with(
            "Authorization", "token test-token"
        )

    @patch.dict("os.environ", {}, clear=True)
    @patch("tools.doit.install_tools.urllib.request.urlopen")
    @patch("tools.doit.install_tools.urllib.request.Request")
    def test_no_auth_header_when_no_token(
        self, mock_request_cls: MagicMock, mock_urlopen: MagicMock
    ) -> None:
        """Test that no Authorization header is added without GITHUB_TOKEN."""
        mock_request_instance = MagicMock()
        mock_request_cls.return_value = mock_request_instance

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"tag_name": "v1.0.0"}).encode()
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        get_latest_github_release("owner/repo")

        mock_request_instance.add_header.assert_not_called()

    @patch("tools.doit.install_tools.urllib.request.urlopen")
    @patch("tools.doit.install_tools.urllib.request.Request")
    def test_constructs_correct_api_url(
        self, mock_request_cls: MagicMock, mock_urlopen: MagicMock
    ) -> None:
        """Test that the correct GitHub API URL is constructed."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"tag_name": "v1.0.0"}).encode()
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        get_latest_github_release("owner/repo")

        mock_request_cls.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/releases/latest"
        )


class TestGetInstallDir:
    """Tests for get_install_dir function."""

    @patch("tools.doit.install_tools.Path.home")
    def test_returns_local_bin_path(self, mock_home: MagicMock, tmp_path: Path) -> None:
        """Test that ~/.local/bin path is returned."""
        mock_home.return_value = tmp_path
        result = get_install_dir()
        assert result == tmp_path / ".local" / "bin"

    @patch("tools.doit.install_tools.Path.home")
    def test_creates_directory_if_not_exists(self, mock_home: MagicMock, tmp_path: Path) -> None:
        """Test that the directory is created when it does not exist."""
        mock_home.return_value = tmp_path
        expected = tmp_path / ".local" / "bin"
        assert not expected.exists()

        get_install_dir()

        assert expected.exists()

    @patch("tools.doit.install_tools.Path.home")
    def test_no_error_if_directory_exists(self, mock_home: MagicMock, tmp_path: Path) -> None:
        """Test that no error occurs when directory already exists."""
        mock_home.return_value = tmp_path
        expected = tmp_path / ".local" / "bin"
        expected.mkdir(parents=True)

        result = get_install_dir()

        assert result == expected


class TestDownloadGithubReleaseBinary:
    """Tests for download_github_release_binary function."""

    @patch("tools.doit.install_tools.get_install_dir")
    @patch("tools.doit.install_tools.urllib.request.urlretrieve")
    def test_downloads_to_correct_path(
        self,
        mock_urlretrieve: MagicMock,
        mock_get_install_dir: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test that binary is downloaded to the correct destination."""
        mock_get_install_dir.return_value = tmp_path
        dest = tmp_path / "mytool"
        dest.touch()

        result = download_github_release_binary(
            repo="owner/repo",
            version="1.2.3",
            asset_pattern="mytool.linux-amd64",
            dest_name="mytool",
        )

        assert result == dest
        mock_urlretrieve.assert_called_once_with(
            "https://github.com/owner/repo/releases/download/v1.2.3/mytool.linux-amd64",
            dest,
        )

    @patch("tools.doit.install_tools.get_install_dir")
    @patch("tools.doit.install_tools.urllib.request.urlretrieve")
    def test_version_placeholder_in_asset_pattern(
        self,
        mock_urlretrieve: MagicMock,
        mock_get_install_dir: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test that {version} placeholder is substituted in asset_pattern."""
        mock_get_install_dir.return_value = tmp_path
        dest = tmp_path / "tool"
        dest.touch()

        download_github_release_binary(
            repo="owner/repo",
            version="3.0.0",
            asset_pattern="tool-v{version}-linux-amd64",
            dest_name="tool",
        )

        mock_urlretrieve.assert_called_once_with(
            "https://github.com/owner/repo/releases/download/v3.0.0/tool-v3.0.0-linux-amd64",
            dest,
        )

    @patch("tools.doit.install_tools.get_install_dir")
    @patch("tools.doit.install_tools.urllib.request.urlretrieve")
    def test_sets_executable_permissions(
        self,
        mock_urlretrieve: MagicMock,
        mock_get_install_dir: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test that the binary is made executable after download."""
        mock_get_install_dir.return_value = tmp_path
        dest = tmp_path / "mytool"
        dest.touch(mode=0o644)

        download_github_release_binary(
            repo="owner/repo",
            version="1.0.0",
            asset_pattern="mytool.linux-amd64",
            dest_name="mytool",
        )

        assert dest.stat().st_mode & 0o755 == 0o755


class TestInstallTool:
    """Tests for install_tool function."""

    @patch("tools.doit.install_tools.subprocess.run")
    @patch("tools.doit.install_tools.shutil.which", return_value="/usr/bin/mytool")
    def test_skips_install_when_tool_exists(
        self, mock_which: MagicMock, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that install is skipped when tool is already on PATH."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["mytool", "--version"], returncode=0, stdout="1.0.0\n", stderr=""
        )

        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        captured = capsys.readouterr()
        assert "already installed" in captured.out
        assert "1.0.0" in captured.out

    @patch("tools.doit.install_tools.subprocess.run")
    @patch("tools.doit.install_tools.shutil.which", return_value="/usr/bin/mytool")
    def test_uses_custom_version_cmd(self, mock_which: MagicMock, mock_run: MagicMock) -> None:
        """Test that custom version_cmd is used for version check."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["mytool", "version"], returncode=0, stdout="2.0.0\n", stderr=""
        )

        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
            version_cmd=["mytool", "version"],
        )

        mock_run.assert_called_once_with(
            ["mytool", "version"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("tools.doit.install_tools.subprocess.run")
    @patch("tools.doit.install_tools.shutil.which", return_value="/usr/bin/mytool")
    def test_falls_back_to_stderr_for_version(
        self, mock_which: MagicMock, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that stderr is used when stdout is empty for version output."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["mytool", "--version"], returncode=0, stdout="", stderr="3.0.0\n"
        )

        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        captured = capsys.readouterr()
        assert "3.0.0" in captured.out

    @patch("tools.doit.install_tools.download_github_release_binary")
    @patch("tools.doit.install_tools.get_latest_github_release", return_value="2.0.0")
    @patch("tools.doit.install_tools.platform.system", return_value="Linux")
    @patch("tools.doit.install_tools.shutil.which", return_value=None)
    def test_installs_on_linux(
        self,
        mock_which: MagicMock,
        mock_system: MagicMock,
        mock_get_release: MagicMock,
        mock_download: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that tool is downloaded on Linux when not installed."""
        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        mock_download.assert_called_once_with(
            repo="owner/repo",
            version="2.0.0",
            asset_pattern="mytool.linux-amd64",
            dest_name="mytool",
        )
        captured = capsys.readouterr()
        assert "mytool installed" in captured.out

    @patch("tools.doit.install_tools.subprocess.run")
    @patch("tools.doit.install_tools.get_latest_github_release", return_value="2.0.0")
    @patch("tools.doit.install_tools.platform.system", return_value="Darwin")
    @patch("tools.doit.install_tools.shutil.which", return_value=None)
    def test_installs_via_brew_on_darwin(
        self,
        mock_which: MagicMock,
        mock_system: MagicMock,
        mock_get_release: MagicMock,
        mock_run: MagicMock,
    ) -> None:
        """Test that brew is used on macOS."""
        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        mock_run.assert_called_once_with(["brew", "install", "mytool"], check=True)

    @patch("tools.doit.install_tools.get_latest_github_release", return_value="1.0.0")
    @patch("tools.doit.install_tools.platform.system", return_value="Windows")
    @patch("tools.doit.install_tools.shutil.which", return_value=None)
    def test_exits_on_unsupported_os(
        self,
        mock_which: MagicMock,
        mock_system: MagicMock,
        mock_get_release: MagicMock,
    ) -> None:
        """Test that sys.exit is called for unsupported OS."""
        with pytest.raises(SystemExit):
            install_tool(
                name="mytool",
                repo="owner/repo",
                asset_patterns={"linux": "mytool.linux-amd64"},
            )

    @patch("tools.doit.install_tools.download_github_release_binary")
    @patch("tools.doit.install_tools.get_latest_github_release", return_value="1.0.0")
    @patch("tools.doit.install_tools.platform.system", return_value="Linux")
    @patch("tools.doit.install_tools.shutil.which", return_value=None)
    def test_prints_post_install_message(
        self,
        mock_which: MagicMock,
        mock_system: MagicMock,
        mock_get_release: MagicMock,
        mock_download: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that post_install_message is printed after install."""
        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
            post_install_message="Run 'mytool init' to get started.",
        )

        captured = capsys.readouterr()
        assert "Run 'mytool init' to get started." in captured.out

    @patch("tools.doit.install_tools.download_github_release_binary")
    @patch("tools.doit.install_tools.get_latest_github_release", return_value="1.0.0")
    @patch("tools.doit.install_tools.platform.system", return_value="Linux")
    @patch("tools.doit.install_tools.shutil.which", return_value=None)
    def test_no_post_install_message_when_none(
        self,
        mock_which: MagicMock,
        mock_system: MagicMock,
        mock_get_release: MagicMock,
        mock_download: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test that no extra message is printed when post_install_message is None."""
        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        captured = capsys.readouterr()
        assert captured.out.strip().endswith("mytool installed.")

    @patch("tools.doit.install_tools.subprocess.run")
    @patch("tools.doit.install_tools.shutil.which", return_value="/usr/bin/mytool")
    def test_default_version_cmd(self, mock_which: MagicMock, mock_run: MagicMock) -> None:
        """Test that default version_cmd is [name, '--version']."""
        mock_run.return_value = subprocess.CompletedProcess(
            args=["mytool", "--version"], returncode=0, stdout="1.0.0\n", stderr=""
        )

        install_tool(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        mock_run.assert_called_once_with(
            ["mytool", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )


class TestCreateInstallTask:
    """Tests for create_install_task function."""

    def test_returns_valid_doit_task(self) -> None:
        """Test that a valid doit task dict is returned."""
        result = create_install_task(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        assert isinstance(result, dict)
        assert "actions" in result
        assert "title" in result
        assert len(result["actions"]) == 1
        assert callable(result["actions"][0])

    @patch("tools.doit.install_tools.install_tool")
    def test_action_calls_install_tool(self, mock_install: MagicMock) -> None:
        """Test that the task action calls install_tool with correct args."""
        result = create_install_task(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
            version_cmd=["mytool", "version"],
            post_install_message="Done!",
        )

        # Execute the action
        result["actions"][0]()

        mock_install.assert_called_once_with(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
            version_cmd=["mytool", "version"],
            post_install_message="Done!",
        )

    @patch("tools.doit.install_tools.install_tool")
    def test_action_passes_none_defaults(self, mock_install: MagicMock) -> None:
        """Test that None defaults are passed through to install_tool."""
        result = create_install_task(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
        )

        result["actions"][0]()

        mock_install.assert_called_once_with(
            name="mytool",
            repo="owner/repo",
            asset_patterns={"linux": "mytool.linux-amd64"},
            version_cmd=None,
            post_install_message=None,
        )

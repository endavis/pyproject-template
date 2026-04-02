"""Reusable framework for installing tools from GitHub releases."""

import json
import os
import platform
import shutil
import subprocess  # nosec B404 - subprocess is required for version checks
import sys
import urllib.request
from pathlib import Path
from typing import Any

from doit.tools import title_with_actions


def get_latest_github_release(repo: str) -> str:
    """Get the latest release version for a GitHub repository.

    Queries the GitHub API for the latest release tag. Supports
    authenticated requests via GITHUB_TOKEN environment variable.

    Args:
        repo: GitHub repository in "owner/name" format (e.g. "direnv/direnv").

    Returns:
        Version string with leading 'v' stripped (e.g. "2.34.0").
    """
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(url)

    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        request.add_header("Authorization", f"token {github_token}")

    with urllib.request.urlopen(request) as response:  # nosec B310 - URL is hardcoded GitHub API
        data = json.loads(response.read().decode())
        tag_name: str = data["tag_name"]
        return tag_name.lstrip("v")


def get_install_dir() -> Path:
    """Get the standard installation directory for user-local binaries.

    Returns:
        Path to ~/.local/bin, created if it does not exist.
    """
    install_dir = Path.home() / ".local" / "bin"
    install_dir.mkdir(parents=True, exist_ok=True)
    return install_dir


def download_github_release_binary(
    repo: str, version: str, asset_pattern: str, dest_name: str
) -> Path:
    """Download a binary asset from a GitHub release.

    Constructs the download URL from the repo, version, and asset pattern,
    downloads the file to the user-local bin directory, and makes it
    executable.

    Args:
        repo: GitHub repository in "owner/name" format.
        version: Release version (without leading 'v').
        asset_pattern: Filename pattern with {version} placeholder
            (e.g. "tool.linux-amd64" or "tool-v{version}-linux-amd64").
        dest_name: Name of the installed binary (e.g. "tool").

    Returns:
        Path to the downloaded and installed binary.
    """
    asset_name = asset_pattern.format(version=version)
    url = f"https://github.com/{repo}/releases/download/v{version}/{asset_name}"
    install_dir = get_install_dir()
    dest_path = install_dir / dest_name

    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest_path)  # nosec B310 - downloading from constructed GitHub release URL
    dest_path.chmod(0o755)  # nosec B103 - rwxr-xr-x is required for executable binary

    return dest_path


def install_tool(
    name: str,
    repo: str,
    asset_patterns: dict[str, str],
    version_cmd: list[str] | None = None,
    post_install_message: str | None = None,
) -> None:
    """Install a tool from GitHub releases if not already present.

    Checks if the tool is already on PATH. If so, prints its version
    and returns. Otherwise, downloads the latest release for the current
    platform and installs it.

    Args:
        name: Tool name used for PATH lookup and as the binary dest name.
        repo: GitHub repository in "owner/name" format.
        asset_patterns: Mapping of platform.system().lower() values
            (e.g. "linux", "darwin") to asset filename patterns.
            Patterns may include a {version} placeholder.
        version_cmd: Command list to run for checking installed version
            (e.g. ["tool", "--version"]). Defaults to [name, "--version"].
        post_install_message: Optional message printed after installation.
    """
    if version_cmd is None:
        version_cmd = [name, "--version"]

    if shutil.which(name):
        result = subprocess.run(
            version_cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        version_output = result.stdout.strip() or result.stderr.strip()
        print(f"\u2713 {name} already installed: {version_output}")
        return

    print(f"Installing {name}...")
    version = get_latest_github_release(repo)
    print(f"Latest version: {version}")

    system = platform.system().lower()
    if system == "darwin":
        subprocess.run(["brew", "install", name], check=True)
    elif system in asset_patterns:
        download_github_release_binary(
            repo=repo,
            version=version,
            asset_pattern=asset_patterns[system],
            dest_name=name,
        )
    else:
        print(f"Unsupported OS for {name}: {system}")
        sys.exit(1)

    print(f"\u2713 {name} installed.")
    if post_install_message:
        print(post_install_message)


def create_install_task(
    name: str,
    repo: str,
    asset_patterns: dict[str, str],
    version_cmd: list[str] | None = None,
    post_install_message: str | None = None,
) -> dict[str, Any]:
    """Create a doit task dict for installing a tool from GitHub releases.

    This is a factory function that returns a doit-compatible task
    dictionary. The task's action calls install_tool with the provided
    parameters.

    Args:
        name: Tool name used for PATH lookup and as the binary dest name.
        repo: GitHub repository in "owner/name" format.
        asset_patterns: Mapping of platform names to asset filename patterns.
        version_cmd: Command list for version check. Defaults to [name, "--version"].
        post_install_message: Optional message printed after installation.

    Returns:
        A doit task dictionary with actions and title.
    """

    def _action() -> None:
        install_tool(
            name=name,
            repo=repo,
            asset_patterns=asset_patterns,
            version_cmd=version_cmd,
            post_install_message=post_install_message,
        )

    return {
        "actions": [_action],
        "title": title_with_actions,
    }

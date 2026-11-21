"""configure must keep the repo name, PyPI name and package name apart (#1268).

A project whose GitHub repo is ``my-tool`` and whose import package is ``mytool``
needs ``[project].name`` to be the PyPI name and every GitHub URL to use the repo
name, not the package name. The maintainer address from settings must also reach
``.github/SECURITY.md``.
"""

from __future__ import annotations

import shutil
import sys
import tomllib
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COPIED = (
    "pyproject.toml",
    "mkdocs.yml",
    "README.template.md",
    "README.md",
    ".github/SECURITY.md",
)


def _defaults(**extra: str) -> dict[str, str]:
    base = {
        "project_name": "My Tool",
        "package_name": "mytool",
        "pypi_name": "my-tool",
        "description": "A tool",
        "author_name": "Test Author",
        "author_email": "author@real.example",
        "github_user": "example-user",
        "github_repo": "my-tool",
    }
    base.update(extra)
    return base


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for rel in COPIED:
        dest = tmp_path / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / rel, dest)
    (tmp_path / "src" / "package_name").mkdir(parents=True)
    (tmp_path / "src" / "package_name" / "__init__.py").write_text("", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _run(defaults: dict[str, str], remote: str = "") -> int:
    from tools.pyproject_template.configure import run_configure

    with patch("tools.pyproject_template.configure.get_git_config", return_value=remote):
        return run_configure(auto=True, yes=True, defaults=defaults)


def test_project_name_is_pypi_name_and_urls_use_repo(project: Path) -> None:
    assert _run(_defaults()) == 0

    text = (project / "pyproject.toml").read_text(encoding="utf-8")
    data = tomllib.loads(text)
    assert data["project"]["name"] == "my-tool"
    assert data["project"]["urls"]["Repository"] == "https://github.com/example-user/my-tool"
    assert data["project"]["scripts"] == {"my-tool": "mytool.cli:main"}
    assert "example-user/mytool" not in text

    mkdocs = (project / "mkdocs.yml").read_text(encoding="utf-8")
    assert "repo_name: example-user/my-tool" in mkdocs
    assert "repo_url: https://github.com/example-user/my-tool" in mkdocs
    assert "site_url: https://example-user.github.io/my-tool" in mkdocs
    assert "/mytool" not in mkdocs

    readme = (project / "README.md").read_text(encoding="utf-8")
    assert "example-user/mytool" not in readme


def test_repo_falls_back_to_git_remote(project: Path) -> None:
    defaults = _defaults()
    del defaults["github_repo"]
    assert _run(defaults, remote="https://github.com/example-user/remote-name") == 0
    mkdocs = (project / "mkdocs.yml").read_text(encoding="utf-8")
    assert "repo_name: example-user/remote-name" in mkdocs


def test_repo_falls_back_to_pypi_name(project: Path) -> None:
    defaults = _defaults()
    del defaults["github_repo"]
    assert _run(defaults) == 0
    mkdocs = (project / "mkdocs.yml").read_text(encoding="utf-8")
    assert "repo_name: example-user/my-tool" in mkdocs


def test_action_configure_carries_author_email_to_security_md(project: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "tools" / "pyproject_template"))
    from tools.pyproject_template import manage

    settings = type(
        "S",
        (),
        {
            "project_name": "My Tool",
            "package_name": "mytool",
            "pypi_name": "my-tool",
            "description": "A tool",
            "author_name": "Test Author",
            "author_email": "author@real.example",
            "github_user": "example-user",
            "github_repo": "my-tool",
            "maintainer_name": "",
            "maintainer_email": "",
        },
    )()
    manager = type("M", (), {"settings": settings})()

    with patch("tools.pyproject_template.configure.get_git_config", return_value=""):
        assert manage.action_configure(manager, dry_run=False, yes=True) == 0

    security = (project / ".github" / "SECURITY.md").read_text(encoding="utf-8")
    assert "author@real.example" in security
    assert "your.email@example.com" not in security
    assert "security@example.com" not in security


def test_readme_clone_directory_is_repo_name(project: Path) -> None:
    """``cd`` after the clone names the repo directory, not the package (#1268)."""
    assert _run(_defaults()) == 0
    readme = (project / "README.md").read_text(encoding="utf-8")
    assert "cd my-tool\n" in readme
    assert "cd mytool\n" not in readme
    assert "__REPO_NAME__" not in readme


def test_setup_repo_builds_repo_identity_from_repo_name(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The bootstrap path uses the repo name for URLs, slugs and the clone dir."""
    from unittest.mock import MagicMock

    from tools.pyproject_template.setup_repo import RepositorySetup

    setup = RepositorySetup()
    setup.config = {
        "repo_owner": "example-user",
        "repo_name": "my-tool",
        "package_name": "mytool",
        "pypi_name": "my-tool",
        "description": "A tool",
        "author_name": "Test Author",
        "author_email": "author@real.example",
    }
    with patch("tools.pyproject_template.setup_repo.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        setup.configure_placeholders()

    mkdocs = (project / "mkdocs.yml").read_text(encoding="utf-8")
    assert "repo_name: example-user/my-tool" in mkdocs
    assert "/mytool" not in mkdocs
    pyproject = (project / "pyproject.toml").read_text(encoding="utf-8")
    assert "example-user/mytool" not in pyproject

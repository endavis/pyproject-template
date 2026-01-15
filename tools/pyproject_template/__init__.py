"""
pyproject-template tools package.

Provides utilities for managing Python projects based on pyproject-template.
"""

from tools.pyproject_template.check_template_updates import (
    compare_files,
    download_template,
    get_latest_release,
    run_check_updates,
)
from tools.pyproject_template.configure import (
    load_defaults,
    run_configure,
)
from tools.pyproject_template.migrate_existing_project import (
    run_migrate,
)
from tools.pyproject_template.settings import (
    ProjectContext,
    ProjectSettings,
    SettingsManager,
    TemplateState,
    get_template_commits_since,
    get_template_latest_commit,
)
from tools.pyproject_template.utils import (
    Colors,
    GitHubCLI,
    Logger,
    download_and_extract_archive,
    prompt,
    prompt_confirm,
    update_file,
    validate_email,
    validate_package_name,
    validate_pypi_name,
)

__all__ = [
    # Settings
    "ProjectContext",
    "ProjectSettings",
    "SettingsManager",
    "TemplateState",
    "get_template_commits_since",
    "get_template_latest_commit",
    # Configure
    "load_defaults",
    "run_configure",
    # Check updates
    "compare_files",
    "download_template",
    "get_latest_release",
    "run_check_updates",
    # Migrate
    "run_migrate",
    # Utils
    "Colors",
    "GitHubCLI",
    "Logger",
    "download_and_extract_archive",
    "prompt",
    "prompt_confirm",
    "update_file",
    "validate_email",
    "validate_package_name",
    "validate_pypi_name",
]

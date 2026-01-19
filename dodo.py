"""Doit task runner configuration.

This file imports all task definitions from the tools/tasks/ modules.
Each module contains related tasks grouped by functionality.
"""

# Configuration
from tools.tasks.base import DOIT_CONFIG  # noqa: F401

# Build and publish tasks
from tools.tasks.build import (  # noqa: F401
    task_build,
    task_publish,
)

# Documentation tasks
from tools.tasks.docs import (  # noqa: F401
    task_docs_build,
    task_docs_deploy,
    task_docs_serve,
    task_spell_check,
)

# Git tasks
from tools.tasks.git import (  # noqa: F401
    task_bump,
    task_changelog,
    task_commit,
    task_pre_commit_install,
    task_pre_commit_run,
)

# GitHub issue and PR tasks
from tools.tasks.github import (  # noqa: F401
    task_issue,
    task_pr,
)

# Installation tasks
from tools.tasks.install import (  # noqa: F401
    task_install,
    task_install_dev,
    task_install_direnv,
)

# Maintenance tasks
from tools.tasks.maintenance import (  # noqa: F401
    task_cleanup,
    task_completions,
    task_completions_install,
    task_fmt_pyproject,
    task_update_deps,
)

# Code quality tasks
from tools.tasks.quality import (  # noqa: F401
    task_check,
    task_complexity,
    task_deadcode,
    task_format,
    task_format_check,
    task_lint,
    task_maintainability,
    task_type_check,
)

# Release tasks
from tools.tasks.release import (  # noqa: F401
    task_release,
    task_release_dev,
    task_release_pr,
    task_release_tag,
)

# Security tasks
from tools.tasks.security import (  # noqa: F401
    task_audit,
    task_licenses,
    task_security,
)

# Testing tasks
from tools.tasks.testing import (  # noqa: F401
    task_coverage,
    task_test,
)

# All Documents

Complete index of all documentation, organized by audience and as a full alphabetical list.

> These lists are auto-generated from document frontmatter.
> Run `python tools/generate_doc_toc.py` to update.

## By Audience

### For Users
<!-- BEGIN:audience=users -->
- [__PROJECT_NAME__ Documentation](index.md) - Welcome and overview of the project
- [API Development Guide](examples/api.md) - Building REST APIs with FastAPI - patterns, testing, and best practices
- [API Reference](reference/api.md) - Complete API documentation for __PROJECT_NAME__
- [CLI Guide](usage/cli.md) - The application's user-facing command-line interface and how to extend it
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [Examples](examples/README.md) - Example scripts demonstrating how to use the package
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Keeping Up to Date](template/updates.md) - Stay in sync with improvements to the pyproject-template
- [Migration Guide](template/migration.md) - Migrate existing Python projects to use this template
- [New Project Setup](template/new-project.md) - Create a new Python project from this template
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [Template Management](template/manage.md) - Unified interface for creating projects, checking updates, and syncing
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Usage Guide](usage/basics.md) - Package usage and development workflows
- [Using This Template](template/index.md) - Overview of using pyproject-template for your Python projects
<!-- END:audience=users -->

### For Contributors
<!-- BEGIN:audience=contributors -->
- [__PROJECT_NAME__ Documentation](index.md) - Welcome and overview of the project
- [Add a Feature: End-to-End Walkthrough](examples/add-a-feature.md) - Step-by-step example of adding a module, CLI subcommand, tests, and docs to the project
- [ADR-9001: Use uv for package management](decisions/9001-use-uv-for-package-management.md) - Use uv for dependency management, virtual environments and package installation
- [ADR-9002: Use doit for task automation](decisions/9002-use-doit-for-task-automation.md) - Use doit as the task runner for testing, linting, building and other routine operations
- [ADR-9003: Use ruff for linting and formatting](decisions/9003-use-ruff-for-linting-and-formatting.md) - Use ruff as the one tool for linting and formatting, in place of flake8, black and isort
- [ADR-9004: Auto-discover doit tasks from modules](decisions/9004-auto-discover-doit-tasks.md) - Import every task_* function under tools/doit/ automatically instead of listing each one in dodo.py
- [ADR-9005: AI agent command restrictions via hooks](decisions/9005-ai-agent-command-restrictions.md) - Block dangerous commands such as --force, --admin and --no-verify at the tool level, through each AI agent's hooks
- [ADR-9006: Merge-gate workflow requiring ready-to-merge label](decisions/9006-merge-gate-workflow.md) - A merge-gate workflow, enforced by branch protection, keeps a PR from merging until it carries the ready-to-merge label
- [ADR-9007: Use mypy for static type checking](decisions/9007-use-mypy-for-type-checking.md) - Use mypy in strict mode, run by doit check, the pre-commit hooks and CI
- [ADR-9008: PR-based development workflow](decisions/9008-pr-based-development-workflow.md) - Every change goes Issue → Branch → Commit → PR → Merge, and nothing is committed to main directly
- [ADR-9009: Use pre-commit hooks for quality gates](decisions/9009-use-pre-commit-hooks-for-quality-gates.md) - Run quality and safety checks through the pre-commit framework before every commit
- [ADR-9010: Use conventional commits format](decisions/9010-use-conventional-commits-format.md) - Write every commit message, merge commits included, in the Conventional Commits format
- [ADR-9011: Use pytest for testing](decisions/9011-use-pytest-for-testing.md) - Use pytest, with pytest-xdist for parallel runs and pytest-cov for coverage
- [ADR-9012: Use mkdocs with Material theme for documentation](decisions/9012-use-mkdocs-with-material-theme-for-documentation.md) - Build the documentation with MkDocs and the Material theme, and host it on GitHub Pages
- [ADR-9013: Python version support policy with bookend CI strategy](decisions/9013-python-version-support-policy.md) - Support the last three Python versions, testing the oldest and newest on every PR and older ones on demand
- [ADR-9014: Use click for application CLI](decisions/9014-use-click-for-application-cli.md) - Build the package's user-facing command-line interface with click, registered as a console script
- [ADR-9015: install_tools framework: archive extraction and custom URLs](decisions/9015-install-tools-framework-archive-extraction-and-custom-urls.md) - Extend the install_tools framework with archive extraction and custom download URLs, keeping it backward compatible
- [ADR-9016: Unify ADR directories under docs/decisions](decisions/9016-unify-adr-directories.md) - Keep every ADR in docs/decisions/, numbering template decisions 9XXX and project decisions from 0001
- [ADR-9017: Template tooling and its tests are template-owned](decisions/9017-template-tooling-and-its-tests-are-template-owned.md) - A test under tests/template/ is template-owned when its target does not survive configuration
- [ADR-9018: AGENTS.md carries only shared, always-on instructions](decisions/9018-agentsmd-carries-only-shared-always-on-instructions.md) - Content belongs in AGENTS.md only when it holds for every agent and must be in effect at all times
- [ADR-9019: The dangerous-command hook is a guardrail, not a security boundary](decisions/9019-the-dangerous-command-hook-is-a-guardrail-not-a-security-boundary.md) - The dangerous-command hook guards against a non-adversarial agent, not a determined one
- [ADR-9020: A template version is a commit SHA](decisions/9020-a-template-version-is-a-commit-sha.md) - A template version is a commit SHA, not a release tag or a branch name
- [ADR-9021: A PR may target the unmerged branch it builds on](decisions/9021-a-pr-may-target-the-unmerged-branch-it-builds-on.md) - A PR may target the unmerged branch it builds on, but it merges only into main
- [ADR-9022: Worktrees live in worktrees/, each with its own environment](decisions/9022-worktrees-live-in-worktrees-each-with-its-own-environment.md) - A worktree lives in worktrees/<branch>, is created with doit worktree, and has its own environment
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Copilot, Codex, and Antigravity for this project
- [AI Agent Token-Efficiency Add-Ons](development/ai/token-efficiency-add-ons.md) - Opt-in catalogue of external tools for reducing token usage in Claude Code sessions
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Development Guide](examples/api.md) - Building REST APIs with FastAPI - patterns, testing, and best practices
- [API Reference](reference/api.md) - Complete API documentation for __PROJECT_NAME__
- [Architecture Decision Records](decisions/README.md) - What an ADR is, the two numbering series, the ADR format, and how to create one with doit adr
- [Auto-Checkpoint and Session-Restore Hooks](development/ai/auto-checkpoint-hook.md) - PreCompact and SessionStart hooks that preserve context across autocompact events
- [CI/CD Testing Guide](development/ci-cd-testing.md) - GitHub Actions pipelines for testing, linting, and coverage
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [CLI Guide](usage/cli.md) - The application's user-facing command-line interface and how to extend it
- [Cross-Agent Delegation Matrix](development/ai/cross-agent-delegation.md) - Commands that let any supported AI CLI hand a plan, implement or review task to any other
- [Dependabot Auto-merge](development/dependabot-automerge.md) - How the dependabot auto-merge workflow evaluates, enables, and skips PRs
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [install_tools Framework](development/install-tools-framework.md) - Reusable framework for installing developer tools from GitHub releases or other URLs into ~/.local/bin
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [LSP Tool and Diagnostic Noise](development/ai/lsp-tool.md) - What the LSP tool gives an AI agent, why pyright diagnostics arrive stale, and the two opt-outs agents can flip on themselves
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) - What each tool is for, who uses it, and where runtime code ends and dev tooling begins
<!-- END:audience=contributors -->

### For AI Agents
<!-- BEGIN:audience=ai-agents -->
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Copilot, Codex, and Antigravity for this project
- [AI Agent Sync Checklist](template/ai-sync-checklist.md) - Step-by-step checklist for AI agents synchronizing downstream projects with pyproject-template
- [AI Agent Token-Efficiency Add-Ons](development/ai/token-efficiency-add-ons.md) - Opt-in catalogue of external tools for reducing token usage in Claude Code sessions
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [Architecture Decision Records](decisions/README.md) - What an ADR is, the two numbering series, the ADR format, and how to create one with doit adr
- [Auto-Checkpoint and Session-Restore Hooks](development/ai/auto-checkpoint-hook.md) - PreCompact and SessionStart hooks that preserve context across autocompact events
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [Cross-Agent Delegation Matrix](development/ai/cross-agent-delegation.md) - Commands that let any supported AI CLI hand a plan, implement or review task to any other
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [LSP Tool and Diagnostic Noise](development/ai/lsp-tool.md) - What the LSP tool gives an AI agent, why pyright diagnostics arrive stale, and the two opt-outs agents can flip on themselves
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
- [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) - What each tool is for, who uses it, and where runtime code ends and dev tooling begins
<!-- END:audience=ai-agents -->

## Complete Index
<!-- BEGIN:all -->
- [__PROJECT_NAME__ Documentation](index.md) - Welcome and overview of the project
- [Add a Feature: End-to-End Walkthrough](examples/add-a-feature.md) - Step-by-step example of adding a module, CLI subcommand, tests, and docs to the project
- [ADR-9001: Use uv for package management](decisions/9001-use-uv-for-package-management.md) - Use uv for dependency management, virtual environments and package installation
- [ADR-9002: Use doit for task automation](decisions/9002-use-doit-for-task-automation.md) - Use doit as the task runner for testing, linting, building and other routine operations
- [ADR-9003: Use ruff for linting and formatting](decisions/9003-use-ruff-for-linting-and-formatting.md) - Use ruff as the one tool for linting and formatting, in place of flake8, black and isort
- [ADR-9004: Auto-discover doit tasks from modules](decisions/9004-auto-discover-doit-tasks.md) - Import every task_* function under tools/doit/ automatically instead of listing each one in dodo.py
- [ADR-9005: AI agent command restrictions via hooks](decisions/9005-ai-agent-command-restrictions.md) - Block dangerous commands such as --force, --admin and --no-verify at the tool level, through each AI agent's hooks
- [ADR-9006: Merge-gate workflow requiring ready-to-merge label](decisions/9006-merge-gate-workflow.md) - A merge-gate workflow, enforced by branch protection, keeps a PR from merging until it carries the ready-to-merge label
- [ADR-9007: Use mypy for static type checking](decisions/9007-use-mypy-for-type-checking.md) - Use mypy in strict mode, run by doit check, the pre-commit hooks and CI
- [ADR-9008: PR-based development workflow](decisions/9008-pr-based-development-workflow.md) - Every change goes Issue → Branch → Commit → PR → Merge, and nothing is committed to main directly
- [ADR-9009: Use pre-commit hooks for quality gates](decisions/9009-use-pre-commit-hooks-for-quality-gates.md) - Run quality and safety checks through the pre-commit framework before every commit
- [ADR-9010: Use conventional commits format](decisions/9010-use-conventional-commits-format.md) - Write every commit message, merge commits included, in the Conventional Commits format
- [ADR-9011: Use pytest for testing](decisions/9011-use-pytest-for-testing.md) - Use pytest, with pytest-xdist for parallel runs and pytest-cov for coverage
- [ADR-9012: Use mkdocs with Material theme for documentation](decisions/9012-use-mkdocs-with-material-theme-for-documentation.md) - Build the documentation with MkDocs and the Material theme, and host it on GitHub Pages
- [ADR-9013: Python version support policy with bookend CI strategy](decisions/9013-python-version-support-policy.md) - Support the last three Python versions, testing the oldest and newest on every PR and older ones on demand
- [ADR-9014: Use click for application CLI](decisions/9014-use-click-for-application-cli.md) - Build the package's user-facing command-line interface with click, registered as a console script
- [ADR-9015: install_tools framework: archive extraction and custom URLs](decisions/9015-install-tools-framework-archive-extraction-and-custom-urls.md) - Extend the install_tools framework with archive extraction and custom download URLs, keeping it backward compatible
- [ADR-9016: Unify ADR directories under docs/decisions](decisions/9016-unify-adr-directories.md) - Keep every ADR in docs/decisions/, numbering template decisions 9XXX and project decisions from 0001
- [ADR-9017: Template tooling and its tests are template-owned](decisions/9017-template-tooling-and-its-tests-are-template-owned.md) - A test under tests/template/ is template-owned when its target does not survive configuration
- [ADR-9018: AGENTS.md carries only shared, always-on instructions](decisions/9018-agentsmd-carries-only-shared-always-on-instructions.md) - Content belongs in AGENTS.md only when it holds for every agent and must be in effect at all times
- [ADR-9019: The dangerous-command hook is a guardrail, not a security boundary](decisions/9019-the-dangerous-command-hook-is-a-guardrail-not-a-security-boundary.md) - The dangerous-command hook guards against a non-adversarial agent, not a determined one
- [ADR-9020: A template version is a commit SHA](decisions/9020-a-template-version-is-a-commit-sha.md) - A template version is a commit SHA, not a release tag or a branch name
- [ADR-9021: A PR may target the unmerged branch it builds on](decisions/9021-a-pr-may-target-the-unmerged-branch-it-builds-on.md) - A PR may target the unmerged branch it builds on, but it merges only into main
- [ADR-9022: Worktrees live in worktrees/, each with its own environment](decisions/9022-worktrees-live-in-worktrees-each-with-its-own-environment.md) - A worktree lives in worktrees/<branch>, is created with doit worktree, and has its own environment
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Copilot, Codex, and Antigravity for this project
- [AI Agent Sync Checklist](template/ai-sync-checklist.md) - Step-by-step checklist for AI agents synchronizing downstream projects with pyproject-template
- [AI Agent Token-Efficiency Add-Ons](development/ai/token-efficiency-add-ons.md) - Opt-in catalogue of external tools for reducing token usage in Claude Code sessions
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Development Guide](examples/api.md) - Building REST APIs with FastAPI - patterns, testing, and best practices
- [API Reference](reference/api.md) - Complete API documentation for __PROJECT_NAME__
- [Architecture Decision Records](decisions/README.md) - What an ADR is, the two numbering series, the ADR format, and how to create one with doit adr
- [Auto-Checkpoint and Session-Restore Hooks](development/ai/auto-checkpoint-hook.md) - PreCompact and SessionStart hooks that preserve context across autocompact events
- [CI/CD Testing Guide](development/ci-cd-testing.md) - GitHub Actions pipelines for testing, linting, and coverage
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [CLI Guide](usage/cli.md) - The application's user-facing command-line interface and how to extend it
- [Consumer Notes](template/consumer-notes.md) - Breaking changes and behaviour changes that arrive when a project syncs from the template.
- [Cross-Agent Delegation Matrix](development/ai/cross-agent-delegation.md) - Commands that let any supported AI CLI hand a plan, implement or review task to any other
- [Dependabot Auto-merge](development/dependabot-automerge.md) - How the dependabot auto-merge workflow evaluates, enables, and skips PRs
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [Examples](examples/README.md) - Example scripts demonstrating how to use the package
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [install_tools Framework](development/install-tools-framework.md) - Reusable framework for installing developer tools from GitHub releases or other URLs into ~/.local/bin
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Keeping Up to Date](template/updates.md) - Stay in sync with improvements to the pyproject-template
- [LSP Tool and Diagnostic Noise](development/ai/lsp-tool.md) - What the LSP tool gives an AI agent, why pyright diagnostics arrive stale, and the two opt-outs agents can flip on themselves
- [Migration Guide](template/migration.md) - Migrate existing Python projects to use this template
- [New Project Setup](template/new-project.md) - Create a new Python project from this template
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
- [Template Management](template/manage.md) - Unified interface for creating projects, checking updates, and syncing
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) - What each tool is for, who uses it, and where runtime code ends and dev tooling begins
- [Usage Guide](usage/basics.md) - Package usage and development workflows
- [Using This Template](template/index.md) - Overview of using pyproject-template for your Python projects
<!-- END:all -->

---

## Contributing to Documentation

When adding new documentation:

1. Add frontmatter with `title`, `description`, `audience`, and `tags`:
   ```yaml
   ---
   title: My New Guide
   description: Short description for the index
   audience:
     - users
     - contributors
   tags:
     - setup
     - getting-started
   ---
   ```

2. Place the file in the appropriate directory

3. Run `python tools/generate_doc_toc.py` to update this index

4. The pre-commit hook will also run automatically on commit

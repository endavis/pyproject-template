# All Documents

Complete index of all documentation, organized by audience and as a full alphabetical list.

> These lists are auto-generated from document frontmatter.
> Run `python tools/generate_doc_toc.py` to update.

## By Audience

### For Users
<!-- BEGIN:audience=users -->
- [API Reference](reference/api.md) - Complete API documentation for Package Name
- [Examples](examples/README.md) - Example scripts demonstrating how to use the package
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Keeping Up to Date](template/updates.md) - Stay in sync with improvements to the pyproject-template
- [Migration Guide](template/migration.md) - Migrate existing Python projects to use this template
- [New Project Setup](template/new-project.md) - Create a new Python project from this template
- [Package Name Documentation](index.md) - Welcome and overview of the project
- [Template Management](template/manage.md) - Unified interface for creating projects, checking updates, and syncing
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Usage Guide](usage/basics.md) - Package usage and development workflows
- [Using This Template](template/index.md) - Overview of using pyproject-template for your Python projects
<!-- END:audience=users -->

### For Contributors
<!-- BEGIN:audience=contributors -->
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Gemini, and Codex for this project
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Reference](reference/api.md) - Complete API documentation for Package Name
- [CI/CD Testing Guide](development/ci-cd-testing.md) - GitHub Actions pipelines for testing, linting, and coverage
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Package Name Documentation](index.md) - Welcome and overview of the project
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
<!-- END:audience=contributors -->

### For AI Agents
<!-- BEGIN:audience=ai-agents -->
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Gemini, and Codex for this project
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
<!-- END:audience=ai-agents -->

## Complete Index
<!-- BEGIN:all -->
- [ADR-0001: Use uv for package management](decisions/0001-use-uv-for-package-management.md)
- [ADR-0002: Use doit for task automation](decisions/0002-use-doit-for-task-automation.md)
- [ADR-0003: Use ruff for linting and formatting](decisions/0003-use-ruff-for-linting-and-formatting.md)
- [ADR-0004: Auto-discover doit tasks from modules](decisions/0004-auto-discover-doit-tasks.md)
- [ADR-0005: AI agent command restrictions via hooks](decisions/0005-ai-agent-command-restrictions.md)
- [ADR-0006: Merge-gate workflow requiring ready-to-merge label](decisions/0006-merge-gate-workflow.md)
- [ADR-0007: Use mypy for static type checking](decisions/0007-use-mypy-for-type-checking.md)
- [ADR-NNNN: Title](decisions/adr-template.md)
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Gemini, and Codex for this project
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Reference](reference/api.md) - Complete API documentation for Package Name
- [Architecture Decision Records](decisions/README.md)
- [CI/CD Testing Guide](development/ci-cd-testing.md) - GitHub Actions pipelines for testing, linting, and coverage
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [Examples](examples/README.md) - Example scripts demonstrating how to use the package
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Keeping Up to Date](template/updates.md) - Stay in sync with improvements to the pyproject-template
- [Migration Guide](template/migration.md) - Migrate existing Python projects to use this template
- [New Project Setup](template/new-project.md) - Create a new Python project from this template
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Package Name Documentation](index.md) - Welcome and overview of the project
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Template Management](template/manage.md) - Unified interface for creating projects, checking updates, and syncing
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
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

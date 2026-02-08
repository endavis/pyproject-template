# Template Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the **pyproject-template** itself — the decisions that shaped the template's tooling, workflows, and conventions.

These are separate from [project-specific ADRs](../../decisions/README.md), which document decisions made for your own project.

## Template ADR Numbering

Template ADRs use the **9XXX** range to avoid conflicts with project-specific ADRs (which start at 0001).

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [9001](9001-use-uv-for-package-management.md) | Use uv for package management | Accepted |
| [9002](9002-use-doit-for-task-automation.md) | Use doit for task automation | Accepted |
| [9003](9003-use-ruff-for-linting-and-formatting.md) | Use ruff for linting and formatting | Accepted |
| [9004](9004-auto-discover-doit-tasks.md) | Auto-discover doit tasks from modules | Accepted |
| [9005](9005-ai-agent-command-restrictions.md) | AI agent command restrictions via hooks | Accepted |
| [9006](9006-merge-gate-workflow.md) | Merge-gate workflow requiring ready-to-merge label | Accepted |
| [9007](9007-use-mypy-for-type-checking.md) | Use mypy for static type checking | Accepted |
| [9008](9008-pr-based-development-workflow.md) | PR-based development workflow | Accepted |
| [9009](9009-use-pre-commit-hooks-for-quality-gates.md) | Use pre-commit hooks for quality gates | Accepted |
| [9010](9010-use-conventional-commits-format.md) | Use conventional commits format | Accepted |
| [9011](9011-use-pytest-for-testing.md) | Use pytest for testing | Accepted |
| [9012](9012-use-mkdocs-with-material-theme-for-documentation.md) | Use mkdocs with Material theme for documentation | Accepted |
| [9013](9013-python-version-support-policy.md) | Python version support policy with bookend CI strategy | Accepted |

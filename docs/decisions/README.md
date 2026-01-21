# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for this project.

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences. ADRs help:

- **Document decisions** that might otherwise be lost in PR discussions or tribal knowledge
- **Onboard new contributors** by explaining why certain patterns were chosen
- **Track evolution** of the project's architecture over time
- **Facilitate discussion** when revisiting or challenging past decisions

## ADR Format

We use a simplified MADR (Markdown Any Decision Records) format. See [adr-template.md](adr-template.md) for the template.

## Creating a New ADR

Use the doit task to create a new ADR:

```bash
doit adr --title="Your decision title"
```

This will:

1. Create a new ADR file with the next sequential number
2. Populate the template with the title and current date
3. Place it in this directory

## Naming Convention

ADR files follow the pattern: `NNNN-short-title.md`

- `NNNN`: Four-digit sequential number (e.g., 0001, 0002)
- `short-title`: Kebab-case summary of the decision

Example: `0001-use-uv-for-package-management.md`

## ADR Statuses

- **Proposed**: Under discussion, not yet accepted
- **Accepted**: Decision has been agreed upon and is in effect
- **Deprecated**: No longer relevant but kept for historical context
- **Superseded**: Replaced by a newer ADR (link to the new one)

## Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-use-uv-for-package-management.md) | Use uv for package management | Accepted | 2025-01-21 |
| [0002](0002-use-doit-for-task-automation.md) | Use doit for task automation | Accepted | 2025-01-21 |
| [0003](0003-use-ruff-for-linting-and-formatting.md) | Use ruff for linting and formatting | Accepted | 2025-01-21 |
| [0004](0004-auto-discover-doit-tasks.md) | Auto-discover doit tasks from modules | Accepted | 2025-01-21 |
| [0005](0005-ai-agent-command-restrictions.md) | AI agent command restrictions via hooks | Accepted | 2025-01-21 |
| [0006](0006-merge-gate-workflow.md) | Merge-gate workflow requiring ready-to-merge label | Accepted | 2025-01-21 |
| [0007](0007-use-mypy-for-type-checking.md) | Use mypy for static type checking | Accepted | 2025-01-21 |
| [0008](0008-pr-based-development-workflow.md) | PR-based development workflow | Accepted | 2025-01-21 |
| [0009](0009-use-pre-commit-hooks-for-quality-gates.md) | Use pre-commit hooks for quality gates | Accepted | 2025-01-21 |
| [0010](0010-use-conventional-commits-format.md) | Use conventional commits format | Accepted | 2025-01-21 |
| [0011](0011-use-pytest-for-testing.md) | Use pytest for testing | Accepted | 2025-01-21 |
| [0012](0012-use-mkdocs-with-material-theme-for-documentation.md) | Use mkdocs with Material theme for documentation | Accepted | 2025-01-21 |

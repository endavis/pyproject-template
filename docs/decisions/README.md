# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for this project.

## What is an ADR?

An ADR documents an architectural decision: what was decided and why. The detailed discussion and specification lives in the GitHub Issue; the ADR provides a summary with links.

## ADR Format

ADRs use a simplified format:

```markdown
# ADR-NNNN: Title

## Status
Accepted

## Decision
Brief summary of what was decided.

## Rationale
Why this decision was made.

## Related Issues
- Issue #XX: Description

## Related Documentation
- [Relevant Doc](../path/to/doc.md)
```

See [adr-template.md](adr-template.md) for the template.

## Creating a New ADR

```bash
# Interactive (opens editor)
doit adr --title="Your decision title"

# Non-interactive (for scripts/AI)
doit adr --title="Use Redis" --body="## Status\nAccepted\n..."
doit adr --title="Use Redis" --body-file=adr.md
```

## When to Create an ADR

Create an ADR when:
- Introducing a new tool, framework, or library
- Changing development workflow or processes
- Making decisions that affect project architecture

The Issue contains the full discussion; the ADR summarizes the outcome.

## ADR Statuses

- **Accepted**: Decision is in effect
- **Deprecated**: No longer relevant (kept for history)
- **Superseded**: Replaced by a newer ADR

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-use-uv-for-package-management.md) | Use uv for package management | Accepted |
| [0002](0002-use-doit-for-task-automation.md) | Use doit for task automation | Accepted |
| [0003](0003-use-ruff-for-linting-and-formatting.md) | Use ruff for linting and formatting | Accepted |
| [0004](0004-auto-discover-doit-tasks.md) | Auto-discover doit tasks from modules | Accepted |
| [0005](0005-ai-agent-command-restrictions.md) | AI agent command restrictions via hooks | Accepted |
| [0006](0006-merge-gate-workflow.md) | Merge-gate workflow requiring ready-to-merge label | Accepted |
| [0007](0007-use-mypy-for-type-checking.md) | Use mypy for static type checking | Accepted |
| [0008](0008-pr-based-development-workflow.md) | PR-based development workflow | Accepted |
| [0009](0009-use-pre-commit-hooks-for-quality-gates.md) | Use pre-commit hooks for quality gates | Accepted |
| [0010](0010-use-conventional-commits-format.md) | Use conventional commits format | Accepted |
| [0011](0011-use-pytest-for-testing.md) | Use pytest for testing | Accepted |
| [0012](0012-use-mkdocs-with-material-theme-for-documentation.md) | Use mkdocs with Material theme for documentation | Accepted |

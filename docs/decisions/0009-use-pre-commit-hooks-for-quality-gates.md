# ADR-0009: Use pre-commit hooks for quality gates

## Status

Accepted

## Date

2025-01-21

## Context

Code quality checks (linting, formatting, type checking, security scanning) can be run at different points:

- **IDE/Editor**: Real-time feedback but inconsistent across team members
- **Pre-commit hooks**: Run before commits are created, blocking bad commits
- **CI pipeline**: Run on push/PR, catches issues but after commit is made
- **Manual**: Developer runs checks when they remember

The project needed to ensure quality checks are:

- Consistently applied to all changes
- Run before bad code enters the repository
- Fast enough to not disrupt developer workflow
- Configurable and extensible

## Decision

Use **pre-commit** framework with hooks that run before every commit:

**Quality checks:**
- `ruff` - Linting (replaces flake8, pylint)
- `ruff-format` - Code formatting (replaces black)
- `mypy` - Type checking
- `bandit` - Security scanning
- `codespell` - Spell checking

**Safety checks:**
- Prevent commits to main branch
- Prevent committing local config files
- Protect dynamic version configuration
- Check branch naming convention

**Automation:**
- Generate documentation TOC
- Trim trailing whitespace
- Fix end of files
- Check YAML/TOML syntax

Hooks are defined in `.pre-commit-config.yaml` and installed via `pre-commit install`.

## Consequences

### Positive

- Bad code never enters the repository
- Consistent formatting across all contributors
- Fast feedback loop (seconds, not minutes)
- Works offline (no CI dependency)
- Catches issues before PR review
- Safety checks prevent dangerous operations

### Negative

- Initial setup required (`pre-commit install`)
- Can slow down commits if checks are slow
- Developers may bypass with `--no-verify` (blocked for AI agents)
- Must keep hooks in sync with CI checks

### Neutral

- Requires pre-commit package as dev dependency
- Hook failures block commits (by design)

## Participants

- Project maintainers

## Related

- [ADR-0003: Use ruff for linting](0003-use-ruff-for-linting-and-formatting.md)
- [ADR-0007: Use mypy for type checking](0007-use-mypy-for-type-checking.md)
- [ADR-0005: AI agent command restrictions](0005-ai-agent-command-restrictions.md)

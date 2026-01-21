# ADR-0003: Use ruff for linting and formatting

## Status

Accepted

## Date

2025-01-21

## Context

Python projects benefit from automated code quality tools for linting (detecting errors, enforcing style) and formatting (consistent code style). Traditional tools include:

- **Linting**: flake8, pylint, pyflakes, pycodestyle
- **Formatting**: black, autopep8, yapf
- **Import sorting**: isort

Using multiple tools means:

- Multiple configuration files
- Different execution times
- Potential conflicts between tools
- More dependencies to manage

## Decision

Use **ruff** as the single tool for both linting and formatting.

ruff is an extremely fast Python linter and formatter written in Rust. It provides:

- Linting rules from flake8, pylint, pyflakes, and many others
- Built-in formatter (compatible with Black)
- Import sorting (replaces isort)
- Single configuration in `pyproject.toml`
- 10-100x faster than traditional Python-based tools

## Consequences

### Positive

- Single tool replaces flake8, black, isort, and others
- Extremely fast execution (Rust-based)
- Single configuration section in `pyproject.toml`
- Consistent code style enforcement
- Active development and growing rule set
- Same maintainers as uv (Astral), ensuring aligned tooling

### Negative

- Not all rules from pylint are implemented
- Formatter output may differ slightly from Black in edge cases
- Relatively new tool (though rapidly maturing)

### Neutral

- Migration from existing tools requires updating configuration
- Team needs to learn ruff-specific configuration options

## Participants

- Project maintainers

## Related

- [ruff documentation](https://docs.astral.sh/ruff/)
- [ADR-0001: Use uv for package management](0001-use-uv-for-package-management.md)
- [ADR-0002: Use doit for task automation](0002-use-doit-for-task-automation.md)

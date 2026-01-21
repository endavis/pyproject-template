# ADR-0001: Use uv for package management

## Status

Accepted

## Date

2025-01-21

## Context

Python projects require a package manager for dependency management, virtual environment creation, and package installation. Traditional tools include pip, pip-tools, poetry, and pipenv. Each has trade-offs in terms of speed, features, and complexity.

The project needed a modern package manager that:

- Is fast and efficient
- Supports modern Python packaging standards (PEP 517, PEP 621)
- Handles both dependency resolution and virtual environment management
- Has a simple, intuitive interface
- Is actively maintained

## Decision

Use **uv** as the primary package manager for this project.

uv is a modern Python package manager written in Rust by Astral (creators of ruff). It provides:

- Extremely fast dependency resolution and installation (10-100x faster than pip)
- Built-in virtual environment management (`uv venv`)
- Compatible with `pyproject.toml` and standard Python packaging
- Drop-in replacement for pip commands
- Lock file support for reproducible builds

## Consequences

### Positive

- Significantly faster CI builds and local development workflows
- Single tool handles venv creation, dependency installation, and locking
- Consistent with modern Python packaging standards
- Same maintainers as ruff, ensuring aligned tooling philosophy
- Growing community adoption and active development

### Negative

- Relatively new tool (less battle-tested than pip/poetry)
- Team members need to learn new commands
- Some edge cases may not be handled as well as mature tools
- Requires Rust for building from source (pre-built binaries available)

### Neutral

- Migrating from pip/poetry requires updating CI scripts and documentation
- Lock file format differs from poetry.lock or requirements.txt

## Participants

- Project maintainers

## Related

- [uv documentation](https://docs.astral.sh/uv/)
- [ADR-0002: Use doit for task automation](0002-use-doit-for-task-automation.md)
- [ADR-0003: Use ruff for linting and formatting](0003-use-ruff-for-linting-and-formatting.md)
- Issue #166: Block uv add in AI agent hooks/settings
- Issue #148: dodo.py uses Unix-only shell syntax for UV_CACHE_DIR

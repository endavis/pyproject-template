# ADR-0007: Use mypy for static type checking

## Status

Accepted

## Date

2025-01-21

## Context

Python is dynamically typed, but type hints (PEP 484) enable static analysis to catch type errors before runtime. Several tools provide static type checking:

- **mypy**: The original and most mature type checker
- **pyright**: Microsoft's type checker, used in Pylance/VS Code
- **pytype**: Google's type checker
- **pyre**: Facebook's type checker

The project needed static type checking to:

- Catch type errors early in development
- Improve code documentation through type hints
- Enable better IDE support
- Enforce type safety in CI

## Decision

Use **mypy** in strict mode for static type checking.

mypy is configured in `pyproject.toml` with strict settings:

```toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_ignores = true
```

mypy runs as part of:

- `doit check` (local development)
- Pre-commit hooks (before commits)
- CI pipeline (on all PRs)

## Consequences

### Positive

- Early detection of type errors
- Better code documentation through required type hints
- Improved IDE support (autocomplete, hover info)
- Consistent with Python community standards
- Well-integrated with ruff for linting

### Negative

- Strict mode requires type hints everywhere (more verbose code)
- Some dynamic patterns are hard to type correctly
- False positives occasionally require `# type: ignore` comments
- Third-party libraries may lack type stubs

### Neutral

- Type hints are documentation that can't become stale
- Gradual typing allows incremental adoption

## Participants

- Project maintainers

## Related

- [mypy documentation](https://mypy.readthedocs.io/)
- [ADR-0003: Use ruff for linting and formatting](0003-use-ruff-for-linting-and-formatting.md)
- Issue #61: Make doit check use strict mypy mode

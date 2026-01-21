# ADR-0011: Use pytest for testing

## Status

Accepted

## Date

2025-01-21

## Context

Python has several testing frameworks:

- **unittest**: Built-in, xUnit-style, verbose boilerplate
- **pytest**: Third-party, minimal boilerplate, powerful fixtures
- **nose/nose2**: Extended unittest, largely superseded by pytest
- **doctest**: Tests in docstrings, limited capabilities

The project needed a testing framework that:

- Minimizes boilerplate code
- Has excellent plugin ecosystem
- Supports parallel test execution
- Provides clear, readable test output
- Integrates well with CI/CD
- Is widely adopted (easy to find help)

## Decision

Use **pytest** as the testing framework with key plugins:

- **pytest-xdist**: Parallel test execution (`-n auto`)
- **pytest-cov**: Coverage reporting

Configuration in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

Test execution via doit:
- `doit test`: Run all tests with pytest
- `doit check`: Run tests as part of full quality check

Test file conventions:
- Tests in `tests/` directory
- Test files named `test_*.py`
- Test functions named `test_*`
- Test classes named `Test*`

## Consequences

### Positive

- Minimal boilerplate (plain functions, no classes required)
- Powerful fixture system for setup/teardown
- Excellent assertion introspection
- Parallel execution speeds up CI
- Rich plugin ecosystem
- Industry standard for Python testing

### Negative

- Third-party dependency (not built-in)
- Some magic behavior can be confusing
- Fixture scope can be tricky to understand

### Neutral

- Compatible with unittest-style tests if needed
- Coverage integrated but optional

## Participants

- Project maintainers

## Related

- [pytest documentation](https://docs.pytest.org/)
- [ADR-0009: Use pre-commit hooks](0009-use-pre-commit-hooks-for-quality-gates.md)
- Issue #126: Add tests for template tools and exclude from generated projects
- Issue #83: Add multi-OS CI testing (Windows, macOS)

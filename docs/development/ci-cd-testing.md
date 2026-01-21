---
title: CI/CD Testing Guide
description: GitHub Actions pipelines for testing, linting, and coverage
audience:
  - contributors
tags:
  - ci-cd
  - testing
  - github-actions
---

# CI/CD Testing Guide

## Overview

CI runs lint/format, tests, coverage, and quality checks to guard against regressions. GitHub Actions pipelines target multiple Python versions and publish coverage artifacts/comments.

## Audience and Prerequisites

- **Audience:** Contributors and reviewers ensuring CI health
- **Prerequisites:** GitHub Actions access; local tools (`uv`, `doit`, pytest, ruff, mypy) to replicate checks

## When to Use This

- Before opening/merging PRs to mirror CI locally
- Understanding pipeline stages and coverage expectations
- Expanding tests or adjusting quality thresholds

## Quick Start

Local commands:
```bash
doit format && doit lint
uv run pytest
doit coverage
```

## Python Version Support Policy

### Active Support

Only the **last 3 major Python versions** are actively supported. This means:
- Bug fixes and new features are tested against these versions
- CI runs these versions on every PR (using bookend strategy - oldest + newest)
- Documentation and examples target these versions

**Current active versions:** Python 3.12, 3.13, 3.14

### Passive Compatibility

Older Python versions may continue to work but are not actively maintained:
- We continue testing previous versions in CI via the `full-matrix` label
- Once a version fails CI tests, it is removed from the matrix and marked incompatible
- Users on older Python versions can use version-tagged releases (e.g., `v1.2.3-py310-final`)

### Version Lifecycle

| Stage | Description | CI Testing |
|-------|-------------|------------|
| **Active** | Last 3 major versions | Every PR (bookend strategy) |
| **Passive** | Older versions still passing | On-demand (`full-matrix` label) |
| **Deprecated** | Fails CI tests | Removed from matrix |

### CI Matrix Strategy

To balance test coverage with CI efficiency:

| PR State | Python Versions Tested | Jobs |
|----------|----------------------|------|
| Default | Bookends only (oldest + newest active) × 3 OSes | 6 |
| `full-matrix` label | All supported versions × 3 OSes | 9-15 |

The **bookend strategy** tests the oldest and newest supported versions. If both pass, intermediate versions are assumed compatible. Use the `full-matrix` label when:
- Making changes that might affect version compatibility
- Preparing a release
- Investigating compatibility issues

### Deprecation Process

When a Python version starts failing CI:

1. **Assess**: Determine if the failure is fixable without significant effort
2. **Decide**: Fix compatibility or deprecate the version
3. **Tag**: If deprecating, tag the last compatible release (e.g., `v1.2.3-py310-final`)
4. **Update**: Remove version from CI matrix and update `pyproject.toml` classifiers
5. **Document**: Update this documentation and release notes

## Pipeline Details (GitHub Actions)

### Recommended Workflow Structure

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.14"]  # Bookend strategy: oldest + newest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          uv sync --dev

      - name: Run format check
        run: uv run doit format_check

      - name: Run linter
        run: uv run doit lint

      - name: Run type checker
        run: uv run doit type_check
        continue-on-error: true  # Optional: make non-blocking

      - name: Run tests with coverage
        run: uv run pytest --cov=src --cov-report=xml --cov-report=html

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.12'
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

      - name: Upload coverage artifacts
        uses: actions/upload-artifact@v4
        if: matrix.python-version == '3.12'
        with:
          name: coverage-report
          path: htmlcov/
```

### Pipeline Jobs

#### Code Quality Job

```yaml
code-quality:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Install uv
      uses: astral-sh/setup-uv@v1
    - name: Install dependencies
      run: uv sync --dev
    - name: Format check
      run: uv run doit format_check
    - name: Lint check
      run: uv run doit lint
    - name: Type check
      run: uv run doit type_check
      continue-on-error: true
```

#### Security Scan Job

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Install uv
      uses: astral-sh/setup-uv@v1
    - name: Install security tools
      run: uv sync --extra security
    - name: Run security audit
      run: uv run doit audit
    - name: Run bandit scan
      run: uv run doit security
```

### Coverage Requirements

- **Recommended threshold**: ≥70%
- **Configuration**: Set in `pyproject.toml` and pytest command
- **Artifacts**: Upload HTML coverage reports for review
- **Integration**: Use Codecov or similar service for tracking

**Example pytest configuration in `pyproject.toml`:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=70",
]
```

### PR Comments

Add coverage comments to PRs using GitHub Actions:

```yaml
- name: Coverage comment
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ github.token }}
    MINIMUM_GREEN: 80
    MINIMUM_ORANGE: 70
```

## Local Development Workflow

### Running Tests Locally

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_config.py

# Run specific test
uv run pytest tests/test_config.py::test_load_config

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
xdg-open htmlcov/index.html  # Open in browser
```

### Quality Checks

```bash
# Format code
doit format

# Check formatting (CI mode)
doit format_check

# Lint code
doit lint

# Type check
doit type_check

# Run all quality checks
doit check
```

### Coverage Analysis

```bash
# Run with coverage
doit coverage

# View coverage report
xdg-open tmp/htmlcov/index.html

# Check coverage threshold
pytest --cov=src --cov-fail-under=70
```

## Validation and Checks

### Pre-commit Integration

The template includes pre-commit hooks that run automatically:

```bash
# Install hooks
uv run pre-commit install

# Run manually on all files
uv run pre-commit run --all-files

# Update hook versions
uv run pre-commit autoupdate
```

**Pre-commit configuration (`.pre-commit-config.yaml`):**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff-format
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true
```

### Continuous Integration Checklist

Before pushing to CI:
- [ ] Run `doit format` to format code
- [ ] Run `doit lint` to check for issues
- [ ] Run `doit type_check` to verify types
- [ ] Run `uv run pytest` to ensure tests pass
- [ ] Run `doit coverage` to check coverage threshold
- [ ] Review changes and commit messages

## Testing Best Practices

### Test Organization

```
tests/
├── unit/           # Unit tests (fast, isolated)
│   ├── test_config.py
│   ├── test_utils.py
│   └── test_models.py
├── integration/    # Integration tests (slower, with dependencies)
│   ├── test_api.py
│   └── test_database.py
├── fixtures/       # Test data and fixtures
│   └── sample_config.json
└── conftest.py     # Shared pytest fixtures
```

### Writing Good Tests

```python
import pytest
from myproject import Config, ConfigError

@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"key": "value"}')
    return config_file

def test_config_load_success(temp_config_file):
    """Test successful config loading."""
    config = Config.load(str(temp_config_file))
    assert config.get("key") == "value"

def test_config_load_file_not_found():
    """Test config loading with missing file."""
    with pytest.raises(ConfigError, match="not found"):
        Config.load("nonexistent.json")

@pytest.mark.parametrize("value,expected", [
    ("true", True),
    ("false", False),
    ("1", True),
    ("0", False),
])
def test_parse_bool(value, expected):
    """Test boolean parsing with various inputs."""
    assert parse_bool(value) == expected
```

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch
import pytest

def test_api_call_success():
    """Test successful API call."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        mock_get.return_value.status_code = 200

        result = fetch_data("https://api.example.com/data")
        assert result["status"] == "ok"
        mock_get.assert_called_once_with("https://api.example.com/data")

def test_api_call_failure():
    """Test API call failure handling."""
    with patch("requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("Network error")

        with pytest.raises(APIError, match="Network error"):
            fetch_data("https://api.example.com/data")
```

## Examples

### Running Specific Tests

```bash
# Run all tests in a file
pytest tests/unit/test_config.py

# Run a specific test class
pytest tests/unit/test_config.py::TestConfigManager

# Run a specific test method
pytest tests/unit/test_config.py::TestConfigManager::test_load_config

# Run tests matching a pattern
pytest -k "test_config"

# Run tests with markers
pytest -m "slow"  # Run only tests marked as slow
pytest -m "not slow"  # Skip slow tests
```

### Coverage Analysis

```bash
# Generate coverage report
doit coverage

# View HTML coverage report
xdg-open tmp/htmlcov/index.html

# Check specific module coverage
pytest --cov=src/myproject/config --cov-report=term-missing

# Generate XML coverage for CI
pytest --cov=src --cov-report=xml
```

### Testing Multiple Python Versions

Using `tox`:

```ini
# tox.ini
[tox]
envlist = py312,py313,py314

[testenv]
deps =
    pytest
    pytest-cov
commands = pytest {posargs}
```

```bash
# Run tests on all environments
tox

# Run on specific environment
tox -e py314
```

## Merge Gate Workflow

The repository uses a merge gate to ensure PRs are only merged after explicit approval.

### How It Works

The merge gate is implemented in `.github/workflows/merge-gate.yml`:

```yaml
name: Merge Gate

on:
  pull_request:
    branches: [main]
    types: [opened, labeled, unlabeled, synchronize, reopened]

jobs:
  require-label:
    runs-on: ubuntu-latest
    steps:
      - name: Check for ready-to-merge label
        run: |
          if [[ "${{ contains(github.event.pull_request.labels.*.name, 'ready-to-merge') }}" != "true" ]]; then
            echo "::error::PR requires 'ready-to-merge' label before merging"
            exit 1
          fi
```

### The `ready-to-merge` Label

This label is a **pure merge gate** - it signals that a PR is approved for merge but does not trigger additional CI runs. The default CI matrix (6 jobs) provides sufficient coverage.

**When to add the label:**
- All CI checks have passed
- Code review is complete and approved
- All review feedback has been addressed

**Adding the label:**
```bash
# Via GitHub CLI
gh pr edit <PR-NUMBER> --add-label "ready-to-merge"

# Or via GitHub web UI: PR page → Labels → ready-to-merge
```

### The `full-matrix` Label

Use this label to trigger comprehensive compatibility testing across all supported Python versions:

**When to use:**
- Changes that might affect Python version compatibility
- Preparing a release
- Investigating compatibility issues reported by users

```bash
# Add full-matrix label for comprehensive testing
gh pr edit <PR-NUMBER> --add-label "full-matrix"
```

### Branch Protection Integration

Configure branch protection rules to require the merge gate:

1. Go to **Settings** → **Branches** → **Branch protection rules**
2. Select or create rule for `main`
3. Enable **Require status checks to pass before merging**
4. Add `require-label` to required status checks

This ensures PRs cannot be merged until:
- The `ready-to-merge` label is present
- All CI checks pass (default 6-job matrix)

### Interaction with Approval Workflows

The merge gate works alongside GitHub's approval requirement:

| Check | Type | Purpose |
|-------|------|---------|
| Approvals | GitHub built-in | Ensures code review is complete |
| CI checks | GitHub Actions | Tests code on bookend Python versions × all OSes |
| Merge gate | Custom workflow | Explicit "ready" signal via label |

**Recommended merge flow:**

```
PR opened → CI runs (6 jobs) → Review/Approval → Add ready-to-merge label → Merge
```

**Optional full compatibility check:**

```
PR opened → CI runs → Add full-matrix label → Full CI runs (9-15 jobs) → Review → Add ready-to-merge → Merge
```

## Troubleshooting

### Coverage Below Threshold

**Symptom**: `pytest --cov-fail-under=70` fails
**Fix**:
- Add tests for new/changed code paths
- Use `pytest --cov=src --cov-report=html` to see uncovered lines
- Review coverage report: `xdg-open tmp/htmlcov/index.html`

### Ruff/Format Failures

**Symptom**: Formatting or linting errors in CI
**Fix**:
- Run `doit format` locally to auto-format
- Run `doit lint` to see all violations
- Address violations or add exceptions to `pyproject.toml`

### Mypy Type Errors

**Symptom**: Type checking fails
**Fix**:
- Add proper type annotations
- Use `# type: ignore[error-code]` sparingly with explanatory comments
- Review mypy output for specific issues
- Consider making mypy non-blocking initially (`continue-on-error: true`)

### Tests Fail in CI but Pass Locally

**Symptom**: Tests pass locally but fail in CI
**Fix**:
- Check for environment-specific dependencies
- Ensure all test dependencies are in `pyproject.toml`
- Look for timing issues or race conditions
- Check for file system or path differences

### Pre-commit Hooks Too Slow

**Symptom**: Pre-commit hooks take too long
**Fix**:
- Skip test hook for routine commits: `git commit --no-verify`
- Run tests manually before pushing
- Consider running only fast unit tests in pre-commit
- Move integration tests to CI only

## Related Documentation

- [Coding Standards](coding-standards.md)
- [Release Automation](release-and-automation.md)

---

[Back to Documentation Index](../TABLE_OF_CONTENTS.md)

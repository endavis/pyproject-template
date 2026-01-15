# Contributing to Package Name

Thank you for your interest in contributing to this project! We welcome contributions from everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment (see below)
4. Create a new branch for your changes
5. Make your changes
6. Run tests and checks
7. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [direnv](https://direnv.net/) - Automatic environment management (recommended)

### Initial Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/package_name.git
cd package_name

# Set up direnv
direnv allow
# Optional: Create .envrc.local for personal settings
cp .envrc.local.example .envrc.local

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Or let direnv handle this
uv pip install -e ".[dev]"

# Install pre-commit hooks
doit pre_commit_install
```

### Available Commands

View all available development tasks:
```bash
doit list
```

Common commands:
```bash
doit test          # Run tests
doit coverage      # Run tests with coverage
doit lint          # Run linting
doit format        # Format code
doit type_check    # Run type checking
doit check         # Run all checks
doit cleanup       # Clean build artifacts
```

## How to Contribute

### Types of Contributions

We welcome many types of contributions:

- **Bug fixes** - Fix issues in the codebase
- **New features** - Add new functionality
- **Documentation** - Improve docs, docstrings, examples
- **Tests** - Add or improve test coverage
- **Refactoring** - Improve code quality without changing behavior
- **Performance** - Optimize performance

### Before You Start

1. **Check existing issues** - See if someone is already working on it
2. **Open an issue** - Discuss your proposed changes before starting work
3. **Get feedback** - Especially for large changes or new features

## Coding Standards

### Python Style

- **Python version:** 3.12+ with modern type hints
- **Line length:** Max 100 characters
- **Docstrings:** Google-style for all public APIs
- **Type hints:** Required for all public functions/methods
- **Naming:** `snake_case` for functions/variables, `PascalCase` for classes

### Type Hints

Use modern type hint syntax:
```python
# Good
def process_items(items: list[str]) -> dict[str, int]:
    pass

# Bad
from typing import List, Dict
def process_items(items: List[str]) -> Dict[str, int]:
    pass
```

### Docstrings

Use Google-style docstrings:
```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.

    Longer description if needed, explaining the purpose,
    behavior, and any important details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
    """
```

### Code Organization

Organize imports in three groups:
```python
# Standard library
import os
from pathlib import Path

# Third-party
import click
import pytest

# Local
from package_name import module
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Maintain or improve test coverage (target: ≥80%)
- Use descriptive test names: `test_function_does_something_when_condition`
- Use fixtures for common setup
- Test edge cases and error conditions

### Running Tests

```bash
# Run all tests
doit test

# Run with coverage
doit coverage

# Run specific test file
uv run pytest tests/test_example.py

# Run specific test
uv run pytest tests/test_example.py::test_specific_function -v
```

### Test Structure

```python
import pytest

def test_feature_works_correctly():
    """Test that feature produces expected output."""
    # Arrange
    input_data = "test input"

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_output


@pytest.mark.parametrize("input_value,expected", [
    ("value1", "expected1"),
    ("value2", "expected2"),
])
def test_feature_with_multiple_inputs(input_value, expected):
    """Test feature with various inputs."""
    assert function_to_test(input_value) == expected
```

## Commit Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

### Commit Format

```
<type>: <subject>

[optional body]

[optional footer]
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, whitespace (no code change)
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks (deps, tooling)
- `ci`: CI/CD changes
- `revert`: Reverting previous commits

### Examples

```bash
feat: add support for async operations

fix: handle None values in data processor

docs: update installation instructions

test: add tests for edge cases in parser
```

### Breaking Changes

For breaking changes, include `BREAKING CHANGE:` in the footer:

```
refactor: change API to use async/await

BREAKING CHANGE: All public methods are now async.
Update calling code to use `await`.
```

## Pull Request Process

### Before Submitting

1. **Run all checks locally:**
   ```bash
   doit check
   ```

2. **Update CHANGELOG.md** (for notable changes)

3. **Update documentation** (if needed)

4. **Self-review your code**

### PR Title

Use the same format as commits: `<type>: <subject>`

Examples:
- `feat: add support for custom validators`
- `fix: handle edge case in data parsing`
- `docs: improve API documentation`

### PR Description

Fill out the PR template (`.github/pull_request_template.md`):
- Provide a clear summary
- List specific changes
- Reference related issues
- Describe testing performed
- Note any breaking changes

### PR Review Process

1. **Automated checks** - CI must pass (tests, lint, type-check)
2. **Code review** - At least one maintainer approval required
3. **Address feedback** - Respond to review comments
4. **Merge** - Maintainer will merge when approved

### After Merge

- Delete your branch
- Update your fork with the latest changes
- Close any related issues

## Reporting Bugs

Use the bug report template (`.github/ISSUE_TEMPLATE/bug_report.md`):

1. Go to **Issues** → **New Issue** → **Bug Report**
2. Fill out all sections:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, package version)
   - Error messages or logs
3. Add relevant labels
4. Be responsive to follow-up questions

## Requesting Features

Use the feature request template (`.github/ISSUE_TEMPLATE/feature_request.md`):

1. Go to **Issues** → **New Issue** → **Feature Request**
2. Fill out all sections:
   - Problem statement
   - Proposed solution
   - Alternative solutions considered
   - Use cases
   - Benefits
3. Be open to discussion and feedback
4. Be willing to implement it yourself (or help)

## Development Workflow

**MANDATORY RULE:** All changes must originate from a GitHub Issue.

### Issue-Driven Development

Every code change must be linked to a GitHub Issue. This ensures:
- **Traceability:** Every change is linked to a documented need
- **Context:** Issues capture the "why" behind changes
- **Planning:** Better project management and prioritization
- **History:** Searchable record of decisions and rationale
- **Collaboration:** Clear communication about work in progress

### Workflow Steps

#### 1. **Issue:** Ensure GitHub Issue Exists

**Create issue using doit (recommended):**
```bash
# Interactive: Opens $EDITOR with template
doit issue --type=feature    # For new features
doit issue --type=bug        # For bugs and defects
doit issue --type=refactor   # For code refactoring
doit issue --type=doc        # For documentation
doit issue --type=chore      # For maintenance tasks

# Non-interactive: For AI agents or scripts
doit issue --type=feature --title="Add export" --body-file=issue.md
doit issue --type=doc --title="Add guide" --body="## Description\n..."
```

**Or use gh CLI directly:**
```bash
gh issue create --title "<description>" --label "enhancement" --body "..."
```

**Issue types auto-apply labels:**
- `feature` → `enhancement, needs-triage`
- `bug` → `bug, needs-triage`
- `refactor` → `refactor, needs-triage`
- `doc` → `documentation, needs-triage`
- `chore` → `chore, needs-triage`

**Required fields ensure complete information** - Fill all fields to provide context.

#### 2. **Branch:** Create Branch Linked to Issue

**Branch Format:** `<type>/<number>-<description>`

**Allowed Types:**
- `issue`, `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `perf`, `hotfix`
- Special: `release/<version>` (no issue number required)

**Examples:**
```bash
feat/42-user-authentication
fix/123-handle-null-values
docs/41-update-guidelines
refactor/55-simplify-parser
```

**Create and link branch:**
```bash
# Option 1: GitHub CLI (auto-links)
gh issue develop <issue-number> --checkout

# Option 2: Manual (include issue number in name)
git checkout -b feat/42-add-feature
```

**Branch naming is enforced by pre-commit hooks.**

#### 3. **Commit:** Use Conventional Commits

**Format:** `<type>: <subject>`

Use `doit commit` for interactive commit creation with commitizen.

**Enforced by:**
- Pre-commit hooks (locally)
- CI checks (on PR)

#### 4. **Pull Request:** Submit PR from Branch to `main`

**Create PR using doit (recommended):**
```bash
# Interactive: Opens $EDITOR with template
doit pr

# Non-interactive: For AI agents or scripts
doit pr --title="feat: add export" --body-file=pr.md
doit pr --title="feat: add export" --body="## Description\n..."

# Create as draft
doit pr --draft
```

Features:
- Auto-detects issue number from branch name (e.g., `feat/42-description` → `Closes #42`)
- Pre-fills the PR template with detected issue
- Validates required fields before creating

**PR Title:**
- Must follow conventional commit format: `<type>: <subject>`
- PR title becomes the merge commit message
- Examples: ✅ `feat: add validators`, ❌ `Add validators`

**PR Description Requirements (enforced by CI):**
- Minimum 50 characters
- Reference related issue: "Closes #42" or "Part of #42"
- Describe what changed and why
- Include testing information

#### 5. **Merge:** Format Must Include PR and Issue Numbers

**When PR completes the issue:**
```
<type>: <subject> (merges PR #XX, closes #YY)
```

**When PR is part of multi-PR issue:**
```
<type>: <subject> (merges PR #XX, part of #YY)
```

**Examples - Correct:**
```
feat: add user authentication (merges PR #18, closes #42)
fix: handle None values (merges PR #23, closes #19)
docs: update installation guide (merges PR #29, closes #25)
```

**Examples - Incorrect:**
```
❌ Merge pull request #18 from user/branch
❌ feat: Add Feature (capitalized subject)
❌ added feature (missing type)
❌ feat: add feature (missing PR reference)
```

### Edge Cases

**Issue needs to be split during work:**
- Create new issues for discovered separate concerns
- Update original issue to reference the new issues
- Continue work on current branch or create new branches

**Issue is obsolete or duplicate:**
- Comment explaining why it's obsolete/duplicate
- Link to the duplicate issue if applicable
- Close with appropriate label (duplicate, wontfix)
- Delete branch if no work committed

**Work spans multiple sessions:**
- Update issue with progress comments
- Document decisions and approaches tried
- Push commits regularly
- Keep PR description updated

### Keeping Your Fork Updated

```bash
# Add upstream remote (one-time setup)
git remote add upstream https://github.com/original-owner/package_name.git

# Fetch and merge upstream changes
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

## Questions?

If you have questions:

1. Check the [README.md](README.md) and [AGENTS.md](AGENTS.md)
2. Search existing [Issues](https://github.com/username/package_name/issues)
3. Open a new issue with the "question" label
4. Join our discussions (if available)

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

For more detailed information, see:
- [README.md](../README.md) - Project overview
- [AGENTS.md](../AGENTS.md) - Development guide for AI agents
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community guidelines
- [SECURITY.md](SECURITY.md) - Security policy

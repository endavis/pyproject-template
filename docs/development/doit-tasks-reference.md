---
title: Doit Tasks Reference
description: Complete reference for all doit automation tasks
audience:
  - users
  - contributors
tags:
  - doit
  - automation
  - reference
---

# Doit Tasks Reference

Complete reference for all available `doit` tasks in this project template.

## Quick Reference

```bash
# List all available tasks
doit list

# Get help for a specific task
doit help <task_name>

# Run a task
doit <task_name>
```

## Task Categories

| Category | Tasks | Description |
|----------|-------|-------------|
| [Testing](#testing-tasks) | `test`, `coverage` | Run tests and coverage |
| [Benchmarking](#benchmarking-tasks) | `benchmark`, `benchmark_save`, `benchmark_compare` | Performance benchmarks |
| [Code Quality](#code-quality-tasks) | `format`, `lint`, `type_check`, `check` | Code formatting and linting |
| [Code Analysis](#code-analysis-tasks) | `complexity`, `maintainability`, `deadcode` | Code metrics and analysis |
| [Security](#security-tasks) | `security`, `audit`, `licenses` | Security scanning |
| [Documentation](#documentation-tasks) | `docs_serve`, `docs_build`, `docs_deploy`, `docs_toc` | Documentation management |
| [Dependencies](#dependency-tasks) | `install`, `install_dev`, `update_deps` | Package management |
| [GitHub Workflow](#github-workflow-tasks) | `issue`, `pr`, `pr_merge`, `adr` | Issue and PR management |
| [Release](#release-tasks) | `release`, `release_dev`, `release_pr`, `release_tag`, `publish` | Version and release management |
| [Version](#version-tasks) | `bump`, `changelog` | Version bumping and changelog |
| [Setup](#setup-tasks) | `pre_commit_install`, `completions`, `install_direnv` | Development environment |
| [Maintenance](#maintenance-tasks) | `cleanup`, `template_clean` | Project cleanup |

---

## Testing Tasks

### `test`

Run pytest with parallel execution for faster test runs.

```bash
doit test
```

**What it does:**
- Runs `pytest -n auto -v` for parallel test execution
- Uses all available CPU cores

**Equivalent command:**
```bash
uv run pytest -n auto -v
```

### `coverage`

Run tests with coverage reporting.

```bash
doit coverage
```

**What it does:**
- Runs pytest with coverage tracking (parallel execution disabled for accuracy)
- Generates terminal, HTML, and XML coverage reports
- Reports are saved to `tmp/` directory

**Equivalent command:**
```bash
uv run pytest --cov=src --cov-report=term-missing --cov-report=html:tmp/htmlcov --cov-report=xml:tmp/coverage.xml -v
```

**Output locations:**
- Terminal: Shows coverage summary with missing lines
- HTML: `tmp/htmlcov/index.html`
- XML: `tmp/coverage.xml`

---

## Benchmarking Tasks

### `benchmark`

Run performance benchmarks.

```bash
doit benchmark
```

**What it does:**
- Runs pytest on `tests/benchmarks/` with `--benchmark-enable --benchmark-only`
- Benchmarks are disabled by default during normal test runs

**Equivalent command:**
```bash
uv run pytest tests/benchmarks/ --benchmark-enable --benchmark-only -v
```

### `benchmark_save`

Run benchmarks and save results as a baseline.

```bash
doit benchmark_save
```

**What it does:**
- Runs benchmarks and saves results to `tmp/benchmarks/`
- Saved baseline can be used for comparison with `benchmark_compare`

**Equivalent command:**
```bash
uv run pytest tests/benchmarks/ --benchmark-enable --benchmark-only --benchmark-save=baseline --benchmark-storage=tmp/benchmarks -v
```

### `benchmark_compare`

Run benchmarks and compare against a saved baseline.

```bash
doit benchmark_compare
```

**What it does:**
- Runs benchmarks and compares results against the saved baseline
- Shows performance regressions or improvements

**Equivalent command:**
```bash
uv run pytest tests/benchmarks/ --benchmark-enable --benchmark-only --benchmark-compare=0001_baseline --benchmark-storage=tmp/benchmarks -v
```

---

## Code Quality Tasks

### `format`

Format code with ruff.

```bash
doit format
```

**What it does:**
- Runs `ruff format` to format Python code
- Runs `ruff check --fix` to auto-fix linting issues

**Equivalent command:**
```bash
uv run ruff format src/ tests/
uv run ruff check --fix src/ tests/
```

### `format_check`

Check code formatting without making changes.

```bash
doit format_check
```

**What it does:**
- Checks if code is properly formatted (CI mode)
- Returns non-zero exit code if formatting is needed

**Equivalent command:**
```bash
uv run ruff format --check src/ tests/
```

### `lint`

Run ruff linting checks.

```bash
doit lint
```

**What it does:**
- Runs ruff linter on source and test code
- Reports violations without auto-fixing

**Equivalent command:**
```bash
uv run ruff check src/ tests/
```

### `type_check`

Run mypy type checking.

```bash
doit type_check
```

**What it does:**
- Runs mypy on `src/` directory
- Uses configuration from `pyproject.toml`

**Equivalent command:**
```bash
uv run mypy src/
```

### `check`

Run all quality checks in sequence.

```bash
doit check
```

**What it does:**
- Runs format check, lint, type check, security, spelling, and tests
- Stops on first failure

**Task dependencies:**
- `format_check`
- `lint`
- `type_check`
- `security` (if available)
- `spell_check`
- `test`

### `spell_check`

Check spelling in code and documentation.

```bash
doit spell_check
```

**What it does:**
- Runs codespell on all text files
- Uses configuration from `pyproject.toml` `[tool.codespell]`

**Configuration example:**
```toml
[tool.codespell]
skip = ".git,*.lock,tmp,htmlcov"
ignore-words-list = "crate"
```

### `fmt_pyproject`

Format `pyproject.toml` with pyproject-fmt.

```bash
doit fmt_pyproject
```

**What it does:**
- Formats and validates pyproject.toml structure
- Sorts dependencies alphabetically
- Standardizes formatting

---

## Code Analysis Tasks

### `complexity`

Analyze cyclomatic complexity with radon.

```bash
doit complexity
```

**What it does:**
- Analyzes all Python files for cyclomatic complexity
- Reports functions/methods with complexity grades (A-F)
- Grade A (1-5) is best, F (41+) indicates highly complex code

**Interpretation:**

| Grade | CC Score | Risk Level |
|-------|----------|------------|
| A | 1-5 | Low - simple, easy to test |
| B | 6-10 | Low - slightly complex |
| C | 11-20 | Moderate - more difficult to test |
| D | 21-30 | High - difficult to test |
| E | 31-40 | Very high - untestable |
| F | 41+ | Extremely high - error-prone |

**Target:** Keep all functions at grade B or better (CC ≤ 10).

**Equivalent command:**
```bash
uv run radon cc src/ -a -s
```

### `maintainability`

Analyze maintainability index with radon.

```bash
doit maintainability
```

**What it does:**
- Calculates maintainability index for all modules
- Higher scores indicate more maintainable code

**Interpretation:**

| Grade | MI Score | Meaning |
|-------|----------|---------|
| A | 20-100 | Highly maintainable |
| B | 10-19 | Moderately maintainable |
| C | 0-9 | Difficult to maintain |

**Target:** Keep all modules at grade A (MI ≥ 20).

**Equivalent command:**
```bash
uv run radon mi src/ -s
```

### `deadcode`

Detect unused code with vulture.

```bash
doit deadcode
```

**What it does:**
- Scans for unused functions, variables, imports, and classes
- Uses configuration from `pyproject.toml` `[tool.vulture]`
- Reports findings with confidence scores

**Configuration example:**
```toml
[tool.vulture]
min_confidence = 80
paths = ["src", "tests"]
ignore_names = ["test_*"]
ignore_decorators = ["@pytest.fixture"]
```

**Handling false positives:**
- Add to `ignore_names` in pyproject.toml
- Add to `ignore_decorators` for framework-specific patterns
- Use a whitelist file for complex cases

See [Coding Standards - Dead Code Detection](coding-standards.md#dead-code-detection) for details.

---

## Security Tasks

### `security`

Run static security analysis with bandit.

```bash
doit security
```

**What it does:**
- Scans Python code for security vulnerabilities
- Uses configuration from `pyproject.toml` `[tool.bandit]`
- Excludes tests, tmp, and .venv directories

**Requires:** `[security]` extras installed (`uv sync --extra security`)

### `audit`

Run dependency vulnerability audit with pip-audit.

```bash
doit audit
```

**What it does:**
- Scans all dependencies for known CVE vulnerabilities
- Reports any security advisories

**Requires:** `[security]` extras installed (`uv sync --extra security`)

### `licenses`

Check licenses of all dependencies.

```bash
doit licenses
```

**What it does:**
- Lists all dependency licenses for compliance review
- Outputs in markdown table format

**Requires:** `[security]` extras installed (`uv sync --extra security`)

---

## Documentation Tasks

### `docs_serve`

Serve documentation locally with live reload.

```bash
doit docs_serve
```

**What it does:**
- Starts MkDocs development server
- Watches for file changes and auto-reloads
- Available at http://127.0.0.1:8000

**Equivalent command:**
```bash
uv run mkdocs serve
```

### `docs_build`

Build static documentation site.

```bash
doit docs_build
```

**What it does:**
- Builds documentation to `site/` directory
- Ready for deployment

**Equivalent command:**
```bash
uv run mkdocs build
```

### `docs_deploy`

Deploy documentation to GitHub Pages.

```bash
doit docs_deploy
```

**What it does:**
- Builds documentation
- Pushes to `gh-pages` branch
- Requires GitHub Pages enabled in repository settings

**Equivalent command:**
```bash
uv run mkdocs gh-deploy
```

### `docs_toc`

Generate documentation table of contents.

```bash
doit docs_toc
```

**What it does:**
- Runs `tools/generate_doc_toc.py`
- Generates `docs/TABLE_OF_CONTENTS.md` from frontmatter
- Automatically runs as a pre-commit hook when docs change

---

## Dependency Tasks

### `install`

Install package with dependencies.

```bash
doit install
```

**What it does:**
- Syncs dependencies from lock file
- Installs package in editable mode

**Equivalent command:**
```bash
uv sync
```

### `install_dev`

Install package with development dependencies.

```bash
doit install_dev
```

**What it does:**
- Syncs all dependencies including dev extras
- Installs pre-commit hooks
- Marks `src/package_name/_version.py` as assume-unchanged so the version file regenerated by setuptools-scm does not appear as modified in `git status`

**Equivalent command:**
```bash
uv sync --all-extras --dev
uv run pre-commit install
git update-index --assume-unchanged src/package_name/_version.py
```

> **Note:** To undo the assume-unchanged flag, run:
> `git update-index --no-assume-unchanged src/package_name/_version.py`

### `update_deps`

Update dependencies and verify with tests.

```bash
doit update_deps
```

**What it does:**
1. Updates all dependencies to latest compatible versions
2. Regenerates lock file
3. Runs test suite to verify nothing broke

**When to use:**
- Periodically to get security updates
- Before releases to ensure latest dependencies work
- After adding new dependencies

**Equivalent commands:**
```bash
uv lock --upgrade
uv sync --all-extras --dev
uv run pytest
```

---

## GitHub Workflow Tasks

### `issue`

Create a GitHub issue from a template.

```bash
# Interactive mode (opens $EDITOR)
doit issue --type=feature

# Non-interactive mode (for scripts/AI)
doit issue --type=feature --title="Add feature" --body="## Problem\n..."
doit issue --type=bug --title="Fix bug" --body-file=issue.md
```

**Issue types:**
- `feature` - New feature request
- `bug` - Bug report
- `refactor` - Code refactoring
- `doc` - Documentation improvement
- `chore` - Maintenance task

**Options:**
- `--type` (required): Issue type
- `--title`: Issue title (non-interactive)
- `--body`: Issue body content (non-interactive)
- `--body-file`: File containing issue body (non-interactive)

### `pr`

Create a pull request from a template.

```bash
# Interactive mode (opens $EDITOR)
doit pr

# Non-interactive mode
doit pr --title="feat: add feature" --body="## Description\n..."
doit pr --title="fix: bug fix" --body-file=pr.md

# Create draft PR
doit pr --draft
```

**Features:**
- Auto-detects issue number from branch name (e.g., `feat/42-add-feature`)
- Pre-fills template with branch information
- Validates required fields

**Options:**
- `--title`: PR title (non-interactive)
- `--body`: PR body content (non-interactive)
- `--body-file`: File containing PR body (non-interactive)
- `--draft`: Create as draft PR

### `pr_merge`

Merge a pull request with properly formatted commit message.

```bash
# Merge PR for current branch
doit pr_merge

# Merge specific PR
doit pr_merge --pr=123
```

**What it does:**
1. Finds PR associated with current branch (or uses `--pr`)
2. Validates PR is approved and checks pass
3. Merges with conventional commit format: `<type>: <subject> (merges PR #XX, addresses #YY)`

**Options:**
- `--pr`: PR number to merge (defaults to PR for current branch)

### `adr`

Create an Architecture Decision Record.

```bash
# Interactive mode
doit adr

# Non-interactive mode
doit adr --title="Use Redis for caching" --body="## Status\nAccepted\n..."
doit adr --title="Use Redis" --body-file=adr.md
```

**What it does:**
- Creates a new ADR in `docs/decisions/`
- Auto-numbers based on existing ADRs
- Uses ADR template format

**Options:**
- `--title`: ADR title (non-interactive)
- `--body`: ADR body content (non-interactive)
- `--body-file`: File containing ADR body (non-interactive)

See [ADR Documentation](../decisions/README.md) for more information.

---

## Release Tasks

### `release`

Create a production release (full workflow).

```bash
doit release
```

**What it does:**
1. Verifies you're on `main` branch
2. Checks for uncommitted changes
3. Pulls latest changes
4. Runs governance validations (merge commit format, issue links)
5. Runs all quality checks (`doit check`)
6. Uses commitizen to bump version and update CHANGELOG.md
7. Creates git tag
8. Pushes commits and tags to trigger CI/CD

**Requirements:**
- Must be on `main` branch
- No uncommitted changes
- All checks must pass

See [Release Automation](release-and-automation.md) for details.

### `release_dev`

Create a pre-release for TestPyPI testing.

```bash
# Create alpha (default)
doit release_dev

# Create beta
doit release_dev --type=beta

# Create release candidate
doit release_dev --type=rc
```

**What it does:**
1. Verifies branch (warns if not on main)
2. Runs quality checks
3. Creates pre-release tag (e.g., `v1.0.0-alpha.1`)
4. Pushes to trigger TestPyPI publish

**Options:**
- `--type`: Pre-release type (`alpha`, `beta`, `rc`)

### `release_pr`

Create a release PR with changelog updates.

```bash
doit release_pr
```

**What it does:**
- Creates a PR that includes version bump and changelog updates
- Used for PR-based release workflows
- Alternative to direct `doit release`

### `release_tag`

Tag a release after a release PR is merged.

```bash
doit release_tag
```

**What it does:**
- Creates the release tag after `release_pr` is merged
- Triggers CI/CD to build and publish

### `publish`

Build and publish package to PyPI.

```bash
doit publish
```

**What it does:**
1. Builds package (`uv build`)
2. Publishes to PyPI (`uv publish`)

**Requirements:**
- PyPI credentials configured
- Package must build successfully

**Note:** Typically triggered by CI/CD after release tag is pushed, not run manually.

---

## Version Tasks

### `bump`

Bump version based on conventional commits.

```bash
doit bump
```

**What it does:**
- Analyzes commits since last tag
- Determines version bump (major/minor/patch) from commit types
- Updates version according to semantic versioning

**Commit type → Version bump:**
- `feat!` or `BREAKING CHANGE` → Major
- `feat` → Minor
- `fix`, `refactor`, `perf` → Patch

### `changelog`

Generate CHANGELOG from conventional commits.

```bash
doit changelog
```

**What it does:**
- Generates/updates `CHANGELOG.md` from commit history
- Groups changes by type (Features, Bug Fixes, etc.)
- Uses commitizen for generation

---

## Setup Tasks

### `pre_commit_install`

Install pre-commit hooks.

```bash
doit pre_commit_install
```

**What it does:**
- Installs pre-commit hooks to `.git/hooks/`
- Hooks run automatically on `git commit`

**Equivalent command:**
```bash
uv run pre-commit install
```

### `pre_commit_run`

Run pre-commit on all files.

```bash
doit pre_commit_run
```

**What it does:**
- Runs all pre-commit hooks on all files
- Useful for checking entire codebase

**Equivalent command:**
```bash
uv run pre-commit run --all-files
```

### `completions`

Generate shell completion scripts.

```bash
doit completions
```

**What it does:**
- Generates completion scripts in `completions/` directory
- Creates `doit.bash` and `doit.zsh`

**Output:**
- `completions/doit.bash` - Bash completions
- `completions/doit.zsh` - Zsh completions

### `completions_install`

Install shell completions to your shell config.

```bash
doit completions_install
```

**What it does:**
1. Generates completion scripts
2. Adds source lines to `~/.bashrc` and/or `~/.zshrc`
3. Completions activate on next shell session

**After installation:**
```bash
source ~/.bashrc   # For Bash
source ~/.zshrc    # For Zsh
```

### `install_direnv`

Install direnv for automatic environment loading.

```bash
doit install_direnv
```

**What it does:**
- Installs direnv if not present
- Provides instructions for shell integration

**After installation:**
```bash
# Add to shell config (one-time)
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# Allow direnv in project
direnv allow
```

### `commit`

Interactive commit with commitizen.

```bash
doit commit
```

**What it does:**
- Opens interactive commit prompt
- Ensures conventional commit format
- Guides through commit message creation

**Equivalent command:**
```bash
uv run cz commit
```

---

## Maintenance Tasks

### `cleanup`

Clean build and cache artifacts (deep clean).

```bash
doit cleanup
```

**What it does:**
- Removes `build/`, `dist/`, `*.egg-info/`
- Removes `__pycache__/` directories
- Removes `tmp/` directory
- Removes `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`

### `template_clean`

Remove template-specific files after project setup.

```bash
# Remove setup files only (keep update checking)
doit template_clean --setup

# Remove all template files
doit template_clean --all

# Preview what would be deleted
doit template_clean --dry-run
```

**Setup mode (`--setup`)** removes:
- `bootstrap.py`
- `tools/pyproject_template/setup_repo.py`
- `tools/pyproject_template/migrate_existing_project.py`
- `docs/template/new-project.md`
- `docs/template/migration.md`

**All mode (`--all`)** removes:
- All setup files (above)
- `tools/pyproject_template/` directory
- `docs/template/` directory
- `.config/pyproject_template/` directory

**Options:**
- `--setup`: Remove setup files only
- `--all`: Remove all template files
- `--dry-run`: Show what would be deleted

See [Template Tools Reference](../template/tools-reference.md#cleanuppy) for details.

### `build`

Build the package.

```bash
doit build
```

**What it does:**
- Builds source distribution and wheel
- Output in `dist/` directory

**Equivalent command:**
```bash
uv build
```

---

## Pre-commit Hooks

The following hooks run automatically on `git commit`:

| Hook | Purpose |
|------|---------|
| `ruff` | Lint and auto-fix Python code |
| `ruff-format` | Format Python code |
| `mypy` | Type checking |
| `bandit` | Security scanning (if installed) |
| `codespell` | Spell checking |
| `check-branch-name` | Enforce branch naming convention |
| `generate-doc-toc` | Update documentation TOC |
| `no-commit-to-main` | Prevent direct commits to main |
| `no-local-config` | Prevent committing local config files |
| `protect-dynamic-version` | Protect version configuration |
| `conventional-pre-commit` | Enforce conventional commit format |

### Dynamic Version Protection

The `protect-dynamic-version` hook prevents accidental changes to the `dynamic` field in `pyproject.toml`. This ensures version management remains git-tag-based.

**What it blocks:**
- Any changes to the `dynamic = ["version"]` line

**Why this matters:**
- Version is derived from git tags via hatch-vcs
- Modifying this breaks automated versioning
- See [Release Automation](release-and-automation.md#automated-versioning) for details

---

## See Also

- [Usage Guide](../usage/basics.md) - Development workflows
- [Release Automation](release-and-automation.md) - Release process details
- [Coding Standards](coding-standards.md) - Code quality guidelines
- [CI/CD Testing](ci-cd-testing.md) - Continuous integration

---

[Back to Documentation Index](../TABLE_OF_CONTENTS.md)

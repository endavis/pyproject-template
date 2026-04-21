---
title: Release Automation & Security
description: Automated versioning, release management, and security tooling
audience:
  - contributors
  - maintainers
tags:
  - release
  - security
  - automation
---

# Release Automation & Security

This guide covers automated versioning, release management, governance validation, and security tooling available in this Python project template.

## Table of Contents
- [Automated Versioning](#automated-versioning)
- [Release Management](#release-management)
- [Release Notes](#release-notes)
- [PR Merging](#pr-merging)
- [Security & Quality Tasks](#security-quality-tasks)
- [SBOM Generation](#sbom-generation)
- [Governance Validation](#governance-validation)
- [Environment Configuration](#environment-configuration)

## Automated Versioning

This template uses **hatch-vcs** for automated, git tag-based versioning. Version numbers are derived from git tags - no manual edits to `pyproject.toml` or `_version.py` are required.

### How It Works

- **Git Tags**: Version source of truth (e.g., `v0.1.0`, `v1.0.0`)
- **Automatic Generation**: The `_version.py` file is auto-generated during builds
- **Dynamic Versioning**: Version is set to `dynamic = ["version"]` in `pyproject.toml`

### Version Formats

```bash
# Production releases
v1.0.0         # Major release
v1.1.0         # Minor release (new features)
v1.1.1         # Patch release (bug fixes)

# Pre-releases (for TestPyPI)
v1.0.0-alpha.1   # Alpha release
v1.0.0-beta.1    # Beta release
v1.0.0-rc.1      # Release candidate
```

### Checking Current Version

```bash
# From installed package (replace 'your-package' with your package name)
uv run python -c "from importlib.metadata import version; print(version('your-package'))"

# Development version (shows git-based dev version)
# Example output: 0.0.1.dev519+g295cc7b6b.d20251229
```

## Release Management

Releases follow a single PR-based flow powered by **commitizen**. The
changelog and version bump are reviewed in a pull request; after the PR
merges, a lightweight tagging step triggers the publish workflow. Direct-to-
`main` release commands are not supported — they are incompatible with the
template-default `no-commit-to-main` hook.

### Release Flow

```bash
# Step 1: open a release PR (production or pre-release)
uv run doit release [--prerelease=alpha|beta|rc] [--increment=MAJOR|MINOR|PATCH]

# --> reviewer merges the PR --

# Step 2: tag main and trigger publish
uv run doit release_tag
```

Both commands must be run from `main` with a clean working tree.
`--prerelease` and `--increment` are mutually exclusive on `doit release`.

### Step 1: Create the release PR (`doit release`)

`doit release` determines the next version, creates a `release/vX.Y.Z`
branch, updates `CHANGELOG.md`, and opens a PR for review.

```bash
# Auto-detect the next version from conventional commits
uv run doit release

# Force a specific increment
uv run doit release --increment=major   # 1.0.0 → 2.0.0
uv run doit release --increment=minor   # 1.0.0 → 1.1.0
uv run doit release --increment=patch   # 1.0.0 → 1.0.1

# Open a pre-release PR (TestPyPI)
uv run doit release --prerelease=alpha  # 1.0.0 → 1.0.1a0
uv run doit release --prerelease=beta
uv run doit release --prerelease=rc
```

**What it does:**

1. ✅ Verifies you're on the `main` branch
2. ✅ Validates `--prerelease` (must be empty, `alpha`, `beta`, or `rc`)
3. ✅ Rejects `--prerelease` combined with `--increment` (mutually exclusive)
4. ✅ Checks for uncommitted changes
5. ✅ Pulls latest changes from remote
6. ✅ **Runs governance validations** (merge commit format, issue links)
7. ✅ Runs all quality checks (`doit check`)
8. ✅ Asks commitizen for the next version (`cz bump --get-next`)
9. ✅ Creates a `release/vX.Y.Z` branch
10. ✅ Updates `CHANGELOG.md` and commits it
11. ✅ Pushes the branch and opens a PR titled `release: vX.Y.Z`

The PR can be reviewed, discussed, and approved like any other change.

### Step 2: Tag the release (`doit release_tag`)

After the release PR is merged to `main`:

```bash
git checkout main
git pull
uv run doit release_tag
```

**What it does:**

1. ✅ Verifies you're on the `main` branch
2. ✅ Pulls latest changes
3. ✅ Finds the most recently merged `release: vX.Y.Z` PR
4. ✅ Extracts the version from the PR title (falls back to the branch name)
5. ✅ Creates the git tag `vX.Y.Z` on `main`
6. ✅ Pushes the tag, which triggers the publish workflow

### Pre-releases (TestPyPI)

Pass `--prerelease=<type>` to `doit release` to open a pre-release PR:

| Type | Use when |
| --- | --- |
| `alpha` | Early, unstable snapshots for internal testing |
| `beta` | Feature-complete but not yet stable |
| `rc` | Release candidate; only fixes expected before the final release |

Pre-release tags (e.g. `v1.2.0a0`, `v1.2.0-rc.1`) trigger the TestPyPI publish
workflow; production tags (e.g. `v1.2.0`) trigger TestPyPI followed by PyPI.
See the [Workflow Triggers](../../.github/CONTRIBUTING.md#workflow-triggers)
table in `CONTRIBUTING.md` for the full mapping.

### Example Release Cycle

```bash
# 1. Develop features with conventional commits on feature branches
git commit -m "feat: add new feature (#99)"
git commit -m "fix: resolve bug (#100)"

# 2. Cut an alpha for internal testing
uv run doit release --prerelease=alpha
# --> Opens PR "release: v0.2.0a0"
# --> Reviewer merges the PR
uv run doit release_tag
# --> Tag v0.2.0a0 pushed; TestPyPI publish triggered

# 3. Install from TestPyPI for testing
pip install --index-url https://test.pypi.org/simple/ your-package==0.2.0a0

# 4. Fix issues and cut a beta
git commit -m "fix: address alpha feedback (#101)"
uv run doit release --prerelease=beta
# --> ... merge PR, tag, publish to TestPyPI ...

# 5. Cut the final release
uv run doit release
# --> Opens PR "release: v0.2.0", reviewer merges
uv run doit release_tag
# --> Tag v0.2.0 pushed; publish workflow runs TestPyPI → PyPI
```

## Release Notes

Release notes are automatically generated from merged pull requests when a GitHub release is created. The release workflow creates a GitHub release with auto-generated notes after publishing to PyPI.

### How It Works

1. When a version tag (e.g., `v1.0.0`) is pushed, the release workflow runs
2. After the package is published to PyPI, the `github-release` job creates a GitHub release
3. GitHub generates release notes by categorizing merged PRs since the last release
4. SBOM files are attached to the release as downloadable assets

### Category Configuration

PR labels and conventional commit prefixes are mapped to release note sections in `.github/release.yml`:

| Section | Labels |
|---------|--------|
| **Breaking Changes** | `breaking` |
| **New Features** | `enhancement`, `feat` |
| **Bug Fixes** | `bug`, `fix` |
| **Documentation** | `documentation`, `docs` |
| **Performance** | `performance`, `perf` |
| **Other Changes** | Everything else |

PRs with the `dependencies` or `needs-triage` labels are excluded from release notes.

### Customizing Categories

To add or modify categories, edit `.github/release.yml`:

```yaml
changelog:
  exclude:
    labels:
      - dependencies
      - needs-triage
  categories:
    - title: Breaking Changes
      labels:
        - breaking
    - title: New Features
      labels:
        - enhancement
        - feat
    # Add more categories here
    - title: Other Changes
      labels:
        - "*"
```

Categories are evaluated in order. A PR is placed in the first matching category. The `"*"` wildcard matches any label and serves as a catch-all.

### Further Reading

- [GitHub Docs: Automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
- [GitHub Docs: Configuring automatically generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes#configuring-automatically-generated-release-notes)

## PR Merging

Use `doit pr_merge` to merge pull requests with properly formatted commit messages. This task enforces the merge commit format and provides a consistent workflow.

### Basic Usage

```bash
# Merge PR for current branch
doit pr_merge

# Merge specific PR by number
doit pr_merge --pr=123

# Keep the branch after merge (default deletes it)
doit pr_merge --delete-branch=false

# Automatically close linked issues after merge
doit pr_merge --auto-close
```

### What It Does

1. **Validates PR title** - Ensures the title follows conventional commit format (`<type>: <subject>`)
2. **Extracts linked issues** - Parses PR body for `addresses #XX`
3. **Formats merge commit** - Creates a standardized commit message with PR and issue references
4. **Squash merges** - Uses squash merge to maintain clean history
5. **Deletes branch** - Removes the source branch after merge (default behavior)
6. **Reminds to close issues** - Displays commands to manually close linked issues

### Merge Commit Format

The task automatically formats the merge commit subject:

```
<type>: <subject> (merges PR #XX, addresses #YY)
<type>: <subject> (merges PR #XX)
```

**Examples:**
```
feat: add user authentication (merges PR #102, addresses #99)
fix: resolve parsing error (merges PR #103, addresses #100, #101)
docs: update installation guide (merges PR #104)
refactor: extract helper functions (merges PR #105, addresses #50)
```

### Linking Issues in PRs

In your PR body, use the `Addresses` keyword to link issues:

| Keyword | Effect | Use When |
|---------|--------|----------|
| `Addresses #XX` | Included as `addresses #XX` in merge commit | PR relates to the issue |

**Example PR body:**
```markdown
## Summary
- Add login form component
- Implement session management

Addresses #99

## Test Plan
- [ ] Test login flow
```

### Closing Issues After Merge

By default, issues are **not automatically closed** when using `Addresses`. After merging, `doit pr_merge` prints the `gh issue close` commands so you can close linked issues manually:

```bash
# The task displays these commands after merge
gh issue close 99 --comment "Addressed in PR #102"
gh issue close 100 --comment "Addressed in PR #103"
```

This ensures issues are explicitly closed with a reference to the PR that addressed them.

#### Auto-closing linked issues

Pass `--auto-close` to have `doit pr_merge` run the `gh issue close` commands itself after a successful merge:

```bash
doit pr_merge --auto-close
doit pr_merge --pr=123 --auto-close
```

Each linked issue is closed with the comment `Addressed in PR #XX`, matching the format used in the manual reminder.

### Why Use `doit pr_merge`?

| Direct `gh pr merge` | `doit pr_merge` |
|---------------------|-----------------|
| Default commit message | Enforced format with PR/issue links |
| May not validate title | Validates conventional commit format |
| Manual issue tracking | Extracts and displays linked issues |
| No post-merge guidance | Reminds to close issues |

## Security & Quality Tasks

This template includes comprehensive security scanning and code quality tools.

### Security Tasks

```bash
# Run dependency vulnerability audit (pip-audit)
uv run doit audit

# Run static security analysis (bandit)
uv run doit security

# Check all dependency licenses
uv run doit licenses
```

**Installing Security Tools:**
```bash
# Security tools are optional to keep dev environment lean
uv sync --extra security
```

### Quality Tasks

```bash
# Check spelling in code and docs (codespell)
uv run doit spell_check

# Format pyproject.toml (pyproject-fmt)
uv run doit fmt_pyproject
```

### Task Details

#### `doit audit`
- **Tool**: pip-audit
- **Purpose**: Scans dependencies for known CVE vulnerabilities
- **When**: Run before releases, periodically in CI
- **Example**:
  ```bash
  $ uv run doit audit
  No known vulnerabilities found
  ```

#### `doit security`
- **Tool**: bandit
- **Purpose**: Static security analysis of Python code
- **Configuration**: See `[tool.bandit]` in `pyproject.toml`
- **Excludes**: tests/, tmp/, .venv/
- **Example**:
  ```bash
  $ uv run doit security
  [main]  INFO    profile include tests: None
  [main]  INFO    profile exclude tests: None
  [main]  INFO    running on Python 3.12.0
  Run started
  ...
  Code scanned:
          Total lines of code: 5234
          Total lines skipped: 123
  ```

#### `doit spell_check`
- **Tool**: codespell
- **Purpose**: Catches typos in code, tests, docs, README
- **Configuration**: See `[tool.codespell]` in `pyproject.toml`
- **Example**:
  ```bash
  $ uv run doit spell_check
  # Checks all files for common typos and suggests corrections
  ```

#### `doit fmt_pyproject`
- **Tool**: pyproject-fmt
- **Purpose**: Formats and validates pyproject.toml structure
- **Auto-fixes**: Sorts dependencies, standardizes formatting
- **Example**:
  ```bash
  $ uv run doit fmt_pyproject
  Formatted pyproject.toml
  ```

#### `doit licenses`
- **Tool**: pip-licenses
- **Purpose**: Lists all dependency licenses for compliance
- **Output**: Markdown table by license type
- **Example**:
  ```bash
  $ uv run doit licenses
  | Name         | Version | License     |
  |--------------|---------|-------------|
  | click        | 8.1.7   | BSD-3-Clause|
  | pydantic     | 2.5.0   | MIT         |
  ```

#### `doit sbom`
- **Tool**: cyclonedx-py
- **Purpose**: Generates a Software Bill of Materials (SBOM) in CycloneDX format
- **Output**: `tmp/sbom.json` (JSON) and `tmp/sbom.xml` (XML)
- **Example**:
  ```bash
  $ uv run doit sbom
  # Generates tmp/sbom.json and tmp/sbom.xml
  ```

### SBOM Generation

A **Software Bill of Materials (SBOM)** is a machine-readable inventory of all software components and dependencies in a project. SBOMs are increasingly required for regulatory compliance (e.g., US Executive Order 14028) and are essential for security auditing and supply chain transparency.

#### Why SBOM Matters

- **Compliance**: Many organizations and government agencies require SBOMs for software procurement
- **Security Auditing**: Enables automated vulnerability scanning across all dependencies
- **Supply Chain Transparency**: Provides a complete picture of third-party components
- **Incident Response**: Quickly determine if a newly discovered vulnerability affects your software

#### Local Usage

Generate SBOMs locally using the `doit sbom` task:

```bash
# Install security extras (if not already installed)
uv sync --extra security

# Generate SBOM files
uv run doit sbom
```

This produces two files in the `tmp/` directory:

- `tmp/sbom.json` — CycloneDX JSON format
- `tmp/sbom.xml` — CycloneDX XML format

#### Release Integration

SBOMs are automatically generated and attached to every GitHub release:

1. During the **build** job, `cyclonedx-py` generates both JSON and XML SBOMs
2. The SBOM files are included in the `dist/` artifact alongside wheel and sdist packages
3. After publishing to PyPI, the **github-release** job creates a GitHub release with auto-generated notes and attaches the SBOMs as release assets

Users can download the SBOM from the GitHub release page for any version.

#### Using SBOMs for Vulnerability Scanning

You can feed the generated SBOM into vulnerability scanners for continuous monitoring:

```bash
# Using grype (https://github.com/anchore/grype)
grype sbom:tmp/sbom.json

# Using trivy (https://github.com/aquasecurity/trivy)
trivy sbom tmp/sbom.json

# Using osv-scanner (https://github.com/google/osv-scanner)
osv-scanner --sbom=tmp/sbom.json
```

### Integrating into CI

Add security checks to your CI pipeline:

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v1
      - name: Run security audit
        run: uv run doit audit
      - name: Run bandit scan
        run: uv run doit security
```

## Governance Validation

This template enforces governance rules to ensure code quality and traceability.

### Validation Functions

#### 1. Merge Commit Format Validation

**Purpose**: Ensures all merge commits follow conventional format with PR/issue links.

**Required Format**:
```
<type>: <subject> (merges PR #XX, addresses #YY)
<type>: <subject> (merges PR #XX)
```

**Examples**:
```
✅ feat: add new feature (merges PR #102, addresses #99)
✅ fix: resolve bug (merges PR #103, addresses #100)
✅ docs: update guide (merges PR #104)
✅ refactor: extract utils (merges PR #105, addresses #50)

❌ Add new feature                    # Missing type
❌ feat: add feature                  # Missing PR reference
❌ feat: add feature (PR #102)        # Wrong format
```

See [PR Merging](#pr-merging) for details.

**Valid Types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `perf`

**When It Runs**: During `doit release` (blocks on failure)

#### 2. Issue Link Validation

**Purpose**: Encourages linking commits to issues for better tracking.

**Checks**: All non-docs, non-merge commits should reference an issue (`#123`)

**Examples**:
```
✅ feat: add new feature (#99)
✅ fix: resolve bug addresses #100
✅ docs: update README                # Docs exempt

⚠️ feat: add new feature             # Warning only
```

**When It Runs**: During `doit release` (warning only, doesn't block)

### Pre-commit Hooks

The template includes pre-commit hooks that run on every commit:

```yaml
# .pre-commit-config.yaml
hooks:
  - ruff-format: Auto-format Python code
  - ruff-check: Lint and auto-fix issues
  - mypy: Type checking (strict mode)
  - tests: Run test suite
  - check-branch-name: Enforce branch naming convention
```

**Branch Naming Convention**:
```
✅ issue/99-feature-name
✅ feat/102-add-feature
✅ fix/103-resolve-bug
✅ docs/installation-guide
✅ hotfix/critical-fix
✅ release/v1.0.0
✅ main
✅ develop

❌ my-feature-branch
❌ fix-bug
❌ random-name
```

### Conventional Commits

All commits should follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

**Format**:
```
<type>[(scope)]: <subject>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature (triggers MINOR version bump)
- `fix`: Bug fix (triggers PATCH version bump)
- `refactor`: Code refactoring (triggers PATCH version bump)
- `perf`: Performance improvement (triggers PATCH version bump)
- `docs`: Documentation only
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Breaking Changes** (triggers MAJOR version bump):
```
feat!: redesign API

BREAKING CHANGE: API interface has changed. See migration guide.
```

**Examples**:
```bash
# Feature commit
git commit -m "feat: add new capability (#99)"

# Bug fix commit
git commit -m "fix: resolve parsing issue (#100)"

# Documentation commit
git commit -m "docs: add release guide"

# Breaking change
git commit -m "feat!: redesign plugin system

BREAKING CHANGE: Plugin registration API has changed.
Plugins must now implement the new PluginProtocol interface.
See docs/template/migration.md for upgrade instructions."
```

## Environment Configuration

### Using direnv (Recommended)

This template supports `direnv` for automatic environment management:

```bash
# Install direnv
uv run doit install_direnv

# Hook into your shell (one-time)
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

# Allow direnv in this directory
direnv allow
```

Once configured, direnv automatically:
- Activates the virtual environment
- Sets cache directories (UV_CACHE_DIR, RUFF_CACHE_DIR, etc.)
- Loads project-specific environment variables
- Creates tmp/ directory structure

### Manual Environment Setup

Without direnv:

```bash
# Activate virtual environment
source .venv/bin/activate

# Set cache directories (optional but recommended)
export UV_CACHE_DIR="$(pwd)/tmp/.uv_cache"
export RUFF_CACHE_DIR="$(pwd)/tmp/.ruff_cache"
export MYPY_CACHE_DIR="$(pwd)/tmp/.mypy_cache"
export COVERAGE_FILE="$(pwd)/tmp/.coverage"

# Create tmp directory
mkdir -p tmp
```

### Cache Management

All cache files are stored in `tmp/` to keep the project root clean:

```
tmp/
├── .uv_cache/         # uv package cache
├── .ruff_cache/       # ruff linter cache
├── .mypy_cache/       # mypy type checker cache
├── .coverage          # coverage data
└── htmlcov/           # coverage HTML reports
```

The `tmp/` directory is gitignored and can be safely deleted:

```bash
# Clean all caches
rm -rf tmp/
doit cleanup  # Also removes build artifacts
```

## Quick Reference

### Common Tasks

```bash
# Development
uv run doit format          # Format code
uv run doit lint            # Run linter
uv run doit type_check      # Run mypy
uv run doit test            # Run tests
uv run doit check           # Run all checks

# Security & Quality
uv run doit audit           # Vulnerability scan
uv run doit security        # Security analysis
uv run doit spell_check     # Spell checking
uv run doit licenses        # License compliance
uv run doit sbom            # Generate SBOM (CycloneDX)

# Releases
uv run doit release --prerelease=alpha   # Open a pre-release PR (TestPyPI)
uv run doit release                      # Open a production release PR (PyPI)
uv run doit release_tag                  # Tag main after the release PR is merged
```

### Installation Options

```bash
# Standard development setup
uv sync --dev

# Include security tools
uv sync --dev --extra security

# Include all extras
uv sync --dev --all-extras
```

### Pre-commit

```bash
# Install hooks
doit pre_commit_install

# Run manually on all files
doit pre_commit_run

# Skip hooks (emergency only)
git commit --no-verify
```

## Troubleshooting

### Release Fails: "Not on main branch"

**Problem**: `doit release` requires main branch

**Solution**:
```bash
git checkout main
git pull
uv run doit release
```

### Release Fails: "Uncommitted changes"

**Problem**: Working directory has uncommitted changes

**Solution**:
```bash
git status
git add .
git commit -m "feat: finalize changes before release"
uv run doit release
```

### Governance Validation Fails

**Problem**: Merge commit format doesn't match required pattern

**Solution**: Use `doit pr_merge` which automatically formats the commit message:
```bash
# Merge the PR with proper format
doit pr_merge --pr=102
```

If you need to fix an existing merge commit, use interactive rebase (advanced):
```bash
git rebase -i HEAD~1
# Change 'pick' to 'reword', then edit the message to:
# feat: add new feature (merges PR #102, addresses #99)
```

### Security Task Fails: "pip-audit not installed"

**Problem**: Security tools are optional dependencies

**Solution**:
```bash
uv sync --extra security
uv run doit audit
```

### Spell Check Finds False Positives

**Problem**: Technical terms flagged as typos

**Solution**: Add to ignore list in `pyproject.toml`:
```toml
[tool.codespell]
ignore-words-list = "crate,kubernetes,terraform"
```

## See Also

- [Coding Standards](coding-standards.md) - Code style guidelines
- [CI/CD Testing](ci-cd-testing.md) - Continuous integration setup

---

[Back to Documentation Index](../TABLE_OF_CONTENTS.md)

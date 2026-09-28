# __PROJECT_NAME__

[![CI](https://github.com/__GH_OWNER__/__PACKAGE_NAME__/actions/workflows/ci.yml/badge.svg)](https://github.com/__GH_OWNER__/__PACKAGE_NAME__/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/__GH_OWNER__/__PACKAGE_NAME__/branch/main/graph/badge.svg)](https://codecov.io/gh/__GH_OWNER__/__PACKAGE_NAME__)
[![PyPI version](https://badge.fury.io/py/__PYPI_NAME__.svg)](https://badge.fury.io/py/__PYPI_NAME__)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

__DESCRIPTION__

## Features

- Modern tooling: `uv` for deps, `ruff` for format/lint, `mypy` in strict mode
- CI/CD ready: GitHub Actions for checks, coverage upload, and releases
- Release automation: hatch-vcs + commitizen-driven tagging and changelog

## Installation

```bash
pip install __PYPI_NAME__
```

## Quick Start

```python
from __PACKAGE_NAME__ import greet

# Example usage
message = greet("Python")
print(message)  # Output: Hello, Python!
```

## Documentation

📚 **Full documentation is available in the [docs/](docs/) directory**

Build and view locally:
```bash
doit docs_serve  # Opens at http://127.0.0.1:8000
```

Key documentation files:
- [Installation Guide](docs/getting-started/installation.md) - Setup instructions
- [Usage Guide](docs/usage/basics.md) - Development workflows and commands
- [API Reference](docs/reference/api.md) - Complete API documentation
- [Extensions Guide](docs/development/extensions.md) - Optional tools and extensions

## Development Setup

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [direnv](https://direnv.net/) - Automatic environment variable loading (optional but recommended)

### Quick Start

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/username/package_name.git
cd __PACKAGE_NAME__

# Create virtual environment and install dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
doit pre_commit_install

# Optional: Install direnv for automatic environment management
# macOS:
brew install direnv

# Linux (using doit helper):
doit install_direnv

# Hook direnv into your shell (one-time setup)
# Bash:
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

# Zsh:
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc

# Allow direnv to load .envrc
direnv allow

# Optional: Create .envrc.local for personal overrides
cp .envrc.local.example .envrc.local
```

The development tools, `doit` included, live in the `dev` and `security` extras, and a plain
`uv sync` uninstalls them. Sync again later with `doit install_dev`, which runs the same command.

## Versioning & Releases

This project uses automated versioning and releases powered by `commitizen` and `hatch-vcs`.

- **Single Source of Truth:** The Git tag is the definitive version. `pyproject.toml` and `_version.py` are generated at build time from tags (no manual edits).
- **Versioning Scheme:**
    - **Production:** Standard SemVer (e.g., `v1.0.0`).
    - **Pre-release:** PEP 440, as commitizen writes it (e.g., `v1.0.1a0`, `v1.0.1b0`, `v1.0.1rc0`).

### Creating a Release

A release goes through a pull request. Run both steps from `main`.

**1. Open the release PR:**
```bash
doit release                     # Production release (PyPI)
doit release --prerelease=alpha  # Pre-release (TestPyPI): alpha, beta or rc
```
This automated task will:
1.  Calculate the next version based on conventional commits.
2.  Create a `release/v<version>` branch.
3.  Update `CHANGELOG.md` on it, merging any pre-release entries (commitizen `--merge-prerelease`).
4.  Push the branch and open a PR titled `release: v<version>`.

**2. After the PR merges, tag the release:**
```bash
doit release_tag
```
This tags `main` with `v<version>` and pushes the tag:
- A production tag (e.g., `v1.0.0`) triggers the `release` workflow, which publishes to TestPyPI and then PyPI.
- A pre-release tag (e.g., `v1.0.1a0`) triggers the `testpypi` workflow.

### Environment Variables

This project uses direnv for automatic environment management. After setup:
- `.envrc` (committed) contains project defaults and is loaded automatically
- `.envrc.local` (git-ignored) is for personal overrides and credentials
- Environment variables are set automatically when you enter the project directory
- Virtual environment is activated automatically

### Manual Setup (without direnv)

If you prefer not to use direnv:

```bash
# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Set environment variables manually
export UV_CACHE_DIR="$(pwd)/tmp/.uv_cache"

# Install dependencies
uv sync --all-extras --dev
```

## Available Tasks

View all available tasks:

```bash
doit list
```

### Quick Commands

```bash
# Testing
doit test          # Run tests (parallel execution with pytest-xdist)
doit coverage      # Run tests with coverage report

# Code Quality
doit format        # Format code with ruff
doit lint          # Run linting
doit type_check    # Run type checking with mypy
doit check         # Run ALL checks (format, lint, type check, security, audit, spell, test)

# Security
doit security      # Run security scan with bandit
doit audit         # Run dependency vulnerability audit
doit spell_check   # Check for typos with codespell
doit licenses      # Check licenses of dependencies

# Code Formatting
doit fmt_pyproject # Format pyproject.toml with pyproject-fmt

# Version Management (Commitizen)
doit commit        # Interactive commit with conventional format
doit release       # Open a release PR (--prerelease=alpha|beta|rc for TestPyPI)
doit release_tag   # Tag main after the release PR merges

# Documentation
doit docs_serve    # Serve docs locally with live reload
doit docs_build    # Build documentation site
doit docs_deploy   # Deploy docs to GitHub Pages

# Maintenance
doit cleanup       # Clean build artifacts and caches
doit update_deps   # Update dependencies and run tests
```

See the [Usage Guide](docs/usage/basics.md) for comprehensive documentation of all development workflows.

## Running Tests

```bash
# Run all tests (parallel execution - fast!)
doit test

# Run with coverage
doit coverage

# View coverage report
open tmp/htmlcov/index.html

# Advanced: Run specific test directly
uv run pytest tests/test_example.py::test_version -v
```

## Code Quality

This project includes comprehensive tooling:

### Core Tools
- **uv** - Fast Python package installer and dependency manager
- **ruff** - Extremely fast Python linter and formatter
- **mypy** - Static type checker with strict mode
- **pytest** - Testing framework with parallel execution (pytest-xdist)

### Quality & Security
- **bandit** - Security vulnerability scanner
- **codespell** - Spell checker for code and documentation
- **pip-audit** - Dependency vulnerability auditor
- **pip-licenses** - License compliance checker
- **pre-commit** - Git hooks for automated quality checks
- **pyproject-fmt** - Keep pyproject.toml formatted and organized
- **commitizen** - Enforce conventional commit message standards

### Documentation
- **MkDocs** - Documentation site generator
- **mkdocs-material** - Material Design theme for MkDocs

Run all quality checks:

```bash
doit check
```

### Pre-commit Hooks

Install hooks to run checks automatically before each commit:

```bash
doit pre_commit_install
```

Hooks include:
- Code formatting (ruff)
- Type checking (mypy)
- Security scanning (bandit)
- Spell checking (codespell)
- YAML/TOML validation
- Trailing whitespace removal
- Private key detection

## AI Agent Support

This template supports **Claude Code**, **GitHub Copilot CLI**, **Codex CLI**, and **Antigravity CLI** (`agy`). All four agents ship a complete cross-agent command surface for self-action and cross-agent delegation, with slash names that differ by host: Claude uses colon separators (`/claude:plan`, `/claude:implement`); Copilot and Codex use hyphen separators (`/copilot-review`, `$codex-adversarial-review`) because their command surface is skills and skill names cannot contain colons; Antigravity activates skills by `description:` match with no prefix. The shared workflow is: `/<currentai>:plan → /<currentai>:implement → /ghi-finalize → doit pr_merge --auto-close` (substitute `-` for `:` in Copilot/Codex).

### Requirements

> **Important:** [GitHub CLI (`gh`)](https://cli.github.com/) is **required** for AI-assisted workflows.
>
> Many `doit` tasks use `gh` for issue creation, PR management, and repository operations.
> Install and authenticate before using AI agents:
> ```bash
> # Install (macOS)
> brew install gh
>
> # Install (Linux) - see https://github.com/cli/cli/blob/trunk/docs/install_linux.md
>
> # Authenticate
> gh auth login
> ```

### Features

- **AGENTS.md** - Instructions and protocols for AI agents
- **Dangerous command blocking** - Hooks prevent destructive operations (force push to main, branch deletion, etc.)
- **Workflow automation** - `doit issue` and `doit pr` for GitHub operations

See [AI Agent Setup](docs/development/AI_SETUP.md) and [AI Command Blocking](docs/development/ai/command-blocking.md) for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and checks (`doit check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Add acknowledgments here

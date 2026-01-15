# Package Name

[![CI](https://github.com/username/package_name/actions/workflows/ci.yml/badge.svg)](https://github.com/username/package_name/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/username/package_name/branch/main/graph/badge.svg)](https://codecov.io/gh/username/package_name)
[![PyPI version](https://badge.fury.io/py/package-name.svg)](https://badge.fury.io/py/package-name)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A short description of your package.

## Features

- Modern tooling: `uv` for deps, `ruff` for format/lint, `mypy` in strict mode
- CI/CD ready: GitHub Actions for checks, coverage upload, and releases
- Release automation: hatch-vcs + commitizen-driven tagging and changelog

## Installation

```bash
pip install package-name
```

## Quick Start

```python
from package_name import greet

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
- [Installation Guide](docs/installation.md) - Setup instructions
- [Usage Guide](docs/usage.md) - Development workflows and commands
- [API Reference](docs/api.md) - Complete API documentation
- [Extensions Guide](docs/extensions.md) - Optional tools and extensions

## Quick Setup (Automated)

🚀 **The fastest way to create a new project from this template:**

```bash
curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/bootstrap.py | python3
```

The script will:
- ✅ Create a new repository from this template on GitHub
- ✅ Configure repository settings (merge options, features)
- ✅ Set up branch protection rules
- ✅ Replicate labels
- ✅ Run placeholder replacement automatically
- ✅ Provide a checklist of manual steps (secrets, etc.)

**Requirements:**
- [GitHub CLI](https://cli.github.com/) installed and authenticated (`gh auth login`)
- Git installed
- Python 3.12+

**What you'll need to add manually:**
- PyPI tokens (for publishing packages)
- Codecov token (optional, for coverage reports)
- Collaborators/team access

📖 See [New Project Setup](docs/template/new-project.md) for detailed instructions.

## Using This Template (Manual)

**First time setup:** This is a template repository. If you prefer to clone manually:

```bash
# Clone the template
git clone https://github.com/username/package_name.git my-project
cd my-project

# Run the interactive configuration script
python3 tools/pyproject_template/configure.py
```

The script will prompt you for:
- Project name, description
- Package name (Python import name)
- PyPI package name
- Author name and email
- GitHub username

It will automatically:
- Rename the package directory
- Update all template placeholders
- Self-destruct after completion

📖 See [New Project Setup](docs/template/new-project.md) for detailed instructions and post-setup steps.

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
cd package_name

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

## Versioning & Releases

This project uses automated versioning and releases powered by `commitizen` and `hatch-vcs`.

- **Single Source of Truth:** The Git tag is the definitive version. `pyproject.toml` and `_version.py` are generated at build time from tags (no manual edits).
- **Versioning Scheme:**
    - **Production:** Standard SemVer (e.g., `v1.0.0`).
    - **Development:** SemVer Pre-release (e.g., `v1.0.0-alpha.1`, `v1.0.0-beta.0`).

### Migrating an Existing Project

Bring your existing Python project into this template:

```bash
python tools/pyproject_template/migrate_existing_project.py --target /path/to/your/project
```

The script backs up existing files, copies template tooling/workflows/configs, and prints a summary. After running, complete the migration by configuring placeholders, moving your code, and merging dependencies.

📖 See [Migration Guide](docs/template/migration.md) for the complete step-by-step checklist.

### Keeping Up to Date

Already using this template? Stay in sync with improvements:

```bash
python tools/pyproject_template/check_template_updates.py
```

This compares your project against the latest template and shows what's changed.

📖 See [Keeping Up to Date](docs/template/updates.md) for the update workflow.

### Creating a Release

**Production Release (PyPI):**
```bash
doit release
```
This automated task will:
1.  Calculate the next version based on conventional commits.
2.  Update `CHANGELOG.md`, merging any pre-release entries (commitizen `--merge-prerelease`).
3.  Create a git tag (e.g., `v1.0.0`).
4.  Push commits and tags to GitHub, triggering the `release` workflow.

**Development/Pre-release (TestPyPI):**
```bash
doit release_dev              # Defaults to alpha
doit release_dev --type beta  # Specify type (alpha, beta, rc)
```
This automated task will:
1.  Bump the version to the next pre-release (e.g., `v1.0.0-alpha.1`).
2.  Update `CHANGELOG.md` for the prerelease.
3.  Create a prerelease git tag (e.g., `v1.0.0-alpha.1`).
4.  Push to GitHub, triggering the `testpypi` workflow.

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
doit check         # Run ALL checks (format, lint, type check, test)

# Security
doit security      # Run security scan with bandit
doit audit         # Run dependency vulnerability audit
doit spell_check   # Check for typos with codespell
doit licenses      # Check licenses of dependencies

# Code Formatting
doit fmt_pyproject # Format pyproject.toml with pyproject-fmt

# Version Management (Commitizen)
doit commit        # Interactive commit with conventional format
doit release       # Production release (commitizen-driven)
doit release_dev   # Pre-release/TestPyPI (commitizen-driven)

# Documentation
doit docs_serve    # Serve docs locally with live reload
doit docs_build    # Build documentation site
doit docs_deploy   # Deploy docs to GitHub Pages

# Maintenance
doit cleanup       # Clean build artifacts and caches
doit update_deps   # Update dependencies and run tests
```

See the [Usage Guide](docs/usage.md) for comprehensive documentation of all development workflows.

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

This project includes configuration for AI coding assistants (Claude Code, Gemini CLI, Codex).

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

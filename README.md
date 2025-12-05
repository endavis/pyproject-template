# Package Name

[![CI](https://github.com/username/package_name/workflows/CI/badge.svg)](https://github.com/username/package_name/actions)
[![codecov](https://codecov.io/gh/username/package_name/branch/main/graph/badge.svg)](https://codecov.io/gh/username/package_name)
[![PyPI version](https://badge.fury.io/py/package-name.svg)](https://badge.fury.io/py/package-name)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A short description of your package.

## Features

- Feature 1
- Feature 2
- Feature 3

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

## Using This Template

**First time setup:** This is a template repository. After cloning, run the configuration script to customize it for your project:

```bash
# Clone the template
git clone https://github.com/username/package_name.git my-project
cd my-project

# Run the interactive configuration script
python3 configure.py
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

See the [Installation Guide](docs/installation.md) for detailed setup instructions.

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
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

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
uv pip install -e ".[dev]"
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
doit bump          # Bump version based on commits
doit changelog     # Generate CHANGELOG from commits

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
uv run pytest tests/test_core.py::test_greet_default -v
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

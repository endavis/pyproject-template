---
title: Development Deployment Guide
description: Guide for setting up and running the application in development environments
audience:
  - users
  - contributors
tags:
  - deployment
  - development
  - setup
---

# Development Deployment Guide

This guide covers setting up and running Python applications built with this template in development environments.

## Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd <project-name>

# Install dependencies
uv sync

# Run tests to verify setup
doit test

# Start development
uv run python -m package_name
```

## Environment Setup

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Runtime |
| uv | Latest | Package management |
| git | Latest | Version control |
| Docker | Latest | (Optional) Containerized services |

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### Project Setup

```bash
# Create virtual environment and install dependencies
uv sync

# Install with development dependencies
uv sync --all-extras

# Activate the environment (optional, uv run handles this)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

## Configuration

### Environment Variables

Create a `.env` file for local configuration:

```bash
# Copy the example file
cp .env.example .env

# Edit with your local settings
```

**Common development variables:**

```bash
# .env
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./dev.db
SECRET_KEY=dev-secret-key-not-for-production
```

### Local Configuration Files

The project supports local configuration overrides:

| File | Purpose | Git Status |
|------|---------|------------|
| `.env` | Environment variables | Ignored |
| `.envrc.local` | direnv local overrides | Ignored |
| `settings.local.toml` | Local settings | Ignored |

**Important:** Never commit files containing secrets. These local files are in `.gitignore`.

## Running the Application

### Using uv run

The recommended way to run commands:

```bash
# Run the main module
uv run python -m package_name

# Run a specific script
uv run python scripts/example.py

# Run with arguments
uv run python -m package_name --verbose
```

### Using doit Tasks

```bash
# List all available tasks
doit list

# Run tests
doit test

# Run linting and type checks
doit lint
doit typecheck

# Run all checks
doit check

# Format code
doit fmt
```

### Direct Python Execution

If you've activated the virtual environment:

```bash
# Activate first
source .venv/bin/activate

# Then run directly
python -m package_name
```

## Development Workflow

### Making Changes

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes** and run tests frequently:
   ```bash
   doit test
   ```

3. **Format and lint** before committing:
   ```bash
   doit fmt
   doit check
   ```

4. **Commit** with conventional commit messages:
   ```bash
   git commit -m "feat: add new feature"
   ```

### Running Tests

```bash
# Run all tests
doit test

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_specific.py

# Run tests matching pattern
uv run pytest -k "test_feature"

# Run with verbose output
uv run pytest -v
```

### Debugging

#### VS Code

Add to `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Module",
      "type": "debugpy",
      "request": "launch",
      "module": "package_name",
      "cwd": "${workspaceFolder}",
      "envFile": "${workspaceFolder}/.env"
    },
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "cwd": "${workspaceFolder}",
      "envFile": "${workspaceFolder}/.env"
    }
  ]
}
```

#### PyCharm

1. Go to **Run > Edit Configurations**
2. Add new **Python** configuration
3. Set **Module name**: `package_name`
4. Set **Working directory**: project root
5. Add **Environment variables** from `.env`

#### Command Line Debugging

```bash
# Using pdb
uv run python -m pdb -m package_name

# Using breakpoint() in code
# Add breakpoint() where you want to stop, then run normally
uv run python -m package_name
```

## Local Services

### Using Docker Compose

For services like databases and caches:

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: devdb
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f postgres
```

### SQLite for Development

For simpler setups, use SQLite:

```bash
# .env
DATABASE_URL=sqlite:///./dev.db
```

SQLite requires no external services and is suitable for most development work.

## Code Quality

### Pre-commit Hooks

The project uses pre-commit hooks for quality gates:

```bash
# Install hooks (done automatically by uv sync)
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files

# Skip hooks (use sparingly)
git commit --no-verify -m "WIP: work in progress"
```

### Type Checking

```bash
# Run mypy
doit typecheck

# Or directly
uv run mypy src/
```

### Linting

```bash
# Run ruff linter
doit lint

# Auto-fix issues
uv run ruff check --fix src/
```

### Formatting

```bash
# Format code
doit fmt

# Check format without changing
uv run ruff format --check src/
```

## Troubleshooting

### Common Issues

#### Virtual Environment Not Found

```bash
# Recreate the environment
rm -rf .venv
uv sync
```

#### Import Errors

```bash
# Ensure package is installed in editable mode
uv sync

# Verify installation
uv run python -c "import package_name; print(package_name.__version__)"
```

#### Permission Denied

```bash
# Fix script permissions
chmod +x scripts/*.py

# On Windows, run as administrator or check antivirus
```

#### Pre-commit Hook Failures

```bash
# Update hooks
uv run pre-commit autoupdate

# Run checks to see what's failing
doit check
```

### Environment Issues

#### Wrong Python Version

```bash
# Check current version
python --version

# Use uv to manage Python
uv python install 3.12
uv python use 3.12
```

#### Dependency Conflicts

```bash
# Clear cache and reinstall
uv cache clean
rm -rf .venv uv.lock
uv sync
```

## IDE Setup

### VS Code Extensions

Recommended extensions (`.vscode/extensions.json`):

- `ms-python.python` - Python support
- `ms-python.vscode-pylance` - Type checking
- `charliermarsh.ruff` - Ruff linter/formatter
- `tamasfe.even-better-toml` - TOML support
- `github.copilot` - AI assistance (optional)

### VS Code Settings

Recommended settings (`.vscode/settings.json`):

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },
  "python.analysis.typeCheckingMode": "basic"
}
```

### PyCharm Setup

1. **Set interpreter**: File > Settings > Project > Python Interpreter > Add > Existing Environment > `.venv/bin/python`
2. **Enable ruff**: Install Ruff plugin from marketplace
3. **Configure mypy**: Install Mypy plugin, set to use project's mypy.ini

## Hot Reloading

For web applications or services that support it:

```bash
# Using uvicorn with reload
uv run uvicorn package_name.app:app --reload

# Using Flask debug mode
FLASK_DEBUG=1 uv run flask run

# Using watchfiles for custom scripts
uv run watchfiles "python -m package_name" src/
```

## Performance Profiling

### CPU Profiling

```bash
# Using cProfile
uv run python -m cProfile -o profile.stats -m package_name

# Analyze results
uv run python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"
```

### Memory Profiling

```bash
# Install memory profiler
uv add --dev memory-profiler

# Run with profiling
uv run python -m memory_profiler script.py
```

## Publishing to TestPyPI

TestPyPI is a separate instance of PyPI for testing package publishing without affecting the real index.

### Why Use TestPyPI?

- Test your publishing workflow before production
- Verify package metadata and README rendering
- Catch packaging issues early
- Safe environment for experimentation

### Configure TestPyPI Credentials

Generate a token at https://test.pypi.org/manage/account/token/

```bash
# Set TestPyPI token
export UV_PUBLISH_TOKEN=pypi-xxxxxxxxxxxx
```

### Build and Publish to TestPyPI

```bash
# Build distribution packages
uv build

# Publish to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Or with explicit token
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-xxxxxxxxxxxx
```

### Test Installation from TestPyPI

```bash
# Install from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ package-name

# If your package has dependencies from real PyPI, use both indexes
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ package-name
```

### Verify Package

```bash
# Check the package page
# https://test.pypi.org/project/package-name/

# Verify installation works
uv venv /tmp/test-install
uv pip install --python /tmp/test-install --index-url https://test.pypi.org/simple/ package-name
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Version already exists | Increment version, TestPyPI doesn't allow re-uploads |
| Missing dependencies | Use `--extra-index-url https://pypi.org/simple/` |
| README not rendering | Check pyproject.toml `readme` field, validate markdown |
| Authentication failed | Regenerate token, check URL is correct |

## See Also

- [Installation Guide](../getting-started/installation.md) - Initial project setup
- [Usage Guide](../usage/basics.md) - Package usage patterns
- [Production Deployment Guide](production.md) - Deploying to production
- [CI/CD Testing Guide](../development/ci-cd-testing.md) - Automated pipelines

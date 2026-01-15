# Usage Guide

This guide covers both package usage and development workflows.

## Package Usage

### Basic Usage

```python
from package_name import greet

# Simple greeting
message = greet("World")
print(message)  # Output: Hello, World!

# Custom name
message = greet("Python")
print(message)  # Output: Hello, Python!
```

### API Documentation

See the [API Reference](../reference/api.md) for complete documentation of all available functions and classes.

---

## Development Workflows

This section is for developers working on the project.

### Migration

Coming from an existing project? See the [Migration Guide](../template/migration.md) for step-by-step instructions to adopt this template (configure placeholders, move code to `src/`, update deps, and align CI/release).

### Quick Reference

```bash
# Run tests (parallel)
uv run pytest -n auto -v

# Run all quality checks
uv run doit check

# Format code
uv run doit format

# Build documentation
uv run doit docs_serve
```

### Available Tasks

Use `doit list` to see all available tasks:

```bash
uv run doit list
```

#### Testing Tasks

```bash
# Run tests with parallel execution
uv run doit test
# or directly: uv run pytest -n auto -v

# Run tests with coverage report
uv run doit coverage

# Run specific test file
uv run pytest tests/test_example.py -v

# Run specific test function
uv run pytest tests/test_example.py::test_version -v
```

#### Code Quality Tasks

```bash
# Format code (ruff format + ruff check --fix)
uv run doit format

# Check formatting without changes
uv run doit format_check

# Run linting
uv run doit lint

# Run type checking
uv run doit type_check

# Run all checks (format, lint, type check, test)
uv run doit check
```

#### Security Tasks

```bash
# Run security scan with bandit
uv run doit security

# Run dependency vulnerability audit
uv run doit audit

# Check for typos
uv run doit spell_check
```

#### Documentation Tasks

```bash
# Serve docs locally with live reload (http://127.0.0.1:8000)
uv run doit docs_serve

# Build static documentation site
uv run doit docs_build

# Deploy documentation to GitHub Pages
uv run doit docs_deploy
```

#### Pre-commit Tasks

```bash
# Install pre-commit hooks
uv run doit pre_commit_install

# Run pre-commit on all files
uv run doit pre_commit_run

# Or run pre-commit directly
uv run pre-commit run --all-files
```

#### GitHub Workflow Tasks

```bash
# Create GitHub issue (interactive - opens $EDITOR with template)
uv run doit issue --type=feature    # For new features
uv run doit issue --type=bug        # For bugs and defects
uv run doit issue --type=refactor   # For code refactoring

# Create GitHub issue (non-interactive - for scripts/AI)
uv run doit issue --type=feature --title="Add export" --body-file=issue.md
uv run doit issue --type=feature --title="Add export" --body="## Problem\n..."

# Create Pull Request (interactive - opens $EDITOR with template)
uv run doit pr

# Create Pull Request (non-interactive - for scripts/AI)
uv run doit pr --title="feat: add export" --body-file=pr.md
uv run doit pr --title="feat: add export" --body="## Description\n..."

# Create draft PR
uv run doit pr --draft
```

Features:
- **Interactive mode**: Opens `$EDITOR` with pre-filled template
- **Auto-detection**: Extracts issue number from branch name (e.g., `feat/42-add-feature`)
- **Validation**: Checks required fields before creating issue/PR
- **Non-interactive mode**: Pass `--body` or `--body-file` for AI agents or scripts

### Pre-commit Hooks

The project includes pre-commit hooks that run automatically before each commit:

- **ruff** - Code formatting and linting (auto-fixes issues)
- **mypy** - Type checking (strict mode)
- **bandit** - Security vulnerability scanning
- **codespell** - Spell checking
- **trailing-whitespace** - Remove trailing whitespace
- **end-of-file-fixer** - Ensure files end with newline
- **check-yaml** - Validate YAML syntax
- **check-toml** - Validate TOML syntax
- **check-merge-conflict** - Detect merge conflict markers
- **detect-private-key** - Prevent committing private keys

Install hooks after cloning:

```bash
uv run pre-commit install
```

## Creating Custom doit Tasks

While the template provides standard tasks (test, lint, format, etc.), you'll likely need application-specific tasks for your project. This section shows patterns for extending `dodo.py`.

### Pattern 1: CLI Wrapper Tasks

If your package provides a CLI, create convenience tasks:

```python
# dodo.py
def task_run_server():
    """Start development server."""
    return {
        "actions": ["uv run package-name server --debug --port 8080"],
        "title": title_with_actions,
    }

def task_init_db():
    """Initialize database."""
    return {
        "actions": [
            "uv run package-name db create",
            "uv run package-name db migrate",
            "uv run package-name db seed-dev",
        ],
        "title": title_with_actions,
    }
```

Usage:
```bash
doit run_server
doit init_db
```

### Pattern 2: Environment-Specific Tasks

For applications with multiple deployment environments:

```python
def task_deploy_dev():
    """Deploy to development environment."""
    return {
        "actions": [
            "uv run package-name validate --env dev",
            "uv run package-name deploy --env dev --auto-approve",
        ],
        "title": title_with_actions,
    }

def task_deploy_prod():
    """Deploy to production (with safety checks)."""

    def check_and_deploy():
        console = Console()

        # Safety check
        response = input("Deploy to PRODUCTION? Type 'yes' to confirm: ")
        if response.lower() != "yes":
            console.print("[red]✗ Deployment cancelled[/red]")
            return False

        # Run deployment
        subprocess.run(
            "uv run package-name deploy --env prod",
            shell=True,
            check=True
        )
        console.print("[green]✓ Deployed to production[/green]")

    return {
        "actions": [check_and_deploy],
        "verbosity": 2,
    }
```

### Pattern 3: Integration Test Tasks

For tests requiring external services (databases, APIs, Docker containers):

```python
def task_test_integration():
    """Run integration tests (requires Docker)."""
    return {
        "actions": [
            # Start services
            "docker-compose up -d postgres redis",
            # Wait for services to be ready
            "sleep 5",
            # Run integration tests
            "pytest tests/integration/ -v --maxfail=1",
            # Cleanup (always runs)
            "docker-compose down || true",
        ],
        "title": title_with_actions,
    }

def task_test_e2e():
    """Run end-to-end tests with full stack."""
    return {
        "actions": [
            "docker-compose -f docker-compose.test.yml up --abort-on-container-exit",
            "docker-compose -f docker-compose.test.yml down -v",
        ],
        "title": title_with_actions,
    }
```

### Pattern 4: Data Processing Tasks

For data pipelines, ETL operations, or batch processing:

```python
def task_process_data():
    """Run data processing pipeline."""
    return {
        "actions": [
            "uv run package-name extract --source api --output tmp/raw.json",
            "uv run package-name transform --input tmp/raw.json --output tmp/clean.json",
            "uv run package-name load --input tmp/clean.json --target postgres",
        ],
        "title": title_with_actions,
    }

def task_backup_data():
    """Backup production database."""
    return {
        "actions": [
            "uv run package-name backup create --env prod --output backups/$(date +%Y%m%d-%H%M%S).sql.gz",
        ],
        "title": title_with_actions,
    }

def task_restore_data():
    """Restore from latest backup."""

    def restore_latest():
        import glob
        backups = sorted(glob.glob("backups/*.sql.gz"), reverse=True)
        if not backups:
            print("No backups found!")
            return False

        latest = backups[0]
        print(f"Restoring from: {latest}")
        subprocess.run(
            f"uv run package-name backup restore --file {latest} --env dev",
            shell=True,
            check=True
        )

    return {
        "actions": [restore_latest],
        "title": title_with_actions,
    }
```

### Pattern 5: Dependency Tasks

Tasks that depend on other tasks completing first:

```python
def task_full_check():
    """Run all quality checks before committing."""
    return {
        "actions": [success_message],  # Run after all deps complete
        "task_dep": [
            "format_check",
            "lint",
            "type_check",
            "test",
            "security",
            "spell_check",
        ],
        "title": title_with_actions,
    }

def task_build_all():
    """Build package and documentation."""
    return {
        "actions": [
            lambda: print("✓ All builds complete!"),
        ],
        "task_dep": ["build", "docs_build"],
        "title": title_with_actions,
    }
```

### Pattern 6: Tasks with Parameters

Create tasks that accept arguments:

```python
def task_deploy():
    """Deploy to specified environment."""

    def deploy_to_env(env):
        console = Console()
        console.print(f"[cyan]Deploying to {env}...[/cyan]")

        # Validate environment
        valid_envs = ["dev", "staging", "prod"]
        if env not in valid_envs:
            console.print(f"[red]Invalid environment: {env}[/red]")
            console.print(f"Valid: {', '.join(valid_envs)}")
            return False

        # Deploy
        subprocess.run(
            f"uv run package-name deploy --env {env}",
            shell=True,
            check=True
        )
        console.print(f"[green]✓ Deployed to {env}[/green]")

    return {
        "actions": [CmdAction(deploy_to_env)],
        "params": [
            {
                "name": "env",
                "short": "e",
                "long": "env",
                "default": "dev",
                "help": "Environment to deploy to (dev, staging, prod)",
            }
        ],
        "title": title_with_actions,
    }
```

Usage:
```bash
doit deploy              # Deploys to dev (default)
doit deploy --env staging # Deploys to staging
doit deploy -e prod      # Deploys to prod
```

### Pattern 7: Monitoring and Validation Tasks

Tasks for checking system health, validating configs, or monitoring:

```python
def task_validate_config():
    """Validate all configuration files."""
    return {
        "actions": [
            "uv run package-name config validate --env dev",
            "uv run package-name config validate --env prod",
        ],
        "title": title_with_actions,
    }

def task_health_check():
    """Check health of all services."""
    return {
        "actions": [
            "curl -f http://localhost:8000/health || echo 'Service down!'",
            "uv run package-name db ping",
            "uv run package-name cache status",
        ],
        "title": title_with_actions,
    }
```

### Pattern 8: Code Generation Tasks

For projects that generate code from schemas, templates, or specs:

```python
def task_generate_models():
    """Generate data models from OpenAPI spec."""
    return {
        "actions": [
            "uv run datamodel-codegen --input api-spec.yaml --output src/package_name/models/",
        ],
        "file_dep": ["api-spec.yaml"],
        "targets": ["src/package_name/models/api.py"],
        "title": title_with_actions,
    }

def task_generate_client():
    """Generate API client from specification."""
    return {
        "actions": [
            "openapi-generator generate -i api-spec.yaml -g python -o generated/client/",
        ],
        "file_dep": ["api-spec.yaml"],
        "title": title_with_actions,
    }
```

### Best Practices for Custom Tasks

1. **Descriptive Names**: Use verb-noun format (e.g., `run_server`, `deploy_prod`, `backup_data`)
2. **Clear Docstrings**: They appear in `doit list` - make them helpful
3. **Use title_with_actions**: Shows what's running during execution
4. **Set Verbosity**: For important tasks, set `"verbosity": 2`
5. **Handle Errors**: Use `|| true` for optional steps, or proper error handling in Python functions
6. **Cleanup After Failures**: Use try/finally or `|| cleanup_command` patterns
7. **Group Related Tasks**: Use task dependencies to compose workflows
8. **Document Parameters**: If using params, document them clearly
9. **Validate Inputs**: Check that required files/configs exist before running
10. **Provide Feedback**: Use Rich console or simple prints to show progress

### Example: Complete Custom Task

Here's a complete example combining several patterns:

```python
import os
import subprocess
from pathlib import Path
from rich.console import Console
from doit.action import CmdAction
from doit.tools import title_with_actions

console = Console()

def task_benchmark():
    """Run performance benchmarks and generate report."""

    def run_benchmarks(suite="all"):
        console.print(f"[cyan]Running benchmark suite: {suite}[/cyan]")

        # Validate benchmark suite exists
        benchmark_dir = Path("benchmarks")
        if not benchmark_dir.exists():
            console.print("[red]✗ benchmarks/ directory not found[/red]")
            return False

        # Create output directory
        output_dir = Path("tmp/benchmarks")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Run benchmarks
        cmd = f"uv run pytest benchmarks/test_{suite}.py --benchmark-only --benchmark-json=tmp/benchmarks/results.json"
        result = subprocess.run(cmd, shell=True)

        if result.returncode != 0:
            console.print("[red]✗ Benchmarks failed[/red]")
            return False

        # Generate HTML report
        subprocess.run(
            "uv run pytest-benchmark compare tmp/benchmarks/results.json --html=tmp/benchmarks/report.html",
            shell=True
        )

        console.print("[green]✓ Benchmarks complete[/green]")
        console.print(f"Report: tmp/benchmarks/report.html")

    return {
        "actions": [CmdAction(run_benchmarks)],
        "params": [
            {
                "name": "suite",
                "short": "s",
                "long": "suite",
                "default": "all",
                "help": "Benchmark suite to run (all, api, database, etc.)",
            }
        ],
        "verbosity": 2,
        "title": title_with_actions,
    }
```

Usage:
```bash
doit benchmark                  # Run all benchmarks
doit benchmark --suite api      # Run API benchmarks only
doit list                       # See the task description
```

## Making Changes

1. **Create a branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes**

3. **Format and check**:
   ```bash
   uv run doit format
   uv run doit check
   ```

4. **Commit** (pre-commit hooks run automatically):
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create PR**:
   ```bash
   git push -u origin feature/my-feature
   ```

### Running CI Locally

To run the same checks that CI runs:

```bash
# Format check (what CI runs)
uv run ruff format --check src/ tests/

# Linting
uv run ruff check src/ tests/

# Type checking
uv run mypy src/

# Tests with coverage
uv run pytest --cov=package_name --cov-report=xml:tmp/coverage.xml --cov-report=term -v
```

### Updating Dependencies

```bash
# Show outdated packages
uv pip list --outdated

# Update dependencies and run tests
uv run doit update_deps

# Or manually:
uv pip install --upgrade -e ".[dev,security]"
uv lock
uv run doit check
```

### Building Documentation

#### Local Development

```bash
# Serve with live reload
uv run mkdocs serve

# Or using doit
uv run doit docs_serve
```

Open http://127.0.0.1:8000 in your browser.

#### Switching to Material Theme

The template includes mkdocs-material but uses ReadTheDocs theme by default. To switch:

1. Edit `mkdocs.yml`
2. Change `name: readthedocs` to `name: material`
3. Uncomment the Material theme features
4. Rebuild docs: `uv run doit docs_build`

#### Deploying to GitHub Pages

```bash
# Build and deploy to gh-pages branch
uv run doit docs_deploy
```

This builds the documentation and pushes to the `gh-pages` branch. Enable GitHub Pages in your repository settings to host it.

### Creating a Release

```bash
# Create release tag, changelog, and push (commitizen-powered)
uv run doit release
```

Notes:
- Versions are derived from git tags via hatch-vcs; no manual edits to `pyproject.toml` or `_version.py` are required.
- Use `v*` tags for production (e.g., `v1.0.0`) and prerelease `v*` tags for TestPyPI (e.g., `v1.0.0-alpha.1`). The `doit release` task runs commitizen to choose the next version, update CHANGELOG.md, and create/push the stable `v*` tag; for TestPyPI, run `uv run doit release_dev` to compute the next prerelease via commitizen, create the prerelease `v*` tag, and push.

This will:
1. Verify you're on the main branch
2. Check for uncommitted changes
3. Pull latest changes
4. Run all quality checks
5. Use commitizen to update CHANGELOG.md (merging prerelease entries) and create the `v*` git tag
6. Push the tag
7. Trigger CI/CD to build and publish to PyPI

The release workflow includes:
- ✅ All CI checks (format, lint, type check, tests)
- ✅ Build package artifacts
- ✅ Publish to TestPyPI (for verification)
- ✅ Publish to PyPI (production)

### Environment Configuration

#### Using direnv (Optional)

The project includes `.envrc` for automatic environment setup:

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

#### Manual Environment Setup

Without direnv:

```bash
# Activate virtual environment
source .venv/bin/activate

# Set cache directories (optional)
export UV_CACHE_DIR="$(pwd)/tmp/.uv_cache"
export RUFF_CACHE_DIR="$(pwd)/tmp/.ruff_cache"
export MYPY_CACHE_DIR="$(pwd)/tmp/.mypy_cache"
export COVERAGE_FILE="$(pwd)/tmp/.coverage"
```

### Troubleshooting

#### Tests Failing

```bash
# Run with verbose output
uv run pytest -vv

# Run without parallel execution
uv run pytest -v

# Clear cache and retry
rm -rf .pytest_cache tmp/
uv run pytest -v
```

#### Type Checking Issues

```bash
# Show detailed error information
uv run mypy --show-error-codes --pretty src/

# Check specific file
uv run mypy src/package_name/core.py
```

#### Pre-commit Hook Failures

```bash
# Skip hooks (only when absolutely necessary)
git commit --no-verify -m "message"

# Update pre-commit hooks
uv run pre-commit autoupdate

# Clear pre-commit cache
uv run pre-commit clean
```

#### Clean Build

```bash
# Deep clean all artifacts
uv run doit cleanup

# Remove virtual environment and reinstall
rm -rf .venv
uv venv
uv sync --all-extras --dev
uv run pre-commit install
```

## Best Practices

### Code Style

- Follow PEP 8 (enforced by ruff)
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions small and focused

### Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases and error conditions

### Documentation

- Update docstrings when changing functions
- Add examples for new features
- Update CHANGELOG.md for notable changes
- Keep README.md up to date

### Git Commits

- Use conventional commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- Keep commits atomic and focused
- Write clear commit messages
- Reference issues in commits when applicable

## Next Steps

- Check the [API Reference](../reference/api.md) for complete documentation
- Read [CONTRIBUTING.md](https://github.com/username/package_name/blob/main/.github/CONTRIBUTING.md) for contribution guidelines
- Review the docs and TODOs in this template to identify improvements for your project

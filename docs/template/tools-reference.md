# Template Tools Reference

Complete reference for all template tools in `tools/pyproject_template/`.

> **Note:** For most use cases, the **[Template Manager](manage.md)** (`manage.py`) provides a unified, interactive interface to all these tools. Use this reference for advanced usage, scripting, or understanding the underlying CLI options.

## bootstrap.py

Remote bootstrap script for one-command setup.

### Usage

```bash
curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/bootstrap.py | python3
```

### Description

This is a thin wrapper that downloads and runs `setup_repo.py`. It's designed to be fetched and executed directly from the template repository.

### Requirements

- Python 3.12+
- Internet connection

---

## setup_repo.py

Full repository setup orchestration from the template.

### Usage

```bash
python tools/pyproject_template/setup_repo.py
```

### Description

Automates the complete process of creating a new GitHub repository from this template:

1. Creates repository from template on GitHub
2. Configures repository settings
3. Sets up branch protection rules
4. Replicates labels from template
5. Runs `configure.py` for placeholder replacement
6. Clones repository locally
7. Displays post-setup checklist

### Interactive Prompts

| Prompt | Description |
|--------|-------------|
| Repository name | Name for the new GitHub repository |
| Description | Short project description |
| Visibility | Public or private repository |
| Package name | Python import name (snake_case) |
| Author name | Your name for package metadata |
| Author email | Your email for package metadata |

### Requirements

- GitHub CLI (`gh`) installed and authenticated
- Git installed
- Python 3.12+

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (missing requirements, API failure, etc.) |

---

## configure.py

Replace placeholder values with your project information.

### Usage

```bash
python tools/pyproject_template/configure.py
```

### Description

Interactively prompts for project information and replaces all placeholder values throughout the template files.

### Interactive Prompts

| Prompt | Default | Description |
|--------|---------|-------------|
| Project name | Package Name | Display name for the project |
| Package name | package_name | Python import name (snake_case) |
| PyPI name | package-name | Name on PyPI (typically hyphenated) |
| Author name | Your Name | Author for package metadata |
| Author email | your.email@example.com | Contact email |
| GitHub username | username | Your GitHub username |
| Description | A short description... | One-line project description |

### Files Modified

- `pyproject.toml`
- `README.md`
- `mkdocs.yml`
- `dodo.py`
- `AGENTS.md`
- `CHANGELOG.md`
- `.github/workflows/*`
- `.github/SECURITY.md`
- `docs/*`
- `examples/*`

### Actions Performed

1. Replaces placeholder strings with provided values
2. Renames `src/package_name/` to `src/your_package_name/`
3. Updates all URLs and badge links
4. Updates documentation references

### Requirements

- Python 3.12+
- Must be run from template root directory

---

## migrate_existing_project.py

Copy template scaffolding into an existing repository.

### Usage

```bash
python tools/pyproject_template/migrate_existing_project.py --target /path/to/your/project
```

### Description

Copies template tooling, configuration, and documentation into an existing Python project. Creates backups of any files it overwrites.

### CLI Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--target` | Yes | - | Path to your existing repository |
| `--template` | No | Script's repo | Path to template root |
| `--download` | No | False | Download template instead of using local |
| `--archive-url` | No | GitHub main.zip | URL to template archive |

### Examples

```bash
# Use local template checkout
python tools/pyproject_template/migrate_existing_project.py --target ~/projects/myapp

# Download fresh template
python tools/pyproject_template/migrate_existing_project.py --target ~/projects/myapp --download

# Use specific template archive
python tools/pyproject_template/migrate_existing_project.py \
  --target ~/projects/myapp \
  --archive-url https://github.com/endavis/pyproject-template/archive/refs/tags/v2.0.0.zip
```

### Files Copied

The script copies these template files/directories:

**Configuration & Tooling:**
- `pyproject.toml`
- `dodo.py`
- `.envrc`, `.envrc.local.example`
- `.pre-commit-config.yaml`
- `.python-version`
- `mkdocs.yml`
- `.editorconfig`
- `.gitignore`

**Documentation & Guides:**
- `AGENTS.md`
- `CHANGELOG.md`
- `docs/`
- `examples/`

**Project Scaffolding:**
- `.github/` (workflows, templates)
- `.vscode/`
- `.devcontainer/`
- `.claude/`, `.codex/`, `.gemini/`
- `tools/pyproject_template/`
- `src/package_name/` (template source)
- `tests/` (template tests)

### Backup Behavior

- Creates timestamped backup directory: `backup_YYYYMMDD_HHMMSS/`
- Backs up any existing files before overwriting
- Prints summary of backed up files

### Post-Migration Steps

After running the script:

1. Run `python tools/pyproject_template/configure.py`
2. Move your code into `src/your_package_name/`
3. Merge your dependencies into `pyproject.toml`
4. Run `uv lock` to regenerate lock file
5. Run `doit check` to verify

See [Migration Guide](migration.md) for detailed steps.

---

## check_template_updates.py

Compare your project against the latest template version.

### Usage

```bash
python tools/pyproject_template/check_template_updates.py
```

### Description

Fetches the latest template release (or specified version), compares it against your project, and shows what files differ.

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--template-version` | Latest release | Compare against specific version (e.g., `v2.2.0`) |
| `--skip-changelog` | False | Don't open CHANGELOG.md in editor |
| `--keep-template` | False | Keep downloaded template after comparison |

### Examples

```bash
# Compare against latest release
python tools/pyproject_template/check_template_updates.py

# Compare against specific version
python tools/pyproject_template/check_template_updates.py --template-version v2.2.0

# Quick comparison without changelog review
python tools/pyproject_template/check_template_updates.py --skip-changelog

# Keep template for manual inspection
python tools/pyproject_template/check_template_updates.py --keep-template
```

### Output Categories

| Category | Description |
|----------|-------------|
| Modified | Files that exist in both but have different content |
| Missing | Files in template that don't exist in your project |
| Extra | Files in your project that don't exist in template |

### Skipped Paths

The comparison automatically skips:

- `.git/`
- `.venv/`, `venv/`
- `__pycache__/`
- `tmp/`
- `*.pyc`, `*.pyo`
- `*.egg-info/`
- `.coverage`, `htmlcov/`
- Project-specific source files

### Requirements

- Python 3.12+
- Internet connection (to fetch template)
- `$EDITOR` environment variable (for changelog viewing)

---

## utils.py

Shared utilities used by other template tools.

### Description

Internal module providing common functionality:

- `Colors` - ANSI color codes for terminal output
- `Logger` - Formatted logging (info, success, warning, error)
- `GitHubCLI` - Wrapper for `gh` CLI commands
- `prompt()` - Interactive input with defaults
- `prompt_confirm()` - Yes/no confirmation prompts
- `update_file()` - Safe file content replacement
- `download_and_extract_archive()` - Download and extract zip/tar archives

### Usage

This module is not meant to be run directly. It's imported by other template tools:

```python
from tools.pyproject_template.utils import Logger, prompt

Logger.info("Starting process...")
name = prompt("Enter name", default="default_value")
```

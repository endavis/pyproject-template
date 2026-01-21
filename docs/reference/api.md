---
title: API Reference
description: Complete API documentation for Package Name
audience:
  - users
  - contributors
tags:
  - reference
  - api
---

# API Reference

Complete API documentation for Package Name.

## Core Module

### `package_name.core`

Core functionality for the package.

#### Functions

##### `greet()`

```python
def greet(name: str = "World") -> str
```

Return a greeting message.

**Parameters:**
- `name` (str, optional): The name to greet. Defaults to "World".

**Returns:**
- `str`: A greeting message string.

**Example:**

```python
from package_name import greet

# Default greeting
message = greet()
print(message)  # Output: "Hello, World!"

# Custom greeting
message = greet("Python")
print(message)  # Output: "Hello, Python!"
```

**Doctests:**

```python
>>> greet()
'Hello, World!'
>>> greet("Python")
'Hello, Python!'
```

## Package Metadata

### `__version__`

```python
from package_name import __version__
```

The current version of the package as a string.

**Example:**

```python
import package_name
print(package_name.__version__)  # Derived from the git tag by hatch-vcs
```

## Module Structure

The package is organized as follows:

```
package_name/
├── __init__.py      # Package initialization, exports greet and __version__
├── _version.py      # Version information (generated from git tags at build time)
└── core.py          # Core functionality (greet function)
```

## Type Hints

All public APIs include type hints for better IDE support and type checking:

```python
from package_name import greet

# Type checkers will infer the correct types
message: str = greet("Python")
```

## Extending the Package

This template provides a starting point. To add your own functionality:

### Adding a New Module

1. Create a new file in `src/package_name/`:
   ```python
   # src/package_name/new_module.py
   """New module description."""

   def new_function(param: str) -> str:
       """Function documentation."""
       return f"Processed: {param}"
   ```

2. Export it in `__init__.py`:
   ```python
   from .new_module import new_function

   __all__ = ["__version__", "greet", "new_function"]
   ```

3. Add tests in `tests/`:
   ```python
   # tests/test_new_module.py
   from package_name import new_function

   def test_new_function() -> None:
       """Test new_function."""
       assert new_function("test") == "Processed: test"
   ```

### Adding Exception Classes

```python
# src/package_name/exceptions.py
"""Package exceptions."""

class PackageError(Exception):
    """Base exception for package errors."""
    pass

class ValidationError(PackageError):
    """Raised when validation fails."""
    pass
```

Export them:

```python
# src/package_name/__init__.py
from .exceptions import PackageError, ValidationError

__all__ = [
    "__version__",
    "greet",
    "PackageError",
    "ValidationError",
]
```

### Adding CLI Support

1. Add `click` or `typer` to dependencies in `pyproject.toml`

2. Create CLI module:
   ```python
   # src/package_name/cli.py
   """Command-line interface."""
   import click
   from . import greet

   @click.command()
   @click.argument("name", default="World")
   def main(name: str) -> None:
       """Greet someone."""
       click.echo(greet(name))
   ```

3. Add entry point in `pyproject.toml`:
   ```toml
   [project.scripts]
   package-cli = "package_name.cli:main"
   ```

## Documentation Best Practices

When adding new functions or classes:

1. **Always include type hints**:
   ```python
   def process(data: str, validate: bool = True) -> dict[str, Any]:
       """Process data."""
   ```

2. **Write comprehensive docstrings**:
   ```python
   def process(data: str, validate: bool = True) -> dict[str, Any]:
       """Process input data.

       Args:
           data: The input data to process.
           validate: Whether to validate the data. Defaults to True.

       Returns:
           A dictionary containing the processed results.

       Raises:
           ValueError: If validation fails and validate is True.

       Example:
           >>> process("test")
           {'result': 'test'}
       """
   ```

3. **Include examples in docstrings**

4. **Update this API documentation**

5. **Add tests for all new functionality**

## Testing

All public APIs should have comprehensive tests:

```bash
# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=package_name --cov-report=term-missing

# Run specific test
uv run pytest tests/test_example.py::test_version -v
```

## Type Checking

Run mypy to verify type hints:

```bash
# Check entire source
uv run mypy src/

# Check specific file
uv run mypy src/package_name/core.py
```

## Changelog

See [CHANGELOG.md](https://github.com/username/package_name/blob/main/CHANGELOG.md) for version history and changes.

## Contributing

See [CONTRIBUTING.md](https://github.com/username/package_name/blob/main/.github/CONTRIBUTING.md) for information on contributing to the API.

---

## mkdocstrings Configuration

This project uses [mkdocstrings](https://mkdocstrings.github.io/) to automatically generate API documentation from Python docstrings.

### How It Works

1. **Source scanning**: mkdocstrings parses your Python source files
2. **Docstring extraction**: Extracts docstrings from modules, classes, and functions
3. **Rendering**: Converts docstrings to HTML using the configured style

### Configuration

mkdocstrings is configured in `mkdocs.yml`:

```yaml
plugins:
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          options:
            docstring_style: google        # Use Google-style docstrings
            show_source: true              # Show source code link
            show_signature_annotations: true  # Show type annotations
            show_symbol_type_heading: true    # Show type in headings
            show_symbol_type_toc: true        # Show type in TOC
            members_order: source          # Order by source file position
            merge_init_into_class: true    # Merge __init__ into class docs
            show_root_heading: true        # Show module/class heading
            show_root_full_path: false     # Don't show full import path
```

### Adding Module Documentation

To document a new module, add it to `docs/reference/api.md`:

```markdown
## My Module

Description of what this module does.

::: package_name.my_module
    options:
      show_root_heading: true
      show_root_full_path: true
```

### Customizing Per-Module Options

Override options for specific modules:

```markdown
::: package_name.internal
    options:
      show_source: false        # Hide source for internal module
      members: ["public_func"]  # Only document specific members
```

### Available Options

| Option | Default | Description |
|--------|---------|-------------|
| `docstring_style` | `google` | Docstring format: `google`, `numpy`, `sphinx` |
| `show_source` | `true` | Show link to source code |
| `show_signature_annotations` | `true` | Display type hints in signatures |
| `members_order` | `source` | Order: `source`, `alphabetical` |
| `merge_init_into_class` | `true` | Combine `__init__` docs with class |
| `show_root_heading` | `true` | Display module/class name as heading |
| `members` | `null` | List of specific members to document |

### Building API Docs

```bash
# Preview documentation locally
doit docs_serve

# Build static site
doit docs_build
```

### Troubleshooting

**Module not found errors:**
- Ensure the package is installed: `uv sync --dev`
- Check import paths match your package structure

**Docstrings not rendering:**
- Verify Google-style format is used
- Check for syntax errors in docstrings
- Run `doit docs_serve` and check console for errors

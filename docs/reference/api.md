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

Complete API documentation for Package Name, auto-generated from source code docstrings.

## Package Overview

::: package_name
    options:
      show_root_heading: false
      show_source: false
      members: false

## Core Module

The core module provides the main functionality of the package.

::: package_name.core
    options:
      show_root_heading: true
      show_root_full_path: true

## Logging Module

Centralized logging configuration with console and structured file output.

::: package_name.logging
    options:
      show_root_heading: true
      show_root_full_path: true

---

## Extending the Package

This template provides a starting point. To add your own functionality:

### Adding a New Module

1. Create a new file in `src/package_name/`:
   ```python
   # src/package_name/new_module.py
   """New module description."""

   def new_function(param: str) -> str:
       """Process a parameter.

       Args:
           param: The input parameter.

       Returns:
           The processed result.

       Examples:
           >>> new_function("test")
           'Processed: test'
       """
       return f"Processed: {param}"
   ```

2. Export it in `__init__.py`:
   ```python
   from .new_module import new_function

   __all__ = ["__version__", "greet", "new_function"]
   ```

3. Add documentation to this file:
   ```markdown
   ## New Module

   ::: package_name.new_module
   ```

4. Add tests in `tests/`.

### Docstring Format

This project uses **Google-style docstrings**. See the
[Docstring Standards](../development/coding-standards.md#docstring-standards) for the full format.

Quick reference:

```python
def example_function(param1: str, param2: int = 10) -> dict[str, Any]:
    """Short description of the function.

    Longer description if needed, explaining the behavior
    in more detail.

    Args:
        param1: Description of param1.
        param2: Description of param2. Defaults to 10.

    Returns:
        Description of what is returned.

    Raises:
        ValueError: When param1 is empty.

    Examples:
        >>> example_function("test")
        {'result': 'test', 'count': 10}
    """
```

## Type Hints

All public APIs include type hints for better IDE support and type checking:

```python
from package_name import greet

# Type checkers will infer the correct types
message: str = greet("Python")
```

Run mypy to verify type hints:

```bash
uv run mypy src/
```

## Testing

All public APIs should have comprehensive tests:

```bash
# Run all tests
doit test

# Run with coverage
uv run pytest --cov=package_name --cov-report=term-missing
```

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

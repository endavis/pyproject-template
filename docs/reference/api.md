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

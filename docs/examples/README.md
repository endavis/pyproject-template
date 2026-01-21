---
title: Examples
description: Example scripts demonstrating how to use the package
audience:
  - users
tags:
  - examples
  - getting-started
---

# Examples

This directory contains example scripts demonstrating how to use the package.

## Running Examples

Make sure you have the package installed:

```bash
# Install in development mode
uv pip install -e .

# Or install from PyPI
pip install package-name
```

Then run any example:

```bash
python examples/basic_usage.py
python examples/advanced_usage.py
python examples/cli_usage.py
```

## Available Examples

### basic_usage.py

Simple example demonstrating basic functionality.

**What it covers:**
- Importing the package
- Basic operations
- Simple error handling

### advanced_usage.py

Advanced example with more complex features.

**What it covers:**
- Advanced configuration
- Custom settings
- Complex data processing
- Best practices

### cli_usage.py

Example of using the command-line interface (if available).

**What it covers:**
- CLI commands
- Options and arguments
- Output formatting

### api/ (FastAPI Application)

Complete REST API example demonstrating FastAPI best practices.

**What it covers:**
- Application factory pattern
- Router organization
- Pydantic validation
- Dependency injection
- Error handling
- OpenAPI documentation

See the [API Development Guide](api.md) for detailed documentation.

**Running the API example:**

```bash
# Install FastAPI dependencies
uv add fastapi uvicorn[standard]

# Run the server
uvicorn examples.api.main:app --reload

# Visit http://localhost:8000/docs for Swagger UI
```

## Contributing Examples

Have an interesting use case? We'd love to add it!

1. Create a new `.py` file in this directory
2. Add clear comments explaining what it does
3. Add it to this README
4. Submit a pull request

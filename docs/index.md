---
title: Package Name Documentation
description: Welcome and overview of the project
audience:
  - users
  - contributors
tags:
  - overview
  - getting-started
---

# Package Name Documentation

Welcome to the documentation for Package Name!

## Overview

Package Name is a modern Python project template with comprehensive tooling for development, testing, documentation, and deployment.

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [User Guide](usage/basics.md)
- [API Reference](reference/api.md)
- [Contributing](https://github.com/endavis/pyproject-template/blob/main/.github/CONTRIBUTING.md)

## Features

- ✅ **Modern Build System**: Uses `uv` for fast dependency management
- ✅ **Comprehensive Testing**: pytest with parallel execution (pytest-xdist)
- ✅ **Type Safety**: mypy with strict type checking in pre-commit hooks
- ✅ **Code Quality**: ruff for linting and formatting
- ✅ **Security Scanning**: bandit for security analysis
- ✅ **Spell Checking**: codespell for typo prevention
- ✅ **Documentation**: MkDocs with Material theme support
- ✅ **CI/CD**: GitHub Actions with safe release workflows
- ✅ **Pre-commit Hooks**: Automated code quality checks
- ✅ **Auto Dependency Sync**: Post-merge and post-checkout hooks keep dependencies in sync
- ✅ **Mutation Testing**: mutmut for test suite effectiveness analysis
- ✅ **Property-Based Testing**: Hypothesis for invariant-based testing with random inputs
- ✅ **Benchmark Tracking**: Historical CI benchmarks with regression detection
- ✅ **SBOM Generation**: CycloneDX Software Bill of Materials for compliance and security

## Quick Start

```python
from package_name import greet

# Simple greeting example
message = greet("Python")
print(message)  # Output: Hello, Python!
```

## Documentation Sections

### For Users

- **[Installation](getting-started/installation.md)** - How to install the package
- **[Usage Guide](usage/basics.md)** - How to use the package
- **[CLI Guide](usage/cli.md)** - Command-line interface reference and how to add subcommands
- **[API Reference](reference/api.md)** - Complete API documentation

### For Contributors

- **[Contributing Guide](https://github.com/endavis/pyproject-template/blob/main/.github/CONTRIBUTING.md)** - Development workflow, coding standards, and best practices (**source of truth**)
- **[Code of Conduct](https://github.com/endavis/pyproject-template/blob/main/.github/CODE_OF_CONDUCT.md)** - Community guidelines
- **[AI First 5 Minutes](development/ai/first-5-minutes.md)** - Narrative walkthrough of the AI agent workflow (primary agent: Claude Code)
- **[AI Agent Setup](development/AI_SETUP.md)** - Setup guide for AI coding assistants (Claude Code is the primary agent; Gemini and Codex have narrower roles)

### Tooling roles

The template layers a small runtime package, a heavier set of development tools, and `doit` as the dev task runner. Knowing which tool belongs to which audience prevents the most common architectural mistake: treating `doit` as if it were the application's user-facing CLI. See [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) for the full breakdown.

## Support

- **Issues:** [GitHub Issues](https://github.com/endavis/pyproject-template/issues)
- **Discussions:** [GitHub Discussions](https://github.com/endavis/pyproject-template/discussions)
- **Security:** See [SECURITY.md](https://github.com/endavis/pyproject-template/blob/main/.github/SECURITY.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/endavis/pyproject-template/blob/main/LICENSE) file for details.

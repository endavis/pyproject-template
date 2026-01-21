# ADR-0002: Use doit for task automation

## Status

Accepted

## Date

2025-01-21

## Context

Modern software projects require task automation for common operations like testing, linting, building, and deployment. Common approaches include:

- Make/Makefiles - ubiquitous but syntax is arcane and platform-dependent
- npm scripts - JavaScript-centric, not ideal for Python projects
- Invoke/Fabric - Python-based but limited dependency tracking
- Just - modern but requires learning a new DSL
- Tox - focused on testing across environments, not general automation

The project needed a task runner that:

- Is Python-native (no context switching)
- Supports task dependencies and incremental builds
- Is flexible enough for custom workflows
- Has good documentation and community
- Integrates well with CI/CD pipelines

## Decision

Use **doit** as the task automation framework.

doit is a Python-based build tool that acts like Make but with Python syntax. It provides:

- Pure Python task definitions (no DSL to learn)
- Automatic task dependency resolution
- Incremental builds (only run what changed)
- Parameterized tasks with command-line arguments
- Rich ecosystem of plugins and integrations

## Consequences

### Positive

- Tasks are defined in Python, leveraging existing skills
- Powerful dependency graph ensures correct execution order
- Incremental builds save time in development
- `doit list` provides discoverability of available tasks
- Easy to extend with custom Python code
- Modular task organization (auto-discovery from `tools/doit/`)

### Negative

- Less well-known than Make (smaller community)
- Slightly higher learning curve than simple shell scripts
- Requires doit as a dependency

### Neutral

- Task definitions live in `dodo.py` (convention over configuration)
- Modular structure in `tools/doit/` for organization

## Participants

- Project maintainers

## Related

- [doit documentation](https://pydoit.org/)
- [ADR-0001: Use uv for package management](0001-use-uv-for-package-management.md)
- Issue #170: Rename tools/tasks to tools/doit
- Issue #87: Add shell completions for doit tasks
- Issue #80: Add doit issue and doit pr commands for GitHub workflow
- Issue #65: Promote doit and rich to runtime dependencies

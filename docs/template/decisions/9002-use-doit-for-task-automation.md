# ADR-9002: Use doit for task automation

## Status

Accepted

## Decision

Use **doit** as the task automation framework for common operations like testing, linting, building, and deployment.

## Rationale

doit is a Python-based build tool that uses pure Python for task definitions (no DSL to learn), provides automatic task dependency resolution and incremental builds, and encourages modular task organization. Being Python-native means no context switching for developers already working in Python.

## Related Issues

- Issue #170: Rename tools/tasks to tools/doit
- Issue #87: Add shell completions for doit tasks
- Issue #80: Add doit issue and doit pr commands for GitHub workflow
- Issue #65: Promote doit and rich to runtime dependencies

## Related Documentation

- [Tools Reference](../tools-reference.md)

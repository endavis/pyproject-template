# ADR-0010: Use conventional commits format

## Status

Accepted

## Decision

Adopt **Conventional Commits** format (`<type>: <subject>`) for all commit messages. Types include feat, fix, docs, refactor, test, chore, ci, perf. Merge commits follow `<type>: <subject> (merges PR #XX, closes #YY)`.

## Rationale

Provides consistent, readable git history, enables automated changelog generation, and allows easy filtering by change type. Works well with semantic versioning for automated version bumps based on commit types.

## Related Issues

- Issue #176: Add doit pr_merge task with enforced commit format
- Issue #175: Add PR title validation to enforce merge commit format

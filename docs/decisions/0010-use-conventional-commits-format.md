# ADR-0010: Use conventional commits format

## Status

Accepted

## Date

2025-01-21

## Context

Commit messages serve multiple purposes:

- Document what changed and why
- Enable automated changelog generation
- Help reviewers understand changes
- Support git bisect and blame
- Feed into release notes

Without a standard format, commit messages vary wildly in quality and structure, making history hard to read and automation impossible.

Common commit message conventions include:

- **Conventional Commits**: Structured format with type, scope, and description
- **Gitmoji**: Emoji-based categorization
- **Angular**: Similar to Conventional Commits, Angular-specific
- **Freeform**: No standard, whatever developers write

## Decision

Adopt **Conventional Commits** format for all commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance, tooling, CI
- `ci`: CI/CD changes
- `perf`: Performance improvement

**Merge commit format:**
```
<type>: <subject> (merges PR #XX, closes #YY)
```

This is enforced by:
- PR title validation (must match type pattern)
- `doit pr_merge` task formats the merge commit automatically

## Consequences

### Positive

- Consistent, readable git history
- Enables automated changelog generation
- Clear categorization of changes
- Easy to filter history by type
- Works well with semantic versioning

### Negative

- Learning curve for new contributors
- Requires discipline to follow format
- Rejecting commits for format issues can be frustrating

### Neutral

- PR titles must follow same format
- Merge commits capture the canonical message

## Participants

- Project maintainers

## Related

- [ADR-0008: PR-based development workflow](0008-pr-based-development-workflow.md)
- [Conventional Commits specification](https://www.conventionalcommits.org/)
- [CONTRIBUTING.md](../../.github/CONTRIBUTING.md)

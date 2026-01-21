# ADR-0008: PR-based development workflow

## Status

Accepted

## Date

2025-01-21

## Context

Software projects need a defined workflow for how changes flow from idea to production. Common approaches include:

- **Trunk-based development**: Everyone commits directly to main, with feature flags for incomplete work
- **Git Flow**: Long-lived feature branches, develop branch, release branches
- **GitHub Flow**: Short-lived feature branches, PRs to main, continuous deployment
- **Direct commits**: No branches, everyone pushes directly to main

The project needed a workflow that:

- Prevents accidental commits to main
- Provides code review opportunities
- Links changes to tracked issues
- Creates an audit trail of decisions
- Works well with CI/CD pipelines
- Is simple enough for solo developers and AI agents

## Decision

Adopt a **PR-based workflow** with the following steps:

1. **Issue**: Create a GitHub issue describing the work (using `doit issue`)
2. **Branch**: Create a branch linked to the issue (e.g., `feat/42-add-feature`)
3. **Commit**: Make commits on the branch following conventional commit format
4. **PR**: Create a pull request (using `doit pr`)
5. **Merge**: Squash merge with formatted commit message (using `doit pr_merge`)

Key rules:
- **Never commit directly to main** - enforced by pre-commit hooks
- Branch names must follow convention: `<type>/<issue>-<description>`
- PRs require the `ready-to-merge` label before merging
- Merge commits follow format: `<type>: <subject> (merges PR #XX, closes #YY)`

## Consequences

### Positive

- Clear audit trail linking issues → PRs → commits
- Code review opportunity on every change
- CI runs on PRs before merge
- Easy to revert changes (single squash commit per PR)
- Works well with AI agents (structured, predictable)

### Negative

- More steps than direct commits
- Requires discipline to create issues first
- Small fixes still need full workflow

### Neutral

- Squash merge loses individual commit history (by design)
- Requires GitHub-specific tooling (gh CLI)

## Participants

- Project maintainers

## Related

- [ADR-0006: Merge-gate workflow](0006-merge-gate-workflow.md)
- [ADR-0005: AI agent command restrictions](0005-ai-agent-command-restrictions.md)
- [CONTRIBUTING.md](../../.github/CONTRIBUTING.md)
- Issue #80: Add doit issue and doit pr commands for GitHub workflow
- Issue #48: Enforce workflow by blocking direct commits to main
- Issue #176: Add doit pr_merge task with enforced commit format

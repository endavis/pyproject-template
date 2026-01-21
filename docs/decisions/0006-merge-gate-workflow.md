# ADR-0006: Merge-gate workflow requiring ready-to-merge label

## Status

Accepted

## Date

2025-01-21

## Context

Pull requests could be merged without explicit human approval. While CI tests provide automated verification, there was no enforcement of a human review checkpoint before merging.

Issues included:

- PRs could be merged while CI was still running
- No explicit "ready for merge" signal from reviewer
- AI agents could potentially merge PRs prematurely

The project needed a lightweight mechanism to:

- Require explicit human approval before merge
- Prevent premature merges
- Work with GitHub's branch protection rules

## Decision

Implement a merge-gate workflow that requires the `ready-to-merge` label on PRs:

1. **GitHub Actions workflow** (`.github/workflows/merge-gate.yml`) that:
   - Triggers on PR events: opened, labeled, unlabeled, synchronize, reopened
   - Checks for the presence of `ready-to-merge` label
   - Fails with clear error if label is missing
   - Passes when label is present

2. **Branch protection rule** that requires this check to pass before merge

The workflow is lightweight (just a label check) and provides a clear signal that a human has reviewed and approved the PR for merging.

## Consequences

### Positive

- Explicit human approval required for all merges
- Prevents AI agents from merging without human review
- Prevents merges while CI is still running (reviewer waits for CI)
- Simple, low-overhead process (just add a label)
- Clear audit trail of who approved the merge

### Negative

- Extra step required to merge PRs
- Label can be added without thorough review (human discipline required)
- Workflow runs on every PR event (minimal overhead)

### Neutral

- Integrates with existing GitHub branch protection
- Label is purely a gate, doesn't affect CI test matrix

## Participants

- Project maintainers

## Related

- Issue #149: Add merge-gate workflow to require ready-to-merge label
- Issue #154: Fix merge-gate to wait for CI completion before allowing merge

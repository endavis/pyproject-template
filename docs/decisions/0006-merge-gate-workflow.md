# ADR-0006: Merge-gate workflow requiring ready-to-merge label

## Status

Accepted

## Decision

Implement a merge-gate GitHub Actions workflow that requires the `ready-to-merge` label on PRs before allowing merge, enforced via branch protection rules.

## Rationale

PRs could be merged while CI was still running or without explicit human approval. The merge-gate provides a lightweight mechanism requiring explicit "ready" signal after review, preventing premature merges and AI agents from merging without human review.

## Related Issues

- Issue #149: Add merge-gate workflow to require ready-to-merge label
- Issue #154: Fix merge-gate to wait for CI completion before allowing merge

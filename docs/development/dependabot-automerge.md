---
title: Dependabot Auto-merge
description: How the dependabot auto-merge workflow evaluates, enables, and skips PRs
audience:
  - contributors
  - maintainers
tags:
  - dependabot
  - automation
  - ci
---

# Dependabot Auto-merge

The workflow at `.github/workflows/dependabot-automerge.yml` evaluates each
dependabot PR and enables GitHub's native auto-merge for PRs that meet the
project's safety criteria. Qualifying PRs are merged automatically once the
required CI checks pass.

## What gets auto-merged

A dependabot PR qualifies when **all** of the following are true:

- The update type is `version-update:semver-patch` or `version-update:semver-minor`.
- None of the updated dependency names match a glob in the
  `sensitive_dependencies` list.
- The PR has no label listed in `blocking_labels`.

Qualifying PRs receive:

- GitHub's native auto-merge enabled with the **squash** strategy.
- The `ready-to-merge` label applied automatically (satisfying the Merge Gate).
- A sticky status comment confirming auto-merge is enabled.

## What gets skipped

A PR is skipped (no auto-merge, sticky comment posted for human review) when:

- The update is a **major version bump** (`version-update:semver-major`).
- A **sensitive dependency** is touched (e.g. anything matching `*ssl*`,
  `*security*`, `auth*`, `crypt*`, `*jwt*`, `*oauth*`).
- A **blocking label** (`do-not-merge` or `automerge-blocked`) is present.

Skipped PRs require a human reviewer to merge them using the normal workflow.

## The `automerge-blocked` opt-out

To stop auto-merge on a PR that already qualified, add the label
`automerge-blocked` (or `do-not-merge`). The workflow reacts to the `labeled`
event:

- Disables GitHub's auto-merge on the PR.
- Removes the `ready-to-merge` label.
- Posts a sticky comment recording the block.

## Configuration

Lists live in `.github/automerge-config.json`:

```json
{
  "sensitive_dependencies": ["crypt*", "*ssl*", "*security*", "auth*", "*jwt*", "*oauth*"],
  "allowed_update_types": ["version-update:semver-patch", "version-update:semver-minor"],
  "blocking_labels": ["do-not-merge", "automerge-blocked"]
}
```

Globs use `*` as a wildcard and are matched case-insensitively against the full
dependency name. Edit the file via a normal PR to change policy.

## Rebase handling for stale PRs

The workflow includes a scheduled job (every 6 hours, plus `workflow_dispatch`)
that finds qualifying dependabot PRs whose branches have fallen behind `main`
and asks dependabot to rebase:

```
@dependabot rebase
```

This follows the signed-commit rule documented in the
[Dependabot PRs](../../AGENTS.md#dependabot-prs) section of `AGENTS.md`:
**never** call the GitHub `update-branch` API or rebase locally, because both
strip dependabot's verified commit signatures. The job also skips any PR that
already received a `@dependabot rebase` comment within the last hour, so it
does not spam the bot while a rebase is in progress.

## Related

- `AGENTS.md` section [Dependabot PRs](../../AGENTS.md#dependabot-prs)
- `.github/workflows/dependabot-automerge.yml`
- `.github/automerge-config.json`

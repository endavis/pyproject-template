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

The label-driven opt-out path lives in a sibling workflow,
`.github/workflows/dependabot-blocked-label.yml`, which fires only on
`pull_request_target: labeled` events. Splitting label handling out of the
main workflow keeps the `Dependabot Auto-merge` check clean (it runs once per
PR open/sync, not once per auto-applied label) and lets the main workflow use
`concurrency: cancel-in-progress: true` safely.

## What gets auto-merged

A dependabot PR qualifies when **all** of the following are true:

- The update type is `version-update:semver-patch` or `version-update:semver-minor`.
- None of the updated dependency names match a glob in the
  `sensitive_dependencies` list.
- The PR has no label listed in `blocking_labels`.

Qualifying PRs receive:

- The `ready-to-merge` label applied automatically (satisfying the Merge Gate).
  This happens first and is **unconditional** for qualifying PRs.
- GitHub's native auto-merge attempted with the **squash** strategy. This step
  can fail for reasons outside the workflow (e.g. the repository does not have
  `allow_auto_merge` enabled), in which case the run is marked as a failure but
  the label above is already applied.
- A sticky status comment describing the outcome. If auto-merge was enabled, it
  confirms that; if the auto-merge step failed, it notes that the label was
  applied anyway and points at the workflow logs so a maintainer can investigate
  and/or merge manually.

## What gets skipped

A PR is skipped (no auto-merge, sticky comment posted for human review) when:

- The update is a **major version bump** (`version-update:semver-major`).
- A **sensitive dependency** is touched (e.g. anything matching `*ssl*`,
  `*security*`, `auth*`, `crypt*`, `*jwt*`, `*oauth*`).
- A **blocking label** (`do-not-merge` or `automerge-blocked`) is present.

Skipped PRs require a human reviewer to merge them using the normal workflow.

## The `automerge-blocked` opt-out

To stop auto-merge on a PR that already qualified, add the label
`automerge-blocked` (or `do-not-merge`). The `dependabot-blocked-label.yml`
workflow reacts to the `labeled` event:

- Disables GitHub's auto-merge on the PR.
- Removes the `ready-to-merge` label.
- Posts a sticky comment recording the block.

Both workflows share the same `<!-- dependabot-automerge:status -->` sticky
comment marker, so toggling the block updates the existing comment instead of
producing a thread of status messages.

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
- `.github/workflows/dependabot-blocked-label.yml`
- `.github/automerge-config.json`

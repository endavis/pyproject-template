# ADR-0001: PR-based release is the only supported flow

## Status

Accepted

## Decision

The PR-based release flow is the only supported release path in this
project. `doit release [--prerelease=alpha|beta|rc]` creates a release
branch, updates `CHANGELOG.md`, and opens a pull request. A reviewer merges
the PR via the normal PR flow. Afterwards, `doit release_tag` tags `main`
from the merged PR title and pushes the tag, which triggers the publish
workflow. No direct-to-`main` release command is provided.

## Rationale

The original release tasks were inherited from `pyproject-template`, which
shipped three separate doit tasks:

- `task_release` — committed the version bump and tag directly to `main`.
- `task_release_dev` — same, for pre-releases to TestPyPI.
- `task_release_pr` — PR-based; opened a release PR and tagged on merge.

The template-default `no-commit-to-main` pre-commit hook blocks any task
that commits to `main`. Two of the three tasks could not function on a
template-default repo, which made the 3-task split unworkable. Maintainers
either had to bypass the hook with `--no-verify` (a governance violation
that the template explicitly forbids) or fall back to the PR-based flow
every time — in which case the other two tasks were dead weight.

Phase A (PR #634) widened the `release_tag` version regex to accept
PEP440 and semver-style pre-release suffixes. Phase B (PR #637) added
`--prerelease=alpha|beta|rc` to `task_release_pr`. Once those were in
place, the PR-based flow covered production and pre-release cases, and
the two direct-to-`main` tasks were fully redundant. This ADR records the
decision to delete them and promote the PR-based flow to be the single
canonical release story.

## Consequences

- **Breaking CLI change.** `doit release` no longer commits to `main`; it
  opens a PR. `doit release_dev` and `doit release_pr` are removed. The
  migration is documented in the PR description and here:

  | Before | After |
  | --- | --- |
  | `doit release` (direct-to-main) | `doit release` (opens release PR) → reviewer merges → `doit release_tag` |
  | `doit release_dev --type=alpha` | `doit release --prerelease=alpha` → reviewer merges → `doit release_tag` |
  | `doit release_pr` | `doit release` |
  | `doit release_tag` | `doit release_tag` (unchanged) |

- **No direct-to-`main` path.** All releases — production and pre-release
  — now go through code review, matching the same governance applied to
  every other change on the repo.

- **Template port pending.** This ADR is downstream of issue #632. The
  change will be ported to `pyproject-template` after the end-to-end
  release flow is verified here. Until the port lands, there is
  intentional drift between this repo and the upstream template for the
  release tasks and their documentation.

- **Single canonical release story.** Future contributors and AI agents
  reading the codebase see one release flow, one set of docs, and no
  conditional branching on "which release task do I use".

## Related Issues

- Issue #632: fix: consolidate release tasks around the PR-based flow
  (this ADR closes the loop on Phases A, B, and C of #632).
- PR #634 (Phase A): widened the `release_tag` version regex to accept
  PEP440 and semver-style pre-release suffixes.
- PR #637 (Phase B): added `--prerelease=alpha|beta|rc` to the PR-based
  release task.

## Related Documentation

- [Release Automation & Security](../development/release-and-automation.md) — full walk-through of the PR-based flow and the `doit release`/`doit release_tag` commands.
- [Doit Tasks Reference — Release Tasks](../development/doit-tasks-reference.md#release-tasks) — task-level reference.
- [CONTRIBUTING.md — Release Process](../../.github/CONTRIBUTING.md#release-process) — contributor-facing release checklist.

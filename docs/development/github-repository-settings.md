---
title: GitHub Repository Settings
description: Complete reference for all GitHub repository settings the template expects
audience:
  - users
  - contributors
tags:
  - github
  - settings
  - setup
  - configuration
---

# GitHub Repository Settings

Complete reference for the GitHub repository settings this template expects.
New repositories created from the template are configured automatically by
[`repo_settings.py`](../../tools/pyproject_template/repo_settings.py) via
`update_all_repo_settings()`. This page documents what each setting is, why
it is needed, and whether it is set automatically or requires manual action.

For the initial setup workflow, see the [New Project Setup](../template/new-project.md) guide.

## Repository Settings

These are the general repository-level settings applied by
`configure_repository_settings()`.

| Setting | Value | Purpose |
| :--- | :--- | :--- |
| **Default branch** | `main` | Standard branch for PRs and CI |
| **Issues** | Enabled | Issue tracking with custom templates |
| **Wiki** | Disabled | Documentation lives in `docs/` via MkDocs |
| **Projects** | Enabled | Available for project management if needed |
| **Discussions** | Disabled | Not used by default |
| **Allow squash merge** | Yes | Only merge strategy allowed (linear history) |
| **Allow merge commit** | No | Enforces squash-only policy |
| **Allow rebase merge** | No | Enforces squash-only policy |
| **Delete branch on merge** | Yes | Cleans up feature branches automatically |
| **Visibility** | Public | Template default; private repos may lack some security features |

**Automated:** Yes, all settings above are copied from the template repository.

## Branch Protection (Rulesets)

Branch protection uses GitHub **repository rulesets** rather than the legacy
branch protection API. The template has a single ruleset named `main` applied
to the default branch.

### Ruleset: `main`

| Rule | Details |
| :--- | :--- |
| **Enforcement** | Active |
| **Target** | Default branch (`main`) |
| **Deletion** | Blocked -- cannot delete `main` |
| **Non-fast-forward** | Blocked -- no force pushes |
| **Creation** | Controlled |
| **Required linear history** | Enforced (squash merges only) |
| **Required signatures** | Commits must be signed |
| **Pull request required** | Yes, with the following parameters: |
| | Required approving reviews: 0 |
| | Dismiss stale reviews on push: Yes |
| | Require code owner review: No |
| | Require last push approval: No |
| | Required review thread resolution: Yes |
| | Allowed merge methods: squash only |
| **Required status checks** | `require-label` (from the Merge Gate workflow) |
| | Strict policy: Yes (branch must be up to date) |
| **Code scanning** | CodeQL -- errors threshold, high-or-higher security alerts |
| **Code quality** | Errors severity threshold |
| **Bypass actors** | Repository admin role (always) |

**Automated:** Yes, rulesets are replicated from the template by
`configure_branch_protection()`.

## Labels

Labels are used by issue templates, workflows, release notes, and Dependabot.

**Source of truth:** `.github/labels.yml`. The file is a flat list of entries with `name`, `color` (6-char hex, no leading `#`), and `description`. Run `doit labels_sync` to reconcile the repository's labels with the file.

```bash
doit labels_sync --dry-run   # Preview changes
doit labels_sync             # Create missing labels, update drift
doit labels_sync --prune     # Also delete labels not in the file
```

The task is idempotent — running it twice in a row is a no-op the second time. Color comparison is case-insensitive. `--prune` is off by default because deletion is destructive.

To add a label: edit `.github/labels.yml`, run `doit labels_sync --dry-run` to preview, then `doit labels_sync` to apply.

| Label | Color | Description | Used By |
| :--- | :--- | :--- | :--- |
| `automated` | `#02db74` | -- | Dependabot PRs |
| `bug` | `#d73a4a` | Something isn't working | Issue template, release notes |
| `chore` | `#FEF2C0` | Maintenance, tooling, CI tasks | Issue template |
| `dependencies` | `#0366d6` | Pull requests that update a dependency file | Dependabot PRs, release notes exclusion |
| `documentation` | `#0075ca` | Improvements or additions to documentation | Issue template, release notes |
| `duplicate` | `#cfd3d7` | This issue or pull request already exists | Manual triage |
| `enhancement` | `#a2eeef` | New feature or request | Issue template, release notes |
| `full-matrix` | `#1D76DB` | Run CI on all supported Python versions | CI workflow (triggers full matrix) |
| `github_actions` | `#000000` | Pull requests that update GitHub Actions code | Dependabot PRs |
| `good first issue` | `#7057ff` | Good for newcomers | Manual triage |
| `help wanted` | `#008672` | Extra attention is needed | Manual triage |
| `invalid` | `#e4e669` | This doesn't seem right | Manual triage |
| `needs-adr` | `#d4c5f9` | This issue requires an Architecture Decision Record | PR merge gate |
| `needs-triage` | `#FBCA04` | Needs review and prioritization | All issue templates |
| `question` | `#d876e3` | Further information is requested | Manual triage |
| `ready-to-merge` | `#0E8A16` | PR is reviewed and ready to merge. Exception: the `dependabot-automerge` workflow applies this label automatically to qualifying dependabot PRs. | Merge Gate workflow |
| `refactor` | `#F9D0C4` | Code refactoring and cleanup | Issue template |
| `security` | `#d73a4a` | Security vulnerability or fix | Manual triage |
| `wontfix` | `#ffffff` | This will not be worked on | Manual triage |

### Label usage by issue template

| Template | Auto-applied labels |
| :--- | :--- |
| Bug Report | `bug`, `needs-triage` |
| Feature Request | `enhancement`, `needs-triage` |
| Refactor Request | `refactor`, `needs-triage` |
| Documentation Request | `documentation`, `needs-triage` |
| Chore / Maintenance | `chore`, `needs-triage` |

**Automated:** Yes, labels are copied from the template repository.

## GitHub Actions Workflows

All workflow files live in `.github/workflows/`. The table below summarizes
each workflow, its trigger, and required permissions.

| Workflow | File | Trigger | Permissions |
| :--- | :--- | :--- | :--- |
| **CI** | `ci.yml` | PR to `main` (opened, synchronize, reopened, labeled), `workflow_dispatch`, `workflow_call` | `contents: read` |
| **Merge Gate** | `merge-gate.yml` | PR to `main` (opened, labeled, unlabeled, synchronize, reopened) | `contents: read` |
| **PR Validation** | `pr-checks.yml` | PR (opened, edited, synchronize) | Default |
| **Breaking Change Detection** | `breaking-change-detection.yml` | PR (opened, synchronize, edited) | `contents: read`, `issues: write`, `pull-requests: write` |
| **Benchmark** | `benchmark.yml` | Push to `main`, PR to `main`, `workflow_dispatch` | `contents: write`, `pull-requests: write` |
| **Mutation Testing** | `mutation.yml` | Scheduled (Sunday midnight UTC), `workflow_dispatch` | `contents: read` |
| **Release** | `release.yml` | Tag push (`v*.*.*`), `workflow_dispatch` | `contents: read`, `id-token: write` (per job: `contents: write`) |
| **TestPyPI** | `testpypi.yml` | Tag push (`v*-*`), `workflow_dispatch` | `contents: read`, `id-token: write` |

### Key workflow details

- **CI** uses a matrix strategy with Python versions from
  `.github/python-versions.json`. Adding the `full-matrix` label to a PR runs
  all versions; otherwise, only the bookend versions are tested.
- **Merge Gate** requires the `ready-to-merge` label on a PR before the
  `require-label` status check passes. This is a manual gate added by a reviewer.
- **Release** publishes to TestPyPI first, then PyPI, then creates a GitHub
  Release with auto-generated notes and SBOM attachments.

For detailed CI configuration, see the [CI/CD Testing Guide](ci-cd-testing.md).

## GitHub Environments

Release workflows use GitHub environments for OIDC-based publishing.

| Environment | Used By | Purpose |
| :--- | :--- | :--- |
| `testpypi` | `release.yml`, `testpypi.yml` | Publish pre-release and release packages to TestPyPI |
| `pypi` | `release.yml` | Publish release packages to PyPI |

### OIDC Trusted Publisher Configuration

Both environments use PyPI's trusted publisher mechanism instead of API tokens.
Configure the trusted publisher on PyPI and TestPyPI:

- **Publisher:** GitHub Actions
- **Owner:** Your GitHub username or organization
- **Repository:** Your repository name
- **Workflow:** `release.yml` (for PyPI) or `testpypi.yml` (for TestPyPI)
- **Environment:** `pypi` or `testpypi` respectively

**Automated:** No. Environments must be created manually in the repository
settings, and trusted publishers must be configured on PyPI/TestPyPI.

## Secrets and Variables

| Secret/Variable | Required | Purpose |
| :--- | :--- | :--- |
| `GITHUB_TOKEN` | Automatic | Provided by GitHub Actions; used by most workflows |
| `CODECOV_TOKEN` | Optional | Upload coverage reports to Codecov |
| `RELEASE_APP_ID` | Optional | GitHub App ID for release automation |
| `RELEASE_APP_PRIVATE_KEY` | Optional | GitHub App private key for release automation |

PyPI publishing uses OIDC (trusted publishers), so no `PYPI_TOKEN` secret is
needed.

**Automated:** No. Secrets must be added manually in repository settings.

## Security Settings

Security features are configured by `_configure_security_settings()` in
`repo_settings.py`.

| Setting | Status | Purpose |
| :--- | :--- | :--- |
| **Secret scanning** | Enabled | Detects accidentally committed secrets |
| **Secret scanning push protection** | Enabled | Blocks pushes containing secrets |
| **Dependabot security updates** | Enabled | Automatic PRs for vulnerable dependencies |
| **CodeQL analysis** | Configured | Static analysis for security vulnerabilities |

!!! note
    Secret scanning and push protection are available for free on public
    repositories. Private repositories require GitHub Advanced Security (GHAS).

**Automated:** Yes, security settings are copied from the template. CodeQL is
configured separately by `configure_codeql()`.

## Dependabot

Dependabot is configured via `.github/dependabot.yml` with two ecosystems:

| Ecosystem | Directory | Schedule | Labels |
| :--- | :--- | :--- | :--- |
| `uv` | `/` | Weekly (Monday 09:00 UTC) | `dependencies`, `automated` |
| `github-actions` | `/` | Weekly (Monday 09:00 UTC) | `dependencies`, `automated` |

### Grouping

Dev dependencies (`pytest*`, `ruff`, `mypy`, `coverage`) are grouped into a
single PR under the `uv` ecosystem.

### Commit message prefix

All Dependabot commits use the `chore(deps)` prefix to follow conventional
commits format.

**Automated:** No. The `.github/dependabot.yml` file is part of the template
and included in new repositories, but Dependabot itself must be enabled in
repository settings if not already active.

## GitHub Pages

Documentation is published to GitHub Pages from the `gh-pages` branch.

| Setting | Value |
| :--- | :--- |
| **Source branch** | `gh-pages` |
| **Source path** | `/` (root) |
| **Build tool** | MkDocs with Material theme |
| **Deployment** | Handled by CI or manual `doit docs_build` |

**Automated:** Yes, `enable_github_pages()` configures Pages on the
`gh-pages` branch. The branch itself is created on the first documentation
deployment.

## Code Owners

The `.github/CODEOWNERS` file defines default reviewers for pull requests.
The template sets `@username` as the owner for all paths. After creating a
new project, update the file with the actual repository owner's GitHub
username.

Key ownership areas defined:

- `*` -- Default owner for all files
- `/docs/` and `*.md` -- Documentation
- `/.github/` -- GitHub configuration
- `/.github/workflows/` -- CI/CD pipelines
- `/src/` -- Core source code
- `/tests/` -- Test files
- `pyproject.toml` -- Project configuration
- `dodo.py` -- Task automation

**Automated:** No. The file is part of the template but requires manual
update with the correct username.

## Release Notes

Auto-generated release notes are configured in `.github/release.yml`.

| Category | Labels |
| :--- | :--- |
| Breaking Changes | `breaking` |
| New Features | `enhancement`, `feat` |
| Bug Fixes | `bug`, `fix` |
| Documentation | `documentation`, `docs` |
| Performance | `performance`, `perf` |
| Other Changes | `*` (catch-all) |

### Excluded from release notes

PRs with these labels are excluded from auto-generated notes:

- `dependencies`
- `needs-triage`

**Automated:** No. The `.github/release.yml` file is part of the template.

## Special Branches

| Branch | Purpose | Protected |
| :--- | :--- | :--- |
| `main` | Default branch; all PRs target this branch | Yes (ruleset) |
| `gh-pages` | Published documentation site | No |
| `gh-benchmarks` | Benchmark trend data for the Benchmark workflow | No |

## Summary of Manual Steps

After creating a new repository from the template, these items require manual
configuration:

1. **Environments** -- Create `testpypi` and `pypi` environments
2. **OIDC Trusted Publishers** -- Configure on PyPI and TestPyPI
3. **Secrets** -- Add `CODECOV_TOKEN` and optional release app credentials
4. **CODEOWNERS** -- Replace `@username` with the actual owner
5. **Dependabot** -- Verify Dependabot is enabled in repository settings
6. **CodeQL** -- Verify CodeQL is active after initial setup

For the full post-setup checklist, see the [New Project Setup](../template/new-project.md) guide.

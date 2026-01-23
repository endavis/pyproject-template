---
title: AI Agent Sync Checklist
description: Step-by-step checklist for AI agents synchronizing downstream projects with pyproject-template
audience:
  - ai-agents
tags:
  - template
  - sync
  - ai
---

# AI Agent Checklist: Synchronize with pyproject-template

This checklist guides an AI agent through synchronizing a downstream project with the latest pyproject-template. It uses the official `manage.py` tooling documented in [Template Manager](manage.md), [Keeping Up to Date](updates.md), and [Tools Reference](tools-reference.md).

**Prerequisites:**

- Downstream project already uses pyproject-template structure (doit tasks, CI workflows, pre-commit, etc.)
- Template repo: `endavis/pyproject-template`

---

## Pre-Flight

- [ ] Verify on `main` branch and clean working tree (`git status`)
- [ ] Run `doit check` to confirm current state passes
- [ ] Create a GitHub Issue for the sync work:
  ```bash
  doit issue --type=chore --title="chore: synchronize with latest pyproject-template" \
    --body="## Description\nSynchronize project with latest pyproject-template improvements."
  ```
- [ ] Create branch linked to the issue (e.g., `chore/<issue#>-sync-pyproject-template`)

---

## Phase 1: Install Template Management Tools (First-Time Only)

If the project does NOT yet have `tools/pyproject_template/manage.py`, install it using the bootstrap script. Skip this phase if already present.

```bash
curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/bootstrap.py | python3 - --sync
```

This will:

1. Download the management suite to `tools/pyproject_template/`:
    - `__init__.py`, `utils.py`, `settings.py`, `check_template_updates.py`, `manage.py`, `configure.py`, `cleanup.py`
2. Detect project settings from `pyproject.toml`
3. Create `.config/pyproject_template/settings.toml` with detected values
4. Verify the installation

After installation:

- [ ] Review `.config/pyproject_template/settings.toml` and correct any values
- [ ] Decide: Track `.config/pyproject_template/` in git or add to `.gitignore`
- [ ] Verify: `python tools/pyproject_template/manage.py --dry-run check`

---

## Phase 2: Run Template Update Check

Per [Template Manager](manage.md) "Workflow: Staying Up to Date":

```bash
python tools/pyproject_template/manage.py check
```

This will (per [Tools Reference](tools-reference.md)):

1. Fetch the latest template release (or specified version via `--template-version`)
2. Compare all files - categorized as **Modified**, **Missing** (new in template), or **Extra** (project-specific)
3. Keep the template at `tmp/extracted/pyproject-template-main/` for diff commands
4. Show GitHub compare URL for commit history since last sync
5. Save commit info to `.template_commit` for later `sync` marking

**Diff commands** (per documentation):

```bash
diff <file> tmp/extracted/pyproject-template-main/<file>
```

Review the output and proceed with Phases 3-7 to selectively apply changes.

---

## Phase 3: GitHub Workflows (`.github/workflows/`)

For each workflow file flagged as **Modified** or **Missing**:

- [ ] Compare each workflow against the template version
- [ ] Apply updates (new permissions, action version bumps, new features)
- [ ] **Preserve project-specific divergences** (e.g., custom OS matrix, extra setup steps, project-specific env vars)
- [ ] Verify workflows still reference the correct package name

**Files typically synchronized:**

- `ci.yml` - Test matrix, action versions, triggers
- `breaking-change-detection.yml` - Permissions, PR comment reporting
- `release.yml` - Release automation
- `testpypi.yml` - Pre-release testing
- `pr-checks.yml` - PR validation
- `merge-gate.yml` - Merge requirements

**Check for ADRs:** If the project has ADRs documenting intentional divergences from template workflows, respect those decisions.

---

## Phase 4: Doit Tasks (`tools/doit/`)

### 4.1 Core Task Infrastructure

- [ ] Compare `tools/doit/__init__.py` for discovery mechanism updates
- [ ] Compare `tools/doit/base.py` for configuration changes (DOIT_CONFIG, helpers)

### 4.2 Quality Tasks

- [ ] Compare `tools/doit/quality.py` - check for new tasks:
    - `task_deadcode()` (uses vulture)
    - `task_complexity()` (uses radon cc)
    - `task_maintainability()` (uses radon mi)
    - Any new linting/formatting improvements

### 4.3 All Other Task Files

- [ ] Compare each of: `github.py`, `testing.py`, `security.py`, `maintenance.py`, `release.py`, `build.py`, `docs.py`, `git.py`, `install.py`, `adr.py`, `templates.py`
- [ ] Apply differences that are template improvements (not project-specific)
- [ ] Skip `template_clean.py` unless cleanup capability is desired

---

## Phase 5: pyproject.toml Tool Configuration

### 5.1 Add Missing Tool Sections

Check template's pyproject.toml for sections not present in the project:

- [ ] `[tool.vulture]` - Dead code detection configuration
- [ ] `[tool.pyright]` - LSP/type checking for AI code editors

### 5.2 Update Existing Sections

Compare each `[tool.*]` section and apply template improvements:

- [ ] `[tool.ruff]` - New rules, updated ignores
- [ ] `[tool.mypy]` - Configuration updates
- [ ] `[tool.pytest.ini_options]` - Version bumps, new options
- [ ] `[tool.coverage]` - Threshold changes, exclude patterns
- [ ] `[tool.bandit]` - New skips, exclude patterns
- [ ] `[tool.commitizen]` - Format updates

**Decision points (ask user):**

- Coverage `fail_under` threshold (project may intentionally differ)
- Cache directory locations (template uses defaults, project may customize)
- Extended ignores/excludes (project-specific suppressions should be preserved)

### 5.3 Dev Dependencies

Add any new dev dependencies required by new doit tasks:

- [ ] `vulture` (for `task_deadcode()`)
- [ ] `radon` (for `task_complexity()` and `task_maintainability()`)
- [ ] `pyright` (for `[tool.pyright]`)
- [ ] Any other new tools referenced by updated doit tasks

---

## Phase 6: AGENTS.md Updates

- [ ] Compare AGENTS.md between project and template
- [ ] Add new sections from template (e.g., Pre-Action Checks, Reasoning Examples)
- [ ] Update workflow commands and examples to match latest template patterns
- [ ] **Preserve all project-specific sections** (architecture, CLI, patterns, etc.)

---

## Phase 7: Pre-commit & Other Config

- [ ] Compare `.pre-commit-config.yaml` - hook versions, new hooks
- [ ] Compare `.github/CONTRIBUTING.md` for updated processes
- [ ] Compare `.github/pull_request_template.md` for new checklist items
- [ ] Compare `.github/ISSUE_TEMPLATE/*.yml` for template updates
- [ ] Compare `.github/python-versions.json` for version support changes

---

## Phase 8: Validation

- [ ] Run `doit check` - all checks must pass
- [ ] Run `uv run pytest` - all tests must pass
- [ ] Run `uv run pre-commit run --all-files` - all hooks must pass
- [ ] Run `doit lint` - no new linting issues
- [ ] Run `doit type_check` - no new type errors
- [ ] If new quality tasks added: run them and verify output is reasonable

---

## Phase 9: Mark as Synced

Per [Template Manager](manage.md) step [5]:

```bash
python tools/pyproject_template/manage.py sync
```

This:

1. Reads the reviewed commit from `tmp/extracted/pyproject-template-main/.template_commit` (saved during Phase 2)
2. Updates `.config/pyproject_template/settings.toml` with the template commit SHA and date
3. Cleans up the `tmp/extracted/` directory
4. Future runs of `manage.py check` will compare from this sync point

---

## Phase 10: Commit & PR

- [ ] Stage all changes
- [ ] Commit with conventional format:
  ```
  chore: synchronize with pyproject-template

  Syncs the following template improvements:
  - endavis/pyproject-template#<PR1> (description)
  - endavis/pyproject-template#<PR2> (description)
  - <additional changes summary>
  ```
- [ ] Create PR: `doit pr --title="chore: synchronize with pyproject-template" --body-file=<body>`
- [ ] PR body should reference the issue and list all synced template PRs

---

## Future Updates

Once `tools/pyproject_template/manage.py` is installed and sync state is tracked, future updates follow this simplified workflow:

1. **Check:** `python tools/pyproject_template/manage.py check`
2. **Review:** Inspect diffs for Modified/Missing files
3. **Apply:** Manually merge relevant changes
4. **Validate:** `doit check`
5. **Mark synced:** `python tools/pyproject_template/manage.py sync`
6. **Commit:** Follow issue → branch → PR workflow

---

## Key Principles

- **Selective merging:** Not all template changes apply to every project - review diffs carefully
- **Preserve divergences:** Projects may intentionally differ from template (document with ADRs)
- **Replace placeholders:** Any `package_name` references in copied template content must be replaced with the actual package name
- **Validate before commit:** Always run `doit check` before staging - mandatory per project workflow
- **One PR per sync:** Keep all template synchronization changes in a single PR unless scope is too large
- **manage.py is the official tool:** Use it for checking updates and marking sync state
- **Read the CHANGELOG:** Review template CHANGELOG to understand why changes were made before applying

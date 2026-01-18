# Keeping Up to Date

Stay in sync with improvements to the pyproject-template.

> **Tip:** The easiest way to check for updates is through the [Template Manager](manage.md):
> ```bash
> python tools/pyproject_template/manage.py
> ```
> Select option **[3] Check for template updates** to compare your project against the latest template, then **[5] Mark as synced** after applying changes.

## When to Update

Consider checking for template updates when:

- A new template version is released
- You want new tooling or workflow improvements
- You're starting a new phase of development
- Security updates are announced

## Using check_template_updates.py

The `check_template_updates.py` script compares your project against the latest template and shows what's different.

### Basic Usage

```bash
python tools/pyproject_template/check_template_updates.py
```

### What It Does

1. **Fetches the latest template** (or specified version)
2. **Opens CHANGELOG.md** so you can review what changed
3. **Compares files** and categorizes them:
   - **Modified**: Files that exist in both but differ
   - **Missing**: Files in template but not in your project
   - **Extra**: Files in your project but not in template
4. **Generates a diff** for each modified file
5. **Cleans up** temporary files

### CLI Options

```bash
# Compare against specific version
python tools/pyproject_template/check_template_updates.py --template-version v2.2.0

# Skip opening CHANGELOG in editor
python tools/pyproject_template/check_template_updates.py --skip-changelog

# Keep downloaded template for manual inspection
python tools/pyproject_template/check_template_updates.py --keep-template
```

### Example Output

```
Comparing your project against the latest pyproject-template...

Latest template release: v2.3.0
Template extracted to tmp/pyproject-template-2.3.0

Opening CHANGELOG.md for review...
(Close the editor when you're done)

=== Comparison Results ===

Modified files (differ from template):
  - .github/workflows/ci.yml
  - dodo.py
  - .pre-commit-config.yaml

Missing files (in template, not in project):
  - .github/ISSUE_TEMPLATE/chore.yml
  - docs/template/updates.md

Your project-specific files (not in template):
  - src/mypackage/custom_module.py
  - tests/test_custom.py

Would you like to see diffs for modified files? [y/N]
```

## Reviewing Changes

### Understanding the Categories

| Category | Meaning | Action |
|----------|---------|--------|
| **Modified** | File exists in both but content differs | Review diff, merge selectively |
| **Missing** | New file in template you don't have | Consider adding if useful |
| **Extra** | Your project-specific files | Keep as-is (expected) |

### Files to Usually Update

These files typically should be kept in sync:

- `.github/workflows/*.yml` - CI/CD improvements
- `.pre-commit-config.yaml` - New hooks or version bumps
- `dodo.py` - New tasks or improvements
- `tools/pyproject_template/*.py` - Template tooling

### Files to Review Carefully

These may have project-specific customizations:

- `pyproject.toml` - Your dependencies differ
- `mkdocs.yml` - Your navigation differs
- `README.md` - Your content differs
- `.github/CONTRIBUTING.md` - May have project-specific rules

### Files to Usually Skip

These are project-specific:

- `src/your_package/*` - Your code
- `tests/*` - Your tests
- `docs/*.md` - Your documentation content
- `CHANGELOG.md` - Your release history

## Merging Updates

### Manual Merge Process

1. **Run the comparison**:
   ```bash
   python tools/pyproject_template/check_template_updates.py --keep-template
   ```

2. **Review the CHANGELOG** to understand what changed and why

3. **For each modified file**, decide:
   - **Accept template version**: Copy from `tmp/pyproject-template-*/`
   - **Keep your version**: No action needed
   - **Merge selectively**: Manually combine changes

4. **For missing files**, decide:
   - **Add the file**: Copy from template
   - **Skip**: Not needed for your project

5. **Test your changes**:
   ```bash
   doit check
   ```

6. **Commit the updates**:
   ```bash
   git add -A
   git commit -m "chore: update from pyproject-template vX.Y.Z"
   ```

### Using Git Diff Tools

For complex merges, use your preferred diff tool:

```bash
# Compare specific file
diff -u your_file.py tmp/pyproject-template-*/your_file.py

# Use visual diff tool
code --diff your_file.py tmp/pyproject-template-*/your_file.py
```

## Best Practices

1. **Update regularly** - Small, frequent updates are easier than large ones

2. **Read the CHANGELOG** - Understand what changed before merging

3. **Test after updating** - Always run `doit check` after merging changes

4. **Commit updates separately** - Keep template updates in their own commits

5. **Document deviations** - If you intentionally differ from template, note why

## Troubleshooting

### Script Can't Fetch Template

If you're behind a proxy or have network issues:

```bash
# Download template manually
wget https://github.com/endavis/pyproject-template/archive/refs/heads/main.zip
unzip main.zip -d tmp/

# Compare manually
diff -r your_project/ tmp/pyproject-template-main/
```

### Too Many Differences

If your project has diverged significantly:

1. Focus on critical files first (CI, pre-commit)
2. Skip content files (docs, README)
3. Consider a fresh migration if heavily outdated

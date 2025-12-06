## Migrating an Existing Project to This Template

Use this checklist to bring an existing Python project into the template. The flow assumes hatch-vcs for versioning, commitizen for tagging/changelog, uv for deps, and doit for tasks.

### 1) Inventory & Prep
- Note current package import name, supported Python versions, dependencies (runtime/dev/extras), scripts/entry points, CI/release setup.
- Ensure current tests pass before migrating.

### 2) Bring in the Template
- Copy template files into your repo (or work in a branch): `pyproject.toml`, `dodo.py`, `.github/workflows/*`, `.envrc`, `.pre-commit-config.yaml`, `.python-version`, `AGENTS.md`, `AI_SETUP.md`, `docs/*`, `examples/*`, `mkdocs.yml`, `LICENSE`, `README.md`, `tmp/.gitkeep`.
- Keep your code/tests; you’ll move them into `src/<your_package>` and `tests/`.

### 3) Run the Configurator
- From the template root: `python configure.py`.
- Provide project name, package name (import), PyPI name, author, GitHub user, description.
- It rewrites placeholders (badges/links/docs/workflows), renames `src/package_name → src/<your_package>`, and removes itself.

### 4) Move Your Code
- Move your existing package into `src/<your_package>/`.
- Expose public API via `src/<your_package>/__init__.py`.
- Leave `_version.py` as the stub; hatch-vcs generates it at build time from git tags.

### 5) Update pyproject
- Set metadata (name, description, authors, license, classifiers, URLs).
- Add dependencies to `[project.dependencies]`; dev tools to `[project.optional-dependencies]` (e.g., `dev` extras).
- Add entry points under `[project.scripts]` if you have a CLI.
- Keep `dynamic = ["version"]` and hatch-vcs config; versions come from git tags.

### 6) Tests & Coverage
- Move tests to `tests/` (pytest style).
- Ensure coverage paths in `pyproject.toml` point to your package (default: `package_name`; replace with your import name).

### 7) Regenerate Lockfile
- Run `uv lock` to refresh `uv.lock` after deps/metadata changes.

### 8) Tasks and CI
- Local tasks: `doit check` runs format (ruff), lint, mypy, tests. `doit release` (stable), `doit release_dev` (prerelease/TestPyPI).
- Workflows: `ci.yml` runs checks; `release.yml` triggers on stable `v*` tags; `testpypi.yml` triggers on prerelease `v*-<pre>` tags.
- Verify coverage flags in workflows/dodo.py (`--cov=<your_package>`) after rename.

### 9) Docs & Badges
- README badges/links are rewritten by `configure.py`; confirm they point to your repo/PyPI.
- Update docs (`docs/installation.md`, `docs/usage.md`, `docs/api.md`) with your package usage and APIs.
- Note: `__version__` is tag-derived via hatch-vcs.

### 10) Verify Locally
- `uv sync --all-extras --dev`
- `doit check`
- Optional: `uv run doit release_dev` (prerelease test), `uv run doit release` (stable) — ensure conventional commits so commitizen can bump/tag.

### 11) Release Flow
- Prerelease/TestPyPI: `doit release_dev` → prerelease `v*` tag → `testpypi.yml`.
- Production: `doit release` → stable `v*` tag → `release.yml`.
- No manual edits to `pyproject.toml`/`_version.py`; tag is the source of truth.

### 12) Clean Up & Commit
- Remove any old CI/release configs you no longer need.
- `direnv allow` to load `.envrc`; customize `.envrc.local` if needed.
- Commit and push; monitor CI; fix any lint/type/test issues surfaced by the stricter config.

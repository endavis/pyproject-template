"""A path named in the docs should exist, or be a declared placeholder.

`test_markdown_links.py` resolves link *targets* and `test_instruction_pointers.py`
resolves quoted section references and command names. Neither looks at a path
written in backticks in prose, which is how four stale references survived
long enough to be found by a manual sweep (#773):

- `.claude/claude.md` -- named four times, wrong case, and one of them an
  instruction to *verify* a file that does not exist under that name;
- `docs/installation.md`, `docs/usage.md`, `docs/api.md` in the migration guide,
  all three moved when the documentation was reorganised;
- `.github/workflows/tests.yml`, a workflow the reader was told to create;
- `.github/copilot/settings.json`, a settings file neither this repo nor the
  Copilot CLI has.

The allowlist below is the interesting half. A doc legitimately names paths that
do not exist -- placeholders substituted during setup, files created at runtime,
worked examples. Each entry states which, so the list stays a set of decisions
rather than a pile of suppressions.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "site", "node_modules", "__pycache__", "tmp", ".mypy_cache"}

# A backticked path with a directory component and a known extension. Bare
# filenames ("run `configure.py`") are shorthand, not location claims, and are
# deliberately not checked.
DOCUMENTED_PATH = re.compile(r"`([A-Za-z0-9_./-]+\.(?:py|md|toml|yaml|yml|json|cfg|txt|sh))`")

# Allowlist entries that exist on a developer's machine but are never committed.
# They are exempt from the obsolescence check below: finding one on disk says
# nothing about whether a fresh checkout has it, and the whole point of listing
# them is that it does not.
NEVER_COMMITTED = frozenset({".claude/settings.local.json", "tmp/"})

# Paths that are allowed not to exist, and why.
ALLOWED: dict[str, str] = {
    # Substituted by configure.py when a project is created.
    "src/__PACKAGE_NAME__/": "package-name placeholder, substituted during setup",
    # Created at runtime, deliberately not checked in.
    ".config/pyproject_template/": "written by the management suite on first run",
    # Illustrative names in worked examples and templates.
    "path/to/": "generic example path",
    "src/generated/": "worked example in the rule-file READMEs (a downstream project)",
    "codegen/SKILL.md": "worked example in the rule-file READMEs",
    ".github/instructions/NAME.instructions.md": "a naming pattern, not a file",
    "tests/test_file.py": "generic example path",
    "tests/test_cache.py": "worked example in the AI walkthrough",
    "tests/test_farewell.py": "worked example in the add-a-feature tutorial",
    "tests/test_cli_farewell.py": "worked example in the add-a-feature tutorial",
    # Shorthand for a path under the user's home.
    "gh/hosts.yml": "shorthand for ~/.config/gh/hosts.yml",
    # Never committed, by policy. `.claude/settings.local.json` is blocked by the
    # `no-local-config` pre-commit hook; `tmp/` is generated output. Both exist on
    # a developer's machine and in no fresh checkout -- which is precisely why the
    # resolution below must not be satisfied by whatever happens to be on disk.
    ".claude/settings.local.json": "local config; the no-local-config hook blocks committing it",
    "tmp/": "generated artifacts and agent scratch space, gitignored",
    # AGENTS.md's before/after illustration of the temp-file convention.
    "/tmp/pr-body.md": "the 'wrong' half of the temp-file example",
    # Declared as future work.
    ".agents/skills.json": "Antigravity-side suppression, documented as planned",
}


def _markdown_files() -> list[Path]:
    return [
        path
        for path in sorted(REPO_ROOT.rglob("*.md"))
        if not any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts)
    ]


def _is_allowed(raw: str) -> bool:
    return any(raw.startswith(prefix) or raw == prefix for prefix in ALLOWED)


def _documented_paths() -> list[tuple[Path, str]]:
    """Return (doc, path) for every backticked path that claims a location."""
    found: list[tuple[Path, str]] = []
    for doc in _markdown_files():
        for match in DOCUMENTED_PATH.finditer(doc.read_text(encoding="utf-8", errors="replace")):
            raw = match.group(1)
            if "/" not in raw:
                continue  # bare filename: shorthand
            if raw.startswith(("http", "~", "{")) or "<" in raw or "*" in raw:
                continue
            found.append((doc, raw))
    return found


def test_documented_paths_exist() -> None:
    """A path in backticks should resolve, or be a declared placeholder."""
    missing = sorted(
        {
            f"{doc.relative_to(REPO_ROOT)}: {raw}"
            for doc, raw in _documented_paths()
            if not _is_allowed(raw)
            and not (REPO_ROOT / raw).exists()
            and not (doc.parent / raw).exists()
        }
    )
    assert not missing, (
        "documentation names paths that do not exist:\n  "
        + "\n  ".join(missing)
        + "\nFix the path, or add it to ALLOWED with the reason it is not a real file."
    )


def test_the_scanner_reads_something() -> None:
    """Guard against the assertion above passing on an empty scan.

    Deliberately not a threshold on the count: a downstream project has fewer
    docs than the template, and a test that fails because a project is smaller
    is the portability trap this repo warns adopters about. What matters is that
    the regex finds paths *and* that resolution works, so a scan of real files
    could report a real miss.
    """
    found = _documented_paths()
    assert found, "no documented paths found at all; the regex is not matching"
    resolved = [
        raw for doc, raw in found if (REPO_ROOT / raw).exists() or (doc.parent / raw).exists()
    ]
    assert resolved, "no documented path resolved; resolution is broken, not the docs"


def test_allowlist_entries_are_still_needed() -> None:
    """An allowlist entry for a path that now exists is a suppression to drop."""
    stale = sorted(
        prefix
        for prefix in ALLOWED
        if not prefix.endswith("/")
        and prefix not in NEVER_COMMITTED
        and (REPO_ROOT / prefix.lstrip("/")).exists()
    )
    assert not stale, (
        f"these paths exist now, so their allowlist entries are obsolete: {stale}. "
        "Remove them, so the list keeps meaning 'deliberately not a file'."
    )


def test_every_allowlist_entry_carries_a_reason() -> None:
    """The list is decisions, not suppressions."""
    for prefix, reason in ALLOWED.items():
        assert reason.strip(), f"{prefix} is allowlisted without a reason"


def test_never_committed_entries_are_allowlisted() -> None:
    """Every never-committed exemption must also carry a reason in ALLOWED.

    `NEVER_COMMITTED` only suppresses the obsolescence check. If an entry drifts
    out of `ALLOWED` it would stop being exempt from the existence check while
    still looking handled, so the two lists are held together.
    """
    for prefix in NEVER_COMMITTED:
        assert prefix in ALLOWED, f"{prefix} is exempt from staleness but not allowlisted"

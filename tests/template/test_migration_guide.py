"""The migration guide's copy step must stay honest about what it leaves behind.

`docs/template/migration.md` used to name the files to copy. That inclusion list
drifted: it never mentioned `tools/`, which `dodo.py` imports, so a migration
performed by following only the guide could not run `doit check` at all, and it
copied `.github/workflows/` while omitting the issue and PR templates that
`doit issue` and `doit pr` read (#789).

Step 2 is now "copy everything except", which is only as good as its exclusion
list. These tests hold that list to the `rsync` command printed beside it, and
to the paths the guide's own later steps invoke.
"""

from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GUIDE = REPO_ROOT / "docs" / "template" / "migration.md"

# Paths the guide's later steps invoke, and the step that needs each. A
# migration that excluded any of these would follow the guide and still fail.
# Listed as decisions rather than a blanket "nothing else is excluded" so that
# adding a legitimate exclusion stays possible without deleting the check.
REQUIRED_BY_LATER_STEPS: dict[str, str] = {
    "tools": "dodo.py imports tools.doit; without it `doit check` cannot run (step 10)",
    "dodo.py": "defines every doit task the guide invokes",
    ".github": "doit issue reads ISSUE_TEMPLATE/, doit pr reads pull_request_template.md",
    "pyproject.toml": "merged in step 5; carries the tool configuration",
    "mkdocs.yml": "the documentation site built in step 9",
    ".pre-commit-config.yaml": "installed in step 10",
}


def _guide_text() -> str:
    return GUIDE.read_text(encoding="utf-8")


def _rsync_excludes() -> set[str]:
    """Exclusions written as ``--exclude='...'`` in the guide's copy command."""
    return set(re.findall(r"--exclude='([^']+)'", _guide_text()))


def _table_excludes() -> set[str]:
    """First column of the "What is excluded, and why" table."""
    section = _guide_text().split("**What is excluded, and why:**", 1)
    assert len(section) == 2, "the guide no longer has an exclusion table"

    rows: set[str] = set()
    for line in section[1].splitlines():
        if not line.startswith("|"):
            if rows:  # table ended
                break
            continue
        cell = line.split("|")[1].strip()
        if cell.startswith("`") and cell.endswith("`"):
            rows.add(cell.strip("`"))
    return rows


def _tracked_top_level() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    return {line.split("/", 1)[0] for line in result.stdout.splitlines() if line}


def test_exclusion_table_matches_the_copy_command() -> None:
    """The prose table and the command a reader pastes must agree.

    They are two statements of one decision written six lines apart, which is
    exactly the distance at which one gets updated and the other does not.
    """
    assert _rsync_excludes() == _table_excludes(), (
        "the --exclude flags and the exclusion table disagree:\n"
        f"  command only: {sorted(_rsync_excludes() - _table_excludes())}\n"
        f"  table only:   {sorted(_table_excludes() - _rsync_excludes())}"
    )


def test_excluded_paths_are_real_template_entries() -> None:
    """An exclusion for a path the template no longer has is dead text."""
    tracked = _tracked_top_level()
    stale = sorted(
        raw for raw in _table_excludes() if raw != ".git/" and raw.rstrip("/") not in tracked
    )
    assert not stale, (
        f"the guide excludes paths the template does not have: {stale}. "
        "Remove them, or the reader is told to skip something that isn't there."
    )


def test_the_copy_keeps_what_later_steps_invoke() -> None:
    """Nothing a later step depends on may be excluded.

    This is #789 stated as an assertion: the previous guide omitted `tools/`,
    and the failure only surfaced at step 10 when `doit check` could not import
    `tools.doit`.
    """
    excluded = {raw.rstrip("/") for raw in _table_excludes()}
    tracked = _tracked_top_level()

    broken = sorted(
        f"{path} ({reason})"
        for path, reason in REQUIRED_BY_LATER_STEPS.items()
        if path in excluded or path not in tracked
    )
    assert not broken, (
        "the migration would not bring in paths the guide goes on to use:\n  " + "\n  ".join(broken)
    )


def test_the_guide_does_not_reintroduce_an_inclusion_list() -> None:
    """The copy step must stay exclusion-shaped.

    A future edit that reverts to "copy these files" would silently re-open
    #789, and the three tests above would keep passing because they only look
    at the exclusion table.
    """
    text = _guide_text()
    assert "Copy **everything except your own code**" in text, (
        "step 2 no longer states the exclusion rule; an inclusion list drifts "
        "out of date silently (#789)"
    )


def test_the_parsers_read_something() -> None:
    """Guard against the assertions above passing on an empty parse."""
    assert _rsync_excludes(), "no --exclude flags found; the parser or the guide changed"
    assert _table_excludes(), "no exclusion table rows found; the parser or the guide changed"


def _rsync_commands() -> list[str]:
    """Every ``rsync`` command in the guide, backslash continuations joined."""
    text = _guide_text().replace("\\\n", " ")
    return [re.sub(r"\s+", " ", line.strip()) for line in text.splitlines() if "rsync -a" in line]


def test_the_guide_copies_the_shipped_tests() -> None:
    """One command copies the template's tests without replacing the project's.

    The coverage gate measures `tools/`, which ships; with `tests/` excluded
    wholesale, a migrated project had nothing covering it and failed the gate
    (#1175, #731). The second copy carries no `--exclude`, since
    `_rsync_excludes()` collects every one in the guide.
    """
    commands = _rsync_commands()
    ignoring = [c for c in commands if "--ignore-existing" in c]
    assert len(ignoring) == 1, f"expected one --ignore-existing command, found {ignoring}"
    command = ignoring[0]
    assert "../pyproject-template-src/tests/" in command.split()
    assert "./tests/" in command.split()
    assert "--exclude" not in command

    main = [c for c in commands if "--exclude='src/'" in c]
    assert len(main) == 1
    assert "--ignore-existing" not in main[0]


def test_the_guide_points_at_the_mutmut_skeleton_list() -> None:
    """Guards a rename of the key, not the contents of the list it names.

    Step 6 tells the migrator to update this `[tool.mutmut]` key; if it is
    renamed, the instruction points at nothing.
    """
    key = "pytest_add_cli_args_test_selection"
    assert key in _guide_text()
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert key in data["tool"]["mutmut"]


def test_the_guides_do_not_count_hook_types() -> None:
    """Name `commit-msg`, not how many hook types the config declares.

    Both guides said "four hook types" after the config dropped to two (#1174);
    `.pre-commit-config.yaml` is the only place the count belongs.
    """
    pattern = re.compile(r"\b(\d+|one|two|three|four|five) hook types\b", re.I)
    sync_checklist = REPO_ROOT / "docs" / "template" / "ai-sync-checklist.md"
    stale = [
        f"{path.name}: {m.group(0)!r}"
        for path in (GUIDE, sync_checklist)
        for m in pattern.finditer(path.read_text(encoding="utf-8"))
    ]
    assert not stale, f"hook-type counts in prose: {stale}"

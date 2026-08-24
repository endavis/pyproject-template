"""Instruction pointers must resolve to something that exists.

`.claude/CLAUDE.md` told every Claude session, in blocks marked MANDATORY and
ending "NO EXCEPTIONS", to find two `AGENTS.md` sections that were not there and
to run a command that did not exist (#738). Authoritative framing plus no
destination is the documentation form of a control that reports success while
doing nothing.

Two pointer shapes are checked:

1. Quoted section references — ``Read <file> and locate the "## Section" section``.
2. Markdown link anchors — ``[text](path.md#anchor)``. `test_markdown_links.py`
   splits the fragment off before resolving, so it validates the file and never
   the section; this closes that half.

Anchors were all resolving when this was written. The check is preventive, and
`test_anchor_checker_detects_a_broken_anchor` keeps it from passing merely because
it looks at nothing.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# Files that instruct an agent: always-on context, commands, and skills.
INSTRUCTION_GLOBS = (
    ".claude/CLAUDE.md",
    "AGENTS.md",
    ".claude/commands/**/*.md",
    ".claude/agents/*.md",
    ".github/skills/*/SKILL.md",
    ".agents/skills/*/SKILL.md",
    ".copilot/commands/*.md",
    ".github/instructions/*.md",
)

SKIP_DIRS = {".venv", "node_modules", "site", "tmp", ".git", "__pycache__"}

# A quoted markdown heading. Backslashes are excluded so that shell examples like
# `--body="## Problem\nDescribe the problem"` in AGENTS.md are not mistaken for
# section references — they are literal payloads, not pointers.
QUOTED_HEADING = re.compile(r'"(#{1,6} [^"\\]+)"')
MD_FILENAME = re.compile(r"([\w./-]+\.md)")
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def _instruction_files() -> list[Path]:
    files: list[Path] = []
    for pattern in INSTRUCTION_GLOBS:
        files += sorted(REPO_ROOT.glob(pattern))
    return [f for f in files if f.is_file()]


def _markdown_files() -> list[Path]:
    return sorted(
        p for p in REPO_ROOT.rglob("*.md") if not SKIP_DIRS.intersection(p.parts) and p.is_file()
    )


def _headings(path: Path) -> set[str] | None:
    """Return the literal heading lines in *path*, or None if unreadable."""
    try:
        return {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("#")
        }
    except OSError:
        return None


def _slug(heading: str) -> str:
    """GitHub-style anchor slug for a heading line."""
    text = re.sub(r"^#+\s*", "", heading).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def _anchors(path: Path) -> set[str] | None:
    headings = _headings(path)
    return None if headings is None else {_slug(h) for h in headings}


def _section_references() -> list[tuple[Path, int, str, str]]:
    """Return (source, line_no, quoted_heading, target_filename) for each pointer."""
    refs = []
    for source in _instruction_files():
        for line_no, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            for match in QUOTED_HEADING.finditer(line):
                targets = [
                    name
                    for name in MD_FILENAME.findall(line)
                    if name.lower() != source.name.lower()
                ]
                for name in targets:
                    refs.append((source, line_no, match.group(1), name))
    return refs


def _resolve_named(name: str) -> Path | None:
    """Resolve a bare filename mentioned in prose to a file in the repo."""
    direct = REPO_ROOT / name
    if direct.is_file():
        return direct
    for candidate in REPO_ROOT.rglob(Path(name).name):
        if not SKIP_DIRS.intersection(candidate.parts):
            return candidate
    return None


def test_quoted_section_references_resolve() -> None:
    """Every `Read <file> and locate the "## X" section` must name a real heading."""
    broken = []
    for source, line_no, heading, target_name in _section_references():
        target = _resolve_named(target_name)
        if target is None:
            broken.append(f"{source.relative_to(REPO_ROOT)}:{line_no} -> {target_name} not found")
            continue
        headings = _headings(target)
        if headings is not None and heading not in headings:
            broken.append(
                f"{source.relative_to(REPO_ROOT)}:{line_no} -> {heading!r} not in {target_name}"
            )

    assert not broken, "instruction pointers that resolve to nothing:\n  " + "\n  ".join(broken)


def test_markdown_anchors_resolve() -> None:
    """`[text](file.md#anchor)` must name a heading that exists in that file.

    Complements `tests/test_markdown_links.py`, which strips the fragment.
    """
    broken = []
    for source in _markdown_files():
        for match in MD_LINK.finditer(source.read_text(encoding="utf-8")):
            target = match.group(1)
            if target.startswith(("http", "mailto:", "#")) or "#" not in target:
                continue
            path_part, _, fragment = target.partition("#")
            resolved = (source.parent / path_part).resolve()
            anchors = _anchors(resolved)
            if anchors is None:
                broken.append(f"{source.relative_to(REPO_ROOT)}: {target} (file missing)")
            elif fragment.lower() not in anchors:
                broken.append(f"{source.relative_to(REPO_ROOT)}: {target}")

    assert not broken, "markdown links with anchors that resolve to nothing:\n  " + "\n  ".join(
        broken
    )


def test_referenced_commands_exist() -> None:
    """A `/command` or `$skill` named in an instruction file must be installed.

    `/commit-commands:commit` was named in a MANDATORY block for months without
    ever existing (#738).
    """
    known: set[str] = set()
    for path in REPO_ROOT.glob(".claude/commands/**/*.md"):
        rel = path.relative_to(REPO_ROOT / ".claude" / "commands").with_suffix("")
        known.add(rel.as_posix().replace("/", ":"))
    for pattern in (".github/skills/*/SKILL.md", ".agents/skills/*/SKILL.md"):
        known |= {p.parent.name for p in REPO_ROOT.glob(pattern)}
    for path in REPO_ROOT.glob(".copilot/commands/*.md"):
        known.add(path.stem)

    claude_md = REPO_ROOT / ".claude" / "CLAUDE.md"
    broken = [
        name
        # Not preceded by a word char, backtick, slash, dot or @ — so the
        # `@./rules/*.md` import reads as a path, not a command — and not
        # followed by a path separator.
        for name in re.findall(
            r"(?<![\w`/.@])/([a-z][\w-]*(?::[\w-]+)?)(?![\w/-])",
            claude_md.read_text("utf-8"),
        )
        if name not in known and name.split(":")[0] not in known
    ]

    assert not broken, (
        f"CLAUDE.md names commands that are not installed: {sorted(set(broken))}. "
        "Available: " + ", ".join(sorted(known)[:12]) + " ..."
    )


def test_the_scanner_actually_finds_references() -> None:
    """Guard against the pointer regexes silently matching nothing."""
    assert _section_references(), "no quoted section references found; the regex has gone stale"

    anchored = [
        m.group(1)
        for source in _markdown_files()
        for m in MD_LINK.finditer(source.read_text(encoding="utf-8"))
        if "#" in m.group(1) and not m.group(1).startswith(("http", "mailto:", "#"))
    ]
    assert len(anchored) >= 10, f"only {len(anchored)} anchored links found; expected the docs set"


def test_shell_payloads_are_not_treated_as_pointers() -> None:
    """`--body="## Problem\\nDescribe..."` is a payload, not a section reference.

    AGENTS.md's issue-creation examples embed heading text in shell strings. Left
    unfiltered they read as seven dangling pointers and would drown the real ones.
    """
    payload = '--body="## Problem\\nDescribe the problem\\n\\n## Proposed Solution\\nDo it"'
    assert not QUOTED_HEADING.findall(payload), (
        "the quoted-heading regex matched a shell payload; it must exclude escapes"
    )


def test_anchor_checker_detects_a_broken_anchor(tmp_path: Path) -> None:
    """The anchor check must fail on a fragment that names no heading.

    Every anchor in the repo resolves today, so without this the check could pass
    because it found nothing rather than because everything is sound.
    """
    target = tmp_path / "target.md"
    target.write_text("# Real Heading\n", encoding="utf-8")

    assert _anchors(target) == {"real-heading"}
    assert "no-such-heading" not in (_anchors(target) or set())


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        ("## Commit Guidelines", "commit-guidelines"),
        ("### 5. Pre-Action Checks (Dynamic Context)", "5-pre-action-checks-dynamic-context"),
        ("# Overview", "overview"),
    ],
)
def test_slug_matches_github_anchor_rules(heading: str, expected: str) -> None:
    """Anchor slugs must match what GitHub generates, or the check is nonsense."""
    assert _slug(heading) == expected

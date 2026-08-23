"""Contract tests for per-stack rule files.

Rule files are mirrored across all three agent rule surfaces because every agent
in the delegation matrix edits this codebase. The checklist body must stay
identical everywhere: a rule that disagrees with itself across agents is worse
than no rule, because whichever agent is driving decides which version applies.

These tests also enforce the authoring discipline from
``.claude/rules/README.md`` — the 30-line cap and the mandatory
``Observed failures:`` footer, which is what separates a rule derived from real
defects from a generic best-practices checklist.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

RULE_NAME = "typing-branch-narrowing"

# Every surface that must carry the rule, and how each one is loaded.
RULE_PATHS = {
    "claude": REPO_ROOT / ".claude" / "rules" / f"{RULE_NAME}.md",
    "copilot": REPO_ROOT / ".github" / "instructions" / f"{RULE_NAME}.instructions.md",
    "agents": REPO_ROOT / ".agents" / "skills" / RULE_NAME / "SKILL.md",
}

MAX_LINES = 30


def _body(path: Path) -> str:
    """Return the rule body, stripped of any YAML frontmatter.

    Copilot requires ``applyTo:`` frontmatter and Codex/Antigravity require
    ``name:``/``description:``; only the checklist below it must match.
    """
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    return text.strip()


@pytest.mark.parametrize("surface", sorted(RULE_PATHS))
def test_rule_exists_on_every_surface(surface: str) -> None:
    """The rule is present for all three agent families."""
    assert RULE_PATHS[surface].exists(), f"missing {surface} copy: {RULE_PATHS[surface]}"


def test_rule_bodies_are_identical_across_surfaces() -> None:
    """The checklist must not drift between agents."""
    bodies = {name: _body(path) for name, path in RULE_PATHS.items()}
    reference = bodies["claude"]
    mismatched = [name for name, body in bodies.items() if body != reference]
    assert not mismatched, f"rule body differs on {mismatched}; update all three surfaces together"


@pytest.mark.parametrize("surface", sorted(RULE_PATHS))
def test_rule_declares_observed_failures(surface: str) -> None:
    """A rule with no observed-failure link is a guess, not a discipline."""
    body = _body(RULE_PATHS[surface])
    match = re.search(r"^Observed failures:\s*(.+)$", body, re.MULTILINE)
    assert match, f"{surface} copy is missing the 'Observed failures:' footer"
    assert re.search(r"#\d+", match.group(1)), (
        f"{surface} footer must cite at least one real issue or PR"
    )


@pytest.mark.parametrize("surface", sorted(RULE_PATHS))
def test_rule_names_a_skill_gate(surface: str) -> None:
    """``Skill:`` is the first body line — it names the capability gate."""
    assert _body(RULE_PATHS[surface]).splitlines()[0].startswith("Skill: ")


@pytest.mark.parametrize("surface", sorted(RULE_PATHS))
def test_rule_stays_within_the_line_budget(surface: str) -> None:
    """Past 30 lines a rule stops surviving a long context window; split it."""
    count = len(RULE_PATHS[surface].read_text(encoding="utf-8").splitlines())
    assert count <= MAX_LINES, f"{surface} copy is {count} lines (max {MAX_LINES})"


def test_copilot_copy_declares_a_path_scope() -> None:
    """Copilot's loader requires ``applyTo:`` frontmatter to gate the file."""
    text = RULE_PATHS["copilot"].read_text(encoding="utf-8")
    assert text.startswith("---"), "Copilot instructions need YAML frontmatter"
    assert re.search(r"^applyTo:\s*\S+", text, re.MULTILINE)


def test_agents_copy_declares_a_skill_gate_description() -> None:
    """``description:`` is the skill-gate trigger for Codex and Antigravity."""
    text = RULE_PATHS["agents"].read_text(encoding="utf-8")
    assert re.search(r"^name:\s*\S+", text, re.MULTILINE)
    assert re.search(r"^description:\s*\S+", text, re.MULTILINE)


def test_claude_loads_rule_files() -> None:
    """The glob import must be live, not commented out.

    A rule file that ships but never loads is a mechanism built and not used.
    """
    text = (REPO_ROOT / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")
    assert re.search(r"^@\./rules/\*\.md\s*$", text, re.MULTILINE), (
        "CLAUDE.md must import ./rules/*.md (uncommented)"
    )

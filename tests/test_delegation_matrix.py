"""Validate the cross-agent delegation matrix file layout.

Static test only — no CLI or model invocations. Verifies that:

- Every source x target x action command/skill cell resolves to a file at the
  documented path (Codex and Antigravity share the host-agnostic
  `.agents/skills/delegate-*` files, so distinct files number fewer than cells).
- The matrix documentation page exists.

The matrix is sized from the agents this project wires, not from the template's
own four. In the template that is 48 cells over 40 distinct files; a project that
keeps one agent has no cross-agent matrix and checks nothing here, rather than
failing 37 cells for agents it deliberately dropped (#690).

See `docs/development/ai/cross-agent-delegation.md` and issues #550, #640.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from agent_roster import present_agents

REPO_ROOT = Path(__file__).resolve().parents[1]

ACTIONS = ("plan", "implement", "review", "adversarial-review")

# The agents this project actually wires. The template wires all four; a project
# spawned from it keeps only the ones it uses, and must not be told its suite is
# broken for declining the rest (#690).
AGENTS = present_agents()


def _cross_pairs() -> list[tuple[str, str]]:
    """Yield (source, target) pairs where source != target.

    Empty for a single-agent project — there is no cross-agent matrix to check —
    which parametrizes the cell tests away rather than failing them.
    """
    return [(s, t) for s in AGENTS for t in AGENTS if s != t]


def _expected_path(source: str, target: str, action: str) -> Path:
    """Map a (source, target, action) cell to its on-disk location.

    Copilot bridges live under .github/skills/<target>-<action>/SKILL.md.
    Copilot CLI discovers project skills from .github/skills/, .agents/skills/,
    and .claude/skills/ (per @github/copilot SDK index.d.ts), but we use
    .github/skills/ specifically because it's the only one of those paths that
    Claude does not also read — placing the bridges there avoids surfacing
    duplicate slash commands in Claude alongside its native /<target>:<action>.
    Skill names use hyphen because skill names cannot contain colons.
    """
    if source == "claude":
        return REPO_ROOT / ".claude" / "commands" / target / f"{action}.md"
    if source == "copilot":
        return REPO_ROOT / ".github" / "skills" / f"{target}-{action}" / "SKILL.md"
    if source in ("codex", "antigravity"):
        # Antigravity shares Codex's host-agnostic delegate-* skills in
        # .agents/skills/ (both CLIs read that directory). antigravity->codex
        # uses the new delegate-codex-*, codex->antigravity uses
        # delegate-antigravity-*, and delegate-{claude,copilot}-* are
        # reused by both sources.
        return REPO_ROOT / ".agents" / "skills" / f"delegate-{target}-{action}" / "SKILL.md"
    raise ValueError(f"unknown source agent: {source}")


@pytest.mark.parametrize(("source", "target"), _cross_pairs())
@pytest.mark.parametrize("action", ACTIONS)
def test_delegation_file_exists(source: str, target: str, action: str) -> None:
    """Every (source, target, action) cell has a corresponding file."""
    path = _expected_path(source, target, action)
    assert path.is_file(), f"missing delegation file: {path.relative_to(REPO_ROOT)}"


def test_total_file_count() -> None:
    """Every cross-agent cell resolves, and Codex/Antigravity share their files.

    The template wires four agents: 4 sources x 3 targets x 4 actions = 48 cells,
    of which 8 share a file, leaving 40 distinct. Both counts are *derived* from
    the agents this project wires rather than pinned, so dropping an agent
    narrows the matrix instead of failing it (#690).
    """
    cells = [(s, t, a) for s, t in _cross_pairs() for a in ACTIONS]
    expected_cells = len(AGENTS) * max(len(AGENTS) - 1, 0) * len(ACTIONS)
    assert len(cells) == expected_cells

    missing = [
        str(_expected_path(s, t, a).relative_to(REPO_ROOT))
        for s, t, a in cells
        if not _expected_path(s, t, a).is_file()
    ]
    assert not missing, f"missing delegation files: {missing}"

    # Codex and Antigravity both read the host-agnostic .agents/skills/delegate-*
    # files, so when a project wires both, every cell they aim at a third agent
    # collapses onto one file.
    both_share = "codex" in AGENTS and "antigravity" in AGENTS
    shared_cells = (
        len([t for t in AGENTS if t not in ("codex", "antigravity")]) * len(ACTIONS)
        if both_share
        else 0
    )
    distinct = {_expected_path(s, t, a) for s, t, a in cells}
    assert len(distinct) == expected_cells - shared_cells, (
        f"expected {expected_cells - shared_cells} distinct files for agents "
        f"{AGENTS}, found {len(distinct)}"
    )


def test_matrix_doc_exists() -> None:
    """The cross-agent delegation doc page exists."""
    doc = REPO_ROOT / "docs" / "development" / "ai" / "cross-agent-delegation.md"
    assert doc.is_file(), f"missing matrix doc: {doc.relative_to(REPO_ROOT)}"

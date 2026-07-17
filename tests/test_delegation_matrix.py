"""Validate the cross-agent delegation matrix file layout.

Static test only — no CLI or model invocations. Verifies that:

- All 80 source x target x action command/skill cells resolve to files at the
  documented paths (Codex and Antigravity share the host-agnostic
  `.agents/skills/delegate-*` files, so distinct files number 68, not 80).
- `.gemini/settings.json` `skills.disabled` contains all 20 `.agents/skills/`
  delegation skill names (preventing Gemini from loading them).
- The matrix documentation page exists.

See `docs/development/ai/cross-agent-delegation.md` and issues #550, #640.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

AGENTS = ("claude", "codex", "gemini", "copilot", "antigravity")
ACTIONS = ("plan", "implement", "review", "adversarial-review")


def _cross_pairs() -> list[tuple[str, str]]:
    """Yield (source, target) pairs where source != target."""
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
    if source == "gemini":
        return REPO_ROOT / ".gemini" / "commands" / target / f"{action}.toml"
    if source == "copilot":
        return REPO_ROOT / ".github" / "skills" / f"{target}-{action}" / "SKILL.md"
    if source in ("codex", "antigravity"):
        # Antigravity shares Codex's host-agnostic delegate-* skills in
        # .agents/skills/ (both CLIs read that directory). antigravity->codex
        # uses the new delegate-codex-*, codex->antigravity uses
        # delegate-antigravity-*, and delegate-{claude,gemini,copilot}-* are
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
    """5 sources x 4 targets x 4 actions = 80 cross-agent cells.

    Codex and Antigravity share the host-agnostic .agents/skills/delegate-*
    files, so the 12 antigravity->{claude,gemini,copilot} cells reuse Codex's
    files and the distinct-file count is 68, not 80.
    """
    cells = [(s, t, a) for s, t in _cross_pairs() for a in ACTIONS]
    assert len(cells) == 80

    missing = [
        str(_expected_path(s, t, a).relative_to(REPO_ROOT))
        for s, t, a in cells
        if not _expected_path(s, t, a).is_file()
    ]
    assert not missing, f"missing delegation files: {missing}"

    distinct = {_expected_path(s, t, a) for s, t, a in cells}
    assert len(distinct) == 68, f"expected 68 distinct files, found {len(distinct)}"


def test_gemini_disabled_list_contains_delegation_skills() -> None:
    """All 20 .agents/skills/ delegation skill names are disabled in .gemini/settings.json.

    Without this, Gemini auto-loads the skills from .agents/skills/ (its docs document
    that path as cross-agent interop) and may mis-activate them. Codex and Antigravity
    both read .agents/skills/, so every delegate-<target>-<action> across all five agents
    exists there. See docs/development/ai/cross-agent-delegation.md.
    """
    settings_path = REPO_ROOT / ".gemini" / "settings.json"
    settings = json.loads(settings_path.read_text())
    disabled = set(settings["skills"]["disabled"])

    expected_skills = {f"delegate-{target}-{action}" for target in AGENTS for action in ACTIONS}
    assert len(expected_skills) == 20

    missing = expected_skills - disabled
    assert not missing, (
        f"the following delegation skills must be added to "
        f".gemini/settings.json skills.disabled: {sorted(missing)}"
    )


def test_matrix_doc_exists() -> None:
    """The cross-agent delegation doc page exists."""
    doc = REPO_ROOT / "docs" / "development" / "ai" / "cross-agent-delegation.md"
    assert doc.is_file(), f"missing matrix doc: {doc.relative_to(REPO_ROOT)}"

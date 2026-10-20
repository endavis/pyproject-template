"""The cross-agent workflow files must agree, not merely exist.

`test_delegation_matrix.py` checks that every command/skill file is present.
Presence is not agreement: the files encode a shared workflow contract that lets
a user switch agents mid-workflow without losing state. Until #692 nothing
checked that they still said the same things, so the contract held only by
manual discipline across dozens of files.

`plan`, `implement` and the `ghi-finalize` handoff were per-agent matrix files
until #976 replaced them with the single shared `implement-issue` skill
(`.agents/skills/implement-issue/SKILL.md`, generated for Claude by `doit
skills_sync`). Its contract is checked directly against that one source rather
than per-agent, since there is only one file to agree with itself.

The contract itself is documented in
``docs/development/ai/cross-agent-delegation.md``; this module is its enforcement.
When the two disagree, the doc is the specification and this file is the bug.

Per-agent exemptions are declared in `EXEMPTIONS` with a reason, because uniform
prose is not the goal — agreement on the contract is.

Assertions are scoped to the agents a project actually wires, following the
convention in `tests/agent_roster.py` (#690).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from agent_roster import agent_is_present, present_agents

REPO_ROOT = Path(__file__).resolve().parents[1]

# Where each agent keeps its self-action workflow file for a given action.
SELF_ACTION_LAYOUTS = {
    "claude": lambda action: REPO_ROOT / ".claude" / "commands" / "claude" / f"{action}.md",
    "copilot": lambda action: REPO_ROOT / ".github" / "skills" / f"copilot-{action}" / "SKILL.md",
    "codex": lambda action: REPO_ROOT / ".agents" / "skills" / f"codex-{action}" / "SKILL.md",
    "antigravity": (
        lambda action: REPO_ROOT / ".agents" / "skills" / f"antigravity-{action}" / "SKILL.md"
    ),
}

# The single shared implement-issue skill source. Its generated Claude copy is
# asserted byte-identical by tests/template/test_skills_sync.py, so checking
# the source here is sufficient.
IMPLEMENT_ISSUE_FILE = REPO_ROOT / ".agents" / "skills" / "implement-issue" / "SKILL.md"

# Contract elements, by the action whose files must carry them. Each entry is
# (label, substring). Substrings rather than regexes: the contract is a literal
# string the agents must reproduce, so a literal check is the honest test.
CONTRACT = {
    "review": [
        ("read-only constraint", "**Read-only.**"),
    ],
    "adversarial-review": [
        ("read-only constraint", "**Read-only.**"),
    ],
}

# implement-issue carries its own contract — one shared file, not one per agent.
IMPLEMENT_ISSUE_CONTRACT: list[tuple[str, str]] = [
    ("plan-comment header", "Implementation Plan for"),
    ("branch-name pattern", "<type>/"),
    ("validation command", "doit check"),
    ("docs validation command", "doit docs_build"),
    ("pr command", "doit pr"),
    ("issue reference", "Addresses #"),
    ("merge-gate check", "require-label"),
]

# (action, agent) pairs that legitimately omit an element, with the reason.
# An exemption is a documented architectural difference, not a licence to drift.
EXEMPTIONS: dict[tuple[str, str, str], str] = {}

# The identical sentence every review file must carry, so the constraint cannot
# be reworded into something weaker on one surface.
READ_ONLY_SENTENCE = (
    "**Read-only.** Review and report — do not edit files, commit, or push. "
    "Findings go to the user and the PR; any fix is a separate change the user asks for."
)


def _self_action_files(action: str) -> list[tuple[str, Path]]:
    """Return (agent, path) for each wired agent's file for *action*."""
    return [(agent, SELF_ACTION_LAYOUTS[agent](action)) for agent in present_agents()]


def _contract_violations(action: str, agent: str, text: str) -> list[str]:
    """Return the contract elements *text* is missing for (*action*, *agent*).

    Shared by the real check and its non-vacuity companion, so the companion
    exercises the logic that actually runs rather than a restatement of it.
    """
    return [
        f"{agent}/{action} is missing the {label} ({needle!r})"
        for label, needle in CONTRACT[action]
        if needle not in text and (action, agent, label) not in EXEMPTIONS
    ]


@pytest.mark.parametrize("action", sorted(CONTRACT))
def test_self_action_files_carry_the_contract(action: str) -> None:
    """Every wired agent's file for *action* contains that action's contract elements."""
    missing: list[str] = []

    for agent, path in _self_action_files(action):
        if not path.is_file():
            missing.append(f"{agent}: {path.relative_to(REPO_ROOT)} does not exist")
            continue
        missing += _contract_violations(action, agent, path.read_text(encoding="utf-8"))

    assert not missing, (
        "cross-agent contract violations:\n  "
        + "\n  ".join(missing)
        + "\n\nThe contract is specified in docs/development/ai/cross-agent-delegation.md. "
        "If an agent legitimately differs, declare it in EXEMPTIONS with a reason."
    )


def test_read_only_constraint_is_worded_identically() -> None:
    """The review constraint must be the same sentence everywhere.

    A constraint that is paraphrased per host drifts into a weaker version on one
    surface, and whichever agent is driving decides which version applies — the
    same failure mode the rule-file mirror guards against.
    """
    divergent = []
    for action in ("review", "adversarial-review"):
        for agent, path in _self_action_files(action):
            if not path.is_file():
                continue
            if READ_ONLY_SENTENCE not in path.read_text(encoding="utf-8"):
                divergent.append(f"{agent}/{action}")

    assert not divergent, (
        f"these files do not carry the exact read-only sentence: {divergent}. "
        "Reword all of them together or none."
    )


def test_implement_issue_file_carries_its_contract() -> None:
    """The shared `implement-issue` skill carries every literal the workflow promises.

    There is one source file (`.agents/skills/implement-issue/SKILL.md`); its
    generated Claude copy is asserted byte-identical to it by
    `tests/template/test_skills_sync.py`, so checking the source is sufficient.
    """
    assert IMPLEMENT_ISSUE_FILE.is_file(), (
        f"missing implement-issue skill: {IMPLEMENT_ISSUE_FILE.relative_to(REPO_ROOT)}"
    )
    text = IMPLEMENT_ISSUE_FILE.read_text(encoding="utf-8")
    missing = [
        f"{label} ({needle!r})" for label, needle in IMPLEMENT_ISSUE_CONTRACT if needle not in text
    ]
    assert not missing, f"implement-issue skill is missing: {missing}"


def test_implement_issue_forbids_merge_actions() -> None:
    """implement-issue must say it never applies ready-to-merge, merges, or closes the issue.

    Those stay the user's decisions (ADR-9006's merge gate is unchanged by #976).
    """
    text = IMPLEMENT_ISSUE_FILE.read_text(encoding="utf-8")
    assert "ready-to-merge" in text
    assert "never merges" in text or "never merge" in text
    assert "closes the issue" in text or "close the issue" in text


def test_the_contract_scanner_detects_a_violation() -> None:
    """Feeding the checker a file with none of the contract must flag every element.

    Without this, `test_self_action_files_carry_the_contract` could pass because
    the checker finds nothing to complain about rather than because the files
    comply. Uses an agent with no exemptions so nothing is silently skipped.
    """
    empty = "an unrelated document with none of the contract in it"

    for action, elements in CONTRACT.items():
        violations = _contract_violations(action, "copilot", empty)
        assert len(violations) == len(elements), (
            f"scanner found {len(violations)} of {len(elements)} missing elements "
            f"for {action!r}; the needles are too weak to assert on"
        )


def test_exemptions_are_real_and_documented() -> None:
    """Every exemption must name a live agent/action and actually be needed.

    Stops the exemption table from outliving the difference it excuses — the way
    an allowlist quietly becomes a list of things nobody checks.
    """
    stale: list[str] = []
    for (action, agent, label), reason in EXEMPTIONS.items():
        assert reason.strip(), f"exemption ({action}, {agent}, {label}) needs a reason"
        if not agent_is_present(agent):
            continue
        path = SELF_ACTION_LAYOUTS[agent](action)
        needle = next(n for lbl, n in CONTRACT[action] if lbl == label)
        if path.is_file() and needle in path.read_text(encoding="utf-8"):
            stale.append(f"({action}, {agent}, {label}) — the file now carries {needle!r}")

    assert not stale, f"these exemptions are no longer needed and should be removed: {stale}"

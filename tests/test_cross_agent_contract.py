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

The three `multi-*` orchestrators used to hardcode one agent as the one running
inline (`(self)`) and carry their own copy of the non-interactive invocation
table per host, until #975 rewrote each as a single shared skill
(`.agents/skills/multi-{plan,review,adversarial-review}/SKILL.md`, generated
for Claude the same way) that identifies "self" generically: "the entry in the
table that matches the CLI running this skill is you." Their contract is
checked the same way `implement-issue`'s is — against the one shared source.

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

# The three shared multi-* orchestrator sources. Same reasoning as
# IMPLEMENT_ISSUE_FILE: each has one generated Claude copy, asserted
# byte-identical by tests/template/test_skills_sync.py, so checking the source
# is sufficient.
MULTI_AGENT_FILES: dict[str, Path] = {
    "multi-plan": REPO_ROOT / ".agents" / "skills" / "multi-plan" / "SKILL.md",
    "multi-review": REPO_ROOT / ".agents" / "skills" / "multi-review" / "SKILL.md",
    "multi-adversarial-review": (
        REPO_ROOT / ".agents" / "skills" / "multi-adversarial-review" / "SKILL.md"
    ),
}

# The one sentence that makes Codex run every `gh` command as its own standalone
# shell command. The exec-policy allow rule in `.codex/rules/gh.rules` only
# matches when `gh` is the exec'd prefix — chained with `;`, `&&`, or a pipe, the
# exec'd prefix is the shell instead, and the call falls back into the sandbox,
# which has no network at all (#980). Asserted byte-identical everywhere a
# non-interactive prompt reaches Codex, the same way READ_ONLY_SENTENCE is.
GH_STANDALONE_SENTENCE = (
    "Run every `gh` command as its own standalone shell command, never chained with "
    "other commands via `;`, `&&`, or a pipe — only a standalone `gh` matches the Codex "
    "allow rule in `.codex/rules/gh.rules`; chained, it runs inside the sandbox with no "
    "network access."
)

# The non-interactive invocation each CLI needs, copied verbatim from
# docs/development/ai/cross-agent-delegation.md's "Non-interactive flags per
# CLI" table. test_non_interactive_invocations_match_the_doc keeps this copy
# honest against that doc.
NON_INTERACTIVE_INVOCATIONS: dict[str, str] = {
    "claude": "claude -p '<prompt>'",
    "codex": (
        "codex -a never --dangerously-bypass-hook-trust exec "
        f"'{GH_STANDALONE_SENTENCE} <prompt>' < /dev/null"
    ),
    "copilot": "copilot --allow-all -p '<prompt>'",
    "antigravity": (
        "agy -p '<prompt>' --dangerously-skip-permissions "
        '--add-dir "$(git rev-parse --show-toplevel)"'
    ),
}

# The six Codex bridge files that carry a *concrete* (not `<prompt>`-templated)
# exec string rather than a copy of NON_INTERACTIVE_INVOCATIONS["codex"] — Hybrid
# C's "activate $codex-review/$codex-adversarial-review if available" fallback can
# still reach `gh pr view`/`gh pr diff` (#980), so each needs
# GH_STANDALONE_SENTENCE prepended by hand.
CODEX_BRIDGE_FILES: dict[str, Path] = {
    "delegate-codex-review": (
        REPO_ROOT / ".agents" / "skills" / "delegate-codex-review" / "SKILL.md"
    ),
    "delegate-codex-adversarial-review": (
        REPO_ROOT / ".agents" / "skills" / "delegate-codex-adversarial-review" / "SKILL.md"
    ),
    "copilot-codex-review": REPO_ROOT / ".github" / "skills" / "codex-review" / "SKILL.md",
    "copilot-codex-adversarial-review": (
        REPO_ROOT / ".github" / "skills" / "codex-adversarial-review" / "SKILL.md"
    ),
    "claude-codex-review": REPO_ROOT / ".claude" / "commands" / "codex" / "review.md",
    "claude-codex-adversarial-review": (
        REPO_ROOT / ".claude" / "commands" / "codex" / "adversarial-review.md"
    ),
}

CROSS_AGENT_DELEGATION_DOC = REPO_ROOT / "docs" / "development" / "ai" / "cross-agent-delegation.md"

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


# --- multi-* orchestrator contract (#975) ---


def test_non_interactive_invocations_match_the_doc() -> None:
    """NON_INTERACTIVE_INVOCATIONS must still match cross-agent-delegation.md.

    That doc is the specification (see module docstring); if this copy drifts
    from it, this test — not the doc — is the bug to fix.
    """
    doc_text = CROSS_AGENT_DELEGATION_DOC.read_text(encoding="utf-8")
    missing = [
        f"{agent}: {invocation!r}"
        for agent, invocation in NON_INTERACTIVE_INVOCATIONS.items()
        if invocation not in doc_text
    ]
    assert not missing, (
        f"these invocations no longer match {CROSS_AGENT_DELEGATION_DOC.relative_to(REPO_ROOT)}: "
        f"{missing}"
    )


def test_multi_agent_files_carry_every_invocation() -> None:
    """Each multi-* skill's invocation table must carry all four CLIs' commands verbatim.

    A headless run can't reliably go and read cross-agent-delegation.md mid-skill
    (see module docstring), so each multi-* file carries its own copy of the
    table — this is what keeps that copy from drifting.
    """
    missing: list[str] = []
    for name, path in MULTI_AGENT_FILES.items():
        if not path.is_file():
            missing.append(f"{name}: {path.relative_to(REPO_ROOT)} does not exist")
            continue
        text = path.read_text(encoding="utf-8")
        for agent, invocation in NON_INTERACTIVE_INVOCATIONS.items():
            if invocation not in text:
                missing.append(f"{name} is missing the {agent} invocation ({invocation!r})")

    assert not missing, "multi-* invocation table violations:\n  " + "\n  ".join(missing)


def test_multi_agent_files_do_not_hardcode_a_self_agent() -> None:
    """No multi-* file may hardcode one agent as the one running inline.

    The old per-agent files each had a branch like "If `codex` is in the agent
    list (self):". The shared file replaces that with "the entry in the table
    that matches the CLI running this skill is you" — see the module docstring.
    """
    hardcoded = [
        name
        for name, path in MULTI_AGENT_FILES.items()
        if path.is_file() and "(self)" in path.read_text(encoding="utf-8")
    ]
    assert not hardcoded, (
        f"these multi-* files hardcode an agent as (self), which only one CLI can be: {hardcoded}"
    )


def test_multi_review_files_carry_the_read_only_sentence() -> None:
    """`multi-review` and `multi-adversarial-review` must carry READ_ONLY_SENTENCE verbatim.

    They used to only paraphrase it; a paraphrase drifts into a weaker version,
    the same failure mode `test_read_only_constraint_is_worded_identically`
    guards against for the self-action files.
    """
    divergent = [
        name
        for name in ("multi-review", "multi-adversarial-review")
        if READ_ONLY_SENTENCE not in MULTI_AGENT_FILES[name].read_text(encoding="utf-8")
    ]
    assert not divergent, (
        f"these multi-* files do not carry the exact read-only sentence: {divergent}"
    )


def test_codex_bridge_files_carry_the_gh_standalone_sentence() -> None:
    """The six Codex bridge files must carry the sentence and close Codex's stdin.

    Hybrid C's "activate $codex-review/$codex-adversarial-review if available"
    fallback can still reach `gh pr view`/`gh pr diff` from inside a headless
    Codex session, so these bridges need the standalone-`gh` requirement
    prepended to their inline prompt, not just a link to the doc (#980).
    """
    missing: list[str] = []
    for name, path in CODEX_BRIDGE_FILES.items():
        if not path.is_file():
            missing.append(f"{name}: {path.relative_to(REPO_ROOT)} does not exist")
            continue
        text = path.read_text(encoding="utf-8")
        if GH_STANDALONE_SENTENCE not in text:
            missing.append(f"{name} is missing GH_STANDALONE_SENTENCE")
        exec_lines = [line for line in text.splitlines() if "trust exec '" in line]
        if not exec_lines or not all(line.endswith("' < /dev/null") for line in exec_lines):
            missing.append(f"{name}: a codex exec line does not end in < /dev/null")

    assert not missing, "Codex bridge file violations:\n  " + "\n  ".join(missing)

"""Tests for AI agent workflow assets checked into the template."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_codex_workflow_skills_exist() -> None:
    """Codex workflow skills should be present in the repo skills directory."""
    skill_paths = [
        REPO_ROOT / ".agents" / "skills" / "codex-plan" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "codex-implement" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "codex-review" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "codex-adversarial-review" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "ghi-finalize" / "SKILL.md",
    ]

    for skill_path in skill_paths:
        assert skill_path.exists(), f"Missing Codex skill: {skill_path}"


def test_multi_orchestrator_files_exist() -> None:
    """multi-* orchestrators (plan, review, adversarial-review) should exist for all 4 hosts."""
    paths = [
        # Claude
        REPO_ROOT / ".claude" / "commands" / "multi-plan.md",
        REPO_ROOT / ".claude" / "commands" / "multi-review.md",
        REPO_ROOT / ".claude" / "commands" / "multi-adversarial-review.md",
        # Copilot
        REPO_ROOT / ".copilot" / "commands" / "multi-plan.md",
        REPO_ROOT / ".copilot" / "commands" / "multi-review.md",
        REPO_ROOT / ".copilot" / "commands" / "multi-adversarial-review.md",
        # Codex
        REPO_ROOT / ".agents" / "skills" / "multi-plan" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "multi-review" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "multi-adversarial-review" / "SKILL.md",
    ]

    for path in paths:
        assert path.exists(), f"Missing multi-orchestrator file: {path}"


def test_self_action_grid_exists() -> None:
    """All 16 self-action files (4 agents x 4 actions) should exist."""
    paths = [
        # Claude self-action
        REPO_ROOT / ".claude" / "commands" / "claude" / "plan.md",
        REPO_ROOT / ".claude" / "commands" / "claude" / "implement.md",
        REPO_ROOT / ".claude" / "commands" / "claude" / "review.md",
        REPO_ROOT / ".claude" / "commands" / "claude" / "adversarial-review.md",
        # Copilot self-action (skills under .github/skills/ — see docstring in
        # tests/test_delegation_matrix.py::_expected_path for why .github/ vs .claude/)
        REPO_ROOT / ".github" / "skills" / "copilot-plan" / "SKILL.md",
        REPO_ROOT / ".github" / "skills" / "copilot-implement" / "SKILL.md",
        REPO_ROOT / ".github" / "skills" / "copilot-review" / "SKILL.md",
        REPO_ROOT / ".github" / "skills" / "copilot-adversarial-review" / "SKILL.md",
        # Codex self-action (skills)
        REPO_ROOT / ".agents" / "skills" / "codex-plan" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "codex-implement" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "codex-review" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "codex-adversarial-review" / "SKILL.md",
    ]

    for path in paths:
        assert path.exists(), f"Missing self-action file: {path}"


def test_retired_self_action_aliases_are_removed() -> None:
    """The old ghissue-plan/implement/close self-action aliases should be gone."""
    removed = [
        REPO_ROOT / ".claude" / "commands" / "ghissue-plan.md",
        REPO_ROOT / ".claude" / "commands" / "ghissue-implement.md",
        REPO_ROOT / ".claude" / "commands" / "ghissue-close.md",
        REPO_ROOT / ".agents" / "skills" / "ghissue-plan" / "SKILL.md",
        REPO_ROOT / ".agents" / "skills" / "ghissue-implement" / "SKILL.md",
    ]

    for path in removed:
        assert not path.exists(), f"Retired self-action file should not exist: {path}"


def test_retired_dual_agent_files_are_removed() -> None:
    """The old hardcoded dual-agent commands should be gone, replaced by multi-* orchestrators."""
    removed = [
        REPO_ROOT / ".claude" / "commands" / "ghissue-plan-both.md",
        REPO_ROOT / ".claude" / "commands" / "ghissue-review-both.md",
    ]

    for path in removed:
        assert not path.exists(), f"Retired file should not exist: {path}"


def test_retired_workflow_step_aliases_are_removed() -> None:
    """The old ghissue-finalize/ghissue-status workflow steps should be renamed to ghi-*."""
    removed = [
        REPO_ROOT / ".claude" / "commands" / "ghissue-finalize.md",
        REPO_ROOT / ".claude" / "commands" / "ghissue-status.md",
        REPO_ROOT / ".agents" / "skills" / "ghissue-finalize" / "SKILL.md",
    ]

    for path in removed:
        assert not path.exists(), f"Retired workflow step file should not exist: {path}"


def test_codex_config_keeps_shared_dangerous_command_hook() -> None:
    """Codex config should keep the shared dangerous-command hook wired."""
    config = (REPO_ROOT / ".codex" / "config.toml").read_text(encoding="utf-8")

    assert "codex_hooks = true" in config
    assert "[[hooks.PreToolUse]]" in config
    assert "block-dangerous-commands.py" in config


def test_codex_config_uses_current_schema() -> None:
    """Codex config should avoid obsolete keys from older Codex releases."""
    config = (REPO_ROOT / ".codex" / "config.toml").read_text(encoding="utf-8")

    assert 'approval_policy = "untrusted"' in config
    assert "default_policy" not in config
    assert "[[approval_policy]]" not in config
    assert "[shell_env_policy]" not in config


def test_ai_setup_documents_codex_skills_workflow() -> None:
    """AI setup docs should describe the Codex skills-based workflow."""
    content = (REPO_ROOT / "docs" / "development" / "AI_SETUP.md").read_text(encoding="utf-8")

    assert ".agents/skills" in content
    assert "$codex-plan" in content
    assert "shared dangerous-command hook" in content


def test_slash_commands_doc_mentions_codex_skills_instead_of_custom_commands() -> None:
    """Workflow docs should describe Codex via skills rather than custom slash commands."""
    content = (REPO_ROOT / "docs" / "development" / "ai" / "slash-commands.md").read_text(
        encoding="utf-8"
    )

    assert "repo-scoped skills" in content
    assert "/skills" in content
    assert "$codex-implement" in content


def test_enforcement_principles_document_codex_hook_support() -> None:
    """Enforcement docs should reflect current Codex hook support."""
    content = (REPO_ROOT / "docs" / "development" / "ai" / "enforcement-principles.md").read_text(
        encoding="utf-8"
    )

    assert "Codex uses the shared hook" in content
    assert "no hook support" not in content


def test_antigravity_workflow_skills_exist() -> None:
    """Antigravity self-action skills should be present in the shared .agents/skills directory."""
    for action in ("plan", "implement", "review", "adversarial-review"):
        skill_path = REPO_ROOT / ".agents" / "skills" / f"antigravity-{action}" / "SKILL.md"
        assert skill_path.exists(), f"Missing Antigravity skill: {skill_path}"


def test_antigravity_hooks_json_wires_shared_hook() -> None:
    """.agents/hooks.json should wire the shared dangerous-command hook on PreToolUse."""
    hooks_path = REPO_ROOT / ".agents" / "hooks.json"
    assert hooks_path.exists(), f"Missing Antigravity hooks config: {hooks_path}"

    config = json.loads(hooks_path.read_text(encoding="utf-8"))
    commands = [
        handler.get("command", "")
        for group in config.values()
        for entry in group.get("PreToolUse", [])
        for handler in entry.get("hooks", [])
    ]
    assert any("block-dangerous-commands" in c for c in commands), (
        "Antigravity .agents/hooks.json must wire the shared dangerous-command hook on PreToolUse"
    )
    # The hook is agy's only gate (delegated invocations pass
    # --dangerously-skip-permissions), so its path must not depend on the CWD
    # agy happens to run handlers from. A bare "../tools/..." satisfied the
    # assertion above while resolving outside the repo from any other CWD.
    assert any("$(git rev-parse --show-toplevel)" in c for c in commands), (
        "Antigravity hook path must resolve independently of the handler CWD"
    )

    matchers = [
        entry.get("matcher", "")
        for group in config.values()
        for entry in group.get("PreToolUse", [])
    ]
    assert any("run_command" in m for m in matchers), (
        "Antigravity hook matcher must target the run_command tool"
    )


def test_copilot_hooks_json_pins_its_hook_path() -> None:
    """Copilot's wiring must keep an explicit cwd so its relative path resolves."""
    hooks_path = REPO_ROOT / ".github" / "hooks" / "copilot-hooks.json"
    assert hooks_path.exists(), f"Missing Copilot hooks config: {hooks_path}"

    config = json.loads(hooks_path.read_text(encoding="utf-8"))
    entries = config.get("hooks", {}).get("preToolUse", [])
    assert entries, "Copilot config must define a preToolUse hook"

    for entry in entries:
        assert "block-dangerous-commands" in entry.get("bash", ""), (
            "Copilot preToolUse hook must wire the shared dangerous-command hook"
        )
        # The path is relative, so the cwd pin is what makes it resolve.
        assert entry.get("cwd"), (
            "Copilot hook uses a relative path and must pin cwd, or it resolves "
            "against an unstated working directory"
        )


def test_stdout_contract_wirings_route_through_the_launcher() -> None:
    """Antigravity and Copilot must invoke the launcher, not the .py directly.

    Both block only on a stdout deny payload, so a hook that cannot start reads
    as "allow". The launcher denies in that case; calling the .py directly does
    not, because a script that never runs cannot emit its own deny.
    """
    agy = json.loads((REPO_ROOT / ".agents" / "hooks.json").read_text(encoding="utf-8"))
    agy_commands = [
        handler.get("command", "")
        for group in agy.values()
        for entry in group.get("PreToolUse", [])
        for handler in entry.get("hooks", [])
    ]
    copilot = json.loads(
        (REPO_ROOT / ".github" / "hooks" / "copilot-hooks.json").read_text(encoding="utf-8")
    )
    copilot_commands = [e.get("bash", "") for e in copilot.get("hooks", {}).get("preToolUse", [])]

    for label, commands in (("Antigravity", agy_commands), ("Copilot", copilot_commands)):
        assert any("block-dangerous-commands.sh" in c for c in commands), (
            f"{label} must route through the fail-closed launcher"
        )

    launcher = REPO_ROOT / "tools" / "hooks" / "ai" / "block-dangerous-commands.sh"
    assert launcher.exists(), f"Missing launcher: {launcher}"


def test_docs_document_antigravity_agent() -> None:
    """AI setup and command-blocking docs should register Antigravity as a supported agent."""
    ai_setup = (REPO_ROOT / "docs" / "development" / "AI_SETUP.md").read_text(encoding="utf-8")
    assert "Antigravity" in ai_setup
    assert ".agents/hooks.json" in ai_setup

    blocking = (REPO_ROOT / "docs" / "development" / "ai" / "command-blocking.md").read_text(
        encoding="utf-8"
    )
    assert ".agents/hooks.json" in blocking
    assert "write_to_file" in blocking


def test_multi_orchestrators_recognize_antigravity() -> None:
    """All 9 multi-* orchestrator files list antigravity and include an agy invocation block."""
    actions = ("plan", "review", "adversarial-review")
    multi_files = (
        [REPO_ROOT / ".claude" / "commands" / f"multi-{a}.md" for a in actions]
        + [REPO_ROOT / ".copilot" / "commands" / f"multi-{a}.md" for a in actions]
        + [REPO_ROOT / ".agents" / "skills" / f"multi-{a}" / "SKILL.md" for a in actions]
    )
    assert len(multi_files) == 9
    for f in multi_files:
        content = f.read_text(encoding="utf-8")
        assert "`antigravity`" in content, f"{f} does not list antigravity as an allowed agent"
        assert "agy -p" in content, f"{f} has no agy invocation block"


def test_migration_tool_copies_agents_dir() -> None:
    """The migration tool must copy the shared .agents/ dir (Codex + Antigravity config)."""
    src = (REPO_ROOT / "tools" / "pyproject_template" / "migrate_existing_project.py").read_text(
        encoding="utf-8"
    )
    assert '".agents"' in src, "migrate_existing_project.py must include .agents in the copy list"

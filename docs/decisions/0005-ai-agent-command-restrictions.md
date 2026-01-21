# ADR-0005: AI agent command restrictions via hooks

## Status

Accepted

## Date

2025-01-21

## Context

AI coding agents (Claude Code, Gemini CLI, etc.) can execute shell commands as part of their workflow. While documentation in `AGENTS.md` instructs agents to avoid dangerous commands, agents may violate these rules:

- After context compaction when rules fall out of context
- When trying to "help quickly" by bypassing checks
- When interpreting blocking errors as problems to solve

Dangerous commands include:

- `--admin` (bypasses branch protection)
- `--force` / `-f` (force push, potential data loss)
- `--no-verify` (skips pre-commit hooks)
- `git reset --hard` (loses uncommitted changes)
- `rm -rf /` or destructive operations

A real incident occurred where an AI agent attempted to bypass branch protection instead of waiting for CI checks.

## Decision

Implement tool-level enforcement that blocks dangerous commands before execution:

1. **Claude Code**: PreToolUse hooks in `.claude/settings.json` that exit with code 2 to block
2. **Gemini CLI**: BeforeTool hooks with similar blocking mechanism
3. **Codex CLI**: `action = "deny"` approval policy rules

The hooks inspect command arguments and block patterns like:

- `--admin`, `--force`, `-f`
- `--no-verify`, `--no-gpg-sign`
- `git reset --hard`, `git push --force`
- `rm -rf /`, `rm -rf ~`
- `doit release` (requires explicit user action)
- `uv add` (dependencies require approval)

Additionally, `AGENTS.md` includes a "When Blocked Protocol" instructing agents to investigate and report blocks rather than attempt bypasses.

## Consequences

### Positive

- Prevents accidental or intentional bypass of safety controls
- Defense in depth: documentation + enforcement
- Applies regardless of agent context state
- Clear error messages guide correct behavior
- Protects against destructive operations

### Negative

- Legitimate uses of blocked commands require manual execution
- Maintenance burden to keep hooks updated
- May need adjustment for new dangerous patterns

### Neutral

- Hooks are per-agent tool (Claude, Gemini, Codex have different configs)
- Blocking is fail-safe (block on detection, allow by default)

## Participants

- Project maintainers

## Related

- Issue #113: Enforce dangerous command restrictions via hooks and configs
- Issue #117: Block gh issue create and gh pr create commands for AI agents
- Issue #163: Add pre-commit hook to block pyproject.toml version changes
- Issue #164: Block doit release in AI agent hooks
- Issue #166: Block uv add in AI agent hooks
- [AI Command Blocking documentation](../development/ai/command-blocking.md)

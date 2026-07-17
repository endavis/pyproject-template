# Copilot CLI Configuration

This directory is the GitHub Copilot CLI configuration directory for this repository, parallel to `.claude/`, `.gemini/`, and `.codex/`.

**Important:** Copilot CLI does **not** read any `commands/` directory. Per the installed `@github/copilot` SDK (`sdk/index.d.ts`), Copilot only discovers project skills from `skills/` paths: `.github/skills/`, `.agents/skills/`, and `.claude/skills/` (plus the corresponding personal paths under `~/`). Repo-local `.copilot/commands/<name>.md` files are never loaded.

## Workflow Skills

All Copilot-host workflow skills (self-action and cross-agent bridges, 20 total) live under `.github/skills/<target>-<action>/SKILL.md`. Because skill names are directory names and cannot contain colons, the slash surface uses hyphen naming:

- **Self-action:** `/copilot-plan`, `/copilot-implement`, `/copilot-review`, `/copilot-adversarial-review`
- **To Claude:** `/claude-plan`, `/claude-implement`, `/claude-review`, `/claude-adversarial-review`
- **To Codex:** `/codex-plan`, `/codex-implement`, `/codex-review`, `/codex-adversarial-review`
- **To Gemini:** `/gemini-plan`, `/gemini-implement`, `/gemini-review`, `/gemini-adversarial-review`
- **To Antigravity:** `/antigravity-plan`, `/antigravity-implement`, `/antigravity-review`, `/antigravity-adversarial-review`

The `multi-*` orchestrators (`/multi-plan`, `/multi-review`, `/multi-adversarial-review`) and `/ghi-finalize` / `/ghi-status` come from `.agents/skills/` (interoperable Codex skill path) and are auto-discovered by Copilot.

## Known limitation: delegate-* skill bleed

Copilot reads `.agents/skills/`, which contains the 20 `delegate-<target>-<action>` skills (shared by Codex and Antigravity). Those surface as `/delegate-...` slash commands alongside the canonical Copilot ones — they shell out to Codex/Antigravity syntax and are wasted noise in a Copilot session. Copilot supports a `disabledSkills` array, but **only in user config** (`~/.copilot/config.json`) — there is no repo-level setting for it. See [`docs/development/ai/slash-commands.md`](../docs/development/ai/slash-commands.md#copilot) for the user-side config snippet.

## Dangerous Command Hook

The dangerous command hook is wired in `.github/hooks/copilot-hooks.json`. It blocks shell commands identified as dangerous before they execute:

```
.github/hooks/copilot-hooks.json → tools/hooks/ai/block-dangerous-commands.py
```

No changes to this hook are needed when adding new slash commands.

## Subagent / Implement Worker

The `implement-worker` subagent used by `/copilot-implement` (and shared with Claude's `/claude:implement`) is defined in `.claude/agents/implement-worker.md`. Copilot CLI's `task` tool reads this file when spawning the subagent.

## Temporary Files

Agents must write temporary files to `tmp/agents/copilot/` (not `/tmp/`). Include a context identifier (issue number, PR number, or task ID) in the filename to avoid collisions.

## Per-Stack Instructions

GitHub Copilot natively discovers instruction files placed in `.github/instructions/` and named
`NAME.instructions.md`. Each file begins with YAML frontmatter (`applyTo: '<glob>'`) that gates
it to a specific path scope, followed by a skill-gated, numbered self-check body (≤30 lines) and
an `Observed failures:` footer.

This is the Copilot equivalent of `.claude/rules/` (loaded via `@import` in `.claude/CLAUDE.md`)
and `.gemini/rules/` (loaded via `@` directive in `GEMINI.md`). The discipline — build from
observed failures, not generic advice — is shared across all three CLIs.

See [`.github/instructions/README.md`](../.github/instructions/README.md) for the full pattern,
file structure, and a worked example.

## See Also

- `.github/skills/<target>-<action>/SKILL.md` — Copilot-host workflow skills (16 files). `.github/skills/` is used (instead of `.claude/skills/`) because it's the only Copilot project skill path that Claude does not also read — avoids surfacing duplicate slash commands in Claude.
- `.agents/skills/` — interoperable Codex skill path, also read by Copilot
- `.claude/agents/implement-worker.md` — implement-worker subagent definition
- `.github/hooks/copilot-hooks.json` — dangerous command hook wiring
- `.github/instructions/README.md` — per-stack instruction file pattern for Copilot
- `docs/development/ai/slash-commands.md` — full workflow and command reference
- `docs/development/ai/cross-agent-delegation.md` — cross-agent matrix and per-host invocation
- `docs/development/ai/command-blocking.md` — hook documentation

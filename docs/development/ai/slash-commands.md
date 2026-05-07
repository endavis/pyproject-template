---
title: Slash Commands and Workflows
description: Reference for the slash commands and dual-agent workflow this template ships with
audience:
  - contributors
  - ai-agents
tags:
  - ai
  - workflow
  - slash-commands
---

# Slash Commands and Workflows

## Purpose

This page documents the slash commands this template ships under `.claude/commands/` and `.gemini/commands/`, and the single-agent and dual-agent workflows built on top of them. It is written for contributors who want to understand or extend the workflow, and for AI agents that need to know which command to run at each stage of the issue lifecycle.

## Workflows

### Single-agent workflow

The default Claude flow takes an issue from unplanned to closed. Each step produces an artifact the next step expects.

1. **`/ghissue-plan <n>`** — Claude enters plan mode in the main conversation, reads project rules, explores the codebase, drafts a plan, and iterates with the user until approved. On approval the plan is posted as a comment on issue `#n` with the header `## Implementation Plan for #<n>: <title>`. The next step expects this comment to exist.
2. **User review of the plan** — read the comment, discuss revisions in chat, re-run `/ghissue-plan` if needed.
3. **`/ghissue-implement <n>`** — Claude verifies the plan comment exists, creates a branch (`<type>/<n>-<short-description>`) off fresh `main`, then spawns a subagent (Task tool) that reads `AGENTS.md`, fetches the plan, implements files and tests, and runs `doit check`. The main context receives only the summary. The artifact is an uncommitted working tree on the feature branch.
4. **User review of the changes** — inspect the diff and discuss fixes directly in chat; no command is needed for fix-ups.
5. **`/ghissue-finalize`** — Claude detects the branch and issue, spawns a finalization subagent that updates docs/ADRs as needed, runs `doit check`, and drafts a commit message and PR body. The main context presents the drafts and waits for explicit user approval before staging, committing, and creating the PR via `doit pr`. The artifact is an open PR referencing `Addresses #<n>`.
6. **User-driven merge** — the user reviews the PR, adds the `ready-to-merge` label, and merges via `doit pr_merge` (or the web UI). This step is never automated.
7. **`/ghissue-close <n>`** — Claude verifies a merged PR addresses `#n`, updates task checkboxes in the issue body, posts `Addressed in PR #<pr>`, closes the issue, and scans the PR for related issues to optionally close as well.

### Multi-agent workflow

The multi-agent flow replaces the planning and (optionally) review steps with orchestrated calls that spawn any combination of agents in **isolated contexts**. The design intent is that no agent can bias another: each generates its output without seeing the others' work, and the orchestrating agent in the main conversation posts all raw outputs plus a synthesis.

Each agent's output is posted as a separate comment. The orchestrator is the only agent that writes to GitHub — all other agents run in non-interactive mode and emit to stdout only.

1. **`/multi-plan <ais...> <n>`** — replaces `/ghissue-plan-both`. Takes a list of agent names (e.g. `claude gemini`) and an issue number. Each listed agent independently generates a plan in an isolated context; all plans are posted as separate issue comments. The orchestrating agent synthesizes a combined plan, reviews it with the user, and posts the approved synthesized plan.
2. **`/ghissue-implement <n>`** — same as the single-agent flow. The synthesized plan comment is the input.
3. **`/multi-review <ais...>`** — replaces `/ghissue-review-both`. Takes a list of agent names. Each listed agent independently reviews the current branch's PR; all reviews are posted as separate PR comments. The orchestrating agent synthesizes findings into a combined verdict. A user-approval gate precedes the synthesis post.
4. **`/multi-adversarial-review <ais...>`** — replaces `/ghissue-gemini-review` and extends it. Takes a list of agent names. Each listed agent independently challenges the current changes; all adversarial reviews are synthesized. If a PR exists the synthesis is posted; otherwise it appears in-conversation only. A user-approval gate precedes posting.
5. **`/ghissue-finalize`**, merge, and **`/ghissue-close <n>`** — same as the single-agent flow.

### Diagnostic command

**`/ghissue-status`** can be invoked at any point. It inspects the current branch, issue state, plan comment, uncommitted changes, unpushed commits, and open PRs, then reports a status summary and the suggested next command. It has no side effects.

## Command reference

Entries are alphabetical. Each one names the command, its arguments, what it does, its position in the workflow, and any design note worth knowing.

### `/ghissue-close <n>`

**Args:** issue number. **Source:** `.claude/commands/ghissue-close.md`.

Verifies a merged PR references `#n`, updates task checkboxes in the issue body, posts the closing comment `Addressed in PR #<pr-number>`, closes the issue via `gh issue close`, then scans the PR body and comments for related issue references (`Addresses`, `Part of`, `Related to`, `Closes`, `Fixes`, `References`, bare `#N`) and asks the user individually whether to close each open related issue. **Workflow position:** last step of both single-agent and dual-agent flows. **Design note:** never closes an issue without a merged PR unless the user explicitly confirms; never closes related issues without per-issue confirmation.

### `/ghissue-finalize`

**Args:** none. **Source:** `.claude/commands/ghissue-finalize.md`.

Operates on the current feature branch, assuming implementation and review are complete. In the main context it detects the branch, extracts the issue number from the branch name, fetches issue details, and checks for uncommitted changes. It then spawns a general-purpose subagent that reads `AGENTS.md`, `.github/CONTRIBUTING.md`, and `.github/pull_request_template.md`, reviews changed files for doc/ADR updates, runs `doit check`, and drafts a commit message plus a PR body written to a temp file. The main context then presents the drafts to the user, waits for explicit approval, stages files, commits, and creates the PR via `doit pr --title=... --body-file=...`. **Workflow position:** after implementation and review. **Design note:** will not commit or create the PR without explicit user confirmation; stops if run on `main`.

### `/ghissue-implement <n>`

**Args:** issue number. **Source:** `.claude/commands/ghissue-implement.md`.

Validates that the issue is open and that a plan comment exists (otherwise instructs the user to run `/ghissue-plan <n>` first). Checks the current branch: if already on `<type>/<n>-*` it resumes work on that branch, otherwise it checks out `main`, pulls, and creates a new branch whose type is derived from the issue's labels (`enhancement`→`feat`, `bug`→`fix`, `refactor`→`refactor`, `documentation`→`docs`, `chore`→`chore`, else `issue`). It then spawns the custom `implement-worker` subagent (defined in `.claude/agents/implement-worker.md`) that reads `AGENTS.md` and `.claude/CLAUDE.md`, fetches the plan via `gh api`, implements files and tests, and runs `doit check`, fixing failures rather than giving up. The main context receives only the summary. **Workflow position:** after plan exists, before `/ghissue-finalize`. **Design note:** the subagent pattern keeps the main conversation context clean. The command now spawns `implement-worker` rather than the built-in `general-purpose` subagent. The custom subagent has `permissionMode: default` in its YAML frontmatter — per Claude Code's documented sub-agent precedence rules, this should escape parent plan mode because plan mode is not in the parent-overrides-child list. The status-line preamble warning (telling the user to check for "plan mode" before running) is retained as belt-and-suspenders while the override is empirically validated; it can be removed in a follow-up once confirmed on the shipping Claude Code version.


### `/multi-adversarial-review <ais...>`

**Args:** one or more agent names (`claude`, `gemini`, `copilot`, `codex`). **Sources:** `.claude/commands/multi-adversarial-review.md`, `.gemini/commands/multi-adversarial-review.toml`, `.copilot/commands/multi-adversarial-review.md`, `.agents/skills/multi-adversarial-review/SKILL.md`.

Runs each listed agent in an isolated context to independently challenge the current uncommitted changes and the current branch vs `main`. Each agent outputs an adversarial review (Direction Critique / Hidden Assumptions / Failure Modes / Alternatives Worth Considering); all reviews are synthesized into a combined challenge with consensus and per-agent-only findings. A user-approval gate precedes posting. If a PR exists the synthesis is posted as a PR comment; otherwise it is presented in-conversation only. **Workflow position:** optional adversarial challenge before `/ghissue-finalize`. **Design note:** no agent sees any other agent's output while drafting; every non-self agent runs in non-interactive mode and writes only to stdout.

### `/multi-plan <ais...> <issue#>`

**Args:** one or more agent names (`claude`, `gemini`, `copilot`, `codex`) followed by the issue number. **Sources:** `.claude/commands/multi-plan.md`, `.gemini/commands/multi-plan.toml`, `.copilot/commands/multi-plan.md`, `.agents/skills/multi-plan/SKILL.md`.

Multi-agent replacement for the old `/ghissue-plan-both` command. Validates the issue, warns if plan comments already exist, then generates independent plans from each listed agent in isolated contexts. Posts each plan as a separate issue comment, synthesizes a combined plan that highlights agreements and divergences, reviews the synthesis with the user, and only posts the synthesized plan after explicit approval. **Workflow position:** first step of the multi-agent workflow. **Design note:** isolated contexts are mandatory so no agent can see another's output while drafting; the orchestrating agent is the only one that writes to GitHub.

### `/multi-review <ais...>`

**Args:** one or more agent names (`claude`, `gemini`, `copilot`, `codex`). **Sources:** `.claude/commands/multi-review.md`, `.gemini/commands/multi-review.toml`, `.copilot/commands/multi-review.md`, `.agents/skills/multi-review/SKILL.md`.

Multi-agent replacement for the old `/ghissue-review-both` command. Verifies a PR exists for the current branch, warns if reviews already exist, then generates independent code reviews from each listed agent in isolated contexts. Posts each review as a separate PR comment, synthesizes findings into a combined verdict (consensus findings, per-agent-only findings, combined verdict). A user-approval gate precedes the synthesis post. **Workflow position:** after `/ghissue-implement`, before `/ghissue-finalize`, in the multi-agent workflow. **Design note:** same isolation guarantee as `/multi-plan` — no reviewer sees another's output; the synthesis is posted after all raw reviews so readers can audit it against the sources.

### `/ghissue-plan <n>`

**Args:** issue number. **Source:** `.claude/commands/ghissue-plan.md`.

Runs in the main conversation context (not a subagent) so the user can ask questions and refine the plan interactively. Enters plan mode, validates the issue, warns if a plan comment already exists, reads `AGENTS.md` and `.claude/CLAUDE.md`, fetches issue details, explores the codebase, and drafts a plan with the standard sections (Overview, Files to Create/Modify, Test Plan, Documentation, Validation). It iterates inside plan mode with `AskUserQuestion` until the user approves, then exits plan mode and posts the approved plan as an issue comment. **Workflow position:** first step of the single-agent workflow. **Design note:** plan mode is preserved throughout iteration; exiting plan mode means "post the approved plan", nothing more.

### `/ghissue-status`

**Args:** none. **Source:** `.claude/commands/ghissue-status.md`.

Inspects the current git state (branch, uncommitted changes, recent log), extracts the issue number from the branch name if on a feature branch, checks for a plan comment, unpushed commits, and open PRs, then reports a status summary and suggests the next command to run. **Workflow position:** any time. **Design note:** read-only and side-effect-free — safe to run whenever the user is unsure where they are in the lifecycle.

### `/checkpoint <slug>` and `/restore <slug>`

**Args:** optional kebab-case slug. **Sources:** `.claude/commands/checkpoint.md`, `.claude/commands/restore.md` (Claude); `.gemini/commands/checkpoint.md`, `.gemini/commands/restore.md` (Gemini); `.agents/skills/checkpoint/SKILL.md`, `.agents/skills/restore/SKILL.md` (Codex).

Pause-and-resume helpers for long-running workstreams. `/checkpoint` writes a paste-ready resumption prompt to `tmp/checkpoints/{inv_epoch}-{slug}.md`; `/restore` reads the matching file and treats its contents as the session's initial instructions. The `inv_epoch` prefix is a 10-digit decreasing integer so default `ls` lists newest first; users see only the slug. If `/restore` is invoked without a slug, it picks the most recent checkpoint. **Naming:** `checkpoint`/`restore` was chosen over `snapshot`/`resume` to avoid collisions with built-in slash commands across all four supported agents (Claude Code, Gemini CLI, Codex CLI, Copilot CLI all reserve `/resume`; Gemini also reserves `/snapshot`).

**Cross-agent portability:** `tmp/checkpoints/` is intentionally shared (not per-agent), so a checkpoint taken in Claude can be restored in Gemini or Codex and vice versa. This is the documented exception to the `tmp/agents/<agent-type>/` rule in `AGENTS.md`. **Workflow position:** any time, independent of the issue lifecycle. **Design note:** checkpoints are immutable once written; the user is expected to verify referenced issues/PRs are still current before acting on stale references. **When to use it:** at the end of a session when work is unfinished and you want a clean handoff into the next session — capture the goal, current branch state, recommended next step, and any user direction or constraints that should bind the future session.

**Auto-checkpoint (PreCompact / SessionStart hooks):** Claude Code also ships two lifecycle hooks that automate the pause/resume pattern for the most common context-loss event — autocompact firing mid-task. The `PreCompact` hook synthesizes a checkpoint to `tmp/checkpoints/{inv_epoch}-auto-precompact.md` before compaction; the `SessionStart` hook (matcher `compact|resume`) injects the newest auto-precompact file into the new session's context automatically. Auto-precompact files share the same filename convention and directory as manual `/checkpoint` files, so `/restore auto-precompact` also works. Set `CLAUDE_NO_AUTO_RESTORE=1` to opt out of the automatic restore; set `CLAUDE_RESTORE_ANY=1` to widen the restore glob to any `*.md` checkpoint. See [Auto-Checkpoint and Session-Restore Hooks](auto-checkpoint-hook.md) for full details.

## Gemini

Gemini-first users can complete the full issue lifecycle using Gemini-native commands. This workflow shares the same artifacts (plan comments, branch names, PR bodies) as the Claude flow, enabling seamless handoff between agents.

### Standalone workflow

1. **`/ghissue-plan <n>` (Gemini)** — Gemini reads the issue and project rules, explores the codebase, and drafts a plan inline in the conversation. After the user approves the plan, Gemini posts it as a comment on the issue with the header `## Implementation Plan for #<n>: <title>`.
2. **User review of the plan** — same as Claude flow.
3. **`/ghissue-implement <n>` (Gemini)** — Gemini validates the plan comment, creates the feature branch, and implements the changes inline in the conversation. It runs `doit check` to verify the implementation.
4. **User review of the changes** — same as Claude flow.
5. **`/ghissue-finalize` (Gemini)** — Gemini detects the branch and issue, checks for doc/ADR updates, runs `doit check`, and drafts the commit message and PR body. After user approval, it stages, commits, and creates the PR via `doit pr`.

### Command reference

#### `/ghissue-finalize` (Gemini)

**Args:** none. **Source:** `.gemini/commands/ghissue-finalize.md`.

Gemini-native implementation of the finalize command. Detects the branch and issue, checks for uncommitted changes, reviews changed files for documentation/ADR updates, runs `doit check`, and drafts a commit message and PR body (written to `tmp/agents/gemini/pr-body-issue-<n>.md`). After user approval, it stages files, commits, and creates the PR via `doit pr`. **Workflow position:** after implementation and review. **Design note:** unlike the Claude version, all operations happen inline in the main conversation context.

#### `/ghissue-implement <n>` (Gemini)

**Args:** issue number. **Source:** `.gemini/commands/ghissue-implement.md`.

Gemini-native implementation of the implement command. Validates the issue and plan comment, creates the feature branch, and implements the changes inline in the conversation. Runs `doit check` to verify the implementation. **Workflow position:** after plan exists, before `/ghissue-finalize`. **Design note:** performs all implementation steps directly in the main conversation context rather than spawning a subagent.

#### `/ghissue-plan <n>` (Gemini)

**Args:** issue number. **Source:** `.gemini/commands/ghissue-plan.md`.

Gemini-native standalone planning command. Validates the issue, reads `AGENTS.md`, explores the codebase, and drafts a plan inline in the conversation. Iterates with the user until the plan is approved, then posts it to the issue as a comment via `gh issue comment`. Mirrors the behavior of Claude's `/ghissue-plan`. **Workflow position:** start of standalone Gemini workflow, before `/ghissue-implement`. **Design note:** Gemini has no plan-mode equivalent, so iteration happens in the regular conversation context.

## Codex

Codex does not use repo-defined slash commands in this template. Instead, the Codex workflow is provided through **repo-scoped skills** under `.agents/skills/`, which Codex can invoke through its built-in `/skills` browser or explicit mentions such as `$ghissue-plan`, `$ghissue-implement`, and `$ghissue-finalize`.

**Workflow coverage:** the checked-in Codex skills cover planning, implementation, and finalization through PR creation. They preserve the same repo artifact contract used by the Claude flow:

- `$ghissue-plan` posts the approved plan comment with the header `## Implementation Plan for #<n>: <title>`
- `$ghissue-implement` creates or resumes the issue branch and finishes with `doit check`
- `$ghissue-finalize` drafts the commit and PR artifacts and uses `doit pr` after explicit approval

**Config and safety:** `.codex/config.toml` still configures approvals and hook wiring for Codex. The shared dangerous-command hook at `tools/hooks/ai/block-dangerous-commands.py` applies to Codex, and the approval-policy deny rules remain a secondary defense layer.

**Out of scope for Codex in this template:** no repo-defined custom slash commands, no dual-agent orchestration, and no Codex-specific close-issue automation.

## Copilot

GitHub Copilot CLI automatically discovers project skills from `.claude/commands/`. All workflow commands (`/ghissue-plan`, `/ghissue-implement`, `/ghissue-finalize`, `/ghissue-close`, `/ghissue-status`, etc.) are available in Copilot sessions without any additional files.

**Config directory:** `.copilot/` — established as the Copilot CLI config directory for this repo, parallel to `.claude/`, `.gemini/`, and `.codex/`.

**Dangerous command hook:** Already wired in `.github/hooks/copilot-hooks.json`. It invokes `tools/hooks/ai/block-dangerous-commands.py` as a `preToolUse` hook, blocking dangerous shell commands before they execute. See [AI Command Blocking](command-blocking.md) for details.

**Implement-worker subagent:** Shared with Claude — defined in `.claude/agents/implement-worker.md`. Copilot CLI's `task` tool reads this file when `/ghissue-implement` spawns the subagent.

**No parallel command files needed:** Because Copilot CLI discovers skills from `.claude/commands/` directly, you do not need to maintain a separate `.copilot/commands/` directory unless you want to override Claude-specific behavior for Copilot sessions.

## Adding a new slash command

1. **Pick the location.** Claude commands live in `.claude/commands/<name>.md` and become `/<name>` in Claude Code. Gemini commands live in `.gemini/commands/<name>.md` and become `/<name>` in Gemini CLI. Copilot CLI auto-discovers skills from `.claude/commands/` — no separate `.copilot/commands/<name>.md` is needed unless you want to override Claude-specific behaviour for Copilot sessions.
2. **Use the CLI file format** — not the `docs/` frontmatter format. Start with a top-level `# Title` heading, follow with a one-line description (which may include the `$ARGUMENTS` placeholder if the command takes arguments), then a `## Instructions` section containing the step-by-step body. **Do not add YAML frontmatter.** The CLIs expect plain markdown; frontmatter would appear verbatim in the rendered prompt.
3. **Use `$ARGUMENTS` for inputs.** When the user invokes `/<command> foo bar`, every `$ARGUMENTS` occurrence in the file is substituted with `foo bar` before the command body is sent to the model. For commands that take no arguments (like `/ghissue-finalize` or `/ghissue-status`), omit the placeholder.
4. **Decide: subagent or main context?** Delegate to a general-purpose subagent via the Task tool when the command does heavy codebase exploration, writes files, or runs long commands whose output would bloat the main conversation — `.claude/commands/ghissue-implement.md` is the canonical example. Run in the main context when the user needs to interact step by step (plan mode, iteration, explicit approvals) — `.claude/commands/ghissue-plan.md` is the canonical example.
5. **Update this document** when you add or remove a command. The command reference section should list every file under `.claude/commands/` and `.gemini/commands/`.

## Cross-agent delegation matrix

In addition to the self-action `ghissue-*` commands above, this template ships a `<target>:<action>` matrix that lets any source agent delegate `plan`, `implement`, `review`, or `adversarial-review` to any of the other three. The full design — convention, file layout, prefix mapping (`/foo` vs `$foo` for Codex), Hybrid C runtime behavior, and the `.agents/skills/` ↔ Gemini conflict mitigation — is documented separately:

→ See [Cross-Agent Delegation Matrix](cross-agent-delegation.md).

Quick reference:

```text
# In Claude Code / Gemini CLI / Copilot CLI:
/<target>:<action> [args]      # e.g. /codex:plan 42, /gemini:adversarial-review

# In Codex CLI (skills, not slash commands):
$delegate-<target>-<action> [args]  # e.g. $delegate-claude-implement 42
```

## See also

- [Cross-Agent Delegation Matrix](cross-agent-delegation.md) — convention, matrix, and per-host invocation for the `<target>:<action>` family.
- [First 5 Minutes with an AI Agent](first-5-minutes.md) — narrative onboarding walkthrough showing the workflow end to end.
- [AI Agent Setup Guide](../AI_SETUP.md) — per-CLI configuration and whitelists.
- [Architectural Conventions](architectural-conventions.md) — imperative rules for AI-generated code.
- [AI Enforcement Principles](enforcement-principles.md) — how this template enforces rules in code, not just instructions.
- [AI Command Blocking](command-blocking.md) — tool-level hooks that block dangerous commands.
- [AGENTS.md](../../../AGENTS.md) — universal context file and workflow reference.

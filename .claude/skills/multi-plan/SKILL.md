---
name: multi-plan
description: Run multiple AI agents in parallel to create independent implementation plans for a GitHub issue, then synthesize them into a single plan. Works the same from any host CLI (Claude Code, Codex CLI, Copilot CLI, Antigravity CLI).
---

# Multi-Agent Plan

Run multiple AI agents in parallel to create independent implementation plans for a GitHub issue, then synthesize them.

## When to use

Use this skill when the user wants multiple agents to independently plan an issue.

Expected prompt shape:

- `multi-plan claude codex 42`
- "run a multi-agent plan for issue 42 with claude and codex"

If the agent list or issue number is missing, ask for it before continuing.

## Agent invocations

Identify which of the four CLIs is running this skill — **that entry is you.** Run your own part
directly, in this session (Step 3 below). Call every *other* listed agent through its CLI, exactly
as this table gives it — copied from [cross-agent-delegation.md — Non-interactive flags per
CLI](../../../docs/development/ai/cross-agent-delegation.md#non-interactive-flags-per-cli), which
stays the source of truth:

| Agent | Invocation |
| :--- | :--- |
| `claude` | `claude -p '<prompt>'` |
| `codex` | ``codex -a never --dangerously-bypass-hook-trust exec 'Run every `gh` command as its own standalone shell command, never chained with other commands via `;`, `&&`, or a pipe — only a standalone `gh` matches the Codex allow rule in `.codex/rules/gh.rules`; chained, it runs inside the sandbox with no network access. <prompt>' < /dev/null`` |
| `copilot` | `copilot --allow-all -p '<prompt>'` |
| `antigravity` | `agy -p '<prompt>' --dangerously-skip-permissions --add-dir "$(git rev-parse --show-toplevel)"` |

## Instructions

### Step 0: Parse arguments

Extract the agent list and issue number from the user's request.
Allowed agent names: `claude`, `copilot`, `codex`, `antigravity`.

- If the issue number is missing, tell the user the required syntax and stop.
- If any agent name is not in the allowed list, report the unknown name, list allowed names, and stop.

### Step 1: Validate the issue

```bash
gh issue view <issue> --json number,title,state,labels
```

- If the issue does not exist, stop and tell the user.
- If the issue is closed, ask whether to reopen it or stop.

### Step 2: Check for existing plans

```bash
gh api repos/{owner}/{repo}/issues/<issue>/comments --jq '.[].body' | grep -E "^#+ Implementation Plan for"
```

- If plan comments already exist, warn the user and ask for confirmation.

### Step 3: Generate plans in parallel

Every agent's plan comes from the same source — the **Planner brief** in
[`implement-issue`](../implement-issue/SKILL.md#planner-brief) — so the plans are directly
comparable. The brief's format has no `### Risks and Considerations` section; that belonged to the
old per-agent plan format this replaces. Each plan MUST be produced in an isolated context.

#### You (the agent running this skill)

Run the Planner brief for issue #<issue> the same way `implement-issue`'s own Step 3 does — in a
subagent if your host provides one (see `implement-issue`'s [Per-host subagent
notes](../implement-issue/SKILL.md#per-host-subagent-notes)), otherwise inline in this session.
Append `---` followed by `*Plan by: <your agent name>* | *Date: <today>*` to what the brief returns,
and capture that as your plan.

#### Every other listed agent

Invoke it with its row from [Agent invocations](#agent-invocations) above, substituting this prompt
(filling in `<issue>` and `<agent name>`):

> Read the Planner brief in `.agents/skills/implement-issue/SKILL.md` (the `## Planner brief`
> section) and follow it for issue #<issue> in the current repository. Append `---` followed by
> `*Plan by: <agent name>* | *Date: <today>*`. Output ONLY the resulting plan markdown.

For example, to delegate to Claude:

```bash
claude -p 'Read the Planner brief in .agents/skills/implement-issue/SKILL.md (the "## Planner brief" section) and follow it for issue #<issue> in the current repository. Append --- followed by *Plan by: Claude* | *Date: <today>*. Output ONLY the resulting plan markdown.'
```

Capture stdout as that agent's plan.

If any agent fails or produces empty output, report the error and ask whether to continue or retry.

### Step 4: Post each plan to the issue

```bash
gh issue comment <issue> --body "<agent plan>"
```

Post one comment per agent.

### Step 5: Synthesize the final plan

Create a synthesized plan combining the best elements from all plans. Note agreements (high
confidence) and divergences (needs discussion). Use the same format as the Planner brief.

Signature:
```
---
*Synthesized Plan by: <host agent> (from <agent1> + <agent2> + ... input)* | *Date: <today>*
```

### Step 6: Iterate with user

Present the synthesized plan and ask for feedback. Do NOT post until the user approves.

### Step 7: Post the approved synthesized plan

```bash
gh issue comment <issue> --body "<synthesized plan>"
```

Tell the user the plans have been posted and the next step is "implement issue <issue>" (optionally
"... with \<agent\>" to hand off only the coding step).

## See also

- [`implement-issue`](../implement-issue/SKILL.md) — the Planner brief this skill reuses, and the
  single-agent flow that follows once a plan is posted.
- [Cross-Agent Delegation Matrix](../../../docs/development/ai/cross-agent-delegation.md) — the
  non-interactive invocation table this skill's [Agent invocations](#agent-invocations) section
  copies.

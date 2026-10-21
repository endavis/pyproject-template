---
name: multi-review
description: Run multiple AI agents in parallel to independently review the current PR, then synthesize findings. Works the same from any host CLI (Claude Code, Codex CLI, Copilot CLI, Antigravity CLI).
---

# Multi-Agent Review

Run multiple AI agents in parallel to independently review the current branch's pull request, then synthesize findings.

## When to use

Use this skill when the user wants multiple agents to independently review an open PR.

Expected prompt shape:

- `multi-review claude codex`
- "run multi-agent review with claude and codex"

If the agent list is missing, ask for it before continuing.

**Read-only.** Review and report — do not edit files, commit, or push. Findings go to the user and the PR; any fix is a separate change the user asks for.

## Agent invocations

Step 0 below already removed your own CLI from the agent list. Run your own review directly, in this
session (Step 3 below). Call every agent that list left through its CLI, exactly as this table gives
it — copied from [cross-agent-delegation.md — Non-interactive flags per
CLI](../../../docs/development/ai/cross-agent-delegation.md#non-interactive-flags-per-cli), which
stays the source of truth:

| Agent | Invocation |
| :--- | :--- |
| `claude` | `claude -p '<prompt>'` |
| `codex` | ``codex -a never --dangerously-bypass-hook-trust exec 'Run every `gh` command as its own standalone shell command, never chained with other commands via `;`, `&&`, or a pipe — only a standalone `gh` matches the Codex allow rule in `.codex/rules/gh.rules`; chained, it runs inside the sandbox with no network access. If any `gh` command fails, print `DELEGATION-ERROR:` and the error, then stop. <prompt>' < /dev/null`` |
| `copilot` | `copilot --allow-all -p '<prompt>'` |
| `antigravity` | `agy -p '<prompt>' --dangerously-skip-permissions --add-dir "$(git rev-parse --show-toplevel)"` |

A headless Codex host (`codex exec -a never`) can read GitHub through `.codex/rules/gh.rules` but cannot write to it or delegate to another agent CLI — see [Headless Codex host limits](../../../docs/development/ai/cross-agent-delegation.md#headless-codex-host-limits). It cannot run Step 3's delegation to the other listed agents or Step 4's `gh pr comment` headless; Codex hosts this skill interactively instead.

## Instructions

### Step 0: Parse arguments

Extract the agent list from the user's request.
Allowed agent names: `claude`, `copilot`, `codex`, `antigravity`.

- If no agents are given, ask for the agent list.
- If any agent name is not in the allowed list, report the unknown name, list allowed names, and stop.

Then remove your own name — the CLI running this skill — from the agent list. Every later step uses only the agents that remain: you never call your own CLI. If no agent remains, tell the user and stop.

### Step 1: Verify the PR exists

```bash
gh pr view --json number,title,body,headRefName
```

- If no PR exists for the current branch, stop and tell the user.
- Save the PR number for later use.

### Step 2: Check for existing reviews

```bash
gh pr view --json comments --jq '.comments[].body' | grep -E "\*Review by:"
```

- If review comments already exist, warn the user and ask for confirmation.

### Step 3: Generate reviews in parallel

Each review MUST be in an isolated context.

#### You (the agent running this skill)

Run your review inline:
1. Run `gh pr view --json number,title,body,headRefName`
2. Run `gh pr diff`
3. Read AGENTS.md and .github/CONTRIBUTING.md
4. Review for correctness, style, testing, security, documentation, architecture, breaking changes
5. Draft the review in the standard format:
   ```
   ## PR Review: #<number> — <title>
   ### Summary
   ### Findings
   #### Critical
   #### Suggestions
   #### Positive
   ### Verdict
   ---
   *Review by: <your agent name>* | *Date: <today>*
   ```

#### Every agent remaining after Step 0 removed yours

Invoke it with its row from [Agent invocations](#agent-invocations) above, substituting this prompt
(filling in `<agent name>`):

> Read AGENTS.md and .github/CONTRIBUTING.md. Get the PR via `gh pr view --json
> number,title,body,headRefName`. Get the diff via `gh pr diff`. Review for: correctness, style,
> testing, security, documentation, architecture, breaking changes. Output ONLY the review: ## PR
> Review: #<number> — <title> / ### Summary / ### Findings / #### Critical / #### Suggestions /
> #### Positive / ### Verdict. End with --- and *Review by: <agent name>* | *Date: <today>*.

For example, to delegate to Claude:

```bash
claude -p 'Read AGENTS.md and .github/CONTRIBUTING.md. Get the PR via `gh pr view --json number,title,body,headRefName`. Get the diff via `gh pr diff`. Review for: correctness, style, testing, security, documentation, architecture, breaking changes. Output ONLY the review: ## PR Review: #<number> — <title> / ### Summary / ### Findings / #### Critical / #### Suggestions / #### Positive / ### Verdict. End with --- and *Review by: Claude* | *Date: <today>*.'
```

Capture stdout as that agent's review.

If any agent fails or produces empty output, report the error and ask whether to continue or retry. Also treat output containing `DELEGATION-ERROR:` as a failed run: the agent could not reach GitHub, so whatever else it printed rests on no data.

### Step 4: Post each review to the PR

```bash
gh pr comment <PR_NUMBER> --body "<agent review>"
```

Post one comment per agent.

### Step 5: Synthesize the findings

Create a synthesis listing: consensus findings (all agents), per-agent-only findings, combined verdict.

Format:
```
## Combined Review Summary

### Consensus Findings (all agents flagged)
- Description

### Per-Agent-Only Findings
- **<Agent>:** Description

### Combined Verdict
**Approve / Request Changes / Comment** — justification

---
*Synthesized Review by: <host agent> (from <agent1> + <agent2> + ... input)* | *Date: <today>*
```

### Step 6: User-approval gate

Present the synthesis and ask for approval before posting.

### Step 7: Post the approved synthesis

```bash
gh pr comment <PR_NUMBER> --body "<synthesis>"
```

## See also

- [Cross-Agent Delegation Matrix](../../../docs/development/ai/cross-agent-delegation.md) — the
  non-interactive invocation table this skill's [Agent invocations](#agent-invocations) section
  copies, and the read-only constraint every review file carries.

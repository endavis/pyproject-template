---
title: Plan-Mode State Hook
description: PostToolUse hooks that expose Claude Code plan mode as a file
audience:
  - contributors
  - ai-agents
tags:
  - ai
  - hooks
  - plan-mode
---

# Plan-Mode State Hook

Claude Code enters "plan mode" via the `EnterPlanMode` tool and exits via
`ExitPlanMode`. The state is not otherwise observable from disk, which
makes it impossible for slash commands (notably `/implement`) to
programmatically detect that their parent session is in plan mode before
they spawn a sub-agent via the Task tool.

This hook pair writes the current plan-mode state to a small file so
other tooling can check it.

## State file

- **Path:** `.claude/.plan-mode-state` (relative to `$CLAUDE_PROJECT_DIR`)
- **Values:**
    - `active` — plan mode is on.
    - `inactive` — plan mode is off.
    - *file missing* — treat as inactive (readers must handle this).
- **Format:** exactly one word, **no trailing newline**, so shell
  consumers can compare with `==`.
- **Gitignored:** yes — it is local runtime state.

## How it works

Two PostToolUse hooks are registered in
[`.claude/settings.json`](../../../.claude/settings.json):

| Matcher         | Script                                     | Writes       |
| --------------- | ------------------------------------------ | ------------ |
| `EnterPlanMode` | `tools/hooks/ai/plan-mode-enter.py`        | `active`     |
| `ExitPlanMode`  | `tools/hooks/ai/plan-mode-exit.py`         | `inactive`   |

Both scripts:

- Read and discard stdin (so Claude Code does not SIGPIPE on them).
- Write atomically (temp file in the same directory + `os.replace`), so
  a concurrent reader never sees a partial write.
- Create the `.claude/` directory if it is missing.
- Always exit `0`, even on failure — a hook error must never block a
  tool call. Failures are logged to stderr.

## Why `PostToolUse`, not `PreToolUse`

A `PreToolUse` hook fires before the tool runs, including for tool calls
the user then rejects. If plan-mode-exit were wired `Pre`, a user who
rejected `ExitPlanMode` would still end up with `inactive` on disk even
though plan mode is still on.

`PostToolUse` only runs after the tool successfully executes, so a
rejected `ExitPlanMode` leaves the state file at `active`. This is the
correct, conservative default.

## Known limitation: stale state

Plan mode can be exited **without** an explicit `ExitPlanMode` tool call
(for example, the user clears it via the CLI, or the session ends). In
that case no hook fires and the file stays at `active` even though plan
mode is off. Readers should treat the file as a hint, not a source of
truth, and should still surface the CLI status line to the user as a
backup.

## Consuming the state from shell

```bash
if [[ "$(cat "$CLAUDE_PROJECT_DIR/.claude/.plan-mode-state" 2>/dev/null)" == "active" ]]; then
    echo "plan mode is active"
fi
```

A missing file is treated as inactive by this pattern (the subshell
prints nothing and the comparison fails).

## Related

- [Command blocking hook](command-blocking.md) — the other hook under
  `tools/hooks/ai/`.
- Issue [#389](https://github.com/endavis/pyproject-template/issues/389)
  — the warning preamble in `/implement` that this hook enables to be
  upgraded from "ask the user to eyeball the status line" to a
  programmatic check.

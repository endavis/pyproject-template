---
name: gemini-implement
description: Use to delegate implementation of a GitHub issue from a Copilot CLI session to Gemini CLI via `gemini -y -p`. Captures the resulting summary; does not push or open a PR.
---

# Delegate Implement to Gemini (from Copilot)

Hand off implementation work for a GitHub issue to Gemini CLI via shell.

## When to use

Use this skill when the user explicitly wants implementation done by Gemini (not by Copilot). This is the Copilot-host bridge equivalent of Gemini's `/gemini:implement`.

Expected prompt shape:

- `/gemini-implement 399`
- `/gemini-implement delegate implementation of #399 to Gemini`

If the issue number is missing, ask for it before continuing.

## Instructions

1. Confirm the issue number from the user's request.
2. Run Gemini non-interactively. Hybrid C: prefer the existing `/gemini:implement` command if available, otherwise inline workflow.

   ```bash
   gemini -y -p 'Implement GitHub issue #<n> in the current repository. If the /gemini:implement command is available, run it for this issue. Otherwise, follow this workflow: 1) Read the plan comment from issue #<n> via `gh issue view <n> --json comments`. 2) Read AGENTS.md for branch naming and commit conventions. 3) Create or check out the branch `<type>/<n>-<slug>` (do not commit to main). 4) Implement the changes per the plan. 5) Run `doit check` to validate. Do NOT push the branch or open a PR — the user reviews first.'
   ```

3. After Gemini returns:
   - Summarize what was implemented and the `doit check` result.
   - Show the user the changed files (`git status`, `git diff --stat`) so they can review.
   - Do not push or open a PR yourself.

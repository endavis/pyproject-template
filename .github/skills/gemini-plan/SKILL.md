---
name: gemini-plan
description: Use to delegate planning for a GitHub issue from a Copilot CLI session to Gemini CLI via `gemini -y -p`. Captures the plan from stdout and returns it to the user; does not post to GitHub itself.
---

# Delegate Plan to Gemini (from Copilot)

Hand off planning work for a GitHub issue to Gemini CLI via shell.

## When to use

Use this skill when the user explicitly wants planning done by Gemini (not by Copilot). This is the Copilot-host bridge equivalent of Gemini's `/gemini:plan`.

Expected prompt shape:

- `/gemini-plan 399`
- `/gemini-plan delegate planning for #399 to Gemini`

If the issue number is missing, ask for it before continuing.

## Instructions

1. Confirm the issue number from the user's request.
2. Run Gemini non-interactively. Hybrid C: prefer the existing `/gemini:plan` command if available, otherwise inline workflow.

   ```bash
   gemini -y -p 'Plan the implementation for GitHub issue #<n> in the current repository. If the /gemini:plan command is available, run it for this issue. Otherwise, follow this workflow: 1) Run `gh issue view <n> --json title,body,labels` to read the issue. 2) Read AGENTS.md to understand the workflow and conventions. 3) Explore the relevant files. 4) Draft a plan with three sections: Implementation Plan, Test Plan, Validation Plan. 5) Print the full plan to stdout. Do NOT post a comment to the issue — the user reviews and posts.'
   ```

3. Capture stdout and summarize the plan to the user.
4. If the user wants revisions, invoke Gemini again with their feedback appended.
5. Do NOT post the plan as a comment yourself — the user owns that step.

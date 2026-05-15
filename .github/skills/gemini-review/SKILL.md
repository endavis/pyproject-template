---
name: gemini-review
description: Use to delegate a read-only code review of the current changes from a Copilot CLI session to Gemini CLI via `gemini -y -p`. Captures findings from stdout; does not modify files.
---

# Delegate Review to Gemini (from Copilot)

Hand off a read-only code review of the current changes to Gemini CLI via shell.

## When to use

Use this skill when the user explicitly wants a review by Gemini (not by Copilot). This is the Copilot-host bridge equivalent of Gemini's `/gemini:review`.

Optional focus area can be passed in.

## Instructions

1. Run Gemini non-interactively. Hybrid C: prefer the existing `/gemini:review` command if available, otherwise the prompt is fully inlined.

   ```bash
   gemini -y -p 'Review the current uncommitted changes and the current branch vs main, read-only. 1) Run `git status` and `git diff` to see what changed. 2) Run `git log main..HEAD --oneline` for branch context. 3) Read AGENTS.md and any relevant ADRs in docs/decisions/. 4) Identify correctness issues, risks, missing tests, style/convention violations, and concrete suggestions. 5) Print findings to stdout in a structured format (Summary / Issues / Suggestions). Do NOT modify any files. Focus area (optional): <focus>'
   ```

2. After Gemini returns:
   - Summarize the review findings to the user.
   - Highlight any blocking issues vs nits.
   - The user decides what to act on; do not auto-apply suggestions.

# Review via Codex

Delegate a read-only code review of the current changes to Codex CLI. Optional focus area: $ARGUMENTS.

## Instructions

Use the Bash tool to invoke Codex non-interactively. Hybrid C: prefer the existing `$codex-review` skill if available, otherwise the prompt is fully inlined.

```bash
codex -a never --dangerously-bypass-hook-trust exec 'Run every `gh` command as its own standalone shell command, never chained with other commands via `;`, `&&`, or a pipe — only a standalone `gh` matches the Codex allow rule in `.codex/rules/gh.rules`; chained, it runs inside the sandbox with no network access. Review the current uncommitted changes and the current branch vs main, read-only. 1) Run `git status` and `git diff` to see what changed. 2) Run `git log main..HEAD --oneline` for branch context. 3) Read AGENTS.md and any relevant ADRs in docs/decisions/. 4) Identify correctness issues, risks, missing tests, style/convention violations, and concrete suggestions. 5) Print findings to stdout in a structured format (Summary / Issues / Suggestions). Do NOT modify any files. Focus area (optional): $ARGUMENTS' < /dev/null
```

After Codex returns:
- Summarize the review findings to the user.
- Highlight any blocking issues vs nits.
- The user decides what to act on; do not auto-apply suggestions.

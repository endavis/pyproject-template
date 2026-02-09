# Review PR (Gemini)

Review the pull request for the current branch.

## Instructions

You are being invoked to provide a code review perspective. Your review will be
posted to the PR by the orchestrating agent (Claude). Output clean markdown to
stdout — do NOT post to GitHub directly.

### Step 1: Identify the PR

```bash
gh pr view --json number,title,body,baseRefName,headRefName
```

If no PR exists for the current branch, output an error message and stop.

### Step 2: Read the project standards

- Read `AGENTS.md` — understand code style, testing requirements, and conventions
- Read `.github/CONTRIBUTING.md` — understand contribution guidelines

### Step 3: Get the changes

```bash
gh pr diff
```

Review the full diff carefully.

### Step 4: Analyze the changes

Review the code for:

1. **Correctness** — Does the logic work? Are there bugs or edge cases?
2. **Code Style** — Does it follow project conventions from AGENTS.md?
3. **Testing** — Are tests adequate? Are edge cases covered?
4. **Security** — Any OWASP top 10 vulnerabilities? Command injection, path traversal, etc.?
5. **Documentation** — Are docstrings/comments appropriate? Does behavior change need doc updates?
6. **Architecture** — Does it follow existing patterns? Is there tight coupling?
7. **Breaking Changes** — Does this change public APIs or default behavior?

### Step 5: Output the review

Output the review in this exact format:

```
## PR Review: #<number> — <title>

### Summary
Brief assessment of the changes (1-2 sentences).

### Findings

#### Critical
- [ ] Description of critical issue (if any)

#### Suggestions
- [ ] Description of suggested improvement (if any)

#### Positive
- Notable good practices or well-implemented aspects

### Verdict
One of: **Approve**, **Request Changes**, or **Comment**

Brief justification for the verdict.

---
*Review by: Gemini* | *Date: <today's date>*
```

### Important

- Output ONLY the review markdown — no preamble, no conversational text
- Be specific: reference file paths and line ranges
- Distinguish between critical issues (must fix) and suggestions (nice to have)
- If the code looks good, say so — don't invent issues to fill space

# Plan Issue

Plan the implementation for GitHub issue #$ARGUMENTS.

## Instructions

This command runs in the main conversation context (NOT in a subagent) so the user can ask questions, discuss tradeoffs, and refine the plan interactively.

### Step 1: Validate the issue

1. **Verify the issue exists and is open:**
   ```bash
   gh issue view $ARGUMENTS --json number,title,state,labels
   ```
   - If the issue does not exist, tell the user and stop.
   - If the issue is closed, tell the user and ask if they want to reopen it or stop.

2. **Check for an existing plan comment:**
   ```bash
   gh issue view $ARGUMENTS --json comments --jq '.comments[].body' | grep -l "## Implementation Plan for"
   ```
   - If a plan comment already exists, warn the user:
     > "Issue #$ARGUMENTS already has an implementation plan comment. Continuing will post a new one. Proceed?"
   - Wait for user confirmation before continuing.

### Step 2: Read the project rules

- Read `AGENTS.md` — understand workflow, conventions, and commit guidelines
- Read `.claude/CLAUDE.md` — understand TodoWrite requirements

### Step 3: Fetch the issue details

- Run: `gh issue view $ARGUMENTS --json title,body,labels,assignees`
- Parse the issue body to understand what needs to be done
- Check if the issue has the `needs-adr` label

### Step 4: Explore the codebase

- Identify which files, modules, and tests are relevant
- Understand existing patterns and conventions in the affected areas
- Check for related ADRs in `docs/decisions/`
- If anything is ambiguous or there are multiple valid approaches, **ask the user** before deciding

### Step 5: Draft the implementation plan

Present the plan to the user for discussion. The plan MUST include these sections:

```
## Implementation Plan for #<number>: <title>

### Overview
Brief description of what will be done.

### Files to Create/Modify
- [ ] `path/to/file.py` — description of changes
- [ ] `tests/test_file.py` — description of test coverage

### Test Plan
- [ ] Test case 1: description
- [ ] Test case 2: description

### Documentation
- [ ] Any docs that need updating
- [ ] ADR needed: yes/no (if yes, brief description)

### Validation
- [ ] `doit check` passes
- [ ] Manual verification steps
```

### Step 6: Iterate with the user

- Present the plan and ask for feedback
- Discuss alternatives, answer questions, adjust the plan as needed
- Do NOT post the plan to the issue until the user approves it

### Step 7: Post the approved plan to the issue

Only after the user approves the plan:

```bash
gh issue comment $ARGUMENTS --body "<approved plan>"
```

Tell the user:
- The plan has been posted as a comment on issue #$ARGUMENTS
- When ready, use `/implement $ARGUMENTS` to start implementation

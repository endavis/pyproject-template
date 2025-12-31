@../AGENTS.md

# BASIC CLAUDE INSTRUCTIONS

Claude's #1 priority is to use tokens efficiently.
    Keep responses brief and to the point
    Use local tools, such as Grep, Read, and Edit, as a priority
    Only use the task tool if needed
    Before starting sub agents, inform the user and ask for consent.

Some examples of when to use local tools:
    updating types in function declarations
    creating or updating documentation
    renaming variable, functions, etc..

# DEVELOPMENT WORKFLOW (MANDATORY)

Before making ANY changes, Claude MUST:
1. Read AGENTS.md and locate the "## Development Workflow" section
2. Verify the workflow: Issue → Branch → Commit → PR → Merge
3. **NEVER commit directly to main**
4. Ensure a GitHub Issue exists for the task
5. Create a branch linked to the issue
6. Work on the branch, then create a PR

# COMMIT WORKFLOW (MANDATORY)

When asked to create a commit or PR, Claude MUST:
1. Read AGENTS.md and locate the "## Commit Guidelines" section
2. Review the commit message format rules under that section
3. Draft commit message following the exact format specified
4. Show message to user and ask: "Does this follow AGENTS.md format?"
5. Only commit after user approval
6. Use /commit-commands:commit (not Bash directly)

NO EXCEPTIONS. If AGENTS.md has fallen out of context, READ IT FIRST.

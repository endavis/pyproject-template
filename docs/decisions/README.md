# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for this project.

Template decisions are in [Template Decisions](../template/decisions/README.md).

## What is an ADR?

An ADR documents an architectural decision: what was decided and why. The detailed discussion and specification lives in the GitHub Issue; the ADR provides a summary with links.

## ADR Format

ADRs use a simplified format:

```markdown
# ADR-NNNN: Title

## Status
Accepted

## Decision
Brief summary of what was decided.

## Rationale
Why this decision was made.

## Related Issues
- Issue #XX: Description

## Related Documentation
- [Relevant Doc](../path/to/doc.md)
```

See [adr-template.md](adr-template.md) for the template.

## Creating a New ADR

```bash
# Interactive (opens editor)
doit adr --title="Your decision title"

# Non-interactive (for scripts/AI)
doit adr --title="Use Redis" --body="## Status\nAccepted\n..."
doit adr --title="Use Redis" --body-file=adr.md
```

## When to Create an ADR

Create an ADR when:
- Introducing a new tool, framework, or library
- Changing development workflow or processes
- Making decisions that affect project architecture

The Issue contains the full discussion; the ADR summarizes the outcome.

## ADR Statuses

- **Accepted**: Decision is in effect
- **Deprecated**: No longer relevant (kept for history)
- **Superseded**: Replaced by a newer ADR

## Index

| ADR | Title | Status |
|-----|-------|--------|

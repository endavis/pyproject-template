# ADR-0004: Auto-discover doit tasks from modules

## Status

Accepted

## Date

2025-01-21

## Context

The project uses doit for task automation (see [ADR-0002](0002-use-doit-for-task-automation.md)). Initially, `dodo.py` required manual imports for every task function:

```python
from tools.doit.build import task_build, task_publish
from tools.doit.docs import task_docs_build, task_docs_deploy
# ... 11+ import blocks
```

This approach was error-prone:

- Developers would forget to add imports for new tasks
- Adding a task required editing two files
- Import blocks grew unwieldy as tasks increased

## Decision

Implement automatic task discovery that scans `tools/doit/` modules and imports all `task_*` functions automatically.

The `dodo.py` file is now minimal:

```python
from tools.doit import discover_tasks

globals().update(discover_tasks())
```

The discovery mechanism uses `pkgutil.iter_modules` to find all Python modules in `tools/doit/` and imports any function starting with `task_` or the `DOIT_CONFIG` variable.

## Consequences

### Positive

- New tasks are automatically available without editing `dodo.py`
- Eliminates "forgot to import" errors
- Cleaner, minimal `dodo.py` (3 lines instead of 50+)
- Encourages modular task organization
- New modules in `tools/doit/` are automatically included

### Negative

- Slightly more "magic" - less explicit about what's imported
- Must follow naming convention (`task_` prefix) strictly
- Import errors in any module break all tasks

### Neutral

- Task organization is now purely based on file location
- Module structure in `tools/doit/` defines task grouping

## Participants

- Project maintainers

## Related

- [ADR-0002: Use doit for task automation](0002-use-doit-for-task-automation.md)
- Issue #173: Auto-discover doit tasks from tools/doit modules

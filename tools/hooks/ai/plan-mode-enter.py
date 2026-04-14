#!/usr/bin/env python3
"""
Claude Code PostToolUse hook for EnterPlanMode.

Writes the word ``active`` (no trailing newline) to
``$CLAUDE_PROJECT_DIR/.claude/.plan-mode-state`` so that other tooling
(e.g. /implement) can detect that the parent Claude session is currently
in plan mode before spawning sub-agents.

The write is atomic (temp file + os.replace) so a concurrent reader never
observes a partial write. The hook always exits 0 so a failure here can
never block a tool call.

For full documentation, see: docs/development/ai/plan-mode-hook.md
"""

import contextlib
import os
import sys
import tempfile
from pathlib import Path

STATE_DIR_NAME = ".claude"
STATE_FILE_NAME = ".plan-mode-state"


def write_state(project_dir: Path, value: str) -> None:
    """Atomically write ``value`` (no trailing newline) to the state file."""
    target = project_dir / STATE_DIR_NAME / STATE_FILE_NAME
    target.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        prefix=".plan-mode-state.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(value)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, target)
    except Exception:
        with contextlib.suppress(OSError):
            os.unlink(tmp_path)
        raise


def main() -> int:
    """Entry point. Always returns 0."""
    try:
        sys.stdin.read()
    except Exception as exc:
        print(f"plan-mode-enter: failed to read stdin: {exc}", file=sys.stderr)

    try:
        project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
        write_state(project_dir, "active")
    except Exception as exc:
        print(f"plan-mode-enter: failed to write state: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())

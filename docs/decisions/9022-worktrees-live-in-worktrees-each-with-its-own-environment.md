# ADR-9022: Worktrees live in worktrees/, each with its own environment

## Status
Accepted

## Decision
**A worktree lives in `worktrees/<branch>` at the root of the main checkout, is created with
`doit worktree`, and has its own environment.**

1. `worktrees/` is gitignored, and the repository-wide test walkers skip it.
2. `doit worktree --branch=<branch>` fetches `origin/main`, creates the branch from it with no
   upstream (so `doit pr` pushes it), and runs `uv sync --all-extras --dev` inside the worktree
   with `VIRTUAL_ENV` unset.
3. Inside a worktree, commands run through `uv run`, never with `--active`. The worktree is
   removed with `git worktree remove` once its PR has merged.

## Rationale
An agent needs a separate checkout when the user has uncommitted work in theirs. Doing it by hand
during the #847 trial went wrong three ways (#854):

- **Location.** `tmp/agents/<agent>/` holds files that are deleted when a task ends, and a
  worktree lives until its PR merges. `doit cleanup` also empties `tmp/`
  (`tools/doit/maintenance.py`), which would delete a worktree there along with any uncommitted
  work in it. A directory an agent's own tooling picks is not necessarily ignored:
  `.claude/worktrees/` was not, so a worktree there showed as untracked and `git add -A` would
  have embedded it. It has its own entry since #860.
- **Environment.** A new worktree has no `.venv`, and the shell's `VIRTUAL_ENV` and `PATH` still
  point at the main checkout's. A `.venv` created by plain `uv run` has runtime dependencies
  only, so `pytest`, `ruff` and `mypy` resolved to the main checkout's environment.
- **The obvious fix breaks the main checkout.** `uv run --active` installed the worktree's copy of
  the project into the main checkout's `.venv`. Restoring it needed the full
  `uv sync --all-extras --dev`, because a plain `uv sync` also removes the extras.

`worktrees/` sits inside the repository, in the project directory every agent already works in,
as `tmp/agents/` does. It is outside `tmp/` so that `doit cleanup` cannot reach it.

A `doit` task, rather than documented commands, because each failure was a step done by hand and
done wrong. The task does all three steps. It also resolves a relative `UV_CACHE_DIR` before
running `uv` inside the worktree, so the worktree shares the main checkout's uv cache instead of
starting an empty one.

## Consequences
- **Every repository-wide walker must skip `worktrees/`.** Each worktree is a full copy of the
  repository, so a scan from the main checkout would otherwise judge every copy.
  `tests/test_documented_paths.py`, `tests/test_instruction_pointers.py` and
  `tests/template/test_secret_env_policy.py` skip it, and each has a test that says so. A new
  walker needs the same entry.
- **A worktree's shell still carries the main checkout's environment** until direnv is allowed
  in it. `uv run` is what makes commands use the worktree's `.venv`.
- **Worktrees are always created from `origin/main`.** Branching from an unmerged branch, for
  work that builds on it, is not covered by the task.

## Related Issues
- Issue #854: a gitignored `worktrees/` directory and a `doit worktree` task
- Issue #848: the walkers skipped by absolute path, so a checkout under `tmp/` passed having
  checked nothing
- Issue #847: the stacked-PR trial where the manual worktree procedure failed
- Issue #860: the rule is anchored to `/worktrees/`, and `.claude/worktrees/` has its own entry

## Related Documentation
- [Doit Tasks Reference](../development/doit-tasks-reference.md) — the `worktree` task and how to
  work in a worktree
- [CONTRIBUTING.md](../../.github/CONTRIBUTING.md) — Development Workflow, step 2

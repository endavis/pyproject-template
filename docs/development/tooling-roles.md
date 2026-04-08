---
title: Tooling Roles and Architectural Boundaries
description: What each tool is for, who uses it, and where runtime code ends and dev tooling begins
audience:
  - contributors
  - ai-agents
tags:
  - architecture
  - tooling
  - doit
---

# Tooling Roles and Architectural Boundaries

## Overview

This project ships with a deliberately layered set of tools: a small runtime
package, a heavier set of development tools, and a task runner that ties the
dev workflow together. New contributors (human and AI) often blur these
layers — the most common mistake is treating `doit` as if it were the
application's user-facing CLI. This page is the source of truth for **what
tool belongs to which audience** and **where runtime code ends and
development tooling begins**.

## Layering

The repository has three distinct layers. Each layer has a different
audience, a different lifecycle, and a different set of allowed dependencies.

| Layer | Path | Audience | Purpose |
| :--- | :--- | :--- | :--- |
| **Runtime** | `src/package_name/` | End users of the published package | The actual application/library code that gets shipped to PyPI. |
| **Dev tooling** | `tools/` | Contributors and CI | Helpers, scaffolding, install scripts, doit task definitions, and template-management code. Not shipped. |
| **Dev entry point** | `dodo.py` | Contributors and CI | The doit task discovery file. Loads tasks from `tools/doit/`. Not shipped. |

The hard rule that holds these layers together:

> **`src/package_name/` never imports from `tools/` or `dodo.py`.**

Runtime code must be installable and runnable without any dev tooling
present. If you find yourself wanting to import from `tools/` inside the
runtime package, that is a signal the helper belongs in the runtime package
itself (and needs to be tested as runtime code).

## Tooling Roles

| Tool | Role | Audience | Never use for |
| :--- | :--- | :--- | :--- |
| **Application console script** | The package's user-facing command-line interface, defined as a `[project.scripts]` entry under `src/package_name/`. | End users of the published package. | Development workflow tasks. See [#341](https://github.com/endavis/pyproject-template/issues/341) for the application-CLI guide. |
| **`doit`** | Development task runner. Wraps tests, linting, type-checking, releases, issue and PR creation, and other contributor workflows. | Contributors and CI. | Fronting the application's user-facing CLI. doit is a *dev* surface, not a runtime surface. |
| **`uv`** | Package and environment management. Installs dependencies, runs Python, manages the lockfile. | Contributors and CI. | Replacing the application's runtime entry point. |
| **`gh`** | GitHub API access for operations not wrapped by `doit` (read-only queries, ad-hoc API calls). | Contributors and CI. | Write operations that already have a `doit` wrapper (e.g. use `doit pr` not `gh pr create`). |
| **`git`** | Version control. | Contributors and CI. | Workflow shortcuts that bypass branch protection or signed-commit requirements. |
| **Raw shell commands** | Last resort when nothing above covers the need. | Contributors and CI. | Anything a higher-level tool already wraps. |

This table mirrors the imperative "Tool Reference" table in
[`AGENTS.md`](../../AGENTS.md), which tells contributors *what command to
run*. This page tells them *why the layering exists*.

## Template Philosophy

The template is opinionated about a small number of things:

- **Runtime dependencies stay minimal.** Anything in `[project] dependencies`
  ships to every user of the package. Add to it sparingly.
- **Dev tooling is heavy and lives under `tools/`.** Contributors get the
  full suite (doit, ruff, mypy, pytest, mkdocs, mutmut, etc.) via
  `[dependency-groups] dev`.
- **`doit` is a development tool, not a runtime tool.** Tasks under
  `tools/doit/` exist to make contributor workflows reproducible. They are
  not part of the package's public API.
- **The application's user-facing CLI is a console script under
  `src/package_name/`, not a doit task.** End users should never need to
  install `doit` to use the published package. See
  [#341](https://github.com/endavis/pyproject-template/issues/341) for the
  application-CLI guide.
- **ADRs document the *why*.** When a tooling decision is non-obvious, it
  gets an ADR under `docs/template/decisions/` or `docs/decisions/`.

## Current vs Target State

> **Note — current state of doit and rich:**
> The target state described above is that `doit` and `rich` are
> **development-only** dependencies. As of this writing they are still
> declared in `[project] dependencies` in `pyproject.toml` for historical
> reasons (see [#65](https://github.com/endavis/pyproject-template/issues/65)).
> A separate refactor will move them out of the runtime dependency set. The
> rules on this page describe the intended architecture; the runtime-dependency
> placement of `doit` is a packaging convenience for adopters and does **not**
> make `doit` a runtime CLI surface for the application.

## See also

- [ADR-9002: Use doit for task automation](../template/decisions/9002-use-doit-for-task-automation.md)
- [ADR-9005: AI agent command restrictions](../template/decisions/9005-ai-agent-command-restrictions.md)
- [Doit Tasks Reference](doit-tasks-reference.md)
- [`AGENTS.md`](../../AGENTS.md) — imperative tool reference for contributors and AI agents
- [New Project Setup](../template/new-project.md)

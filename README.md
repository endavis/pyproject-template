# pyproject-template

[![CI](https://github.com/endavis/pyproject-template/actions/workflows/ci.yml/badge.svg)](https://github.com/endavis/pyproject-template/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A batteries-included GitHub template for modern Python projects — `uv`, `doit`, `ruff`, `mypy`,
`pytest`, GitHub Actions, MkDocs, and a first-class AI-agent workflow.

Spawn a project and you get the tooling, the CI, the release automation, and the agent
configuration already wired together and tested.

---

## Quick Setup (Automated)

🚀 **The fastest way to create a new project from this template:**

```bash
curl -sSL https://raw.githubusercontent.com/endavis/pyproject-template/main/bootstrap.py | python3
```

The script will:

- ✅ Create a new repository from this template on GitHub
- ✅ Configure repository settings (merge options, features)
- ✅ Set up branch protection rules
- ✅ Replicate labels
- ✅ Run placeholder replacement automatically
- ✅ Provide a checklist of manual steps (secrets, etc.)

**Requirements:** [GitHub CLI](https://cli.github.com/) authenticated (`gh auth login`), Git, and
Python 3.12+.

**You add manually afterwards:** PyPI tokens, a Codecov token (optional), and collaborator access.

📖 [New Project Setup](docs/template/new-project.md) has the detailed walkthrough.

## Using This Template (Manual)

If you would rather clone than use the bootstrap script:

```bash
git clone https://github.com/endavis/pyproject-template.git my-project
cd my-project
python3 tools/pyproject_template/configure.py
```

`configure.py` prompts for the project name, package name, PyPI name, author and GitHub user, then
renames the package directory, replaces every placeholder, installs `README.template.md` as the
project's `README.md`, and removes itself.

## What you get

| | |
| :--- | :--- |
| **Dependencies** | `uv` — lockfile-based, fast, reproducible |
| **Tasks** | `doit` — 50 tasks covering test, lint, type-check, docs, release, issues and PRs |
| **Quality** | `ruff` (format + lint), `mypy` (strict), `bandit`, `pip-audit`, `vulture`, `codespell` |
| **Testing** | `pytest` with `xdist`, coverage gating, benchmarks, Hypothesis property tests |
| **CI/CD** | GitHub Actions across Linux/macOS/Windows and Python 3.12–3.14, with a merge gate |
| **Releases** | `hatch-vcs` versioning plus commitizen-driven tagging and changelog |
| **Docs** | MkDocs Material, built with `--strict` so broken links fail CI |
| **Decisions** | 17 ADRs recording why the tooling is the way it is |

## AI agent workflow

Four CLIs are supported as first-class agents — **Claude Code**, **GitHub Copilot CLI**,
**Codex CLI**, and **Antigravity CLI** (`agy`) — each able to act on itself or delegate to any of
the others.

- **Enforced workflow.** Issue → branch → `doit check` → PR → merge gate. Agents cannot commit to
  `main`, skip hooks, or apply the `ready-to-merge` label.
- **A shared safety hook** blocks dangerous commands for every agent, and fails *closed* — a hook
  that cannot evaluate a command denies it rather than allowing it.
- **Cross-agent delegation.** `/claude:plan`, `$codex-implement`, `/copilot-review`, and the
  `/multi-*` orchestrators that fan a task out to several agents and synthesize the results.

📖 [AI Agent Setup](docs/development/AI_SETUP.md) ·
[First 5 Minutes](docs/development/ai/first-5-minutes.md) ·
[Cross-Agent Delegation](docs/development/ai/cross-agent-delegation.md) ·
[Command Blocking](docs/development/ai/command-blocking.md)

## Documentation

| Guide | |
| :--- | :--- |
| [Template Overview](docs/template/index.md) | What the template ships and how it fits together |
| [New Project Setup](docs/template/new-project.md) | Creating a project, start to finish |
| [Template Manager](docs/template/manage.md) | The `manage.py` entry point |
| [Keeping Up to Date](docs/template/updates.md) | Pulling template changes into an existing project |
| [Migration Guide](docs/template/migration.md) | Adopting the template in an existing project |
| [Tools Reference](docs/template/tools-reference.md) | Every script under `tools/` |
| [Contributing](.github/CONTRIBUTING.md) | Workflow, commit format, code style |
| [All Documents](docs/TABLE_OF_CONTENTS.md) | Full index |

## Developing the template itself

This is the workflow for working on *this* repository, not on a project spawned from it.

```bash
git clone https://github.com/endavis/pyproject-template.git
cd pyproject-template
uv sync --all-extras --dev
uv run pre-commit install
doit check          # test, lint, type-check, security, spelling
```

`doit list` shows every task. `doit check` is the gate CI enforces — run it before staging.

Contributions follow the same workflow the template ships: an issue, a branch, `doit check`, a PR
via `doit pr`, and a human-applied `ready-to-merge` label. See
[CONTRIBUTING](.github/CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).

> **Note on `README.template.md`:** that file is the README your *spawned project* gets, complete
> with placeholders. `configure.py` moves it into place. This page describes the template itself,
> so the two never have to compromise on each other.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

Built on [uv](https://github.com/astral-sh/uv), [doit](https://pydoit.org/),
[ruff](https://github.com/astral-sh/ruff), [mypy](https://mypy-lang.org/),
[pytest](https://pytest.org/), and [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

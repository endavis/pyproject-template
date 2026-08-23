---
title: AI Command Blocking
description: Hooks that block dangerous commands from AI agents
audience:
  - contributors
  - ai-agents
tags:
  - ai
  - security
  - hooks
---

# AI CLI Hooks

The `tools/hooks/ai/` directory contains hooks for AI coding assistants (Claude Code, Gemini CLI, Copilot CLI, Codex CLI, Antigravity CLI).

## Block Dangerous Commands

### Purpose

AI agents can sometimes attempt dangerous operations like:

- `--admin` - bypasses branch protection
- `--no-verify` - skips pre-commit hooks
- `git reset --hard` - loses uncommitted changes
- `rm -rf /` or `rm -rf ~` - destructive deletions
- Force push to `main`/`master` - overwrites shared history
- Deleting protected branches
- Merge commits on protected branches - violates linear history

These hooks intercept commands before execution and block dangerous patterns, even if the agent doesn't follow the rules in `AGENTS.md`.

### How It Works

The hook uses Python's `shlex` module to properly parse shell quoting:

1. **Tokenize** the command with `shlex.split()`
2. **Check** for dangerous flags as standalone tokens
3. **Check** for dangerous token sequences (e.g., `rm -rf ~`)
4. **Check** for force push to protected branches (main/master) — including refspec forms (`HEAD:main`, `+main`) and commands preceded by git global options (`-C`, `-c`, `--git-dir`, …)
5. **Check** for deletion of protected branches — also handles git global options
6. **Check** for merge commits on protected branches (linear history)
7. **Recurse** into shell-wrapper payloads (`bash -c "..."`, `sh -c "..."`, `eval "..."`) — up to depth 3, so all checks above apply inside wrappers
8. **Block** or **Allow** — Claude/Gemini/Codex block via exit code 2; Copilot and Antigravity block via a stdout decision JSON (exit code 0)

#### Key Feature: Chained Command Detection

The hook scans all token positions, so chained commands using `&&` or `;` are caught:

```bash
# BLOCKED - dangerous command after safe one
git status; git push --force origin main
cd /path && doit release

# ALLOWED - all commands in the chain are safe
cd /path && doit check
git status; git push origin feat/branch
```

#### Key Feature: Git Global Option Handling

Git global options (e.g., `-C <path>`, `-c <k>=<v>`, `--git-dir=<dir>`) appear between the `git`
token and the subcommand. The hook walks past them to find the real subcommand, so these are all
caught:

```bash
# BLOCKED - global options shift the subcommand position, but hook handles them
git -C . push --force origin main
git -c core.pager=cat push --force origin main
git --git-dir=.git push --force origin main
git -C . branch -D main
```

#### Key Feature: Refspec-Aware Branch Extraction

Force push to a protected branch is detected regardless of refspec form:

```bash
# BLOCKED - all target the 'main' branch
git push --force origin HEAD:main
git push origin +main
git push --force-with-lease=HEAD origin HEAD:main

# ALLOWED - destination branch is a feature branch
git push origin main:feature        # pushes local 'main' to remote 'feature'
git push origin HEAD:refs/heads/dev
```

#### Key Feature: Shell-Wrapper Payload Unwrapping

The hook recurses into `bash -c`, `sh -c`, `zsh -c`, `dash -c`, and `eval` payloads (up to depth
3), so all checks apply inside wrappers:

```bash
# BLOCKED - dangerous command inside a wrapper
bash -c "git push --force origin main"
sh -c "git branch -D main"
eval "gh pr merge 1 --admin"

# ALLOWED - safe command inside a wrapper
bash -c "echo main"
bash -c "git status"
```

#### Key Feature: Quote-Aware Parsing

The hook correctly distinguishes between:

```bash
# BLOCKED - actual dangerous flag
gh pr merge --admin

# ALLOWED - flag is just text in a commit message
git commit -m "The --admin flag is dangerous"

# ALLOWED - flag mentioned in heredoc content
doit pr --body="$(cat <<'EOF'
Do not use --force
EOF
)"
```

### Files

| File | Description |
|------|-------------|
| [`block-dangerous-commands.py`](../../../tools/hooks/ai/block-dangerous-commands.py) | The hook script (shared by Claude, Gemini, Copilot, Codex, and Antigravity) |
| [`block-dangerous-commands.sh`](../../../tools/hooks/ai/block-dangerous-commands.sh) | Fail-closed launcher used by the stdout-contract CLIs (Copilot, Antigravity) |
| [`test_hook.py`](../../../tools/hooks/ai/test_hook.py) | Manual test suite (run with `python3 tools/hooks/ai/test_hook.py`) |
| [`tests/test_hook_block_dangerous_commands.py`](../../../tests/test_hook_block_dangerous_commands.py) | Pytest test suite — collected by CI via `testpaths = ["tests"]` |

### Configuration

#### Claude Code

`.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/tools/hooks/ai/block-dangerous-commands.py"
          }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/tools/hooks/ai/block-dangerous-commands.py"
          }
        ]
      }
    ]
  }
}
```

#### Gemini CLI

`.gemini/settings.json`:
```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "run_shell_command",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $GEMINI_PROJECT_DIR/tools/hooks/ai/block-dangerous-commands.py"
          }
        ]
      },
      {
        "matcher": "write_file|replace",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $GEMINI_PROJECT_DIR/tools/hooks/ai/block-dangerous-commands.py"
          }
        ]
      }
    ]
  }
}
```

Gemini's file-write tools are `write_file` (full-file overwrite, `content` param) and `replace` (string replacement, `old_string`/`new_string` params). Both use `file_path`.

#### Copilot CLI

`.github/hooks/copilot-hooks.json`:
```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": "sh ../../tools/hooks/ai/block-dangerous-commands.sh",
        "cwd": ".github/hooks",
        "timeoutSec": 10
      }
    ]
  }
}
```

No change needed for Copilot — the hook fires on every tool call (no `matcher` field), so Edit/Write variants are automatically covered.

#### Codex CLI

`.codex/config.toml`:
```toml
approval_policy = "untrusted"

[features]
codex_hooks = true

[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = 'python3 "$(git rev-parse --show-toplevel)/tools/hooks/ai/block-dangerous-commands.py"'
timeout = 30
statusMessage = "Checking Bash command"

[[hooks.PreToolUse]]
matcher = "^(Edit|Write|MultiEdit)$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = 'python3 "$(git rev-parse --show-toplevel)/tools/hooks/ai/block-dangerous-commands.py"'
timeout = 30
statusMessage = "Checking file edit"
```

Codex uses the shared hook as the primary defense layer. Project docs should not rely on the obsolete `[[approval_policy]]` command-rule format.

#### Antigravity CLI (`agy`)

`.agents/hooks.json`:
```json
{
  "block-dangerous-commands": {
    "PreToolUse": [
      {
        "matcher": "run_command|write_to_file",
        "hooks": [
          {
            "type": "command",
            "command": "sh \"$(git rev-parse --show-toplevel)/tools/hooks/ai/block-dangerous-commands.sh\""
          }
        ]
      }
    ]
  }
}
```

Antigravity sends a distinct hook payload — a nested `toolCall` with PascalCase args
(`{"toolCall": {"name": "run_command", "args": {"CommandLine": "..."}}}`); its file-write tool is
`write_to_file` (`TargetFile` / `CodeContent`). The hook normalizes these to the canonical
`command` / `file_path` / `content` keys.

Unlike Claude/Gemini/Codex (which block via exit code 2), `agy` blocks only when the hook prints
`{"decision": "deny", "reason": "..."}` on **stdout** (exit code 0); a safe command prints nothing
and defers to `agy`'s normal permission flow. A `deny` decision hard-blocks even under
`--dangerously-skip-permissions`.

`agy` exposes no project-dir env var, but it **does** shell-interpret the hook command, so the
path is pinned with `$(git rev-parse --show-toplevel)` rather than left relative.

The handler's working directory is the directory containing `hooks.json`. Verified empirically by
logging `os.getcwd()` from the hook during a real `agy` run:

```
_cwd   = <repo-root>/.agents
_argv0 = ../tools/hooks/ai/block-dangerous-commands.py
```

A relative `../tools/...` therefore did resolve — but only because of that CWD, which is `agy`
behaviour rather than a documented contract. Since the hook is `agy`'s only gate (delegated
invocations pass `--dangerously-skip-permissions`) and its deny contract is stdout-based, a CWD
change in a future `agy` release would have disabled it silently and permissively. The absolute
form removes that dependency.

`agy` only loads workspace customizations for an **active/trusted** workspace, so headless
`agy -p` invocations must pass `--add-dir <repo-root>` for the hook to apply; interactive sessions
prompt to trust the workspace on first open.

To confirm the hook is firing, set `HOOK_BLOCKCOMMAND_DEBUG=1` — without it the hook writes no
debug log and an "is it wired?" probe reads as a false negative:

```bash
HOOK_BLOCKCOMMAND_DEBUG=1 agy -p 'run: git status' --add-dir "$(git rev-parse --show-toplevel)"
cat tools/hooks/ai/hook-debug.jsonl   # a new line means the hook ran
```

### Failure Behaviour

The hook uses two deny contracts, and they diverge on *failure*:

| Agents | Deny contract | If the hook produces nothing |
| :--- | :--- | :--- |
| Claude, Gemini, Codex | exit code 2 + stderr | Blocked — a failed `python3` also exits non-zero |
| Copilot, Antigravity | stdout JSON, exit 0 | **Allowed** — "no payload" means "no objection" |

So for the stdout-contract CLIs, anything that stops the hook from printing its payload silently
removes protection. Two layers close that:

**In-script** (`block-dangerous-commands.py`) — `run()` wraps `main()` so an unexpected exception
denies instead of propagating, and unparsable stdin denies instead of returning `1` (which no CLI
treats as a block). Both paths call `_fail_closed()`, which emits *every* contract at once — a
single JSON object carrying both `decision` and `permissionDecision`, plus exit 2 and stderr —
because at that point the calling CLI is unknown.

**At the wiring** (`block-dangerous-commands.sh`) — a script that never starts cannot emit its own
deny, so the stdout-contract CLIs invoke this launcher instead of the `.py` directly. It denies
when `python3` or the hook script is unavailable.

The launcher checks those preconditions rather than the hook's exit status, deliberately: the hook
exits 2 on its own fail-closed path, which is indistinguishable from "`python3` could not find the
file". Branching on exit status would append a second deny payload after the hook's own, putting
two JSON objects on stdout.

Verified against the real CLIs — `agy`, `copilot`, and Claude Code all block on the combined
payload, and both stdout-contract CLIs tolerate the extra key and the non-zero exit. Gemini and
Codex share Claude's exit-2 contract.

**Known gap:** a syntax error in the hook script, or a hook timeout, still yields no payload and no
launcher precondition failure. Covering that would require the hook to emit something on every
invocation, including allows, which is a protocol change both stdout-contract CLIs would need to
tolerate.

### Testing

Run the test suite after making changes:

```bash
python3 tools/hooks/ai/test_hook.py
```

Output shows green for passing tests, red for failures:

```
Testing hook: /path/to/block-dangerous-commands.py

================================================================================
+ ALLOW (expected ALLOW) | safe command              | git status
+ ALLOW (expected ALLOW) | double quoted             | git commit -m "text with --admin"
+ BLOCK (expected BLOCK) | actual --admin flag       | gh pr merge --admin
================================================================================

Results: 134 passed, 0 failed
```

### Blocked Patterns

#### Dangerous Flags (always blocked)

| Flag | Reason |
|------|--------|
| `--admin` | Bypasses branch protection rules |
| `--no-verify` | Skips pre-commit/pre-push hooks |
| `--hard` | Hard reset - can lose uncommitted changes |

#### Dangerous Sequences (consecutive tokens)

| Sequence | Reason |
|----------|--------|
| `rm -rf /` | Destructive: removes root filesystem |
| `rm -rf ~` | Destructive: removes home directory |
| `sudo rm` | Privileged deletion |

#### Protected Branch Operations

Force push, delete, and merge operations are only blocked when targeting protected branches (`main`, `master`).

| Command | Result |
|---------|--------|
| `git push --force origin main` | BLOCKED |
| `git push --force origin feat/branch` | ALLOWED |
| `git push -f origin master` | BLOCKED |
| `git push --force` (no branch) | BLOCKED (safer default) |
| `git push origin --delete main` | BLOCKED |
| `git push origin :main` | BLOCKED |
| `git branch -D main` | BLOCKED |
| `git branch -D feat/old` | ALLOWED |
| `git merge branch` (on main) | BLOCKED (creates merge commit) |
| `git merge --ff-only branch` (on main) | ALLOWED (fast-forward only) |
| `git merge branch` (on feature) | ALLOWED |

#### Blocked Workflow Commands

These commands should use `doit` wrappers or require user approval:

| Command | Use Instead | Reason |
|---------|-------------|--------|
| `gh issue create` | `doit issue --type=<type>` | Ensures proper template and labels |
| `gh pr create` | `doit pr` | Ensures proper template format |
| `gh pr merge` | `doit pr_merge` | Enforces merge commit format: `<type>: <subject> (merges PR #XX, addresses #YY)` |
| `uv add` | User runs manually | Dependencies require human approval - suggest package, let user run command |
| `doit release*` | User runs manually | Releases require human approval - AI can help prepare but not execute |

#### Governance Labels

Some labels are governance controls that require human approval. AI agents are blocked from adding these labels:

| Label | Reason |
|-------|--------|
| `ready-to-merge` | Signals human approval that PR is ready for merge. Add manually via `gh pr edit --add-label ready-to-merge` or GitHub web UI. |

##### Opt-in: `ALLOW_AI_READY_TO_MERGE`

A human can grant an AI agent a one-session pass to apply the `ready-to-merge` label by setting an environment variable **before launching the AI CLI**:

```bash
export ALLOW_AI_READY_TO_MERGE=1
claude  # or gemini, copilot, codex
```

The hook reads `os.environ` at hook-startup time (the AI CLI's process environment), so the variable must be set in the shell that launches the AI process — not by any command the AI itself runs. The AI has no path to set or persist this variable; attempts to do so are blocked (see [Env-Var Persistence Blocks](#env-var-persistence-blocks) below).

**Truthy values** (case-insensitive): `1`, `true`, `yes`, `on`. All other values (including empty string or unset) are falsy and preserve the block.

**Threat model:**

- The AI cannot set the variable in `os.environ` of its own parent process.
- The AI cannot persist the variable by writing to shell rc files, `.envrc`, `.env`, or AI CLI settings files — the hook blocks those writes.
- Each AI CLI session inherits a fixed snapshot of the environment; a Bash subprocess setting the variable does not affect the hook's already-read `os.environ`.
- The variable is scoped to a single shell session. Close the terminal (or `unset ALLOW_AI_READY_TO_MERGE`) to revoke the pass.

**To disable:** run `unset ALLOW_AI_READY_TO_MERGE`, or close the shell, or restart the AI CLI without the variable set.

#### Env-Var Persistence Blocks

The hook fires on **Edit**, **Write**, and **MultiEdit** (Claude/Codex), **write_file**/**replace** (Gemini), and **write_to_file** (Antigravity) in addition to Bash commands. Any operation whose payload contains the literal string `ALLOW_AI_READY_TO_MERGE` **and** whose target is a known persistence file is blocked.

**Protected file basenames** (Bash redirect target or `file_path` argument):

| File | Notes |
|------|-------|
| `.bashrc`, `.zshrc`, `.profile`, `.bash_profile`, `.bash_login`, `.zshenv` | Shell init files |
| `config.fish` | Only when parent path contains `.config/fish` |
| `.envrc`, `.env`, `.env.local`, `.env.development`, `.env.production` | Project env files |
| `settings.json`, `settings.local.json` | Only when parent dir is `.claude`, `.gemini`, or `.copilot` |
| `config.toml` | Only when parent dir is `.codex` |
| `copilot-hooks.json` | Any path (Copilot's env-injection vector) |

**Example blocked Bash command:**

```bash
# BLOCKED — AI cannot persist the variable via shell redirect
echo "export ALLOW_AI_READY_TO_MERGE=1" >> ~/.bashrc
```

**Example blocked file edit:**

```
# BLOCKED — AI cannot persist the variable via Edit tool
Edit ~/.bashrc
  new_string: "export ALLOW_AI_READY_TO_MERGE=1"
```

### Adding New Patterns

Edit `tools/hooks/ai/block-dangerous-commands.py`:

```python
# Add a new always-blocked flag
DANGEROUS_FLAGS = {
    "--admin": "Bypasses branch protection rules",
    "--new-flag": "Description of why it's dangerous",
}

# Add a new dangerous sequence
DANGEROUS_SEQUENCES = [
    (["rm", "-rf", "/"], "Destructive: removes root filesystem"),
    (["new", "dangerous", "sequence"], "Why it's dangerous"),
]

# Add a new protected branch
PROTECTED_BRANCHES = {"main", "master", "production"}
```

Then run the test suite to verify.

## Related

- [AI Enforcement Principles](enforcement-principles.md) - Why and how we enforce rules in code
- [AGENTS.md](../../../AGENTS.md) - AI agent rules including "When Blocked Protocol"
- [AI Agent Setup](../AI_SETUP.md) - Setting up AI coding assistants
- [Bash raw-tool ban](token-efficiency-add-ons.md#bash-raw-tool-ban-opt-in) - Opt-in hook that blocks raw shell commands AI agents should use native tools for (`cat`, `head`, `tail`, `find`, `grep`, `rg`, `wc`)

#!/usr/bin/env python3
"""
Claude Code PreToolUse hook to block dangerous command patterns.

This hook intercepts Bash commands before execution and blocks those
containing dangerous flags that could bypass security controls.

Uses a lexer to distinguish between actual command flags and quoted text
content (e.g., commit messages mentioning flags are allowed).

Exit codes:
  0 - Allow command
  2 - Block command (shows stderr to Claude)

Lexer source: https://stackoverflow.com/a/29444282 (CC BY-SA 4.0)
"""

import json
import re
import sys

# Dangerous patterns to block (checked against unquoted tokens only)
# Format: (pattern, description)
# Note: Use (^|\s) instead of \b for flags starting with -- since - isn't a word char
DANGEROUS_PATTERNS = [
    # Git bypass flags
    (r"(^|\s)--admin(\s|$)", "Bypasses branch protection rules"),
    (r"(^|\s)--force(\s|$)", "Force operation - can cause data loss"),
    (r"git\s+push\s+.*\s-f(\s|$)", "Force push - can overwrite remote history"),
    (r"(^|\s)--no-verify(\s|$)", "Skips pre-commit/pre-push hooks"),
    (r"git\s+push\s+.*--force-with-lease", "Force push variant"),
    # Destructive operations
    (r"rm\s+-rf\s+/\s*$", "Destructive: removes root filesystem"),
    (r"rm\s+-rf\s+~", "Destructive: removes home directory"),
    (r":>\s*/", "Destructive: truncates system files"),
    # Privilege escalation without context
    (r"^\s*sudo\s+rm\s", "Privileged deletion"),
    # Git history rewriting on main
    (r"git\s+reset\s+--hard", "Hard reset - can lose uncommitted changes"),
    (r"git\s+rebase\s+.*\smain(\s|$)", "Rebasing main branch"),
]


def lex(ln: str) -> list[str]:
    """
    Tokenize a command string, preserving quoted content as single tokens.

    Quoted strings (single, double) and bracketed content ({}, (), [])
    are kept as single tokens WITH their delimiters, allowing callers
    to identify and skip quoted content.

    Source: https://stackoverflow.com/a/29444282 (CC BY-SA 4.0)
    Modified for type hints and simplified comment handling.
    """
    token_delims = "''\"\"{}()[]"
    regex_subexpressions = []
    for i in range(0, len(token_delims), 2):
        # Regex for each delimiter pair: matches opening, non-delim chars, closing
        regex_subexpressions.append(
            rf"\{token_delims[i]}[^{token_delims[i + 1]}]*\{token_delims[i + 1]}"
        )
    # Combine with regex for whitespace-delimited tokens
    regex = "|".join(regex_subexpressions) + r"|\S+"

    tokens = re.findall(regex, ln)
    return tokens


def is_quoted(token: str) -> bool:
    """Check if a token is quoted content (starts with quote or bracket)."""
    if not token:
        return False
    return token[0] in "\"'{}()[]"


def check_command(command: str) -> tuple[bool, str]:
    """
    Check if command contains dangerous patterns in unquoted tokens.

    Tokenizes the command and filters out quoted content before checking,
    so that commit messages or issue bodies mentioning flags are allowed.

    Returns:
        (is_dangerous, reason)
    """
    # Tokenize and filter out quoted content
    tokens = lex(command)
    unquoted_tokens = [t for t in tokens if not is_quoted(t)]

    # Rejoin unquoted tokens for pattern matching
    unquoted_command = " ".join(unquoted_tokens)

    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, unquoted_command, re.IGNORECASE):
            return True, reason
    return False, ""


def main() -> int:
    """Main entry point."""
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        return 1

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only check shell commands (Bash for Claude, run_shell_command for Gemini)
    if tool_name not in ("Bash", "run_shell_command"):
        return 0

    command = tool_input.get("command", "")
    if not command:
        return 0

    is_dangerous, reason = check_command(command)
    if is_dangerous:
        print(
            f"BLOCKED: Command contains dangerous pattern.\n"
            f"Reason: {reason}\n"
            f"Command: {command}\n"
            f"\n"
            f"If this is intentional, ask the user to run it manually.",
            file=sys.stderr,
        )
        return 2  # Exit 2 = Block and show stderr to Claude

    return 0


if __name__ == "__main__":
    sys.exit(main())

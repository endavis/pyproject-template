#!/usr/bin/env python3
"""
Claude Code PreToolUse hook to block dangerous command patterns.

This hook intercepts Bash commands before execution and blocks those
containing dangerous flags that could bypass security controls.

Uses shlex to properly parse shell quoting, then checks for dangerous
patterns as standalone tokens (not embedded in quoted argument values).

Exit codes:
  0 - Allow command
  2 - Block command (shows stderr to Claude)
"""

import json
import shlex
import sys

# Dangerous flags that must appear as exact standalone tokens
DANGEROUS_FLAGS = {
    "--admin": "Bypasses branch protection rules",
    "--force": "Force operation - can cause data loss",
    "--no-verify": "Skips pre-commit/pre-push hooks",
    "--force-with-lease": "Force push variant",
    "--hard": "Hard reset - can lose uncommitted changes",
}

# Dangerous token sequences (checked in order)
# Format: (token_sequence, description)
DANGEROUS_SEQUENCES = [
    (["git", "push", "-f"], "Force push - can overwrite remote history"),
    (["rm", "-rf", "/"], "Destructive: removes root filesystem"),
    (["rm", "-rf", "~"], "Destructive: removes home directory"),
    (["sudo", "rm"], "Privileged deletion"),
]


def tokenize(command: str) -> list[str]:
    """
    Tokenize command using shlex for proper shell quote handling.

    shlex.split() correctly handles:
    - Double quoted strings: "text with --admin"
    - Single quoted strings: 'text with --force'
    - Embedded quotes: --body="value"
    - Escape sequences

    Returns list of tokens with quotes stripped from values.
    """
    try:
        return shlex.split(command, posix=True)
    except ValueError:
        # Fallback for malformed quotes - try non-POSIX mode
        try:
            return shlex.split(command, posix=False)
        except ValueError:
            # Last resort - simple whitespace split
            return command.split()


def check_dangerous_flags(tokens: list[str]) -> tuple[bool, str]:
    """
    Check if any dangerous flag appears as a standalone token.

    A flag in a quoted argument value (e.g., -m "--admin mentioned")
    becomes part of a larger token and won't match.
    """
    for token in tokens:
        if token in DANGEROUS_FLAGS:
            return True, DANGEROUS_FLAGS[token]
    return False, ""


def check_dangerous_sequences(tokens: list[str]) -> tuple[bool, str]:
    """
    Check if dangerous token sequences appear in the command.

    Looks for consecutive tokens matching dangerous patterns.
    """
    tokens_lower = [t.lower() for t in tokens]

    for sequence, reason in DANGEROUS_SEQUENCES:
        seq_len = len(sequence)
        for i in range(len(tokens_lower) - seq_len + 1):
            if tokens_lower[i : i + seq_len] == [s.lower() for s in sequence]:
                return True, reason
    return False, ""


def check_command(command: str) -> tuple[bool, str]:
    """
    Check if command contains dangerous patterns.

    Uses shlex to tokenize, then checks for:
    1. Dangerous flags as standalone tokens
    2. Dangerous token sequences

    Returns:
        (is_dangerous, reason)
    """
    tokens = tokenize(command)

    # Check for dangerous standalone flags
    is_dangerous, reason = check_dangerous_flags(tokens)
    if is_dangerous:
        return True, reason

    # Check for dangerous sequences
    is_dangerous, reason = check_dangerous_sequences(tokens)
    if is_dangerous:
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

#!/usr/bin/env python3
"""
Test suite for the dangerous command blocking hook.

Run this after making changes to the lexer or patterns to verify behavior.

Usage:
    python3 .claude/hooks/test_hook.py
    python3 .gemini/hooks/test_hook.py
"""

import subprocess
import sys
from pathlib import Path

# Find the hook to test (same directory as this test file)
HOOK_PATH = Path(__file__).parent / "block-dangerous-commands.py"

# Test cases: (command, expected_result, description)
# expected_result: 'ALLOW' or 'BLOCK'
TESTS = [
    # === SHOULD ALLOW - Safe commands ===
    ("git status", "ALLOW", "safe command"),
    ("git log --oneline", "ALLOW", "safe with flag"),
    # === SHOULD ALLOW - Dangerous patterns in quoted text ===
    ('git commit -m "text with --admin"', "ALLOW", "double quoted"),
    ('echo "--force flag"', "ALLOW", "double quoted 2"),
    ("echo '--no-verify test'", "ALLOW", "single quoted"),
    ('git commit -m "do not use --force"', "ALLOW", "flag in message"),
    # === SHOULD ALLOW - Heredocs (content inside quotes) ===
    (
        """git commit -m "$(cat <<'EOF'
--admin mentioned in docs
EOF
)\"""",
        "ALLOW",
        "heredoc with --admin",
    ),
    (
        '''doit pr --body="$(cat <<'EOF'
## Blocked Patterns
- `--admin` (bypasses branch protection)
- `rm -rf ~` (destructive)
EOF
)"''',
        "ALLOW",
        "heredoc with markdown",
    ),
    # === SHOULD BLOCK - Actual dangerous commands ===
    ("gh pr merge --admin", "BLOCK", "actual --admin flag"),
    ("git push --force", "BLOCK", "actual --force flag"),
    ("git push --force-with-lease", "BLOCK", "--force-with-lease"),
    ("git commit --no-verify", "BLOCK", "actual --no-verify"),
    ("git reset --hard HEAD", "BLOCK", "git reset --hard"),
    ("git push -f origin main", "BLOCK", "force push with -f"),
]


def run_test(cmd: str, expected: str, desc: str) -> bool:
    """Run a single test and return True if it passed."""
    import json

    json_input = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
    result = subprocess.run(
        ["python3", str(HOOK_PATH)], input=json_input, capture_output=True, text=True
    )
    actual = "BLOCK" if result.returncode == 2 else "ALLOW"
    passed = actual == expected
    mark = "+" if passed else "X"

    # Truncate command for display
    cmd_display = cmd.replace("\n", "\\n")
    if len(cmd_display) > 50:
        cmd_display = cmd_display[:47] + "..."

    print(f"{mark} {actual:5} (expected {expected:5}) | {desc:25} | {cmd_display}")

    if not passed:
        print(f'  stderr: {result.stderr[:200] if result.stderr else "(none)"}')

    return passed


def main() -> int:
    """Run all tests and return exit code."""
    print(f"Testing hook: {HOOK_PATH}\n")
    print("=" * 80)

    passed = 0
    failed = 0

    for cmd, expected, desc in TESTS:
        if run_test(cmd, expected, desc):
            passed += 1
        else:
            failed += 1

    print("=" * 80)
    print(f"\nResults: {passed} passed, {failed} failed")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

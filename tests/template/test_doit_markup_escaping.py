"""Rich markup in ``tools/doit/`` never carries outside text unescaped (#900).

Rich reads a ``[`` followed by a lowercase letter, ``#``, ``/`` or ``@`` as a markup tag. It drops a
tag it does not know and raises ``MarkupError`` on a closing tag with no opener. So git's
``[rejected]`` vanished from ``doit pr``'s push error, and a commit subject holding ``[/tmp]``
crashed its check that the branch is not behind ``main``. Text a task did not write goes through
``rich.markup.escape()`` before it is put into a markup string.

The scan cannot tell outside text from a task's own values, so it looks for the forms #900 found:
a command's ``stdout`` or ``stderr``, the variable an ``except ... as`` clause binds, and the names
the tasks give commit subjects, PR titles and ``git status`` output. Paths, label names and the
user's own flags are outside its scope (#900).
"""

from __future__ import annotations

import ast
import textwrap
from pathlib import Path

import pytest

DOIT_DIR = Path(__file__).resolve().parents[2] / "tools" / "doit"

# Rich parses the text arguments of these as markup: Console.print, .log and .rule, Panel and
# Panel.fit.
_MARKUP_CALLS = frozenset({"print", "log", "rule", "Panel", "fit"})
# Keyword arguments that Panel also renders as markup.
_MARKUP_KEYWORDS = frozenset({"title", "subtitle"})
# The names the tasks give text they did not write.
_OUTSIDE_TEXT = frozenset(
    {"stdout", "stderr", "line", "commit", "status", "pr_title", "merge_subject"}
)


def _name(func: ast.expr) -> str:
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def _parses_markup(call: ast.Call) -> bool:
    """Whether Rich parses ``call``'s text arguments as markup."""
    if isinstance(call.func, ast.Name) and call.func.id == "print":
        return False  # the builtin print
    if _name(call.func) not in _MARKUP_CALLS:
        return False
    return not any(
        keyword.arg == "markup"
        and isinstance(keyword.value, ast.Constant)
        and keyword.value.value is False
        for keyword in call.keywords
    )


def _carries_outside_text(node: ast.AST, caught: frozenset[str]) -> bool:
    """Whether ``node`` puts outside text into the markup without ``escape()``."""
    if isinstance(node, ast.Call) and _name(node.func) == "escape":
        return False
    if isinstance(node, ast.Name) and (node.id in _OUTSIDE_TEXT or node.id in caught):
        return True
    if isinstance(node, ast.Attribute) and node.attr in _OUTSIDE_TEXT:
        return True
    return any(_carries_outside_text(child, caught) for child in ast.iter_child_nodes(node))


def unescaped_outside_text(source: str) -> list[tuple[int, str]]:
    """Return ``(line, argument)`` for each markup argument that carries outside text unescaped."""
    tree = ast.parse(source)
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    found: list[tuple[int, str]] = []
    for call in ast.walk(tree):
        if not isinstance(call, ast.Call) or not _parses_markup(call):
            continue
        caught: set[str] = set()
        scope = parents.get(call)
        while scope is not None:
            if isinstance(scope, ast.ExceptHandler) and scope.name:
                caught.add(scope.name)
            scope = parents.get(scope)
        texts = [*call.args, *(k.value for k in call.keywords if k.arg in _MARKUP_KEYWORDS)]
        found.extend(
            (text.lineno, ast.unparse(text))
            for text in texts
            if _carries_outside_text(text, frozenset(caught))
        )
    return found


def test_no_markup_carries_outside_text_unescaped() -> None:
    paths = sorted(DOIT_DIR.glob("*.py"))
    assert paths, f"no task modules under {DOIT_DIR}"

    found = [
        f"tools/doit/{path.name}:{line}: {text}"
        for path in paths
        for line, text in unescaped_outside_text(path.read_text(encoding="utf-8"))
    ]

    assert not found, (
        "Pass text a task did not write through rich.markup.escape() before it goes into "
        "a markup string (#900):\n" + "\n".join(found)
    )


@pytest.mark.parametrize(
    "source",
    [
        """
        try:
            read()
        except OSError as e:
            console.print(f"[red]Error reading file: {e}[/red]")
        """,
        'console.print(f"[red]Stderr: {e.stderr}[/red]")',
        """
        stderr = (result.stderr or "").strip()
        console.print(f"[red]{stderr}[/red]")
        """,
        """
        for line in log.splitlines():
            console.print(f"  {line}")
        """,
        'console.print(f"  [red]{commit}[/red]")',
        "console.print(status)",
        'console.print(Panel.fit(f"Commit: {merge_subject}"))',
        'console.print(Panel("body", title=f"{pr_title}"))',
        'console.print("[red]" + stderr + "[/red]")',
        'console.print(f"[red]{escape(result.stdout)} {result.stderr}[/red]")',
    ],
)
def test_the_scan_flags_unescaped_outside_text(source: str) -> None:
    assert unescaped_outside_text(textwrap.dedent(source))


@pytest.mark.parametrize(
    "source",
    [
        """
        try:
            read()
        except OSError as e:
            console.print(f"[red]Error reading file: {escape(str(e))}[/red]")
        """,
        'console.print(f"[red]Stderr: {escape(e.stderr)}[/red]")',
        'console.print(f"[red]git worktree add failed: {escape((e.stderr or "").strip())}[/red]")',
        "console.print(escape(status))",
        'console.print(stderr, style="red", markup=False)',
        'print(f"[OK] {stderr}")',
        'console.print(f"[green]Created {path} on {branch}.[/green]")',
        """
        for e in entries:
            console.print(f"[dim]{e}[/dim]")
        """,
        'console.print(f"[dim]{len(lines)} lines[/dim]")',
    ],
)
def test_the_scan_passes_escaped_or_own_text(source: str) -> None:
    assert unescaped_outside_text(textwrap.dedent(source)) == []

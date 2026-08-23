"""Every filesystem path `configure.py` names must exist in the template.

`configure.py` runs once, against a freshly cloned template, to turn it into a
real project. When it gates behaviour on a path that does not exist, the gate
short-circuits: the branch never runs, nothing is printed, and no error is
raised.

That is how the Dependabot option became a silent no-op (#685) — it was gated
on `.github/dependabot.yml.example`, a file that had never existed. Users were
asked whether to enable Dependabot, shown their answer in the configuration
summary, and the answer was then discarded.

The failure is invisible by construction, so it needs a structural check rather
than a behavioural one.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# Scripts that operate on the template tree by naming paths directly.
SCANNED = (
    REPO_ROOT / "tools" / "pyproject_template" / "configure.py",
    REPO_ROOT / "tools" / "pyproject_template" / "cleanup.py",
)

# Paths a script legitimately names before creating them, or that exist only at
# runtime. Add here — with a reason — rather than deleting the assertion.
# Empty today: every path both scripts name already ships with the template.
ALLOWED_MISSING: frozenset[str] = frozenset()


def _path_literals(script: Path) -> list[tuple[int, str]]:
    """Return `(lineno, value)` for every `Path("literal")` in *script*.

    Parsed rather than grepped so that string concatenation, f-strings and
    variables are ignored — only unambiguous literals are asserted on.
    """
    tree = ast.parse(script.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "Path"
            and len(node.args) == 1
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            found.append((node.lineno, node.args[0].value))
    return found


@pytest.mark.parametrize("script", SCANNED, ids=lambda p: p.name)
def test_path_literals_exist_in_the_template(script: Path) -> None:
    """A named path that is absent makes its branch unreachable and silent."""
    missing = [
        f"{script.name}:{lineno} -> {value}"
        for lineno, value in _path_literals(script)
        if value not in ALLOWED_MISSING and not (REPO_ROOT / value).exists()
    ]
    assert not missing, (
        "paths named by the script do not exist in the template:\n  "
        + "\n  ".join(missing)
        + "\n\nA gate on a missing path silently does nothing. Fix the path, or "
        "add it to ALLOWED_MISSING with a reason."
    )


def test_the_scanner_actually_finds_literals() -> None:
    """Guard against the AST walk silently matching nothing.

    Without this, a refactor of the scan could make the assertion above pass
    vacuously — the same way the paths it protects failed silently.
    """
    total = sum(len(_path_literals(script)) for script in SCANNED)
    assert total >= 10, f"expected the configure/cleanup scripts to name paths, found {total}"

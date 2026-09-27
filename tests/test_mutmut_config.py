"""Tests for ``[tool.mutmut]`` in ``pyproject.toml`` (#839).

mutmut 3 renamed two of the keys the template used and reads no ``runner`` at
all. ``paths_to_mutate`` became ``source_paths`` and ``tests_dir`` became
``pytest_add_cli_args_test_selection``; the old names print a deprecation
warning on every mutmut command. ``runner`` fails silently: its pytest flags
never reached pytest, and the ones still wanted now live in
``pytest_add_cli_args``.

These are structural asserts on the parsed TOML. They do not run mutmut.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"

# Keys mutmut 3 deprecates, mapped to the keys that replace them.
REPLACED = {
    "paths_to_mutate": "source_paths",
    "tests_dir": "pytest_add_cli_args_test_selection",
}
# Keys mutmut 3 does not read at all, so nothing warns about them.
UNREAD = {"runner"}


def _mutmut_config() -> dict[str, Any]:
    """Return the ``[tool.mutmut]`` table."""
    with PYPROJECT.open("rb") as f:
        config: dict[str, Any] = tomllib.load(f)["tool"]["mutmut"]
    return config


def test_no_deprecated_or_unread_keys() -> None:
    stale = sorted(set(_mutmut_config()) & (set(REPLACED) | UNREAD))

    assert not stale, f"mutmut 3 deprecates or ignores {stale}"


def test_uses_the_replacement_keys() -> None:
    """Without them mutmut guesses what to mutate and which tests to run."""
    missing = sorted(set(REPLACED.values()) - set(_mutmut_config()))

    assert not missing

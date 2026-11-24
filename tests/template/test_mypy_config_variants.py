"""Guard: the shipped tooling type-checks under variant downstream mypy configs.

A project spawned from this template owns its ``[tool.mypy]`` table and may
change it. Tooling that ships (``tools/doit/``, ``tools/hooks/``) must stay
type-clean under those changes, not only under the template's own config.
Two regressions slipped through that way:

* #1299: ``disallow_subclassing_any = False`` made a ``# type: ignore[misc]``
  unused, which ``warn_unused_ignores`` then reported.
* #1301: ``follow_untyped_imports = True`` on the ``doit.*`` override made
  ``super().execute()`` typed, so ``warn_return_any`` fired.

Each variant in ``VARIANTS`` reads the live ``[tool.mypy]`` table, changes exactly
one setting, and runs mypy over the same paths ``doit type_check`` uses.

This test is template-owned (ADR-9017): it reads the template's own pyproject
and is shed on configuration.

To add a variant, append a ``MypyVariant`` to ``VARIANTS`` whose ``reason``
starts with the issue number, using ``_set`` for a top-level key or
``_set_override`` for a key on one ``[[tool.mypy.overrides]]`` entry.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
import tomllib
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from tools.doit.quality import task_type_check

REPO_ROOT = Path(__file__).resolve().parents[2]

MypyConfig = dict[str, Any]

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason=(
        "doit type_check runs only in the Linux lint job, and mypy evaluates "
        "sys.platform branches for the host with warn_unreachable on"
    ),
)


@dataclass(frozen=True)
class MypyVariant:
    """One downstream mypy configuration: the template's, with one change."""

    name: str
    apply: Callable[[MypyConfig], None]
    reason: str


def _set(key: str, value: object) -> Callable[[MypyConfig], None]:
    """Return a change that sets top-level ``[tool.mypy]`` *key* to *value*."""

    def apply(cfg: MypyConfig) -> None:
        cfg[key] = value

    return apply


def _set_override(module: str, key: str, value: object) -> Callable[[MypyConfig], None]:
    """Return a change that sets *key* on the single override for *module*."""

    def apply(cfg: MypyConfig) -> None:
        matches = [o for o in cfg.get("overrides", []) if o.get("module") == module]
        if len(matches) != 1:
            raise LookupError(f"expected one override for {module!r}, found {len(matches)}")
        matches[0][key] = value

    return apply


VARIANTS: list[MypyVariant] = [
    MypyVariant(
        name="subclassing-any-off",
        apply=_set("disallow_subclassing_any", False),
        reason="#1299: the CmdAction subclass ignore must stay valid when the check is off",
    ),
    MypyVariant(
        name="doit-follow-untyped-imports",
        apply=_set_override("doit.*", "follow_untyped_imports", True),
        reason="#1301: doit tooling must stay type-clean when doit's untyped imports are followed",
    ),
]


def _base_mypy_config() -> MypyConfig:
    """Return the live ``[tool.mypy]`` table from the repo's pyproject.toml."""
    with (REPO_ROOT / "pyproject.toml").open("rb") as fh:
        table: MypyConfig = tomllib.load(fh)["tool"]["mypy"]
    return table


def _build_variant(variant: MypyVariant) -> MypyConfig:
    """Return a deep copy of the base config with *variant* applied."""
    cfg = deepcopy(_base_mypy_config())
    variant.apply(cfg)
    return cfg


def _toml_value(value: object) -> str:
    """Serialize a bool, int, str or list of str as a TOML value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return "[" + ", ".join(json.dumps(v) for v in value) + "]"
    raise TypeError(f"unsupported TOML value type: {type(value).__name__}")


def _to_mypy_toml(cfg: MypyConfig) -> str:
    """Write *cfg* as a pyproject-style file holding only ``[tool.mypy]``."""
    lines = ["[tool.mypy]"]
    lines += [f"{k} = {_toml_value(v)}" for k, v in cfg.items() if k != "overrides"]
    for override in cfg.get("overrides", []):
        lines += ["", "[[tool.mypy.overrides]]"]
        lines += [f"{k} = {_toml_value(v)}" for k, v in override.items()]
    return "\n".join(lines) + "\n"


def _type_check_paths(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Return the paths ``doit type_check`` passes to mypy."""
    monkeypatch.chdir(REPO_ROOT)
    action = task_type_check()["actions"][0]
    assert isinstance(action, str)
    tokens = shlex.split(action)
    assert tokens[:3] == ["uv", "run", "mypy"]
    return tokens[3:]


def _flatten(cfg: MypyConfig) -> dict[str, object]:
    """Flatten *cfg* to leaf paths, keying overrides by their ``module``."""
    flat: dict[str, object] = {}
    for key, value in cfg.items():
        if key != "overrides":
            flat[key] = value
    for override in cfg.get("overrides", []):
        module = json.dumps(override["module"])
        for key, value in override.items():
            flat[f"overrides[{module}].{key}"] = value
    return flat


_IDS = [v.name for v in VARIANTS]


@pytest.mark.parametrize("variant", VARIANTS, ids=_IDS)
def test_variant_type_checks_clean(
    variant: MypyVariant, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = _type_check_paths(monkeypatch)
    config = tmp_path / "pyproject.toml"
    config.write_text(_to_mypy_toml(_build_variant(variant)), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--config-file",
            str(config),
            "--cache-dir",
            str(tmp_path / "mypy-cache"),
            *paths,
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )

    output = f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    assert "Unrecognized option" not in result.stderr, f"{variant.reason}\n{output}"
    assert result.returncode == 0, f"{variant.reason}\n{output}"
    assert "Success: no issues found" in result.stdout, f"{variant.reason}\n{output}"


@pytest.mark.parametrize("variant", VARIANTS, ids=_IDS)
def test_variant_differs_from_base_in_exactly_one_setting(variant: MypyVariant) -> None:
    base = _flatten(_base_mypy_config())
    changed = _flatten(_build_variant(variant))
    differing = {k for k in base.keys() | changed.keys() if base.get(k) != changed.get(k)}
    assert len(differing) == 1, f"{variant.name} changed {sorted(differing)}"


@pytest.mark.parametrize("variant", VARIANTS, ids=_IDS)
def test_variant_serialization_round_trips(variant: MypyVariant) -> None:
    cfg = _build_variant(variant)
    assert tomllib.loads(_to_mypy_toml(cfg))["tool"]["mypy"] == cfg


def test_base_config_round_trips() -> None:
    cfg = _base_mypy_config()
    assert tomllib.loads(_to_mypy_toml(cfg))["tool"]["mypy"] == cfg


def test_serializer_rejects_unsupported_types() -> None:
    with pytest.raises(TypeError):
        _toml_value(1.5)
    with pytest.raises(TypeError):
        _toml_value({"a": 1})


def test_set_override_requires_exactly_one_match() -> None:
    cfg = deepcopy(_base_mypy_config())
    with pytest.raises(LookupError):
        _set_override("no.such.module", "ignore_missing_imports", True)(cfg)


def test_type_check_paths_match_task(monkeypatch: pytest.MonkeyPatch) -> None:
    paths = _type_check_paths(monkeypatch)
    assert {"src/", "tools/", "tests/"} <= set(paths)

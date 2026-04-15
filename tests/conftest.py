"""Shared pytest configuration and Hypothesis profiles."""

import os
from collections.abc import Callable, Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from hypothesis import HealthCheck, settings

# CI profile: fewer examples, relaxed deadline for slow CI runners
settings.register_profile(
    "ci",
    max_examples=50,
    deadline=500,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.differing_executors],
)

# Default profile: more thorough exploration for local development
settings.register_profile(
    "default",
    max_examples=200,
    suppress_health_check=[HealthCheck.differing_executors],
)

settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))


Spec = dict[str, Any] | BaseException | Callable[[list[str]], MagicMock | BaseException]


@pytest.fixture
def mock_subprocess() -> Iterator[MagicMock]:
    """Patch ``tools.doit.github.subprocess.run`` with a prefix-dispatch mock.

    Register command-prefix -> spec mappings via ``.register({...})``. Spec is one
    of: a dict of MagicMock kwargs (``stdout``/``stderr``/``returncode``,
    default ``returncode=0``), a ``BaseException`` instance to raise, or a
    callable ``(cmd) -> MagicMock | BaseException`` for prefix collisions where
    behavior depends on a later argument. Unknown prefixes raise ``AssertionError``.
    """
    with patch("tools.doit.github.subprocess.run") as mock_run:
        dispatch: dict[tuple[str, ...], Spec] = {}

        def side_effect(cmd: list[str], *_a: object, **_kw: object) -> MagicMock:
            for prefix, spec in dispatch.items():
                if tuple(cmd[: len(prefix)]) == prefix:
                    if isinstance(spec, BaseException):
                        raise spec
                    if callable(spec):
                        result = spec(cmd)
                        if isinstance(result, BaseException):
                            raise result
                        return result
                    return MagicMock(
                        returncode=spec.get("returncode", 0),
                        stdout=spec.get("stdout", ""),
                        stderr=spec.get("stderr", ""),
                    )
            raise AssertionError(f"unexpected cmd: {cmd}")

        mock_run.side_effect = side_effect
        mock_run.register = dispatch.update
        yield mock_run

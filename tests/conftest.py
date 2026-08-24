"""Shared pytest configuration and Hypothesis profiles."""

import os
from collections.abc import Callable, Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from hypothesis import HealthCheck, settings

# CI profile: fewer examples, no deadline.
#
# `deadline=None` rather than a larger number (#736). These are property tests
# over string validation — they assert what a value *is*, never how long it took,
# and `benchmark.yml` covers timing separately. A wall-clock budget on a shared
# runner only adds a way for them to fail for reasons unrelated to the property.
#
# Windows runners were seen taking 1506ms on an example's first call and 0.01ms
# on the retry: interpreter and import warmup, not the code under test. The
# earlier 200ms -> 500ms relaxation did not survive that, and any finite
# replacement is a threshold a bad runner can still cross.
#
# Note that `suppress_health_check=[HealthCheck.too_slow]` does *not* cover this.
# The health check and the per-example deadline are separate mechanisms, which is
# why the profile looked protected against slow runners while still failing on
# them.
settings.register_profile(
    "ci",
    max_examples=50,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.differing_executors],
)

# Default profile: more thorough exploration for local development.
# Keeps Hypothesis's default deadline — a developer machine is not a shared
# runner, so a genuinely pathological slowdown is worth surfacing locally.
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


# ---------------------------------------------------------------------------
# Hermetic PATH (#710)
# ---------------------------------------------------------------------------

# Unit tests were reaching the real `gh` binary 18 times per run — 14 of them
# `gh api user`, which is a *network* call. That makes results depend on whether
# the developer happens to be authenticated: #689 spent time diagnosing a 0.54pp
# coverage difference that turned out to be exactly this.
#
# Every test now runs with a stub `gh` ahead of the real one. It answers the
# handful of commands the code under test invokes with fixed output matching an
# unauthenticated CI runner, and exits 127 with a loud marker for anything else —
# so a new unmocked call fails visibly rather than depending on the machine.
#
# Tests needing specific `gh` behaviour prepend their own stub ahead of this one
# (see tests/test_statusline_gh_user.py::_stub_gh), which still works. Tests of
# Python code that shells out should mock `subprocess.run` instead; this fixture
# is the backstop for what slips through, and for shell scripts under test, which
# cannot be mocked at the Python level.
_GH_STUB = """#!/bin/sh
case "$1 $2" in
  "auth status")
    # No token markers, so `_check_token_permissions` takes its else branch.
    # Both branches are pinned explicitly in test_setup_repo.py.
    echo "Logged in to github.com as test-user" >&2
    exit 0
    ;;
  "api user")
    # Unauthenticated: the statusline must render no user segment.
    echo "gh: authentication required" >&2
    exit 1
    ;;
esac
case "$1" in
  --version) echo "gh version 0.0.0-stub (hermetic test stub)" ; exit 0 ;;
esac
echo "HERMETIC-STUB: unmocked 'gh $*' reached the real PATH (#710)" >&2
exit 127
"""


@pytest.fixture(autouse=True)
def _hermetic_path(
    tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Put a stub `gh` ahead of the real one for every test."""
    bin_dir = tmp_path_factory.mktemp("hermetic-bin")
    stub = bin_dir / "gh"
    stub.write_text(_GH_STUB, encoding="utf-8")
    stub.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")

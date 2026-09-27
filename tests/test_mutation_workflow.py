"""Tests for the mutation-testing workflow (#873).

The workflow ran ``uv run mutmut run > ... || true``. mutmut 3 exits non-zero
only when it cannot test the mutants at all, never for surviving mutants, so
``|| true`` masked exactly the failure worth seeing: for months the weekly run
stopped while collecting stats, checked no mutant, and reported success.

The step's script is run for real here, with ``uv`` replaced by a stub that
exits with the status under test. The assertions are on what the step does,
not on how its script is spelled.
"""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / ".github" / "workflows" / "mutation.yml"

# GitHub runs a Linux step's script as `bash -e {0}` unless the step names a
# shell. The Windows runner's `bash` resolves to wsl.exe with no distribution
# installed (see tests/test_statusline_gh_user.py), and this workflow runs on
# ubuntu-latest only.
needs_bash = pytest.mark.skipif(
    sys.platform == "win32",
    reason="the step runs under bash on Linux; the Windows runner has no usable bash",
)


def _job() -> dict[str, Any]:
    """Return the workflow's only job."""
    # yaml.safe_load returns Any; bind to an annotated local for warn_return_any.
    data: dict[str, Any] = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    job: dict[str, Any] = data["jobs"]["mutate"]
    return job


def _steps() -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = _job()["steps"]
    return steps


def _mutmut_run_index() -> int:
    """Return the index of the one step that runs ``mutmut run``."""
    indexes = [i for i, step in enumerate(_steps()) if "mutmut run" in step.get("run", "")]
    assert len(indexes) == 1, f"expected one step running `mutmut run`, found {len(indexes)}"
    return indexes[0]


def _run_step(tmp_path: Path, *, mutmut_status: int) -> subprocess.CompletedProcess[str]:
    """Run the mutmut step's script with a ``uv`` stub that exits *mutmut_status*."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    uv = bin_dir / "uv"
    uv.write_text(
        f"#!/bin/bash\necho 'stub mutmut output'\nexit {mutmut_status}\n", encoding="utf-8"
    )
    uv.chmod(uv.stat().st_mode | stat.S_IEXEC)
    script = tmp_path / "step.sh"
    script.write_text(_steps()[_mutmut_run_index()]["run"], encoding="utf-8")
    return subprocess.run(
        ["bash", "-e", str(script)],
        cwd=tmp_path,
        env={"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
        capture_output=True,
        text=True,
        timeout=10,
    )


@needs_bash
def test_a_mutmut_failure_fails_the_step(tmp_path: Path) -> None:
    """mutmut exits 1 when its stats run fails, and the step must fail with it."""
    result = _run_step(tmp_path, mutmut_status=1)

    assert result.returncode != 0
    assert "::error::" in result.stdout


@needs_bash
def test_a_completed_run_passes_the_step(tmp_path: Path) -> None:
    """Surviving mutants leave mutmut's exit status at 0; the run stays informational."""
    result = _run_step(tmp_path, mutmut_status=0)

    assert result.returncode == 0, result.stdout + result.stderr
    log = tmp_path / "tmp" / "mutmut-run-raw.log"
    assert "stub mutmut output" in log.read_text(encoding="utf-8")


def test_nothing_turns_a_failed_step_green() -> None:
    """``continue-on-error`` would undo the step's failure at the job level."""
    assert not _steps()[_mutmut_run_index()].get("continue-on-error")
    assert not _job().get("continue-on-error")


def test_results_are_shown_and_uploaded_after_a_failure() -> None:
    """The steps after the run print its log and upload its results even when it fails."""
    later = _steps()[_mutmut_run_index() + 1 :]

    assert later, "no step prints or uploads the mutation results"
    assert all("always()" in str(step.get("if", "")) for step in later)


def test_property_tests_run_without_a_deadline() -> None:
    """The ``ci`` profile in tests/conftest.py has no deadline, as ci.yml relies on."""
    assert _job().get("env", {}).get("HYPOTHESIS_PROFILE") == "ci"

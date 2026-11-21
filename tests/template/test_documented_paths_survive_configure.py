"""The documented-paths allowlist must still work after configuration rewrites it (#1269).

`configure` rewrites `package_name` in every test file (`update_test_files`). An
allowlist entry naming `src/package_name/...` was rewritten into one for the new
package while the skills that ship still name `package_name`, so a configured
project failed `test_documented_paths_exist`. This applies the real rewrite to a
copy of the test and asserts the five paths the issue reported stay allowed.

Template-owned: it imports `tools.pyproject_template`, which configuration sheds
(ADR-9017).
"""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import pytest

from tools.pyproject_template.utils import update_test_files

REPO_ROOT = Path(__file__).resolve().parents[2]

REPORTED_PATHS = (
    "src/package_name/__init__.py",
    "src/package_name/core.py",
    "tests/template/test_utils.py",
    "tests/template/test_utils_properties.py",
    "tests/template/test_check_template_updates.py",
)


@pytest.mark.parametrize("package_name", ["mytool", "other_pkg"])
def test_allowlist_survives_the_configure_rewrite(tmp_path: Path, package_name: str) -> None:
    """After the configure rewrite, the reported paths are still exempt."""
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    copy = tests_dir / "test_documented_paths.py"
    shutil.copy(REPO_ROOT / "tests" / "test_documented_paths.py", copy)

    update_test_files(tests_dir, package_name)

    spec = importlib.util.spec_from_file_location("configured_documented_paths", copy)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    not_allowed = [raw for raw in REPORTED_PATHS if not module._is_allowed(raw)]
    assert not_allowed == []

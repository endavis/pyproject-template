"""Guards that a spawned project keeps the tests for the code it actually runs.

Three code paths turn the template into a real project, and all three used to
delete ``tests/template/`` wholesale:

- ``configure.py`` (the "Use this template" route)
- ``setup_repo.py`` (the ``bootstrap.py`` new-project wizard)
- ``cleanup --setup`` (an existing project adopting the template)

Only the third consulted ``TEMPLATE_OWNED_TEST_FILES``. The other two also removed
the suites covering ``tools/doit/`` and ``tools/hooks/`` — code that ships to the
spawned project and that the coverage gate in ``pyproject.toml`` measures. The
result was a generated project that failed its own first CI run at 33.98% against
a ``fail_under`` of 54 (#731).

These tests pin the shed set to one list and assert that the shipped tooling keeps
test coverage on the far side of it.
"""

from __future__ import annotations

import ast
from pathlib import Path

from tools.pyproject_template.cleanup import CleanupMode, get_files_to_delete
from tools.pyproject_template.utils import (
    TEMPLATE_OWNED_TEST_FILES,
    remove_template_owned_tests,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_TESTS = REPO_ROOT / "tests" / "template"

# Tooling directories that ship to and run in the spawned project. Unlike
# tools/pyproject_template/, this code is not shed by any cleanup mode, so
# deleting its tests leaves the project running untested code — and short of
# the coverage gate it also inherits.
SHIPPED_TOOLING = ("tools/doit", "tools/hooks")

# The two wizard entry points that turn a clone into a real project. Both must
# shed through the shared helper rather than naming the directory themselves.
WIZARDS = (
    REPO_ROOT / "tools" / "pyproject_template" / "configure.py",
    REPO_ROOT / "tools" / "pyproject_template" / "setup_repo.py",
)


def _template_test_filenames() -> list[str]:
    """Every ``test_*.py`` filename currently in ``tests/template/``."""
    return sorted(p.name for p in TEMPLATE_TESTS.glob("test_*.py"))


def _populate(root: Path) -> Path:
    """Build a throwaway ``tests/template/`` mirroring the real filenames."""
    tests_dir = root / "tests" / "template"
    tests_dir.mkdir(parents=True)
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")
    for name in _template_test_filenames():
        (tests_dir / name).write_text("# stub\n", encoding="utf-8")
    return tests_dir


def _uncovered_shipped_tooling(surviving: set[str]) -> list[str]:
    """Return the shipped tooling dirs no *surviving* test file references.

    Reads the real test bodies, so it reflects what the suite actually covers
    rather than a filename convention.
    """
    bodies = [(TEMPLATE_TESTS / name).read_text(encoding="utf-8") for name in sorted(surviving)]
    uncovered = []
    for shipped in SHIPPED_TOOLING:
        dotted = shipped.replace("/", ".")
        if not any(shipped in body or dotted in body for body in bodies):
            uncovered.append(shipped)
    return uncovered


def _path_literals(script: Path) -> set[str]:
    """Return every string passed to a ``Path(...)`` call in *script*."""
    tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    literals: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "Path"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            literals.add(node.args[0].value)
    return literals


def test_wizards_shed_through_the_shared_helper() -> None:
    """Neither wizard may name ``tests/template/`` and remove it wholesale again.

    The parity test below checks the helper. This checks that the wizards still
    *use* it — the pre-#731 defect was two hand-rolled ``shutil.rmtree`` calls
    sitting next to a list neither consulted.
    """
    for wizard in WIZARDS:
        source = wizard.read_text(encoding="utf-8")
        assert "remove_template_owned_tests(" in source, (
            f"{wizard.name} must shed template tests via remove_template_owned_tests()"
        )
        offenders = {literal for literal in _path_literals(wizard) if "tests/template" in literal}
        assert not offenders, (
            f"{wizard.name} names {offenders} directly. Shedding belongs in "
            "remove_template_owned_tests() so all paths stay in agreement (#731)."
        )


def test_wizard_and_cleanup_shed_the_same_tests(tmp_path: Path) -> None:
    """configure.py/setup_repo.py must shed exactly what ``cleanup --setup`` sheds.

    ADR-9017 calls ``TEMPLATE_OWNED_TEST_FILES`` the single authoritative list.
    This asserts that claim behaviourally rather than trusting the constant.
    """
    _populate(tmp_path)

    # Must be collected before the shed runs — get_files_to_delete only reports
    # files that still exist.
    cleanup_sheds = {
        path.relative_to(tmp_path).as_posix()
        for path in get_files_to_delete(CleanupMode.SETUP_ONLY, tmp_path)
        if path.as_posix().find("tests/template/") != -1
    }
    wizard_sheds = {
        path.relative_to(tmp_path).as_posix() for path in remove_template_owned_tests(tmp_path)
    }

    assert wizard_sheds == cleanup_sheds, (
        "The wizard and cleanup paths disagree about what is template-owned. "
        "Both must derive from TEMPLATE_OWNED_TEST_FILES (ADR-9017)."
    )


def test_shipped_tooling_keeps_its_tests(tmp_path: Path) -> None:
    """After shedding, surviving tests must still cover tools/doit/ and tools/hooks/."""
    _populate(tmp_path)
    shed = {path.name for path in remove_template_owned_tests(tmp_path)}
    surviving = {name for name in _template_test_filenames() if name not in shed}

    uncovered = _uncovered_shipped_tooling(surviving)
    assert not uncovered, (
        f"No surviving test covers {uncovered}. That code ships to the spawned "
        "project and is measured by the coverage gate in pyproject.toml; shedding "
        "its tests puts the generated project below fail_under on its first CI run."
    )


def test_retention_check_detects_the_regression() -> None:
    """The check above must fail when the tooling tests are gone.

    Without this, ``test_shipped_tooling_keeps_its_tests`` could pass because the
    scanner finds nothing to complain about rather than because coverage survives.
    Feeding it the pre-#731 shape — everything removed — must flag both dirs.
    """
    assert _uncovered_shipped_tooling(set()) == list(SHIPPED_TOOLING)


def test_template_only_tests_are_shed(tmp_path: Path) -> None:
    """Tests whose target does not survive configuration must still be removed."""
    _populate(tmp_path)
    shed = {path.name for path in remove_template_owned_tests(tmp_path)}

    for name in ("test_configure_paths.py", "test_readme_split.py", "test_cleanup.py"):
        assert name in shed, f"{name} targets a template-only artifact and must be shed"


def test_package_dir_survives_when_tests_remain(tmp_path: Path) -> None:
    """``tests/template/`` stays when downstream-owned tests are left in it."""
    tests_dir = _populate(tmp_path)
    remove_template_owned_tests(tmp_path)

    assert tests_dir.is_dir(), "tests/template/ must survive — it still holds tooling tests"
    assert (tests_dir / "test_doit_quality.py").is_file()


def test_package_dir_removed_once_empty(tmp_path: Path) -> None:
    """``tests/template/`` is dropped when shedding leaves nothing behind."""
    tests_dir = tmp_path / "tests" / "template"
    tests_dir.mkdir(parents=True)
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")
    for rel in TEMPLATE_OWNED_TEST_FILES:
        (tmp_path / rel).write_text("# stub\n", encoding="utf-8")

    remove_template_owned_tests(tmp_path)

    assert not tests_dir.exists(), "an emptied tests/template/ should not be left behind"
    assert (tmp_path / "tests").is_dir(), "the parent tests/ directory must remain"


def test_shed_is_a_noop_when_already_clean(tmp_path: Path) -> None:
    """Running against a project with no tests/template/ must not raise."""
    (tmp_path / "tests").mkdir()

    assert remove_template_owned_tests(tmp_path) == []
    assert (tmp_path / "tests").is_dir()

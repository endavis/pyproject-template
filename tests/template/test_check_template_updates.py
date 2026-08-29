"""Tests for sync-exclude support in ``check_template_updates``."""

from __future__ import annotations

import importlib
import types
from pathlib import Path
from unittest import mock

import pytest

from tools.pyproject_template import check_template_updates as ctu
from tools.pyproject_template.check_template_updates import (
    _emit_coupling_warnings,
    compare_files,
    load_sync_excludes,
)
from tools.pyproject_template.utils import TEMPLATE_OWNED_TEST_FILES


def _make_template(
    template_root: Path, files: dict[str, str], *, base: str = "pyproject-template-main"
) -> Path:
    """Create a fake extracted template tree under ``template_root/<base>``.

    Mirrors the directory shape produced by ``download_and_extract_archive``.
    """
    root = template_root / base
    root.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root


def _write_exclude_file(project_root: Path, patterns: list[str]) -> None:
    settings_dir = project_root / ".config" / "pyproject_template"
    settings_dir.mkdir(parents=True, exist_ok=True)
    body = "exclude = [\n" + "".join(f'    "{p}",\n' for p in patterns) + "]\n"
    (settings_dir / "sync-exclude.toml").write_text(body, encoding="utf-8")


class TestLoadSyncExcludes:
    """Direct tests of the ``load_sync_excludes`` loader."""

    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        assert load_sync_excludes(tmp_path) == []

    def test_valid_file_returns_patterns(self, tmp_path: Path) -> None:
        _write_exclude_file(tmp_path, ["examples/api/**", "src/foo.py"])
        assert load_sync_excludes(tmp_path) == ["examples/api/**", "src/foo.py"]

    def test_missing_exclude_key_returns_empty(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / ".config" / "pyproject_template"
        settings_dir.mkdir(parents=True)
        (settings_dir / "sync-exclude.toml").write_text("# no exclude key\n", encoding="utf-8")
        assert load_sync_excludes(tmp_path) == []

    def test_malformed_toml_returns_empty(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / ".config" / "pyproject_template"
        settings_dir.mkdir(parents=True)
        (settings_dir / "sync-exclude.toml").write_text("not = valid toml [[\n", encoding="utf-8")
        assert load_sync_excludes(tmp_path) == []

    def test_non_list_exclude_returns_empty(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / ".config" / "pyproject_template"
        settings_dir.mkdir(parents=True)
        (settings_dir / "sync-exclude.toml").write_text('exclude = "oops"\n', encoding="utf-8")
        assert load_sync_excludes(tmp_path) == []

    def test_non_string_entries_dropped(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / ".config" / "pyproject_template"
        settings_dir.mkdir(parents=True)
        (settings_dir / "sync-exclude.toml").write_text(
            'exclude = ["keep.py", 42, "also.py"]\n', encoding="utf-8"
        )
        assert load_sync_excludes(tmp_path) == ["keep.py", "also.py"]


class TestCompareFilesWithExcludes:
    """``compare_files`` returns ``(different_files, excluded_files)``."""

    @pytest.fixture
    def project(self, tmp_path: Path) -> Path:
        project = tmp_path / "project"
        project.mkdir()
        return project

    @pytest.fixture
    def template(self, tmp_path: Path) -> Path:
        return tmp_path / "template"

    def test_no_exclude_file_is_noop(self, project: Path, template: Path) -> None:
        template_root = _make_template(
            template,
            {"docs/index.md": "upstream", "src/main.py": "upstream"},
        )
        # Project has neither file; both should appear in different_files.
        diff, excluded = compare_files(project, template_root)
        assert excluded == []
        assert sorted(p.as_posix() for p in diff) == ["docs/index.md", "src/main.py"]

    def test_glob_match_lands_in_excluded(self, project: Path, template: Path) -> None:
        template_root = _make_template(
            template,
            {"examples/api/foo.py": "x", "examples/api/sub/bar.py": "y", "src/main.py": "z"},
        )
        _write_exclude_file(project, ["examples/api/**"])
        diff, excluded = compare_files(project, template_root)
        assert sorted(p.as_posix() for p in diff) == ["src/main.py"]
        assert sorted(p.as_posix() for p in excluded) == [
            "examples/api/foo.py",
            "examples/api/sub/bar.py",
        ]

    def test_exact_path_match(self, project: Path, template: Path) -> None:
        template_root = _make_template(
            template,
            {"src/package_name/core.py": "x", "src/package_name/cli.py": "y"},
        )
        _write_exclude_file(project, ["src/package_name/core.py"])
        diff, excluded = compare_files(project, template_root)
        assert [p.as_posix() for p in diff] == ["src/package_name/cli.py"]
        assert [p.as_posix() for p in excluded] == ["src/package_name/core.py"]

    def test_unmatched_file_still_flagged(self, project: Path, template: Path) -> None:
        template_root = _make_template(
            template,
            {"README.md": "x", "examples/api/foo.py": "y"},
        )
        _write_exclude_file(project, ["examples/api/**"])
        diff, excluded = compare_files(project, template_root)
        assert [p.as_posix() for p in diff] == ["README.md"]
        assert [p.as_posix() for p in excluded] == ["examples/api/foo.py"]

    def test_hardcoded_skip_takes_precedence(self, project: Path, template: Path) -> None:
        # __pycache__ is in the hardcoded skip set; user excludes should not
        # override that, and __pycache__ should not appear in either bucket.
        template_root = _make_template(
            template,
            {"__pycache__/cached.pyc": "x", "src/main.py": "y"},
        )
        _write_exclude_file(project, ["__pycache__/**"])
        diff, excluded = compare_files(project, template_root)
        assert [p.as_posix() for p in diff] == ["src/main.py"]
        assert excluded == []

    def test_matching_file_not_reported(self, project: Path, template: Path) -> None:
        # If the project file matches the template, neither bucket should contain it
        # — even if it would otherwise match an exclude pattern.
        template_root = _make_template(template, {"src/main.py": "same"})
        (project / "src").mkdir()
        (project / "src" / "main.py").write_text("same", encoding="utf-8")
        _write_exclude_file(project, ["src/main.py"])
        diff, excluded = compare_files(project, template_root)
        assert diff == []
        assert excluded == []

    def test_excludes_param_overrides_file(self, project: Path, template: Path) -> None:
        # Passing ``excludes=`` explicitly bypasses the on-disk loader, which is
        # how callers (and tests) inject patterns without a TOML file on disk.
        template_root = _make_template(template, {"a.py": "x", "b.py": "y"})
        diff, excluded = compare_files(project, template_root, excludes=["a.py"])
        assert [p.as_posix() for p in diff] == ["b.py"]
        assert [p.as_posix() for p in excluded] == ["a.py"]


class TestCompareFilesExcludesTemplateOwnedTests:
    """``compare_files`` silently skips template-owned tooling test files."""

    @pytest.fixture
    def project(self, tmp_path: Path) -> Path:
        p = tmp_path / "project"
        p.mkdir()
        return p

    @pytest.fixture
    def template(self, tmp_path: Path) -> Path:
        return tmp_path / "template"

    def test_template_owned_test_not_in_different_files(
        self, project: Path, template: Path
    ) -> None:
        """A template-owned test that differs must NOT appear in different_files."""
        # Use the first entry in the constant as the representative case.
        owned = TEMPLATE_OWNED_TEST_FILES[0]  # e.g. tests/template/test_pyproject_template_main.py
        template_root = _make_template(
            template,
            {
                owned: "upstream-content",
                "README.md": "upstream-readme",
            },
        )
        # Project has different content for the owned test and different README.
        (project / "README.md").write_text("project-readme", encoding="utf-8")
        diff, _excluded = compare_files(project, template_root)
        diff_strs = [p.as_posix() for p in diff]
        assert owned not in diff_strs, f"Template-owned test must be excluded: {owned}"
        assert "README.md" in diff_strs, "Non-owned drifted file must still appear"

    def test_all_template_owned_tests_silently_skipped(self, project: Path, template: Path) -> None:
        """Every entry in TEMPLATE_OWNED_TEST_FILES is suppressed, regardless of content."""
        files: dict[str, str] = dict.fromkeys(TEMPLATE_OWNED_TEST_FILES, "upstream")
        files["tools/pyproject_template/utils.py"] = "upstream-tooling"
        template_root = _make_template(template, files)
        diff, _excluded = compare_files(project, template_root)
        diff_strs = [p.as_posix() for p in diff]
        for owned in TEMPLATE_OWNED_TEST_FILES:
            assert owned not in diff_strs, f"Owned test must be skipped: {owned}"
        # The non-owned tooling file still surfaces.
        assert "tools/pyproject_template/utils.py" in diff_strs

    def test_non_owned_test_still_surfaces(self, project: Path, template: Path) -> None:
        """Tests NOT in TEMPLATE_OWNED_TEST_FILES surface normally as drift."""
        template_root = _make_template(
            template,
            {"tests/template/test_templates.py": "upstream"},
        )
        diff, _excluded = compare_files(project, template_root)
        assert "tests/template/test_templates.py" in [p.as_posix() for p in diff]


class TestEmitCouplingWarnings:
    """Tests for ``_emit_coupling_warnings``."""

    def test_warns_when_drifted_test_imports_tooling_and_tooling_drifted(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Warning emitted when a non-owned test imports tooling AND tooling has drifted."""
        project = tmp_path / "project"
        project.mkdir()
        # Create a local non-template-owned test that imports tooling.
        test_dir = project / "tests" / "template"
        test_dir.mkdir(parents=True)
        drifted_test = test_dir / "test_custom.py"
        drifted_test.write_text(
            "from tools.pyproject_template.utils import validate_package_name\n",
            encoding="utf-8",
        )
        different_files = [
            Path("tests/template/test_custom.py"),
            Path("tools/pyproject_template/utils.py"),  # tooling has also drifted
        ]
        _emit_coupling_warnings(different_files, project)
        captured = capsys.readouterr()
        assert "bootstrap --sync" in captured.out
        assert "tests/template/test_custom.py" in captured.out

    def test_silent_when_no_tooling_drift(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """No warning when the drifted test imports tooling but tooling itself has NOT drifted."""
        project = tmp_path / "project"
        project.mkdir()
        test_dir = project / "tests" / "template"
        test_dir.mkdir(parents=True)
        drifted_test = test_dir / "test_custom.py"
        drifted_test.write_text(
            "from tools.pyproject_template.utils import validate_package_name\n",
            encoding="utf-8",
        )
        # No tooling file in different_files.
        different_files = [Path("tests/template/test_custom.py")]
        _emit_coupling_warnings(different_files, project)
        captured = capsys.readouterr()
        assert "bootstrap" not in captured.out

    def test_silent_when_drifted_test_does_not_import_tooling(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """No warning when the drifted test does not import tooling (even if tooling drifted)."""
        project = tmp_path / "project"
        project.mkdir()
        test_dir = project / "tests" / "template"
        test_dir.mkdir(parents=True)
        drifted_test = test_dir / "test_custom.py"
        drifted_test.write_text(
            "from package_name.core import greet\n",
            encoding="utf-8",
        )
        different_files = [
            Path("tests/template/test_custom.py"),
            Path("tools/pyproject_template/utils.py"),
        ]
        _emit_coupling_warnings(different_files, project)
        captured = capsys.readouterr()
        assert "bootstrap" not in captured.out

    def test_silent_when_no_drifted_tests(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """No warning when different_files contains only non-test files."""
        project = tmp_path / "project"
        project.mkdir()
        different_files = [
            Path("tools/pyproject_template/utils.py"),
            Path("README.md"),
        ]
        _emit_coupling_warnings(different_files, project)
        captured = capsys.readouterr()
        assert "bootstrap" not in captured.out


class TestTemplateVersionFlag:
    """`--template-version` must be reachable, and must reach the download (#779).

    The flag existed in `check_template_updates.parse_args` and `manage.py` never
    forwarded it: `action_check_updates` called `run_check_updates` with
    `skip_changelog` and `keep_template` hardcoded and nothing else. The direct
    invocation is refused by a guard, so the argument was dead code reachable
    only from Python while three documents advertised it.

    These tests pin both halves: the flag parses, and the value it carries
    changes the archive URL rather than being accepted and dropped.
    """

    @staticmethod
    def _manage() -> types.ModuleType:
        return importlib.import_module("tools.pyproject_template.manage")

    def test_flag_parses_before_the_subcommand(self) -> None:
        args = self._manage().parse_args(["--template-version", "v2.2.0", "check"])
        assert args.template_version == "v2.2.0"
        assert args.command == "check"

    def test_flag_parses_after_the_subcommand(self) -> None:
        """The order people actually write, and the one manage.md documented."""
        args = self._manage().parse_args(["check", "--template-version", "v2.2.0"])
        assert args.template_version == "v2.2.0"

    def test_show_excluded_parses_in_both_positions(self) -> None:
        """The same fix; `check --show-excluded` was documented and rejected."""
        assert self._manage().parse_args(["check", "--show-excluded"]).show_excluded is True
        assert self._manage().parse_args(["--show-excluded", "check"]).show_excluded is True

    def test_defaults_survive_the_two_parsers(self) -> None:
        """Neither parser's default may overwrite the other's value.

        Both the global parser and the `check` subparser declare these options.
        Without `SUPPRESS` the subparser parses second and writes its own default
        over a value the global parser set, so `--show-excluded check` would
        silently lose the flag.
        """
        args = self._manage().parse_args(["check"])
        assert args.template_version is None
        assert args.show_excluded is False

    def test_the_version_reaches_the_download(self) -> None:
        """Accepting the flag and dropping it would pass every test above."""
        manage = self._manage()
        seen: dict[str, object] = {}

        def _capture(**kwargs: object) -> int:
            seen.update(kwargs)
            return 0

        with (
            mock.patch.object(manage, "run_check_updates", _capture),
            mock.patch.object(manage, "get_template_latest_commit", lambda: None),
        ):
            manage.action_check_updates(mock.MagicMock(), dry_run=True, template_version="v2.2.0")
        assert seen.get("template_version") == "v2.2.0"


class TestRefResolution:
    """A template version is a commit, and every ref kind resolves to one (#781).

    `bootstrap.py` pins a commit SHA; the drift checker used to fetch a release
    tag and fall through to the moving `main` branch when no release existed --
    which is always, since this template has cut none. Two halves of one sync
    disagreeing about what a version is.

    These cover the resolution and the URL it produces. The gap they close is
    real: the first version of this change left a stale `version` reference in
    `run_check_updates` and every existing test passed, because they mock that
    function. It was caught by running the tool.
    """

    def test_a_sha_is_used_as_is(self) -> None:
        """No API call for something already a commit."""
        sha = "0a64c7e7c916a9bb0b4041f20acce8653e01acfa"
        with mock.patch.object(ctu.urllib.request, "urlopen") as opener:
            assert ctu.resolve_template_ref(sha) == sha
        opener.assert_not_called()

    @pytest.mark.parametrize("ref", ["main", "v0.0.0", "some-branch"])
    def test_a_tag_or_branch_resolves_to_a_sha(self, ref: str) -> None:
        sha = "1" * 40
        response = mock.MagicMock()
        response.read.return_value = f"{sha}\n".encode()
        response.__enter__.return_value = response
        with mock.patch.object(ctu.urllib.request, "urlopen", return_value=response):
            assert ctu.resolve_template_ref(ref) == sha

    def test_an_unresolvable_ref_warns_and_passes_through(self) -> None:
        """Offline or rate-limited must not stop a drift check outright."""
        with mock.patch.object(ctu.urllib.request, "urlopen", side_effect=OSError("offline")):
            assert ctu.resolve_template_ref("main") == "main"

    def test_a_non_sha_response_is_not_trusted(self) -> None:
        """A proxy returning HTML must not become the archive path."""
        response = mock.MagicMock()
        response.read.return_value = b"<html>rate limited</html>"
        response.__enter__.return_value = response
        with mock.patch.object(ctu.urllib.request, "urlopen", return_value=response):
            assert ctu.resolve_template_ref("main") == "main"

    def test_the_archive_url_names_the_resolved_commit(self, tmp_path: Path) -> None:
        """One URL shape for tag, branch and SHA -- the resolved commit."""
        sha = "2" * 40
        seen: dict[str, str] = {}

        def _capture(url: str, target: Path) -> Path:
            seen["url"] = url
            return target

        with (
            mock.patch.object(ctu, "resolve_template_ref", return_value=sha),
            mock.patch.object(ctu, "download_and_extract_archive", _capture),
        ):
            ctu.download_template(tmp_path, "v0.0.0")

        assert seen["url"].endswith(f"/archive/{sha}.zip"), seen["url"]
        assert "refs/tags" not in seen["url"], "the release-tag URL shape is gone"
        assert "refs/heads" not in seen["url"], "the moving-branch URL shape is gone"

    def test_the_default_ref_is_main(self, tmp_path: Path) -> None:
        """Stated, rather than reached by failing a releases/latest lookup."""
        assert ctu.DEFAULT_TEMPLATE_REF == "main"
        seen: dict[str, str] = {}
        with (
            mock.patch.object(ctu, "resolve_template_ref", lambda ref: seen.setdefault("ref", ref)),
            mock.patch.object(ctu, "download_and_extract_archive", lambda url, target: target),
        ):
            ctu.download_template(tmp_path, None)
        assert seen["ref"] == "main"

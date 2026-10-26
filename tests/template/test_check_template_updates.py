"""Tests for sync-exclude support in ``check_template_updates``."""

from __future__ import annotations

import importlib
import sys
import types
from collections.abc import Iterator
from email.message import Message
from pathlib import Path
from unittest import mock

import pytest

from tools.pyproject_template import check_template_updates as ctu
from tools.pyproject_template.check_template_updates import (
    TEMPLATE_SYNC_SKILL_REL_PATHS,
    _emit_coupling_warnings,
    _warn_stale_template_sync_skill,
    compare_files,
    load_sync_excludes,
    stale_template_sync_skill_copies,
)
from tools.pyproject_template.utils import TEMPLATE_OWNED_TEST_FILES

REPO_ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = REPO_ROOT / "tests"

# tests/doc_scan.py duplicates load_sync_excludes rather than importing it --
# see its module docstring and ADR-9026. `tests/` is already on sys.path by
# the time pytest collects this file (the same "prepend" mechanism that lets
# `tests/test_markdown_links.py` do `from agent_roster import ...`), so this
# just makes the dependency explicit rather than relying on collection order.
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from doc_scan import load_sync_excludes as duplicated_load_sync_excludes  # noqa: E402


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


def _write_skill_copies(root: Path, agents_content: str, claude_content: str) -> None:
    """Write both ``template-sync`` ``SKILL.md`` copies under ``root``."""
    for rel, content in zip(
        TEMPLATE_SYNC_SKILL_REL_PATHS, (agents_content, claude_content), strict=True
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class TestStaleTemplateSyncSkillCopies:
    """Tests for ``stale_template_sync_skill_copies``."""

    @pytest.fixture
    def project(self, tmp_path: Path) -> Path:
        p = tmp_path / "project"
        p.mkdir()
        return p

    @pytest.fixture
    def template(self, tmp_path: Path) -> Path:
        t = tmp_path / "template"
        t.mkdir()
        return t

    def test_both_copies_match_returns_empty(self, project: Path, template: Path) -> None:
        _write_skill_copies(project, "same-agents", "same-claude")
        _write_skill_copies(template, "same-agents", "same-claude")
        assert stale_template_sync_skill_copies(project, template) == []

    def test_claude_copy_differs(self, project: Path, template: Path) -> None:
        _write_skill_copies(project, "same-agents", "old-claude")
        _write_skill_copies(template, "same-agents", "new-claude")
        stale = stale_template_sync_skill_copies(project, template)
        assert stale == [Path(".claude/skills/template-sync/SKILL.md")]

    def test_agents_copy_differs(self, project: Path, template: Path) -> None:
        _write_skill_copies(project, "old-agents", "same-claude")
        _write_skill_copies(template, "new-agents", "same-claude")
        stale = stale_template_sync_skill_copies(project, template)
        assert stale == [Path(".agents/skills/template-sync/SKILL.md")]

    def test_a_copy_missing_is_stale(self, project: Path, template: Path) -> None:
        # Project has only the .claude/ copy; .agents/ is missing entirely.
        claude_rel = TEMPLATE_SYNC_SKILL_REL_PATHS[1]
        claude_path = project / claude_rel
        claude_path.parent.mkdir(parents=True)
        claude_path.write_text("same-claude", encoding="utf-8")
        _write_skill_copies(template, "new-agents", "same-claude")
        stale = stale_template_sync_skill_copies(project, template)
        assert stale == [Path(TEMPLATE_SYNC_SKILL_REL_PATHS[0])]

    def test_both_copies_stale(self, project: Path, template: Path) -> None:
        _write_skill_copies(project, "old-agents", "old-claude")
        _write_skill_copies(template, "new-agents", "new-claude")
        stale = stale_template_sync_skill_copies(project, template)
        assert stale == sorted(Path(p) for p in TEMPLATE_SYNC_SKILL_REL_PATHS)

    def test_template_lacking_path_is_not_reported_missing(
        self, project: Path, template: Path
    ) -> None:
        """An older template ref that predates #806 must not false-positive as missing."""
        # Project has neither copy; template has neither either.
        assert stale_template_sync_skill_copies(project, template) == []


class TestWarnStaleTemplateSyncSkill:
    """Tests for ``_warn_stale_template_sync_skill``."""

    def test_silent_when_nothing_stale(self, capsys: pytest.CaptureFixture[str]) -> None:
        _warn_stale_template_sync_skill([], Path("."))
        assert capsys.readouterr().out == ""

    def test_names_the_upstream_url_at_the_compared_ref(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        stale = [Path(TEMPLATE_SYNC_SKILL_REL_PATHS[0])]
        _warn_stale_template_sync_skill(stale, tmp_path, "v1.2.3")
        out = capsys.readouterr().out.replace("\n", "")
        expected = ctu.TEMPLATE_SYNC_SKILL_URL.format(repo=ctu.TEMPLATE_REPO, ref="v1.2.3")
        assert expected in out

    def test_lists_each_stale_path_with_status(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        present, missing = (Path(p) for p in TEMPLATE_SYNC_SKILL_REL_PATHS)
        (tmp_path / present).parent.mkdir(parents=True)
        (tmp_path / present).write_text("stale", encoding="utf-8")
        # `missing` is never written -- it does not exist under the project root,
        # which is not the cwd, so the status must come from project_root.
        _warn_stale_template_sync_skill([missing, present], tmp_path)
        out = capsys.readouterr().out
        assert f"{missing} (missing)" in out
        assert f"{present} (differs)" in out


class TestWarnStaleTemplateSyncSkillInRunCheckUpdates:
    """`run_check_updates` must surface the warning, in order, without writing."""

    @pytest.fixture
    def project(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        p = tmp_path / "project"
        p.mkdir()
        monkeypatch.chdir(p)
        return p

    @staticmethod
    def _fake_template(project: Path) -> Path:
        # `run_check_updates` computes `template_dir.relative_to(project_root)`
        # for display, so the fake extraction must live under the project root
        # the way the real `tmp/extracted/pyproject-template-<sha>/` does.
        t = project / "tmp" / "extracted" / "pyproject-template-fake"
        t.mkdir(parents=True)
        return t

    def test_warning_prints_before_comparing_header(
        self, project: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        _write_skill_copies(project, "old-agents", "old-claude")
        template_root = self._fake_template(project)
        _write_skill_copies(template_root, "new-agents", "new-claude")

        with mock.patch.object(ctu, "download_template", lambda _target, _ref: template_root):
            assert ctu.run_check_updates(skip_changelog=True, keep_template=True) == 0

        out = capsys.readouterr().out
        warn_idx = out.index("template-sync skill is older")
        header_idx = out.index("Comparing your project to template")
        assert warn_idx < header_idx

    def test_silent_when_skill_copies_match(
        self, project: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        _write_skill_copies(project, "same-agents", "same-claude")
        template_root = self._fake_template(project)
        _write_skill_copies(template_root, "same-agents", "same-claude")

        with mock.patch.object(ctu, "download_template", lambda _target, _ref: template_root):
            assert ctu.run_check_updates(skip_changelog=True, keep_template=True) == 0

        out = capsys.readouterr().out
        assert "template-sync skill is older" not in out

    def test_run_check_updates_never_writes_the_skill_files(self, project: Path) -> None:
        """The check only warns; the project's skill files must be byte-identical after."""
        _write_skill_copies(project, "old-agents", "old-claude")
        template_root = self._fake_template(project)
        _write_skill_copies(template_root, "new-agents", "new-claude")

        before = {rel: (project / rel).read_bytes() for rel in TEMPLATE_SYNC_SKILL_REL_PATHS}

        with mock.patch.object(ctu, "download_template", lambda _target, _ref: template_root):
            ctu.run_check_updates(skip_changelog=True, keep_template=True)

        after = {rel: (project / rel).read_bytes() for rel in TEMPLATE_SYNC_SKILL_REL_PATHS}
        assert before == after


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
            mock.patch.object(manage, "get_template_commit", lambda _ref: None),
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

    @pytest.fixture(autouse=True)
    def _no_token(self) -> Iterator[None]:
        """Keep the token lookup off the developer's `gh` login (#1026)."""
        with mock.patch.object(ctu, "github_token", return_value=None):
            yield

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

    def test_an_unresolvable_ref_stops_the_check(self) -> None:
        """A moving-ref extract cannot be recorded, so the check must not proceed (#1026)."""
        with (
            mock.patch.object(ctu.urllib.request, "urlopen", side_effect=OSError("offline")),
            pytest.raises(ctu.TemplateRefError, match="offline"),
        ):
            ctu.resolve_template_ref("main")

    def test_a_rate_limit_names_the_cause_and_the_token_remedy(self) -> None:
        """The failure that hid behind a scrolled-past warning (#1026)."""
        error = ctu.urllib.error.HTTPError(
            "https://api.github.com", 403, "rate limit exceeded", Message(), None
        )
        with (
            mock.patch.object(ctu.urllib.request, "urlopen", side_effect=error),
            pytest.raises(ctu.TemplateRefError) as raised,
        ):
            ctu.resolve_template_ref("main")
        message = str(raised.value)
        assert "rate limited" in message
        assert "GITHUB_TOKEN=$(gh auth token)" in message

    def test_the_lookup_sends_a_token_when_one_is_available(self) -> None:
        """`gh auth token` stands in for an unset GITHUB_TOKEN via `github_token`."""
        response = mock.MagicMock()
        response.read.return_value = f"{'4' * 40}\n".encode()
        response.__enter__.return_value = response
        with (
            mock.patch.object(ctu, "github_token", return_value="tok"),
            mock.patch.object(ctu.urllib.request, "urlopen", return_value=response) as opener,
        ):
            ctu.resolve_template_ref("main")
        request = opener.call_args.args[0]
        assert request.get_header("Authorization") == "token tok"

    def test_a_non_sha_response_is_not_trusted(self) -> None:
        """A proxy returning HTML must not become the archive path."""
        response = mock.MagicMock()
        response.read.return_value = b"<html>rate limited</html>"
        response.__enter__.return_value = response
        with (
            mock.patch.object(ctu.urllib.request, "urlopen", return_value=response),
            pytest.raises(ctu.TemplateRefError, match="unexpected response"),
        ):
            ctu.resolve_template_ref("main")

    def test_an_unpinned_ref_leaves_the_reviewed_extract_alone(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The reviewed extract `sync` needs must survive a failed check (#1026)."""
        reviewed = tmp_path / "tmp" / "extracted" / f"pyproject-template-{'5' * 40}"
        reviewed.mkdir(parents=True)
        (reviewed / ".template_commit").write_text(f"{'5' * 40}\n2026-10-26\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        with (
            mock.patch.object(
                ctu, "resolve_template_ref", side_effect=ctu.TemplateRefError("rate limited")
            ),
            mock.patch.object(ctu, "download_and_extract_archive") as download,
        ):
            assert ctu.run_check_updates(skip_changelog=True, keep_template=True) == 1

        download.assert_not_called()
        assert (reviewed / ".template_commit").exists()

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


class TestGuardedScriptsAreNotDocumentedDirectly:
    """Docs must not teach a command the script refuses to run (#778).

    Three scripts in the management suite print "This script should not be run
    directly" and exit. The migration and upgrade docs taught direct invocation
    of all three -- 14 commands that could not work -- while
    `ai-sync-checklist.md` stated the correct rule in the same breath.

    The guarded set is *derived* from the refusal string rather than listed here,
    so a script that gains a guard later is covered without anyone remembering to
    add it.
    """

    REFUSAL = "This script should not be run directly"
    SUITE = REPO_ROOT / "tools" / "pyproject_template"
    DOC_DIRS = (REPO_ROOT / "docs", REPO_ROOT / ".github")

    @classmethod
    def _guarded_scripts(cls) -> list[str]:
        return sorted(
            path.name
            for path in cls.SUITE.glob("*.py")
            if cls.REFUSAL in path.read_text(encoding="utf-8")
        )

    def test_the_guarded_set_is_discoverable(self) -> None:
        """If the refusal wording changes, this test must fail rather than pass blind."""
        guarded = self._guarded_scripts()
        assert guarded, (
            f"no script in {self.SUITE.name} contains {self.REFUSAL!r}. Either the guards were "
            "removed -- in which case delete this class -- or the wording changed and this "
            "check is now looking at nothing."
        )

    def test_no_doc_invokes_a_guarded_script_directly(self) -> None:
        """`manage.py` is the entry point; a documented command must work."""
        guarded = self._guarded_scripts()
        offenders: list[str] = []
        for directory in self.DOC_DIRS:
            if not directory.is_dir():
                continue
            for doc in sorted(directory.rglob("*.md")):
                if doc.name == "TABLE_OF_CONTENTS.md":
                    continue  # generated
                for number, line in enumerate(
                    doc.read_text(encoding="utf-8", errors="replace").splitlines(), 1
                ):
                    for script in guarded:
                        # A path reference is fine; an invocation is not.
                        invoked = "python" in line or line.lstrip().startswith("$")
                        if (
                            f"pyproject_template/{script}" in line
                            and "manage.py" not in line
                            and invoked
                        ):
                            offenders.append(
                                f"{doc.relative_to(REPO_ROOT)}:{number} {line.strip()[:70]}"
                            )
        assert not offenders, (
            "documentation invokes scripts that refuse to run directly:\n  "
            + "\n  ".join(offenders)
            + "\nUse the `manage.py` equivalent -- `manage.py check`, `configure`, `repo`."
        )


class TestCheckToSyncHandoff:
    """`check` must leave behind what `sync` goes looking for (#805).

    Each half was covered on its own and both passed, while the pair was broken
    for every project: `check` wrote `.template_commit` into a hardcoded
    `tmp/extracted/pyproject-template-main`, a directory the download stopped
    producing when #779 switched it to `/archive/<sha>.zip`. The write was
    guarded by `if template_dir.exists()`, so it silently did nothing, and
    `sync` aborted with "No reviewed template found" immediately after a
    successful check.

    These tests drive the two functions against a real extracted-directory shape
    rather than mocking the path, because the path was the bug.
    """

    @staticmethod
    def _manage() -> types.ModuleType:
        return importlib.import_module("tools.pyproject_template.manage")

    @staticmethod
    def _extract(project_root: Path, sha: str) -> Path:
        """Create the archive root `download_and_extract_archive` would produce."""
        root = project_root / "tmp" / "extracted" / f"pyproject-template-{sha}"
        root.mkdir(parents=True)
        return root

    def test_check_records_the_reviewed_commit_where_sync_reads_it(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The end-to-end contract: check writes it, sync finds it."""
        manage = self._manage()
        sha = "3683148e5da66ae682ced50873eace83a6388db5"
        extracted = self._extract(tmp_path, sha)
        monkeypatch.chdir(tmp_path)

        manager = mock.MagicMock()
        manager.template_state.commit = None

        with (
            mock.patch.object(manage, "run_check_updates", lambda **_: 0),
            mock.patch.object(manage, "get_template_commit", lambda _ref: (sha, "2026-09-06")),
        ):
            manage.action_check_updates(manager, dry_run=False)

        commit_file = extracted / ".template_commit"
        assert commit_file.exists(), "check left nothing for sync to read"
        assert commit_file.read_text(encoding="utf-8").splitlines()[:2] == [sha, "2026-09-06"]

    def test_check_records_the_pinned_ref_not_the_tip_of_main(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """`--template-version` exists for staged upgrades; recording `main` defeats it.

        The commit is taken from the archive root's name, so it is whatever was
        actually downloaded and compared -- not whatever `main` points at now.
        """
        manage = self._manage()
        pinned = "b036360e28dfff5328f6c816fbe1074b153b5c94"
        extracted = self._extract(tmp_path, pinned)
        monkeypatch.chdir(tmp_path)

        manager = mock.MagicMock()
        manager.template_state.commit = None

        # If anything reached for `main`, this would supply a different SHA.
        with (
            mock.patch.object(manage, "run_check_updates", lambda **_: 0),
            mock.patch.object(manage, "get_template_commit", lambda ref: (ref, "2026-09-05")),
            mock.patch.object(
                manage, "get_template_latest_commit", lambda: ("f" * 40, "2026-09-06")
            ),
        ):
            manage.action_check_updates(manager, dry_run=False, template_version=pinned)

        recorded = (extracted / ".template_commit").read_text(encoding="utf-8").splitlines()
        assert recorded[0] == pinned

    def test_a_failed_date_lookup_still_records_a_usable_sync_point(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The SHA comes off disk, so only the date depends on the API.

        The file `action_mark_synced` reads is strictly two lines; a blank
        second line is rejected as malformed. A date lookup that fails must not
        cost the sync point it is only decorating.
        """
        manage = self._manage()
        sha = "3683148e5da66ae682ced50873eace83a6388db5"
        extracted = self._extract(tmp_path, sha)
        monkeypatch.chdir(tmp_path)

        manager = mock.MagicMock()
        manager.template_state.commit = None

        with (
            mock.patch.object(manage, "run_check_updates", lambda **_: 0),
            mock.patch.object(manage, "get_template_commit", lambda _ref: None),
        ):
            manage.action_check_updates(manager, dry_run=False)

        recorded = (extracted / ".template_commit").read_text(encoding="utf-8")
        assert recorded.strip().split("\n") == [sha, "unknown"]

        # And the half that consumes it accepts the result.
        assert manage.action_mark_synced(manager, dry_run=True, yes=True) == 0

    def test_no_commit_is_recorded_when_the_ref_never_resolved(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Offline, the archive root is named for the moving ref, which is not a sync point."""
        manage = self._manage()
        extracted = self._extract(tmp_path, "main")
        monkeypatch.chdir(tmp_path)

        manager = mock.MagicMock()
        manager.template_state.commit = None

        with (
            mock.patch.object(manage, "run_check_updates", lambda **_: 0),
            mock.patch.object(manage, "get_template_commit", lambda _ref: None),
        ):
            manage.action_check_updates(manager, dry_run=False)

        assert not (extracted / ".template_commit").exists()

    def test_sync_reads_the_commit_check_recorded(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The half that used to abort: sync must locate the archive by glob."""
        manage = self._manage()
        sha = "3683148e5da66ae682ced50873eace83a6388db5"
        extracted = self._extract(tmp_path, sha)
        (extracted / ".template_commit").write_text(f"{sha}\n2026-09-06\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        manager = mock.MagicMock()
        manager.template_state.commit = None

        # dry_run stops before the settings write and the git commands.
        assert manage.action_mark_synced(manager, dry_run=True, yes=True) == 0

    def test_a_failed_check_records_nothing(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A non-zero check must not write a sync point into a stale extract (#1026)."""
        manage = self._manage()
        extracted = self._extract(tmp_path, "6" * 40)
        monkeypatch.chdir(tmp_path)

        manager = mock.MagicMock()
        manager.template_state.commit = None

        with mock.patch.object(manage, "run_check_updates", lambda **_: 1):
            assert manage.action_check_updates(manager, dry_run=False) == 1

        assert not (extracted / ".template_commit").exists()

    def test_sync_names_the_cause_of_a_moving_ref_extract(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """The bare `No reviewed template found` never pointed at the rate limit (#1026)."""
        manage = self._manage()
        self._extract(tmp_path, "main")
        monkeypatch.chdir(tmp_path)

        assert manage.action_mark_synced(mock.MagicMock(), dry_run=True, yes=True) == 1

        output = capsys.readouterr()
        combined = output.out + output.err
        assert "moving ref" in combined
        assert "GITHUB_TOKEN" in combined

    def test_sync_still_refuses_when_no_check_has_run(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The error path must survive the fix: nothing extracted is still an error."""
        manage = self._manage()
        monkeypatch.chdir(tmp_path)

        assert manage.action_mark_synced(mock.MagicMock(), dry_run=True, yes=True) == 1


class TestDocScanParity:
    """`tests/doc_scan.py` duplicates `load_sync_excludes` rather than importing it (ADR-9026).

    `tests/doc_scan.py` cannot import `tools.pyproject_template.check_template_updates`:
    that module is removed from a downstream project when it sheds the template
    suite (ADR-9017), and `tests/doc_scan.py` ships to every downstream project
    because the doc/link tests that use it do. These tests keep the duplicate
    honest by running both copies against the same fixtures and asserting they
    agree -- this file is template-owned (`TEMPLATE_OWNED_TEST_FILES`), so it is
    never shed and can import both sides safely.
    """

    @pytest.mark.parametrize(
        "patterns",
        [
            [],
            ["examples/api/**"],
            ["src/package_name/core.py", "tests/test_core.py"],
        ],
    )
    def test_valid_file_agrees(self, tmp_path: Path, patterns: list[str]) -> None:
        _write_exclude_file(tmp_path, patterns)
        assert duplicated_load_sync_excludes(tmp_path) == load_sync_excludes(tmp_path)

    def test_missing_file_agrees(self, tmp_path: Path) -> None:
        assert duplicated_load_sync_excludes(tmp_path) == load_sync_excludes(tmp_path) == []

    def test_malformed_toml_agrees(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / ".config" / "pyproject_template"
        settings_dir.mkdir(parents=True)
        (settings_dir / "sync-exclude.toml").write_text("not = valid toml [[\n", encoding="utf-8")
        assert duplicated_load_sync_excludes(tmp_path) == load_sync_excludes(tmp_path) == []

    def test_non_list_exclude_agrees(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / ".config" / "pyproject_template"
        settings_dir.mkdir(parents=True)
        (settings_dir / "sync-exclude.toml").write_text('exclude = "oops"\n', encoding="utf-8")
        assert duplicated_load_sync_excludes(tmp_path) == load_sync_excludes(tmp_path) == []

    def test_non_string_entries_agrees(self, tmp_path: Path) -> None:
        settings_dir = tmp_path / ".config" / "pyproject_template"
        settings_dir.mkdir(parents=True)
        (settings_dir / "sync-exclude.toml").write_text(
            'exclude = ["keep.py", 42, "also.py"]\n', encoding="utf-8"
        )
        assert duplicated_load_sync_excludes(tmp_path) == load_sync_excludes(tmp_path)

    def test_the_real_repo_file_agrees(self) -> None:
        """Against this repository's own (absent) sync-exclude.toml, not a fixture."""
        assert duplicated_load_sync_excludes(REPO_ROOT) == load_sync_excludes(REPO_ROOT)

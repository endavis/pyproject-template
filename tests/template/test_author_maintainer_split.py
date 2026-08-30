"""Author and maintainer are different people once a project changes hands.

PEP 621 separates `[project].authors` from `[project].maintainers`. The template
read only the first and wrote it everywhere, which is right for a greenfield
project and wrong for an adopted or forked one (#787).

Only one substitution actually changes meaning: the security-report address in
`.github/SECURITY.md`. The LICENSE copyright line, `mkdocs.yml`'s `site_author`
and `[project].authors` all want the author and are left alone — these tests pin
that division so a future edit cannot quietly move one of them.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = REPO_ROOT / "tools" / "pyproject_template"
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from tools.pyproject_template.utils import (  # noqa: E402
    get_first_author,
    get_first_maintainer,
)

ADOPTED = {
    "project": {
        "authors": [{"name": "Original Author", "email": "author@example.org"}],
        "maintainers": [{"name": "Current Maintainer", "email": "maintainer@example.org"}],
    }
}

GREENFIELD = {
    "project": {
        "authors": [{"name": "Solo Dev", "email": "solo@example.org"}],
    }
}


class TestExtraction:
    """`get_first_maintainer` beside the author it must not collapse into."""

    def test_reads_the_maintainer_when_the_project_names_one(self) -> None:
        assert get_first_maintainer(ADOPTED) == ("Current Maintainer", "maintainer@example.org")
        assert get_first_author(ADOPTED) == ("Original Author", "author@example.org")

    def test_returns_empty_when_no_maintainer_is_named(self) -> None:
        """Empty, not the author.

        The fallback belongs to the caller: leaving it empty here keeps "names
        no maintainer" distinguishable from "the maintainer is the author",
        which is what lets `configure.py` prompt sensibly.
        """
        assert get_first_maintainer(GREENFIELD) == ("", "")

    def test_handles_a_project_table_that_is_missing_entirely(self) -> None:
        assert get_first_maintainer({}) == ("", "")
        assert get_first_maintainer({"project": {}}) == ("", "")


class TestDefaults:
    """`load_defaults` resolves the fallback so callers never see an empty pair."""

    def _defaults(self, tmp_path: Path, body: str) -> dict[str, str]:
        from tools.pyproject_template.configure import load_defaults

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(body, encoding="utf-8")
        return load_defaults(pyproject)

    def test_greenfield_maintainer_is_the_author(self, tmp_path: Path) -> None:
        """The behaviour every existing project had before the split."""
        defaults = self._defaults(
            tmp_path,
            '[project]\nname = "thing"\ndescription = "d"\n'
            'authors = [{name = "Solo Dev", email = "solo@example.org"}]\n',
        )
        assert defaults["maintainer_name"] == defaults["author_name"] == "Solo Dev"
        assert defaults["maintainer_email"] == defaults["author_email"] == "solo@example.org"

    def test_adopted_project_keeps_the_two_apart(self, tmp_path: Path) -> None:
        defaults = self._defaults(
            tmp_path,
            '[project]\nname = "thing"\ndescription = "d"\n'
            'authors = [{name = "Original Author", email = "author@example.org"}]\n'
            'maintainers = [{name = "Current Maintainer", email = "maintainer@example.org"}]\n',
        )
        assert defaults["author_name"] == "Original Author"
        assert defaults["maintainer_name"] == "Current Maintainer"
        assert defaults["maintainer_email"] == "maintainer@example.org"


class TestSubstitutionTargets:
    """Which files each identity reaches. The point of the whole change."""

    def test_the_security_contact_is_a_substituted_placeholder(self) -> None:
        """Both spawn paths must replace it; neither may ship the example address.

        `setup_repo.py` had `.github/SECURITY.md` in FILES_TO_UPDATE but no
        mapping for the address inside it, so every bootstrapped project told
        reporters to email `security@example.com` (#787).
        """
        configure = (PACKAGE_DIR / "configure.py").read_text(encoding="utf-8")
        setup_repo = (PACKAGE_DIR / "setup_repo.py").read_text(encoding="utf-8")

        for source, name in ((configure, "configure.py"), (setup_repo, "setup_repo.py")):
            assert '"security@example.com":' in source, (
                f"{name} does not substitute the security-report address; a project "
                "configured through it ships an address nobody owns"
            )
            assert '"[INSERT CONTACT EMAIL]":' in source, (
                f"{name} does not substitute the code-of-conduct contact address"
            )

    def test_configure_routes_the_security_contact_to_the_maintainer(self) -> None:
        """configure.py runs against projects that may have changed hands."""
        source = (PACKAGE_DIR / "configure.py").read_text(encoding="utf-8")
        for placeholder in ('"security@example.com":', '"[INSERT CONTACT EMAIL]":'):
            line = next(ln for ln in source.splitlines() if placeholder in ln)
            assert "maintainer_email" in line, (
                f"{placeholder} maps to {line.strip()!r}; vulnerability reports would "
                "reach the original author of an adopted project"
            )

    @pytest.mark.parametrize(
        ("placeholder", "identity", "reason"),
        [
            ('"Your Name":', "author_name", "the LICENSE copyright line belongs to the author"),
            ('"your.email@example.com":', "author_email", "package metadata names the author"),
        ],
    )
    def test_author_owned_substitutions_stay_with_the_author(
        self, placeholder: str, identity: str, reason: str
    ) -> None:
        """Not everything moves.

        `LICENSE`'s copyright, `mkdocs.yml`'s `site_author` and
        `[project].authors` are all fed by these two placeholders and all
        correctly name the author. Routing them to the maintainer would be a
        regression dressed up as consistency.
        """
        source = (PACKAGE_DIR / "configure.py").read_text(encoding="utf-8")
        line = next(ln for ln in source.splitlines() if placeholder in ln)
        assert identity in line, f"{placeholder} must stay on {identity}: {reason}"


def test_the_template_itself_still_names_only_an_author() -> None:
    """The template is greenfield; adding `maintainers` here would be noise.

    Stated as a test because the fallback path — the one every existing project
    takes — is only exercised while this holds.
    """
    import tomllib

    with (REPO_ROOT / "pyproject.toml").open("rb") as fh:
        project = tomllib.load(fh)["project"]

    assert project.get("authors"), "the template must name an author"
    assert "maintainers" not in project, (
        "the template now names maintainers; update the greenfield fallback tests, "
        "which assume it does not"
    )

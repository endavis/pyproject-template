"""The landing-page README and the consumer README must not be confused.

`README.md` is this repository's GitHub landing page. `README.template.md` is
the README a spawned project gets; `configure.py` moves it into place before
placeholder replacement.

Before the split, one file served both purposes, so the landing page opened
with `# __PROJECT_NAME__`, four broken badge images and `pip install
__PYPI_NAME__` (#697). Nothing detected that, because a placeholder is only
wrong depending on which file it is in.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LANDING = REPO_ROOT / "README.md"
CONSUMER = REPO_ROOT / "README.template.md"
CONFIGURE = REPO_ROOT / "tools" / "pyproject_template" / "configure.py"

_PLACEHOLDER_RE = re.compile(r"__[A-Z][A-Z_]*__")


def test_landing_page_has_no_placeholders() -> None:
    """The repository's front page must render as finished content.

    This is the whole point of the split: anyone browsing to the repository
    sees the template described, not a half-configured project.
    """
    found = sorted(set(_PLACEHOLDER_RE.findall(LANDING.read_text(encoding="utf-8"))))
    assert not found, (
        f"README.md is the repository landing page and still contains {found}. "
        "Consumer-facing content belongs in README.template.md."
    )


def test_consumer_readme_exists_and_is_a_template() -> None:
    """`README.template.md` must exist and still carry its placeholders.

    An empty placeholder set would mean the consumer README had been flattened
    into a copy of the landing page — the failure this split exists to prevent,
    in the opposite direction.
    """
    assert CONSUMER.is_file(), "README.template.md is missing; spawned projects would get no README"
    found = set(_PLACEHOLDER_RE.findall(CONSUMER.read_text(encoding="utf-8")))
    assert found, "README.template.md has no placeholders; it is not a template"
    assert "__PACKAGE_NAME__" in found


def test_configure_installs_the_consumer_readme() -> None:
    """`configure.py` must move README.template.md over README.md.

    Without this the spawned project keeps the template's landing page, which
    describes a repository the consumer does not have.
    """
    source = CONFIGURE.read_text(encoding="utf-8")
    assert 'Path("README.template.md")' in source, (
        "configure.py no longer references README.template.md; spawned projects "
        "would inherit the template's landing page"
    )


def test_landing_page_points_at_the_template_docs() -> None:
    """The orientation material must be reachable from the front page.

    #697's substantive complaint was not only the placeholders but that the
    useful guides were several clicks away and unlinked.
    """
    text = LANDING.read_text(encoding="utf-8")
    for target in (
        "docs/template/index.md",
        "docs/template/new-project.md",
        "docs/development/AI_SETUP.md",
    ):
        assert target in text, f"landing page does not link to {target}"

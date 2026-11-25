"""The shipped CHANGELOG.md must carry no placeholder content (#1313).

With `update_changelog_on_bump = true`, `cz changelog --incremental` keeps
everything below the header, so placeholder bullets, a dated `0.1.0` section
and `username/package_name` link references would survive into a spawned
project's first generated release. Template-owned: a downstream project
legitimately fills its own changelog.
"""

from __future__ import annotations

from pathlib import Path

CHANGELOG = Path(__file__).resolve().parents[2] / "CHANGELOG.md"


def test_changelog_has_no_placeholder_content() -> None:
    """No placeholder link targets, dates or bullets in the shipped changelog."""
    text = CHANGELOG.read_text(encoding="utf-8")
    for marker in ("username/package_name", "YYYY-MM-DD", "### Added", "First release"):
        assert marker not in text, f"CHANGELOG.md still contains placeholder {marker!r}"

"""
Helper script to apply this template onto an existing repository.

Usage:
    python tools/migrate_existing_project.py --target /path/to/existing/repo
    # Optional: download the template archive (no local checkout needed)
    python tools/migrate_existing_project.py --target /path/to/repo --download

What it does:
    - Optionally downloads the template (zip/tar) into target/tmp and extracts it
    - Backs up any files/dirs it would overwrite into a timestamped backup folder
      (under target/tmp/)
    - Copies core template files (tooling, docs, workflows, editor config)
    - Prints a summary of moved/backed-up items and next steps

This does NOT run the interactive configurator or move your source code. After
copying, you still need to:
    - Run `python configure.py` in the target repo to set project/package info
    - Move your code into src/<package_name>/ and fix imports
    - Merge dependencies/metadata into the new pyproject.toml
    - Regenerate uv.lock and rerun checks
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import tarfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable

DEFAULT_ARCHIVE_URL = "https://github.com/endavis/pyproject-template/archive/refs/heads/main.zip"


TEMPLATE_REL_PATHS: tuple[str, ...] = (
    # Config and tooling
    "pyproject.toml",
    "dodo.py",
    "configure.py",
    ".envrc",
    ".envrc.local.example",
    ".pre-commit-config.yaml",
    ".python-version",
    "mkdocs.yml",
    ".editorconfig",
    ".gitignore",
    "src/package_name",
    # Docs and guides
    "AGENTS.md",
    "AI_SETUP.md",
    "CHANGELOG.md",
    "docs",
    "examples",
    # Project scaffolding / automation
    ".github",
    ".devcontainer",
    ".vscode",
    ".claude",
    ".codex",
    ".gemini",
    "tmp/.gitkeep",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy pyproject-template scaffolding into an existing repo with backups.",
    )
    parser.add_argument(
        "--target",
        required=True,
        type=Path,
        help="Path to the existing repository you want to update.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=None,
        help="Path to the pyproject-template root (defaults to this script's repo unless --download).",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the template archive into target/tmp instead of using a local checkout.",
    )
    parser.add_argument(
        "--archive-url",
        type=str,
        default=DEFAULT_ARCHIVE_URL,
        help=f"URL to template archive (zip/tarball). Default: {DEFAULT_ARCHIVE_URL}",
    )
    return parser.parse_args()


def ensure_exists(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()
    target_root = args.target.resolve()

    if args.download:
        tmp_dir = target_root / "tmp"
        ensure_exists(tmp_dir)
        archive_path = tmp_dir / "pyproject-template-archive"
        print(f"Downloading template archive from {args.archive_url} ...")
        urllib.request.urlretrieve(args.archive_url, archive_path)

        extract_dir = tmp_dir / "pyproject-template-extracted"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        ensure_exists(extract_dir)

        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as zf:
                # Filter out dangerous paths (path traversal attacks)
                for member in zf.namelist():
                    if member.startswith("/") or ".." in member:
                        continue
                    zf.extract(member, extract_dir)
            contents = list(extract_dir.iterdir())
            template_root = contents[0] if contents else extract_dir
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r:*") as tf:
                # Filter out dangerous members (path traversal, absolute paths, devices)
                safe_members = [m for m in tf.getmembers() if m.name and not (m.name.startswith("/") or ".." in m.name)]
                tf.extractall(extract_dir, members=safe_members)
            contents = list(extract_dir.iterdir())
            template_root = contents[0] if contents else extract_dir
        else:
            raise SystemExit("Unknown archive format. Provide zip or tarball.")
    else:
        template_root = (args.template or Path(__file__).resolve().parent.parent).resolve()

    if not template_root.exists():
        raise SystemExit(f"Template path does not exist: {template_root}")
    if not target_root.exists():
        raise SystemExit(f"Target path does not exist: {target_root}")

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = target_root / "tmp" / f"template-migration-backup-{timestamp}"
    ensure_exists(backup_root)

    backed_up: list[tuple[Path, Path]] = []
    copied: list[Path] = []
    skipped: list[Path] = []

    for rel in TEMPLATE_REL_PATHS:
        src = template_root / rel
        dst = target_root / rel

        if not src.exists():
            skipped.append(src)
            continue

        if dst.exists():
            backup_path = backup_root / rel
            ensure_exists(backup_path.parent)
            shutil.move(str(dst), str(backup_path))
            backed_up.append((dst, backup_path))

        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            ensure_exists(dst.parent)
            shutil.copy2(src, dst)
        copied.append(dst)

    print("\n=== Template Migration Helper ===")
    print(f"Template: {template_root}")
    print(f"Target  : {target_root}")
    print(f"Backup  : {backup_root}")
    print()

    if copied:
        print("Copied:")
        for path in copied:
            print(f"  - {path.relative_to(target_root)}")
    else:
        print("Copied: (none)")

    print()
    if backed_up:
        print("Backed up existing items before overwrite:")
        for original, backup in backed_up:
            print(f"  - {original.relative_to(target_root)} -> {backup.relative_to(target_root)}")
    else:
        print("Backed up: (none needed)")

    if skipped:
        print()
        print("Skipped (not present in template):")
        for path in skipped:
            print(f"  - {path.relative_to(template_root)}")

    print("\nNext steps:")
    print(" 1) In the target repo, run: python configure.py")
    print(" 2) Move your source into src/<package_name>/ and fix imports.")
    print(" 3) Merge dependencies/metadata into the new pyproject.toml.")
    print(" 4) Regenerate uv.lock (uv lock) and run checks (doit check).")
    print(" 5) Compare backups above and port any unique content into the new files.")
    print("\nDone.")


if __name__ == "__main__":
    main()

"""GitHub issue and PR creation doit tasks."""

import os
import re
import subprocess  # nosec B404 - subprocess is required for doit tasks
import sys
import tempfile
from typing import TYPE_CHECKING, Any

from doit.tools import title_with_actions
from rich.console import Console
from rich.panel import Panel

from tools.tasks.templates import get_issue_template, get_pr_template, get_required_sections

if TYPE_CHECKING:
    from rich.console import Console as ConsoleType


def _get_editor() -> str:
    """Get the user's preferred editor."""
    return os.environ.get("EDITOR", os.environ.get("VISUAL", "vi"))


def _open_editor_with_template(template: str, suffix: str = ".md") -> str | None:
    """Open editor with template and return the edited content.

    Args:
        template: The template content to start with
        suffix: File suffix for the temp file

    Returns:
        The edited content (without comment lines), or None if aborted/unchanged
    """
    console = Console()
    editor = _get_editor()

    # Create temp file with template
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
        f.write(template)
        temp_path = f.name

    try:
        # Open editor
        console.print(f"[dim]Opening {editor}...[/dim]")
        result = subprocess.run([editor, temp_path])

        if result.returncode != 0:
            console.print("[red]Editor exited with error.[/red]")
            return None

        # Read the edited content
        with open(temp_path) as f:
            content = f.read()

        # Remove comment lines (starting with #) and HTML comments
        lines = []
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("#") and not stripped.startswith("##"):
                continue  # Skip comment lines but keep ## headers
            lines.append(line)

        edited = "\n".join(lines)

        # Remove HTML comments <!-- ... -->
        edited = re.sub(r"<!--.*?-->", "", edited, flags=re.DOTALL)

        # Clean up extra blank lines
        edited = re.sub(r"\n{3,}", "\n\n", edited).strip()

        return edited

    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def _parse_markdown_sections(content: str) -> dict[str, str]:
    """Parse markdown content into sections by ## headers.

    Args:
        content: Markdown content with ## headers

    Returns:
        Dict mapping section names to their content
    """
    sections: dict[str, str] = {}
    current_section = ""
    current_content: list[str] = []

    for line in content.split("\n"):
        if line.startswith("## "):
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            # Start new section
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def _validate_issue_content(
    sections: dict[str, str], issue_type: str, console: "ConsoleType"
) -> bool:
    """Validate that required sections have content.

    Args:
        sections: Parsed markdown sections
        issue_type: Type of issue (feature, bug, refactor, doc, chore)
        console: Rich console for output

    Returns:
        True if valid, False otherwise
    """
    # Get required sections dynamically from templates
    required_sections = get_required_sections(issue_type)

    missing = []
    placeholder_patterns = [
        "describe the",
        "clear description",
        "paste error",
        "any other relevant",
        "delete section if not needed",
    ]

    for section_name in required_sections:
        content = sections.get(section_name, "").strip()
        if not content:
            missing.append(section_name)
            continue

        # Check for placeholder text
        content_lower = content.lower()
        for pattern in placeholder_patterns:
            if pattern in content_lower:
                console.print(
                    f"[yellow]Warning: '{section_name}' may contain placeholder text.[/yellow]"
                )
                break

    if missing:
        console.print(f"[red]Missing required sections: {', '.join(missing)}[/red]")
        return False

    return True


def _read_body_file(file_path: str, console: "ConsoleType") -> str | None:
    """Read body content from a file.

    Args:
        file_path: Path to the file
        console: Rich console for output

    Returns:
        File content, or None if error
    """
    from pathlib import Path

    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        return None

    try:
        return path.read_text()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return None


def task_issue() -> dict[str, Any]:
    """Create a GitHub issue using the appropriate template.

    Supports five issue types: feature, bug, refactor, doc, chore.
    Labels are automatically applied based on the issue type.

    Three modes:
    1. Interactive (default): Opens $EDITOR with template
    2. --body-file: Reads body from a file
    3. --title + --body: Provides content directly (for AI/scripts)

    Examples:
        Interactive:  doit issue --type=feature
        From file:    doit issue --type=doc --title="Add guide" --body-file=issue.md
        Direct:       doit issue --type=chore --title="Update CI" --body="## Description\\n..."
    """

    def create_issue(
        type: str,
        title: str | None = None,
        body: str | None = None,
        body_file: str | None = None,
    ) -> None:
        console = Console()
        console.print()
        console.print(
            Panel.fit(
                f"[bold cyan]Creating {type} Issue[/bold cyan]",
                border_style="cyan",
            )
        )
        console.print()

        # Get template (validates type and retrieves labels/template dynamically)
        try:
            issue_template = get_issue_template(type)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            sys.exit(1)
        except FileNotFoundError as e:
            console.print(f"[red]Template error: {e}[/red]")
            sys.exit(1)

        labels = issue_template.labels

        # Determine body content
        if body_file:
            # Mode 2: Read from file
            body_content = _read_body_file(body_file, console)
            if body_content is None:
                sys.exit(1)
        elif body:
            # Mode 3: Direct body provided
            body_content = body
        else:
            # Mode 1: Interactive editor
            console.print(
                f"[dim]Opening editor with {type} template. "
                "Fill in the sections, save, and exit.[/dim]"
            )
            body_content = _open_editor_with_template(issue_template.editor_template)
            if body_content is None:
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(0)

        # Parse and validate
        sections = _parse_markdown_sections(body_content)
        if not _validate_issue_content(sections, type, console):
            console.print("[red]Issue content validation failed.[/red]")
            sys.exit(1)

        # Get title if not provided
        if not title:
            console.print("[cyan]Issue title:[/cyan]")
            title = input("> ").strip()
            if not title:
                console.print("[red]Title is required.[/red]")
                sys.exit(1)

        # Create the issue
        console.print("\n[cyan]Creating issue...[/cyan]")
        try:
            result = subprocess.run(
                [
                    "gh",
                    "issue",
                    "create",
                    "--title",
                    title,
                    "--body",
                    body_content,
                    "--label",
                    labels,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            issue_url = result.stdout.strip()
            console.print()
            console.print(
                Panel.fit(
                    f"[bold green]Issue created successfully![/bold green]\n\n{issue_url}",
                    border_style="green",
                )
            )
        except subprocess.CalledProcessError as e:
            console.print("[red]Failed to create issue:[/red]")
            console.print(f"[red]{e.stderr}[/red]")
            sys.exit(1)

    return {
        "actions": [create_issue],
        "params": [
            {
                "name": "type",
                "short": "t",
                "long": "type",
                "default": "feature",
                "help": "Issue type: feature, bug, refactor, doc, chore",
            },
            {"name": "title", "long": "title", "default": None, "help": "Issue title"},
            {"name": "body", "long": "body", "default": None, "help": "Issue body (markdown)"},
            {
                "name": "body_file",
                "long": "body-file",
                "default": None,
                "help": "Read body from file",
            },
        ],
        "title": title_with_actions,
    }


def task_pr() -> dict[str, Any]:
    """Create a GitHub PR using the repository template.

    Auto-detects current branch and linked issue from branch name.

    Three modes:
    1. Interactive (default): Opens $EDITOR with template
    2. --body-file: Reads body from a file
    3. --title + --body: Provides content directly (for AI/scripts)

    Examples:
        Interactive:  doit pr
        From file:    doit pr --title="feat: add export" --body-file=pr.md
        Direct:       doit pr --title="feat: add export" --body="## Description\\n..."
    """

    def create_pr(
        title: str | None = None,
        body: str | None = None,
        body_file: str | None = None,
        draft: bool = False,
    ) -> None:
        console = Console()
        console.print()
        console.print(
            Panel.fit("[bold cyan]Creating Pull Request[/bold cyan]", border_style="cyan")
        )
        console.print()

        # Check we're not on main
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        if current_branch == "main":
            console.print("[red]Cannot create PR from main branch.[/red]")
            console.print("[yellow]Create a feature branch first.[/yellow]")
            sys.exit(1)

        console.print(f"[dim]Current branch: {current_branch}[/dim]")

        # Try to extract issue number from branch name (e.g., feat/42-description)
        detected_issue = None
        branch_issue_match = re.search(r"/(\d+)-", current_branch)
        if branch_issue_match:
            detected_issue = branch_issue_match.group(1)
            console.print(f"[dim]Detected issue from branch: #{detected_issue}[/dim]")

        # Determine body content
        if body_file:
            # Mode 2: Read from file
            body_content = _read_body_file(body_file, console)
            if body_content is None:
                sys.exit(1)
        elif body:
            # Mode 3: Direct body provided
            body_content = body
        else:
            # Mode 1: Interactive editor
            # Get PR template dynamically from .github/
            try:
                template = get_pr_template()
            except FileNotFoundError as e:
                console.print(f"[red]Template error: {e}[/red]")
                sys.exit(1)

            # Pre-fill issue number if detected
            if detected_issue:
                template = template.replace("#(issue)", f"#{detected_issue}")

            console.print(
                "[dim]Opening editor with PR template. Fill in the sections, save, and exit.[/dim]"
            )
            body_content = _open_editor_with_template(template)
            if body_content is None:
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(0)

        # Validate PR has description
        sections = _parse_markdown_sections(body_content)
        description = sections.get("Description", "").strip()
        if not description:
            console.print("[red]Description is required.[/red]")
            sys.exit(1)

        # Get title if not provided
        if not title:
            console.print("[cyan]PR title (e.g., 'feat: add export feature'):[/cyan]")
            title = input("> ").strip()
            if not title:
                console.print("[red]Title is required.[/red]")
                sys.exit(1)

        # Create the PR
        console.print("\n[cyan]Creating PR...[/cyan]")
        cmd = ["gh", "pr", "create", "--title", title, "--body", body_content]
        if draft:
            cmd.append("--draft")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            pr_url = result.stdout.strip()
            console.print()
            console.print(
                Panel.fit(
                    f"[bold green]PR created successfully![/bold green]\n\n{pr_url}",
                    border_style="green",
                )
            )
        except subprocess.CalledProcessError as e:
            console.print("[red]Failed to create PR:[/red]")
            console.print(f"[red]{e.stderr}[/red]")
            sys.exit(1)

    return {
        "actions": [create_pr],
        "params": [
            {"name": "title", "long": "title", "default": None, "help": "PR title"},
            {"name": "body", "long": "body", "default": None, "help": "PR body (markdown)"},
            {
                "name": "body_file",
                "long": "body-file",
                "default": None,
                "help": "Read body from file",
            },
            {
                "name": "draft",
                "long": "draft",
                "type": bool,
                "default": False,
                "help": "Create as draft PR",
            },
        ],
        "title": title_with_actions,
    }

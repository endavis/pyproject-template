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

if TYPE_CHECKING:
    from rich.console import Console as ConsoleType

# Issue templates for editor mode
ISSUE_TEMPLATE_FEATURE = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Problem
<!-- Required: What problem does this feature solve? -->
Describe the problem or limitation you're experiencing.

## Proposed Solution
<!-- Required: How do you envision this feature working? -->
Clear description of what you want to happen.

## Success Criteria
<!-- Optional: How will we know this is complete? Delete section if not needed. -->
- [ ] Feature implements X functionality
- [ ] Tests added and passing
- [ ] Documentation updated

## Additional Context
<!-- Optional: Links, examples, screenshots. Delete section if not needed. -->
Any other relevant information.
"""

ISSUE_TEMPLATE_BUG = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Bug Description
<!-- Required: A clear description of the bug -->
Describe the bug and its impact.

## Steps to Reproduce
<!-- Required: Step-by-step instructions -->
1. Run command `...`
2. With input `...`
3. Observe error `...`

## Expected vs Actual Behavior
<!-- Required: What should happen vs what actually happens -->
**Expected:** The function should return a valid result
**Actual:** The function raises an error

## Environment
<!-- Optional: System information. Delete section if not needed. -->
- Python: 3.12
- OS: Ubuntu 22.04
- Package version: 1.0.0

## Error Output
<!-- Optional: Paste error messages or stack traces. Delete section if not needed. -->
```
Paste error output here
```

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Screenshots, related issues, workarounds attempted.
"""

ISSUE_TEMPLATE_REFACTOR = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Current Code Issue
<!-- Required: Describe the code that needs refactoring -->
Describe what code currently exists, where it's located, and what problems it causes.

## Proposed Improvement
<!-- Required: How you propose to refactor the code -->
Describe the refactoring approach and what the code will look like after.

## Success Criteria
<!-- Optional: How will we know the refactoring is successful? Delete section if not needed. -->
- [ ] Code duplication eliminated
- [ ] All existing tests still pass
- [ ] New tests added for refactored code

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Performance impact, breaking change considerations, migration steps.
"""

ISSUE_TEMPLATE_DOC = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Documentation Type
<!-- Required: What kind of documentation change? -->
New guide / Update existing / Fix incorrect info / Add examples / API docs

## Description
<!-- Required: What documentation is needed? -->
Describe the documentation that is missing or needs improvement.

## Suggested Location
<!-- Optional: Where should this documentation live? Delete section if not needed. -->
- docs/getting-started/
- docs/examples/
- README.md

## Success Criteria
<!-- Optional: How will we know the documentation is complete? Delete section if not needed. -->
- [ ] Topic is fully explained
- [ ] Code examples included
- [ ] Added to navigation/index

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Links to related documentation, examples from other projects.
"""

ISSUE_TEMPLATE_CHORE = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.

## Chore Type
<!-- Required: What kind of maintenance task? -->
CI/CD / Dependencies / Tooling / Cleanup / Configuration

## Description
<!-- Required: What needs to be done and why? -->
Describe the maintenance task.

## Proposed Changes
<!-- Optional: What specific changes need to be made? Delete section if not needed. -->
- Update file X
- Modify configuration Y
- Add/remove dependency Z

## Success Criteria
<!-- Optional: How will we know this task is complete? Delete section if not needed. -->
- [ ] CI passes
- [ ] No breaking changes
- [ ] Documentation updated if needed

## Additional Context
<!-- Optional: Any other relevant information. Delete section if not needed. -->
Related issues, urgency, dependencies on other tasks.
"""

PR_TEMPLATE = """\
# Lines starting with # are comments and will be ignored.
# Fill in the sections below, save, and exit.
# Delete the placeholder text and add your content.
# Mark checkboxes with [x] where applicable.

## Description
<!-- Required: What does this PR do? -->
Provide a clear description of your changes.

## Related Issue
<!-- Link to the issue this PR addresses -->
Closes #ISSUE_NUMBER

## Type of Change
<!-- Mark ONE with [x] -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Test improvement

## Changes Made
<!-- List the main changes -->
- Change 1
- Change 2
- Change 3

## Testing
<!-- Mark with [x] what applies -->
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Manually tested the changes

## Checklist
<!-- Mark with [x] what you've done -->
- [ ] My code follows the code style of this project (ran `doit format`)
- [ ] I have run linting checks (`doit lint`)
- [ ] I have run type checking (`doit type_check`)
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass (`doit test`)
- [ ] I have updated the documentation accordingly
- [ ] I have updated the CHANGELOG.md
- [ ] My changes generate no new warnings

## Screenshots (if applicable)
<!-- Add screenshots or delete this section -->
N/A

## Additional Notes
<!-- Any other information or delete this section -->
N/A
"""


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
    required: dict[str, list[str]] = {
        "feature": ["Problem", "Proposed Solution"],
        "bug": ["Bug Description", "Steps to Reproduce", "Expected vs Actual Behavior"],
        "refactor": ["Current Code Issue", "Proposed Improvement"],
        "doc": ["Documentation Type", "Description"],
        "chore": ["Chore Type", "Description"],
    }

    missing = []
    placeholder_patterns = [
        "describe the",
        "clear description",
        "paste error",
        "any other relevant",
        "delete section if not needed",
    ]

    for section_name in required.get(issue_type, []):
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

        # Validate type
        valid_types = ["feature", "bug", "refactor", "doc", "chore"]
        if type not in valid_types:
            console.print(f"[red]Invalid type: {type}. Must be one of: {valid_types}[/red]")
            sys.exit(1)

        # Map type to labels and template
        type_config = {
            "feature": {"labels": "enhancement,needs-triage", "template": ISSUE_TEMPLATE_FEATURE},
            "bug": {"labels": "bug,needs-triage", "template": ISSUE_TEMPLATE_BUG},
            "refactor": {"labels": "refactor,needs-triage", "template": ISSUE_TEMPLATE_REFACTOR},
            "doc": {"labels": "documentation,needs-triage", "template": ISSUE_TEMPLATE_DOC},
            "chore": {"labels": "chore,needs-triage", "template": ISSUE_TEMPLATE_CHORE},
        }
        config = type_config[type]
        labels = config["labels"]

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
            body_content = _open_editor_with_template(config["template"])
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
            # Pre-fill issue number if detected
            template = PR_TEMPLATE
            if detected_issue:
                template = template.replace("#ISSUE_NUMBER", f"#{detected_issue}")

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
        if not description or description == "Provide a clear description of your changes.":
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

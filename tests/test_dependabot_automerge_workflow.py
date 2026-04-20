"""Tests for the dependabot auto-merge GitHub Actions workflow configuration.

These tests are structural asserts on the parsed YAML. They do not execute the
workflow — they only verify its shape. The most important guarantee here is the
step ordering inside the ``enable-automerge`` job (see issue #423): the
``ready-to-merge`` label must be applied *before* ``gh pr merge --auto`` is
invoked so that a failure of the merge call cannot skip the label.

Issue #424 split the blocked-label handler out into a sibling workflow
(``dependabot-blocked-label.yml``) so this workflow no longer fires on
``labeled`` events. The ``TestOnTriggers`` and ``TestConcurrency`` classes
below guard that split.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / ".github" / "workflows" / "dependabot-automerge.yml"


def _load_workflow() -> dict[Any, Any]:
    """Load and parse the dependabot auto-merge workflow YAML.

    Return type is ``dict[Any, Any]`` (not ``dict[str, Any]``) because
    PyYAML parses the ``on`` key as the boolean ``True`` (YAML 1.1 alias).
    """
    return yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))


def _enable_automerge_steps() -> list[dict[str, Any]]:
    """Return the list of steps in the ``enable-automerge`` job."""
    workflow = _load_workflow()
    job = workflow["jobs"]["enable-automerge"]
    steps: list[dict[str, Any]] = job["steps"]
    return steps


class TestDependabotAutomergeWorkflowExists:
    """The workflow file exists and parses as YAML."""

    def test_workflow_file_exists(self) -> None:
        """The dependabot auto-merge workflow YAML file should exist."""
        assert WORKFLOW_PATH.exists(), f"Workflow not found: {WORKFLOW_PATH}"

    def test_workflow_parses_as_yaml(self) -> None:
        """The workflow file should be valid YAML."""
        workflow = _load_workflow()
        assert isinstance(workflow, dict)
        assert "jobs" in workflow


class TestEnableAutomergeJobShape:
    """The ``enable-automerge`` job has the expected top-level shape."""

    def test_enable_automerge_job_exists(self) -> None:
        """Workflow should define the ``enable-automerge`` job."""
        workflow = _load_workflow()
        assert "enable-automerge" in workflow["jobs"]

    def test_enable_automerge_needs_evaluate(self) -> None:
        """``enable-automerge`` must depend on the ``evaluate`` job."""
        workflow = _load_workflow()
        job = workflow["jobs"]["enable-automerge"]
        assert job["needs"] == "evaluate"

    def test_enable_automerge_qualifies_guard(self) -> None:
        """The job should only run when ``evaluate`` reports ``qualifies == 'true'``."""
        workflow = _load_workflow()
        job = workflow["jobs"]["enable-automerge"]
        assert job["if"] == "needs.evaluate.outputs.qualifies == 'true'"


class TestEnableAutomergeStepOrdering:
    """Regression guard for issue #423.

    The label must be applied before the auto-merge call so a merge failure
    cannot skip the label. The sticky comment must run last and use
    ``if: always()`` so it posts on both success and failure.
    """

    def test_has_three_steps(self) -> None:
        """``enable-automerge`` should have exactly three steps."""
        steps = _enable_automerge_steps()
        assert len(steps) == 3, f"expected 3 steps, got {len(steps)}: {steps}"

    def test_first_step_is_label(self) -> None:
        """The label step must run first so it is applied unconditionally.

        This is the core regression guard for issue #423 — if the merge call is
        reordered to run before the label, a merge failure will skip the label
        and the Merge Gate will stay red forever.
        """
        steps = _enable_automerge_steps()
        assert steps[0]["name"] == "Add ready-to-merge label"

    def test_label_step_adds_ready_to_merge(self) -> None:
        """The label step should add the ``ready-to-merge`` label via ``gh pr edit``."""
        steps = _enable_automerge_steps()
        label_step = steps[0]
        assert "--add-label ready-to-merge" in label_step["run"]

    def test_second_step_is_enable_automerge(self) -> None:
        """The auto-merge call runs second, after the label is already applied."""
        steps = _enable_automerge_steps()
        assert steps[1]["name"] == "Enable auto-merge (squash)"

    def test_enable_automerge_step_has_id(self) -> None:
        """The merge step needs ``id: automerge`` so the comment step can read its outcome."""
        steps = _enable_automerge_steps()
        assert steps[1].get("id") == "automerge"

    def test_enable_automerge_step_uses_squash(self) -> None:
        """The merge step should use the squash strategy with ``--auto``."""
        steps = _enable_automerge_steps()
        merge_step = steps[1]
        assert "gh pr merge --auto --squash" in merge_step["run"]

    def test_third_step_is_sticky_comment(self) -> None:
        """The sticky status comment runs last."""
        steps = _enable_automerge_steps()
        assert steps[2]["name"] == "Post sticky status comment"


class TestStickyCommentStep:
    """The sticky comment step is outcome-aware and always runs."""

    def test_sticky_comment_uses_always(self) -> None:
        """``if: always()`` ensures the comment runs even when the merge step fails."""
        steps = _enable_automerge_steps()
        assert steps[2].get("if") == "always()"

    def test_sticky_comment_uses_github_script(self) -> None:
        """The sticky comment step should use ``actions/github-script``."""
        steps = _enable_automerge_steps()
        assert steps[2]["uses"] == "actions/github-script@v9"

    def test_sticky_comment_exposes_automerge_outcome(self) -> None:
        """The sticky comment step must expose ``AUTOMERGE_OUTCOME`` via ``env``."""
        steps = _enable_automerge_steps()
        env = steps[2].get("env", {})
        assert env.get("AUTOMERGE_OUTCOME") == "${{ steps.automerge.outcome }}"

    def test_sticky_comment_branches_on_outcome(self) -> None:
        """The inline script should branch on ``AUTOMERGE_OUTCOME``.

        Branching lets the script emit either the success copy or the
        failure copy depending on whether the merge call succeeded.
        """
        steps = _enable_automerge_steps()
        script: str = steps[2]["with"]["script"]
        assert "AUTOMERGE_OUTCOME" in script, (
            "sticky comment script must reference AUTOMERGE_OUTCOME so it can "
            "produce a success vs failure body"
        )

    def test_sticky_comment_retains_dedupe_marker(self) -> None:
        """The sticky-comment dedupe marker must survive the refactor."""
        steps = _enable_automerge_steps()
        script: str = steps[2]["with"]["script"]
        assert "<!-- dependabot-automerge:status -->" in script

    def test_sticky_comment_deletes_prior_bot_marker_comments(self) -> None:
        """The dedupe logic (list + delete prior marker comments) must remain."""
        steps = _enable_automerge_steps()
        script: str = steps[2]["with"]["script"]
        assert "deleteComment" in script
        assert "listComments" in script


class TestOnTriggers:
    """Trigger configuration: the ``labeled`` event is handled elsewhere.

    Issue #424 moved label-driven handling to ``dependabot-blocked-label.yml``.
    Leaving ``labeled`` in the trigger list here would re-introduce the
    duplicate-run problem on dependabot PRs (each auto-applied label fires a
    separate workflow run).
    """

    def test_labeled_not_in_pull_request_target_types(self) -> None:
        """The ``labeled`` event type must NOT appear in ``pull_request_target.types``.

        This is the core regression guard for issue #424.
        """
        workflow = _load_workflow()
        triggers = workflow.get("on") or workflow.get(True)
        assert triggers is not None, "workflow has no triggers block"
        types = triggers["pull_request_target"]["types"]
        assert "labeled" not in types, (
            f"'labeled' must not be in pull_request_target.types; got {types}. "
            "Label-driven handling is in dependabot-blocked-label.yml (issue #424)."
        )

    def test_pull_request_target_types_cover_core_lifecycle(self) -> None:
        """The PR trigger must still cover the core lifecycle events so the
        main evaluate/enable-automerge flow still runs on every open/sync."""
        workflow = _load_workflow()
        triggers = workflow.get("on") or workflow.get(True)
        assert triggers is not None
        types = triggers["pull_request_target"]["types"]
        for required in ("opened", "reopened", "synchronize", "ready_for_review"):
            assert required in types, f"pull_request_target.types missing '{required}': {types}"

    def test_schedule_and_workflow_dispatch_retained(self) -> None:
        """``schedule`` and ``workflow_dispatch`` drive the rebase-requester job,
        so they must remain triggers on this workflow."""
        workflow = _load_workflow()
        triggers = workflow.get("on") or workflow.get(True)
        assert triggers is not None
        assert "schedule" in triggers
        assert "workflow_dispatch" in triggers


class TestConcurrency:
    """Workflow-level concurrency block dedupes in-flight runs per PR.

    The concurrency block is only safe to add after the ``labeled`` trigger
    split in issue #424: prior to the split, a labeled event arriving shortly
    after an ``opened`` event would cancel the in-flight ``evaluate`` job
    mid-run. With label events routed to ``dependabot-blocked-label.yml``,
    cancelling stale runs on this workflow is safe.
    """

    def test_concurrency_block_exists(self) -> None:
        """The workflow must declare a top-level ``concurrency`` block."""
        workflow = _load_workflow()
        assert "concurrency" in workflow, "workflow must declare a concurrency block"

    def test_concurrency_group_keyed_on_pr_number_or_ref(self) -> None:
        """The group key must reference ``pull_request.number`` and ``github.ref``.

        ``pull_request.number`` isolates PR runs from each other;
        ``github.ref`` is the fallback for schedule/workflow_dispatch runs
        that have no PR context.
        """
        workflow = _load_workflow()
        group: str = workflow["concurrency"]["group"]
        assert "pull_request.number" in group or "github.event.pull_request.number" in group
        assert "github.ref" in group

    def test_concurrency_cancel_in_progress(self) -> None:
        """``cancel-in-progress: true`` supersedes stale runs on a new PR push."""
        workflow = _load_workflow()
        assert workflow["concurrency"]["cancel-in-progress"] is True

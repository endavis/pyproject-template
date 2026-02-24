"""Tests for the benchmark GitHub Actions workflow configuration."""

from __future__ import annotations

from pathlib import Path

import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / ".github" / "workflows" / "benchmark.yml"


def _load_workflow() -> dict:
    """Load and parse the benchmark workflow YAML."""
    return yaml.safe_load(WORKFLOW_PATH.read_text())


class TestBenchmarkWorkflowExists:
    """Test that the benchmark workflow file exists."""

    def test_workflow_file_exists(self) -> None:
        """The benchmark workflow YAML file should exist."""
        assert WORKFLOW_PATH.exists(), f"Benchmark workflow not found: {WORKFLOW_PATH}"


class TestBenchmarkWorkflowTriggers:
    """Test that the benchmark workflow has correct triggers."""

    def test_has_push_trigger(self) -> None:
        """Workflow should trigger on push to main."""
        workflow = _load_workflow()
        triggers = workflow[True]  # YAML 'on' is parsed as boolean True
        assert "push" in triggers
        assert "main" in triggers["push"]["branches"]

    def test_has_pull_request_trigger(self) -> None:
        """Workflow should trigger on pull requests to main."""
        workflow = _load_workflow()
        triggers = workflow[True]
        assert "pull_request" in triggers
        assert "main" in triggers["pull_request"]["branches"]

    def test_has_workflow_dispatch_trigger(self) -> None:
        """Workflow should support manual dispatch."""
        workflow = _load_workflow()
        triggers = workflow[True]
        assert "workflow_dispatch" in triggers


class TestBenchmarkWorkflowPermissions:
    """Test that the benchmark workflow has correct permissions."""

    def test_has_contents_write_permission(self) -> None:
        """Workflow needs contents:write to push to gh-benchmarks branch."""
        workflow = _load_workflow()
        assert workflow["permissions"]["contents"] == "write"

    def test_has_pull_requests_write_permission(self) -> None:
        """Workflow needs pull-requests:write to post PR comments."""
        workflow = _load_workflow()
        assert workflow["permissions"]["pull-requests"] == "write"


class TestBenchmarkWorkflowSteps:
    """Test that the benchmark workflow has the expected steps."""

    def _get_steps(self) -> list[dict]:
        """Get the steps from the benchmark job."""
        workflow = _load_workflow()
        return workflow["jobs"]["benchmark"]["steps"]

    def _find_step(self, name: str) -> dict | None:
        """Find a step by name."""
        for step in self._get_steps():
            if step.get("name") == name:
                return step
        return None

    def test_has_check_bench_branch_step(self) -> None:
        """Workflow should check if the gh-benchmarks branch exists."""
        step = self._find_step("Check for benchmark data branch")
        assert step is not None, "Missing 'Check for benchmark data branch' step"
        assert step.get("id") == "check-bench-branch"
        assert "gh-benchmarks" in step["run"]

    def test_store_step_conditional_on_branch_existence(self) -> None:
        """Store step should only run on push or when gh-benchmarks branch exists."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        condition = step.get("if", "")
        assert "push" in condition
        assert "check-bench-branch" in condition

    def test_check_bench_branch_before_store_step(self) -> None:
        """Check branch step should come before store step."""
        steps = self._get_steps()
        step_names = [s.get("name") for s in steps]
        check_idx = step_names.index("Check for benchmark data branch")
        store_idx = step_names.index("Store benchmark results")
        assert check_idx < store_idx, "Check branch step must come before Store step"

    def test_store_step_skips_fetch_when_branch_missing(self) -> None:
        """Store step should skip gh-pages fetch when the data branch doesn't exist."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        skip_fetch = step["with"]["skip-fetch-gh-pages"]
        assert "check-bench-branch" in skip_fetch

    def test_has_store_benchmark_results_step(self) -> None:
        """Workflow should have a step to store benchmark results."""
        step = self._find_step("Store benchmark results")
        assert step is not None, "Missing 'Store benchmark results' step"

    def test_store_step_uses_benchmark_action(self) -> None:
        """The store step should use benchmark-action/github-action-benchmark."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["uses"] == "benchmark-action/github-action-benchmark@v1"

    def test_store_step_uses_pytest_tool(self) -> None:
        """The store step should be configured for pytest output."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["with"]["tool"] == "pytest"

    def test_store_step_reads_correct_output_file(self) -> None:
        """The store step should read from the benchmark results JSON."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["with"]["output-file-path"] == "tmp/benchmark-results.json"

    def test_store_step_uses_gh_benchmarks_branch(self) -> None:
        """Results should be stored on the gh-benchmarks branch."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["with"]["gh-pages-branch"] == "gh-benchmarks"

    def test_store_step_uses_dev_bench_data_dir(self) -> None:
        """Results should be stored in the dev/bench directory."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["with"]["benchmark-data-dir-path"] == "dev/bench"

    def test_store_step_auto_push_conditional(self) -> None:
        """Auto-push should only happen on push to main."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        auto_push = step["with"]["auto-push"]
        assert "github.event_name == 'push'" in auto_push
        assert "refs/heads/main" in auto_push

    def test_store_step_comment_on_alert_enabled(self) -> None:
        """Comment-on-alert should be enabled."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["with"]["comment-on-alert"] is True

    def test_store_step_comment_always_on_pr(self) -> None:
        """Comment-always should be conditional on pull_request events."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        comment_always = step["with"]["comment-always"]
        assert "pull_request" in comment_always

    def test_store_step_alert_threshold(self) -> None:
        """Alert threshold should be set to 110% (10% regression tolerance)."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["with"]["alert-threshold"] == "110%"

    def test_store_step_uses_github_token(self) -> None:
        """The store step should use GITHUB_TOKEN for authentication."""
        step = self._find_step("Store benchmark results")
        assert step is not None
        assert step["with"]["github-token"] == "${{ secrets.GITHUB_TOKEN }}"

    def test_upload_artifact_step_still_exists(self) -> None:
        """The existing artifact upload step should still be present."""
        step = self._find_step("Upload benchmark results")
        assert step is not None, "Missing 'Upload benchmark results' artifact step"

    def test_run_benchmarks_step_exists(self) -> None:
        """The run benchmarks step should still be present."""
        step = self._find_step("Run benchmarks")
        assert step is not None, "Missing 'Run benchmarks' step"

    def test_store_step_comes_after_run_step(self) -> None:
        """Store step should come after the run benchmarks step."""
        steps = self._get_steps()
        step_names = [s.get("name") for s in steps]
        run_idx = step_names.index("Run benchmarks")
        store_idx = step_names.index("Store benchmark results")
        assert store_idx > run_idx, "Store step must come after Run benchmarks step"

    def test_upload_step_comes_after_store_step(self) -> None:
        """Upload artifact step should come after the store step."""
        steps = self._get_steps()
        step_names = [s.get("name") for s in steps]
        store_idx = step_names.index("Store benchmark results")
        upload_idx = step_names.index("Upload benchmark results")
        assert upload_idx > store_idx, "Upload step must come after Store step"

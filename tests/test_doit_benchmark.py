"""Tests for benchmark.py doit tasks."""

from tools.doit.benchmark import task_benchmark, task_benchmark_compare, task_benchmark_save


class TestTaskBenchmark:
    """Tests for task_benchmark function."""

    def test_returns_valid_doit_task(self) -> None:
        """Test that task_benchmark returns a valid doit task dict."""
        result = task_benchmark()
        assert isinstance(result, dict)
        assert "actions" in result
        assert "title" in result

    def test_actions_contain_benchmark_flags(self) -> None:
        """Test that actions include benchmark-specific flags."""
        result = task_benchmark()
        action = result["actions"][0]
        assert "--benchmark-enable" in action
        assert "--benchmark-only" in action
        assert "tests/benchmarks/" in action


class TestTaskBenchmarkSave:
    """Tests for task_benchmark_save function."""

    def test_returns_valid_doit_task(self) -> None:
        """Test that task_benchmark_save returns a valid doit task dict."""
        result = task_benchmark_save()
        assert isinstance(result, dict)
        assert "actions" in result
        assert "title" in result

    def test_actions_contain_save_flags(self) -> None:
        """Test that actions include save-specific flags."""
        result = task_benchmark_save()
        action = result["actions"][0]
        assert "--benchmark-enable" in action
        assert "--benchmark-only" in action
        assert "--benchmark-save=baseline" in action
        assert "--benchmark-storage=tmp/benchmarks" in action
        assert "tests/benchmarks/" in action


class TestTaskBenchmarkCompare:
    """Tests for task_benchmark_compare function."""

    def test_returns_valid_doit_task(self) -> None:
        """Test that task_benchmark_compare returns a valid doit task dict."""
        result = task_benchmark_compare()
        assert isinstance(result, dict)
        assert "actions" in result
        assert "title" in result

    def test_actions_contain_compare_flags(self) -> None:
        """Test that actions include compare-specific flags."""
        result = task_benchmark_compare()
        action = result["actions"][0]
        assert "--benchmark-enable" in action
        assert "--benchmark-only" in action
        assert "--benchmark-compare=0001_baseline" in action
        assert "--benchmark-storage=tmp/benchmarks" in action
        assert "tests/benchmarks/" in action

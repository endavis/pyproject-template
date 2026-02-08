"""Performance benchmarks for core module."""

from typing import Any

import pytest

from package_name.core import greet


@pytest.mark.benchmark
def test_bench_greet_default(benchmark: Any) -> None:
    """Benchmark greet() with default argument."""
    benchmark(greet)


@pytest.mark.benchmark
def test_bench_greet_with_name(benchmark: Any) -> None:
    """Benchmark greet() with a name argument."""
    benchmark(greet, "Python")


@pytest.mark.benchmark
def test_bench_greet_long_name(benchmark: Any) -> None:
    """Benchmark greet() with a long name to test scaling."""
    long_name = "A" * 1000
    benchmark(greet, long_name)

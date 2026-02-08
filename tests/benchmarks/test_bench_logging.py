"""Performance benchmarks for logging module."""

from typing import Any

import pytest

from package_name.logging import get_logger, setup_logging


@pytest.mark.benchmark
def test_bench_get_logger(benchmark: Any) -> None:
    """Benchmark get_logger() call."""
    benchmark(get_logger, "test.benchmark")


@pytest.mark.benchmark
def test_bench_setup_logging(benchmark: Any) -> None:
    """Benchmark setup_logging() with console disabled."""
    benchmark(setup_logging, console=False)

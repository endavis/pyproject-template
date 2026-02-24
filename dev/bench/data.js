window.BENCHMARK_DATA = {
  "lastUpdate": 1771952628089,
  "repoUrl": "https://github.com/endavis/pyproject-template",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b4dd0b7702a3a8d76d796de703a5f8d261acc2f3",
          "message": "fix: use checkout instead of switch after orphan branch creation (merges PR #287, addresses #242)\n\nCo-authored-by: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-24T17:03:16Z",
          "tree_id": "71b7e397e1225722d83301433250e882dd7d149c",
          "url": "https://github.com/endavis/pyproject-template/commit/b4dd0b7702a3a8d76d796de703a5f8d261acc2f3"
        },
        "date": 1771952627463,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8428532.21631157,
            "unit": "iter/sec",
            "range": "stddev: 1.00895430484703e-8",
            "extra": "mean: 118.64461976721404 nsec\nrounds: 84948"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8449762.087546226,
            "unit": "iter/sec",
            "range": "stddev: 1.0474336461772662e-8",
            "extra": "mean: 118.34652735061745 nsec\nrounds: 82905"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5765979.075541901,
            "unit": "iter/sec",
            "range": "stddev: 1.2470123544398246e-8",
            "extra": "mean: 173.43108375848857 nsec\nrounds: 56424"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1673139.192009857,
            "unit": "iter/sec",
            "range": "stddev: 2.4248551260142915e-7",
            "extra": "mean: 597.6789048846264 nsec\nrounds: 61801"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 495907.73766274814,
            "unit": "iter/sec",
            "range": "stddev: 4.5910277253054737e-7",
            "extra": "mean: 2.0165041277901374 usec\nrounds: 48452"
          }
        ]
      }
    ]
  }
}
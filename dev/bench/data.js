window.BENCHMARK_DATA = {
  "lastUpdate": 1775127989819,
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
      },
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
          "id": "55e5f1583b9fbb0b2067720e0ce1052ead72275f",
          "message": "docs: update documentation for recent features (PRs #268-#287) (merges PR #289, addresses #288)\n\nCo-authored-by: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-25T09:40:38Z",
          "tree_id": "c28d72ff9974ff88faafcefdd8e8f1179d997948",
          "url": "https://github.com/endavis/pyproject-template/commit/55e5f1583b9fbb0b2067720e0ce1052ead72275f"
        },
        "date": 1772012469920,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8211541.194293148,
            "unit": "iter/sec",
            "range": "stddev: 9.485810008756619e-9",
            "extra": "mean: 121.77981895712578 nsec\nrounds: 79981"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8324692.822945436,
            "unit": "iter/sec",
            "range": "stddev: 1.1065379720195028e-8",
            "extra": "mean: 120.12455249323914 nsec\nrounds: 81887"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5592010.166688492,
            "unit": "iter/sec",
            "range": "stddev: 1.242571400718688e-8",
            "extra": "mean: 178.82657044455726 nsec\nrounds: 54873"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1675256.7355240898,
            "unit": "iter/sec",
            "range": "stddev: 2.194879220559528e-7",
            "extra": "mean: 596.9234319700607 nsec\nrounds: 61958"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 492420.27763606113,
            "unit": "iter/sec",
            "range": "stddev: 4.517692191438786e-7",
            "extra": "mean: 2.0307855817811826 usec\nrounds: 49049"
          }
        ]
      },
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
          "id": "5486031f1f8914323ffb920ef6c979143144e6c9",
          "message": "fix: propagate --yes flag to manage.py subcommands (merges PR #291, addresses #290)\n\nCo-authored-by: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-25T11:08:04Z",
          "tree_id": "e8a1dedb3ed48dc5e89be7cc7b432546eac6cd01",
          "url": "https://github.com/endavis/pyproject-template/commit/5486031f1f8914323ffb920ef6c979143144e6c9"
        },
        "date": 1772017710314,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8166984.352580131,
            "unit": "iter/sec",
            "range": "stddev: 1.2600047111595168e-8",
            "extra": "mean: 122.44421647313159 nsec\nrounds: 83105"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8306651.00208249,
            "unit": "iter/sec",
            "range": "stddev: 1.0151140556058403e-8",
            "extra": "mean: 120.38545976583083 nsec\nrounds: 81150"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5593233.539409745,
            "unit": "iter/sec",
            "range": "stddev: 1.4238505859520605e-8",
            "extra": "mean: 178.7874568358414 nsec\nrounds: 54849"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1683086.6830090855,
            "unit": "iter/sec",
            "range": "stddev: 2.0472155012615866e-7",
            "extra": "mean: 594.1464632184972 nsec\nrounds: 60493"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 488272.1664871446,
            "unit": "iter/sec",
            "range": "stddev: 4.338613854146437e-7",
            "extra": "mean: 2.048038099723074 usec\nrounds: 53150"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "49699333+dependabot[bot]@users.noreply.github.com",
            "name": "dependabot[bot]",
            "username": "dependabot[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a4ea6f360290e42426f2d401c9d13b1415842181",
          "message": "chore(deps): bump actions/download-artifact from 7 to 8 (merges PR #295)\n\nBumps [actions/download-artifact](https://github.com/actions/download-artifact) from 7 to 8.\n- [Release notes](https://github.com/actions/download-artifact/releases)\n- [Commits](https://github.com/actions/download-artifact/compare/v7...v8)\n\n---\nupdated-dependencies:\n- dependency-name: actions/download-artifact\n  dependency-version: '8'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:06:07+01:00",
          "tree_id": "876fbd4ccfe7ac5f5736bec2bb3df3d71c530f63",
          "url": "https://github.com/endavis/pyproject-template/commit/a4ea6f360290e42426f2d401c9d13b1415842181"
        },
        "date": 1775127989557,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8655791.334296377,
            "unit": "iter/sec",
            "range": "stddev: 1.0802365905314459e-8",
            "extra": "mean: 115.52958722996864 nsec\nrounds: 89929"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9103617.770743832,
            "unit": "iter/sec",
            "range": "stddev: 1.1008284421958057e-8",
            "extra": "mean: 109.84643964443299 nsec\nrounds: 88567"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5520948.025598045,
            "unit": "iter/sec",
            "range": "stddev: 1.3569482303304757e-8",
            "extra": "mean: 181.1283126309955 nsec\nrounds: 55951"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1671043.2333879056,
            "unit": "iter/sec",
            "range": "stddev: 3.826332961340223e-7",
            "extra": "mean: 598.428562481044 nsec\nrounds: 63776"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 496441.89945489913,
            "unit": "iter/sec",
            "range": "stddev: 4.942061586359588e-7",
            "extra": "mean: 2.014334408715331 usec\nrounds: 35956"
          }
        ]
      }
    ]
  }
}
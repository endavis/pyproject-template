window.BENCHMARK_DATA = {
  "lastUpdate": 1777394198334,
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
          "id": "c9576a85f57131971d04e8ff995e7764d45ef29a",
          "message": "chore(deps): bump actions/upload-artifact from 6 to 7 (merges PR #296)\n\nBumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 6 to 7.\n- [Release notes](https://github.com/actions/upload-artifact/releases)\n- [Commits](https://github.com/actions/upload-artifact/compare/v6...v7)\n\n---\nupdated-dependencies:\n- dependency-name: actions/upload-artifact\n  dependency-version: '7'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:06:14+01:00",
          "tree_id": "9b35f7d635a9e0265dc801464ec3e75c8325d4d3",
          "url": "https://github.com/endavis/pyproject-template/commit/c9576a85f57131971d04e8ff995e7764d45ef29a"
        },
        "date": 1775128000600,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9045044.277884077,
            "unit": "iter/sec",
            "range": "stddev: 1.2353953466514676e-8",
            "extra": "mean: 110.55777830132764 nsec\nrounds: 89040"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8914543.89240486,
            "unit": "iter/sec",
            "range": "stddev: 1.554290674658872e-8",
            "extra": "mean: 112.17623829885387 nsec\nrounds: 89526"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5223115.782472778,
            "unit": "iter/sec",
            "range": "stddev: 2.1733124551405442e-8",
            "extra": "mean: 191.45660208332015 nsec\nrounds: 51664"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1654310.8536156006,
            "unit": "iter/sec",
            "range": "stddev: 2.83491457736961e-7",
            "extra": "mean: 604.48131487165 nsec\nrounds: 60021"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 495092.88049280585,
            "unit": "iter/sec",
            "range": "stddev: 6.060998727027682e-7",
            "extra": "mean: 2.0198230259433734 usec\nrounds: 49883"
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
          "id": "6c3a844e9edb0b622c62e1e16c551b16de084aab",
          "message": "chore(deps): bump commitizen from 4.13.8 to 4.13.9 (merges PR #300)\n\nBumps [commitizen](https://github.com/commitizen-tools/commitizen) from 4.13.8 to 4.13.9.\n- [Release notes](https://github.com/commitizen-tools/commitizen/releases)\n- [Changelog](https://github.com/commitizen-tools/commitizen/blob/master/CHANGELOG.md)\n- [Commits](https://github.com/commitizen-tools/commitizen/compare/v4.13.8...v4.13.9)\n\n---\nupdated-dependencies:\n- dependency-name: commitizen\n  dependency-version: 4.13.9\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:06:22+01:00",
          "tree_id": "ca2d93f437b4cafdb76dbf8da03e5a398c6a04c5",
          "url": "https://github.com/endavis/pyproject-template/commit/6c3a844e9edb0b622c62e1e16c551b16de084aab"
        },
        "date": 1775128004906,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8670417.551799897,
            "unit": "iter/sec",
            "range": "stddev: 1.4419037624200066e-8",
            "extra": "mean: 115.33469916825509 nsec\nrounds: 88488"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8255370.378980077,
            "unit": "iter/sec",
            "range": "stddev: 2.894941272306336e-8",
            "extra": "mean: 121.13326890168516 nsec\nrounds: 85310"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5419319.520025825,
            "unit": "iter/sec",
            "range": "stddev: 1.5798569101654508e-8",
            "extra": "mean: 184.52501209879475 nsec\nrounds: 53311"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1606824.5462925455,
            "unit": "iter/sec",
            "range": "stddev: 2.747135904366762e-7",
            "extra": "mean: 622.3454840214617 nsec\nrounds: 57363"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 493980.09469980275,
            "unit": "iter/sec",
            "range": "stddev: 5.186242351209401e-7",
            "extra": "mean: 2.0243730683271988 usec\nrounds: 52674"
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
          "id": "fb6160cb5a68591bf3495be72e93f55a237e8028",
          "message": "chore(deps): bump bandit from 1.9.3 to 1.9.4 (merges PR #301)\n\nBumps [bandit](https://github.com/PyCQA/bandit) from 1.9.3 to 1.9.4.\n- [Release notes](https://github.com/PyCQA/bandit/releases)\n- [Commits](https://github.com/PyCQA/bandit/compare/1.9.3...1.9.4)\n\n---\nupdated-dependencies:\n- dependency-name: bandit\n  dependency-version: 1.9.4\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:06:29+01:00",
          "tree_id": "4384b0c0ff9782a88e411e6a4169e21bda084cbb",
          "url": "https://github.com/endavis/pyproject-template/commit/fb6160cb5a68591bf3495be72e93f55a237e8028"
        },
        "date": 1775128016020,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8656814.668114264,
            "unit": "iter/sec",
            "range": "stddev: 3.9956087875720605e-8",
            "extra": "mean: 115.5159303205728 nsec\nrounds: 83181"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8908790.363150453,
            "unit": "iter/sec",
            "range": "stddev: 2.4532090910915097e-8",
            "extra": "mean: 112.24868464032033 nsec\nrounds: 86942"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5396257.214402827,
            "unit": "iter/sec",
            "range": "stddev: 1.6538642288161534e-8",
            "extra": "mean: 185.31362762526584 nsec\nrounds: 55761"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1559228.0087210394,
            "unit": "iter/sec",
            "range": "stddev: 3.73979789621371e-7",
            "extra": "mean: 641.3430200117124 nsec\nrounds: 43152"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 488291.61384671275,
            "unit": "iter/sec",
            "range": "stddev: 7.17937575911733e-7",
            "extra": "mean: 2.0479565317988966 usec\nrounds: 47552"
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
          "id": "9e88955acf162e9bda9fcdbc43f73b89b8f63430",
          "message": "chore(deps): bump codespell from 2.4.1 to 2.4.2 (merges PR #305)\n\nBumps [codespell](https://github.com/codespell-project/codespell) from 2.4.1 to 2.4.2.\n- [Release notes](https://github.com/codespell-project/codespell/releases)\n- [Commits](https://github.com/codespell-project/codespell/compare/v2.4.1...v2.4.2)\n\n---\nupdated-dependencies:\n- dependency-name: codespell\n  dependency-version: 2.4.2\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:06:37+01:00",
          "tree_id": "b22673fc3609b17c3c409c90893d8ccd90c27237",
          "url": "https://github.com/endavis/pyproject-template/commit/9e88955acf162e9bda9fcdbc43f73b89b8f63430"
        },
        "date": 1775128019842,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8672615.345806224,
            "unit": "iter/sec",
            "range": "stddev: 3.1263120948150436e-8",
            "extra": "mean: 115.30547131708836 nsec\nrounds: 84232"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8795622.457884628,
            "unit": "iter/sec",
            "range": "stddev: 3.3329843555706627e-8",
            "extra": "mean: 113.6929199483288 nsec\nrounds: 191976"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5235525.788414557,
            "unit": "iter/sec",
            "range": "stddev: 3.39111640447305e-8",
            "extra": "mean: 191.0027837534201 nsec\nrounds: 199601"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1635984.3832920056,
            "unit": "iter/sec",
            "range": "stddev: 3.068949063137644e-7",
            "extra": "mean: 611.2527785795561 nsec\nrounds: 55424"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 496416.71044312837,
            "unit": "iter/sec",
            "range": "stddev: 5.426754173401062e-7",
            "extra": "mean: 2.0144366194025705 usec\nrounds: 39531"
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
          "id": "d65a2e46ea76df7ad322c1a544df192efcb7cd7f",
          "message": "chore(deps): bump mkdocs-material from 9.7.2 to 9.7.6 (merges PR #310)\n\nBumps [mkdocs-material](https://github.com/squidfunk/mkdocs-material) from 9.7.2 to 9.7.6.\n- [Release notes](https://github.com/squidfunk/mkdocs-material/releases)\n- [Changelog](https://github.com/squidfunk/mkdocs-material/blob/master/CHANGELOG)\n- [Commits](https://github.com/squidfunk/mkdocs-material/compare/9.7.2...9.7.6)\n\n---\nupdated-dependencies:\n- dependency-name: mkdocs-material\n  dependency-version: 9.7.6\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:06:44+01:00",
          "tree_id": "2a22aed7eaebe3a54570c14dd6d4b9bd61d9214f",
          "url": "https://github.com/endavis/pyproject-template/commit/d65a2e46ea76df7ad322c1a544df192efcb7cd7f"
        },
        "date": 1775128041368,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8830573.62867569,
            "unit": "iter/sec",
            "range": "stddev: 1.1444950754397564e-8",
            "extra": "mean: 113.24292645640607 nsec\nrounds: 87635"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8985585.128504755,
            "unit": "iter/sec",
            "range": "stddev: 1.1355207348009182e-8",
            "extra": "mean: 111.28935797711428 nsec\nrounds: 86648"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5633352.44650994,
            "unit": "iter/sec",
            "range": "stddev: 1.4103279193208912e-8",
            "extra": "mean: 177.51419061655469 nsec\nrounds: 54245"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1619816.6237950304,
            "unit": "iter/sec",
            "range": "stddev: 3.0693516282753784e-7",
            "extra": "mean: 617.3538321005271 nsec\nrounds: 45954"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 499399.76519554,
            "unit": "iter/sec",
            "range": "stddev: 4.808841403284254e-7",
            "extra": "mean: 2.0024038249366214 usec\nrounds: 49831"
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
          "id": "236f22ca46bd2be6cf36567fe02c3554d5f7233b",
          "message": "chore(deps): bump pyproject-fmt from 2.16.2 to 2.20.0 (merges PR #311)\n\nBumps [pyproject-fmt](https://github.com/tox-dev/toml-fmt) from 2.16.2 to 2.20.0.\n- [Release notes](https://github.com/tox-dev/toml-fmt/releases)\n- [Commits](https://github.com/tox-dev/toml-fmt/compare/pyproject-fmt/2.16.2...pyproject-fmt/2.20.0)\n\n---\nupdated-dependencies:\n- dependency-name: pyproject-fmt\n  dependency-version: 2.20.0\n  dependency-type: direct:production\n  update-type: version-update:semver-minor\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:06:52+01:00",
          "tree_id": "248806b0a66e96b3179ff1bdb0849a4d13a73993",
          "url": "https://github.com/endavis/pyproject-template/commit/236f22ca46bd2be6cf36567fe02c3554d5f7233b"
        },
        "date": 1775128046203,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9004125.947321063,
            "unit": "iter/sec",
            "range": "stddev: 1.9528797725125302e-8",
            "extra": "mean: 111.0601968309343 nsec\nrounds: 90433"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8863061.36601469,
            "unit": "iter/sec",
            "range": "stddev: 1.146874884632778e-8",
            "extra": "mean: 112.82783213422044 nsec\nrounds: 85485"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6293696.072967848,
            "unit": "iter/sec",
            "range": "stddev: 1.4500187663854935e-8",
            "extra": "mean: 158.88914691879 nsec\nrounds: 63804"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1749906.2018937496,
            "unit": "iter/sec",
            "range": "stddev: 2.4129466706492354e-7",
            "extra": "mean: 571.4592010233459 nsec\nrounds: 59401"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 479927.69099546474,
            "unit": "iter/sec",
            "range": "stddev: 6.414062562082417e-7",
            "extra": "mean: 2.083647221784187 usec\nrounds: 49456"
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
          "id": "488b3379c1d47ce0c31fa992355c2e2d3a0c2822",
          "message": "chore(deps): bump codecov/codecov-action from 5 to 6 (merges PR #313)\n\nBumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 5 to 6.\n- [Release notes](https://github.com/codecov/codecov-action/releases)\n- [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/codecov/codecov-action/compare/v5...v6)\n\n---\nupdated-dependencies:\n- dependency-name: codecov/codecov-action\n  dependency-version: '6'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:07:07+01:00",
          "tree_id": "078a1b4bba2b18c2c1ffee11c2eb4028bc5184c1",
          "url": "https://github.com/endavis/pyproject-template/commit/488b3379c1d47ce0c31fa992355c2e2d3a0c2822"
        },
        "date": 1775128077997,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8881520.33448895,
            "unit": "iter/sec",
            "range": "stddev: 1.1367395492398174e-8",
            "extra": "mean: 112.5933356383562 nsec\nrounds: 83879"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8986588.814621711,
            "unit": "iter/sec",
            "range": "stddev: 1.1353256613008163e-8",
            "extra": "mean: 111.27692839055247 nsec\nrounds: 87866"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5395105.857975195,
            "unit": "iter/sec",
            "range": "stddev: 1.475956792391371e-8",
            "extra": "mean: 185.3531749561081 nsec\nrounds: 53985"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1679002.3451813445,
            "unit": "iter/sec",
            "range": "stddev: 2.692786449704485e-7",
            "extra": "mean: 595.5917827452424 nsec\nrounds: 60093"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 492352.8156592758,
            "unit": "iter/sec",
            "range": "stddev: 5.80604972692398e-7",
            "extra": "mean: 2.0310638391718525 usec\nrounds: 51849"
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
          "id": "1f613446890761bbe2e417e892a123fb190fa330",
          "message": "chore(deps): bump the dev-dependencies group across 1 directory with 2 updates (merges PR #312)\n\nBumps the dev-dependencies group with 2 updates in the / directory: [pytest-cov](https://github.com/pytest-dev/pytest-cov) and [ruff](https://github.com/astral-sh/ruff).\n\n\nUpdates `pytest-cov` from 7.0.0 to 7.1.0\n- [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst)\n- [Commits](https://github.com/pytest-dev/pytest-cov/compare/v7.0.0...v7.1.0)\n\nUpdates `ruff` from 0.15.2 to 0.15.7\n- [Release notes](https://github.com/astral-sh/ruff/releases)\n- [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/astral-sh/ruff/compare/0.15.2...0.15.7)\n\n---\nupdated-dependencies:\n- dependency-name: pytest-cov\n  dependency-version: 7.1.0\n  dependency-type: direct:production\n  update-type: version-update:semver-minor\n  dependency-group: dev-dependencies\n- dependency-name: ruff\n  dependency-version: 0.15.7\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n  dependency-group: dev-dependencies\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:07:00+01:00",
          "tree_id": "2a06c2da9210c66da91ef5dca1ace1860c8a465b",
          "url": "https://github.com/endavis/pyproject-template/commit/1f613446890761bbe2e417e892a123fb190fa330"
        },
        "date": 1775128079526,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8827676.205733664,
            "unit": "iter/sec",
            "range": "stddev: 1.0928496977024734e-8",
            "extra": "mean: 113.2800950889533 nsec\nrounds: 86866"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8796748.08448101,
            "unit": "iter/sec",
            "range": "stddev: 1.403022566440868e-8",
            "extra": "mean: 113.67837187064315 nsec\nrounds: 88961"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5367700.496290636,
            "unit": "iter/sec",
            "range": "stddev: 1.3960058889585893e-8",
            "extra": "mean: 186.29951516316024 nsec\nrounds: 54245"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1682403.238095837,
            "unit": "iter/sec",
            "range": "stddev: 2.616192759099994e-7",
            "extra": "mean: 594.3878241293753 nsec\nrounds: 58542"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 498091.7609674429,
            "unit": "iter/sec",
            "range": "stddev: 5.286283111528295e-7",
            "extra": "mean: 2.007662198743664 usec\nrounds: 45062"
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
          "id": "1aa06a2cc6c4cab1deac97840d3f0e2603205636",
          "message": "chore(deps): bump hypothesis from 6.151.9 to 6.151.10 (merges PR #314)\n\nBumps [hypothesis](https://github.com/HypothesisWorks/hypothesis) from 6.151.9 to 6.151.10.\n- [Release notes](https://github.com/HypothesisWorks/hypothesis/releases)\n- [Commits](https://github.com/HypothesisWorks/hypothesis/compare/hypothesis-python-6.151.9...hypothesis-python-6.151.10)\n\n---\nupdated-dependencies:\n- dependency-name: hypothesis\n  dependency-version: 6.151.10\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:07:15+01:00",
          "tree_id": "d1b78ab4523394f7efee79f989f5afadcae55546",
          "url": "https://github.com/endavis/pyproject-template/commit/1aa06a2cc6c4cab1deac97840d3f0e2603205636"
        },
        "date": 1775128085488,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8795615.21946149,
            "unit": "iter/sec",
            "range": "stddev: 1.0841423895299467e-8",
            "extra": "mean: 113.69301351284271 nsec\nrounds: 84589"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8821599.085972844,
            "unit": "iter/sec",
            "range": "stddev: 1.4334352940680112e-8",
            "extra": "mean: 113.358132721095 nsec\nrounds: 87025"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5344043.791898444,
            "unit": "iter/sec",
            "range": "stddev: 1.523907474602267e-8",
            "extra": "mean: 187.1242150964401 nsec\nrounds: 53548"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1685717.3296174307,
            "unit": "iter/sec",
            "range": "stddev: 4.2265465819542453e-7",
            "extra": "mean: 593.2192678039013 nsec\nrounds: 55024"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 500558.6206011832,
            "unit": "iter/sec",
            "range": "stddev: 5.463968436515078e-7",
            "extra": "mean: 1.9977680112650449 usec\nrounds: 39989"
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
          "id": "048953081700c12ade7b738a8d00b45984fdc56c",
          "message": "chore(deps): bump vulture from 2.14 to 2.16 (merges PR #315)\n\nBumps [vulture](https://github.com/jendrikseipp/vulture) from 2.14 to 2.16.\n- [Release notes](https://github.com/jendrikseipp/vulture/releases)\n- [Changelog](https://github.com/jendrikseipp/vulture/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/jendrikseipp/vulture/compare/v2.14...v2.16)\n\n---\nupdated-dependencies:\n- dependency-name: vulture\n  dependency-version: '2.16'\n  dependency-type: direct:production\n  update-type: version-update:semver-minor\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:07:24+01:00",
          "tree_id": "73dbdb3a018c1137434c4bfdc4fb371a323b8692",
          "url": "https://github.com/endavis/pyproject-template/commit/048953081700c12ade7b738a8d00b45984fdc56c"
        },
        "date": 1775128092351,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8998324.713589584,
            "unit": "iter/sec",
            "range": "stddev: 1.5237029155276775e-8",
            "extra": "mean: 111.13179751001483 nsec\nrounds: 88567"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8872471.056192836,
            "unit": "iter/sec",
            "range": "stddev: 1.153559415341367e-8",
            "extra": "mean: 112.70817269130643 nsec\nrounds: 47217"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5530356.850105462,
            "unit": "iter/sec",
            "range": "stddev: 2.2095937957409967e-8",
            "extra": "mean: 180.82015810262413 nsec\nrounds: 53952"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1630684.3953995586,
            "unit": "iter/sec",
            "range": "stddev: 3.273030039938512e-7",
            "extra": "mean: 613.2394489216749 nsec\nrounds: 48478"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 496825.85052451806,
            "unit": "iter/sec",
            "range": "stddev: 5.719404469133403e-7",
            "extra": "mean: 2.0127777146544643 usec\nrounds: 44011"
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
          "id": "9d349e4febc5c9b7f5cbde142acf1a940a969081",
          "message": "chore(deps): bump pip-licenses from 5.5.1 to 5.5.5 (merges PR #316)\n\nBumps [pip-licenses](https://github.com/raimon49/pip-licenses) from 5.5.1 to 5.5.5.\n- [Release notes](https://github.com/raimon49/pip-licenses/releases)\n- [Changelog](https://github.com/raimon49/pip-licenses/blob/master/CHANGELOG.md)\n- [Commits](https://github.com/raimon49/pip-licenses/compare/v-5.5.1...v-5.5.5)\n\n---\nupdated-dependencies:\n- dependency-name: pip-licenses\n  dependency-version: 5.5.5\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T12:07:32+01:00",
          "tree_id": "bcd6706458bf8840da06e1e0abc2b37b03339270",
          "url": "https://github.com/endavis/pyproject-template/commit/9d349e4febc5c9b7f5cbde142acf1a940a969081"
        },
        "date": 1775128098075,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 7436045.899894581,
            "unit": "iter/sec",
            "range": "stddev: 1.1499186836106471e-8",
            "extra": "mean: 134.4800736119954 nsec\nrounds: 86942"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 7135861.838921922,
            "unit": "iter/sec",
            "range": "stddev: 1.4111033720854157e-8",
            "extra": "mean: 140.1372423644176 nsec\nrounds: 84732"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5200288.4396295175,
            "unit": "iter/sec",
            "range": "stddev: 2.745614292974354e-8",
            "extra": "mean: 192.2970257532951 nsec\nrounds: 194591"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1548403.1037410446,
            "unit": "iter/sec",
            "range": "stddev: 2.7762868640815016e-7",
            "extra": "mean: 645.8266568853638 nsec\nrounds: 64231"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 474233.7635704471,
            "unit": "iter/sec",
            "range": "stddev: 5.1249378280118e-7",
            "extra": "mean: 2.1086647067706106 usec\nrounds: 56297"
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
          "id": "e192d0eaf79e84b24cd100809cfc5a3319eeb396",
          "message": "chore: update pygments and requests for CVE fixes (merges PR #321, addresses #319)\n\n- pygments 2.19.2 → 2.20.0 (CVE-2026-4539)\n- requests 2.32.5 → 2.33.1 (CVE-2026-25645)\n\nAddresses #319",
          "timestamp": "2026-04-02T15:21:34+01:00",
          "tree_id": "3b2d50d14f44b86f075e3278e127207672a12d65",
          "url": "https://github.com/endavis/pyproject-template/commit/e192d0eaf79e84b24cd100809cfc5a3319eeb396"
        },
        "date": 1775139718646,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8617030.737703377,
            "unit": "iter/sec",
            "range": "stddev: 2.4358764438916854e-8",
            "extra": "mean: 116.04925529910798 nsec\nrounds: 84732"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8617753.489039166,
            "unit": "iter/sec",
            "range": "stddev: 2.4410306114081544e-8",
            "extra": "mean: 116.0395225126699 nsec\nrounds: 87018"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5197385.424050143,
            "unit": "iter/sec",
            "range": "stddev: 4.168034962928073e-8",
            "extra": "mean: 192.404433847189 nsec\nrounds: 184129"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1672572.9525549617,
            "unit": "iter/sec",
            "range": "stddev: 2.6527072004553285e-7",
            "extra": "mean: 597.8812454622301 nsec\nrounds: 58002"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 501858.3479442095,
            "unit": "iter/sec",
            "range": "stddev: 6.219196340367717e-7",
            "extra": "mean: 1.9925941335764488 usec\nrounds: 50184"
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
          "id": "dca7e6076ee6a124ece1843bcd2ac4140435fb1c",
          "message": "chore(deps): bump the dev-dependencies group across 1 directory with 2 updates (merges PR #318)\n\nBumps the dev-dependencies group with 2 updates in the / directory: [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy).\n\n\nUpdates `ruff` from 0.15.7 to 0.15.8\n- [Release notes](https://github.com/astral-sh/ruff/releases)\n- [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/astral-sh/ruff/compare/0.15.7...0.15.8)\n\nUpdates `mypy` from 1.19.1 to 1.20.0\n- [Changelog](https://github.com/python/mypy/blob/master/CHANGELOG.md)\n- [Commits](https://github.com/python/mypy/compare/v1.19.1...v1.20.0)\n\n---\nupdated-dependencies:\n- dependency-name: ruff\n  dependency-version: 0.15.8\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n  dependency-group: dev-dependencies\n- dependency-name: mypy\n  dependency-version: 1.20.0\n  dependency-type: direct:production\n  update-type: version-update:semver-minor\n  dependency-group: dev-dependencies\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-02T15:27:32+01:00",
          "tree_id": "a1297d11c9319c2a4da70daf1d55b2269a2cebb2",
          "url": "https://github.com/endavis/pyproject-template/commit/dca7e6076ee6a124ece1843bcd2ac4140435fb1c"
        },
        "date": 1775140077763,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8757112.396261673,
            "unit": "iter/sec",
            "range": "stddev: 1.0834846481470944e-8",
            "extra": "mean: 114.19289313071855 nsec\nrounds: 86498"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8888717.989288853,
            "unit": "iter/sec",
            "range": "stddev: 1.1617330351404918e-8",
            "extra": "mean: 112.50216298964902 nsec\nrounds: 88803"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5411053.173608781,
            "unit": "iter/sec",
            "range": "stddev: 1.5415967174234234e-8",
            "extra": "mean: 184.80690688409413 nsec\nrounds: 54964"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1648190.0775317673,
            "unit": "iter/sec",
            "range": "stddev: 4.071787401795916e-7",
            "extra": "mean: 606.7261377386408 nsec\nrounds: 59592"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 505436.5681341229,
            "unit": "iter/sec",
            "range": "stddev: 4.887067305672338e-7",
            "extra": "mean: 1.9784876343467088 usec\nrounds: 52646"
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
          "id": "e935339996bf17fdef09d90ddaac49a8da86e4b7",
          "message": "fix: block all git push to protected branches, not just force push (merges PR #308, addresses #307)\n\nAlso fixes false positive where git stash push was matched as git push.\n\nCo-authored-by: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-04-02T15:31:14+01:00",
          "tree_id": "43e08ae5033e0a3d23c892e553dbd19c633e5337",
          "url": "https://github.com/endavis/pyproject-template/commit/e935339996bf17fdef09d90ddaac49a8da86e4b7"
        },
        "date": 1775140302116,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8733923.085942661,
            "unit": "iter/sec",
            "range": "stddev: 2.0440638971668242e-8",
            "extra": "mean: 114.49608499638728 nsec\nrounds: 90498"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9197553.125322312,
            "unit": "iter/sec",
            "range": "stddev: 1.486908782794369e-8",
            "extra": "mean: 108.72456906466162 nsec\nrounds: 90408"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5223558.030268149,
            "unit": "iter/sec",
            "range": "stddev: 3.07993543840657e-8",
            "extra": "mean: 191.44039258403058 nsec\nrounds: 194932"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1657548.2941188205,
            "unit": "iter/sec",
            "range": "stddev: 2.6302662270262894e-7",
            "extra": "mean: 603.30067217234 nsec\nrounds: 59806"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 499812.6977671221,
            "unit": "iter/sec",
            "range": "stddev: 4.7682763159162604e-7",
            "extra": "mean: 2.0007494896936975 usec\nrounds: 55359"
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
          "id": "850de17a89e739c0faead647443205cc1e1e07d1",
          "message": "feat: add temporary files policy for AI agents (merges PR #322, addresses #317)\n\nfeat: add temporary files policy for AI agents to AGENTS.md\n\nAddresses #317",
          "timestamp": "2026-04-02T15:42:18+01:00",
          "tree_id": "f7614a7a5334698ccd91630ad52f6269aef2734f",
          "url": "https://github.com/endavis/pyproject-template/commit/850de17a89e739c0faead647443205cc1e1e07d1"
        },
        "date": 1775140963278,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8576688.137181072,
            "unit": "iter/sec",
            "range": "stddev: 2.5650132798293676e-8",
            "extra": "mean: 116.595122033745 nsec\nrounds: 188324"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8768270.03912105,
            "unit": "iter/sec",
            "range": "stddev: 2.7407298572263997e-8",
            "extra": "mean: 114.04758242370944 nsec\nrounds: 89598"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5286004.664046274,
            "unit": "iter/sec",
            "range": "stddev: 1.6588161931039588e-8",
            "extra": "mean: 189.17879637936807 nsec\nrounds: 52367"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1680609.6124821152,
            "unit": "iter/sec",
            "range": "stddev: 4.671802033650337e-7",
            "extra": "mean: 595.0221827680056 nsec\nrounds: 57432"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 501405.41819664487,
            "unit": "iter/sec",
            "range": "stddev: 5.375728631835488e-7",
            "extra": "mean: 1.9943940845246562 usec\nrounds: 57003"
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
          "id": "dbc9884003bd0fdc90cd81f978b87a56d4e862cc",
          "message": "fix: ensure tmp/ directory exists in benchmark CI workflow (merges PR #323, addresses #302)\n\nfix: ensure tmp/ directory exists before benchmark results are written\n\nAddresses #302",
          "timestamp": "2026-04-02T16:24:12+01:00",
          "tree_id": "ef81a6b8348a8021d2454e152ecba328acc90fdd",
          "url": "https://github.com/endavis/pyproject-template/commit/dbc9884003bd0fdc90cd81f978b87a56d4e862cc"
        },
        "date": 1775143485526,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8728938.237929476,
            "unit": "iter/sec",
            "range": "stddev: 2.6147850131389897e-8",
            "extra": "mean: 114.56147044949216 nsec\nrounds: 198060"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8824487.488376206,
            "unit": "iter/sec",
            "range": "stddev: 1.0764640102900196e-8",
            "extra": "mean: 113.32102870758447 nsec\nrounds: 87712"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5218797.625415371,
            "unit": "iter/sec",
            "range": "stddev: 2.8228318211772188e-8",
            "extra": "mean: 191.6150178213528 nsec\nrounds: 197239"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1632351.7689504097,
            "unit": "iter/sec",
            "range": "stddev: 2.5443274722814504e-7",
            "extra": "mean: 612.6130525425856 nsec\nrounds: 55085"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 493165.5322141699,
            "unit": "iter/sec",
            "range": "stddev: 5.251655780708425e-7",
            "extra": "mean: 2.0277167293308 usec\nrounds: 48406"
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
          "id": "67fa7caf8e13b0e21fc53798b636e096a570bd17",
          "message": "docs: add pre-commit exclude pattern guidance for large/generated dirs (merges PR #324, addresses #294)\n\nAddresses #294",
          "timestamp": "2026-04-02T16:34:37+01:00",
          "tree_id": "e91a1246469f026285d9206bdd4ae78a6cfb1ed5",
          "url": "https://github.com/endavis/pyproject-template/commit/67fa7caf8e13b0e21fc53798b636e096a570bd17"
        },
        "date": 1775144102271,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8028010.666531343,
            "unit": "iter/sec",
            "range": "stddev: 1.2844789793973327e-8",
            "extra": "mean: 124.56386040554047 nsec\nrounds: 80691"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8555061.455777109,
            "unit": "iter/sec",
            "range": "stddev: 1.0720310573196015e-8",
            "extra": "mean: 116.88986749764545 nsec\nrounds: 86942"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5405940.513984225,
            "unit": "iter/sec",
            "range": "stddev: 2.9791131609054912e-8",
            "extra": "mean: 184.9816877217155 nsec\nrounds: 54304"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1626518.8868520118,
            "unit": "iter/sec",
            "range": "stddev: 2.7748832059429893e-7",
            "extra": "mean: 614.8099527669269 nsec\nrounds: 61611"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 506261.6526102393,
            "unit": "iter/sec",
            "range": "stddev: 4.610588757791842e-7",
            "extra": "mean: 1.9752631763517747 usec\nrounds: 53865"
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
          "id": "75cbe9b37181359365d57b4e54cb59b8a47507fb",
          "message": "feat: add reusable GitHub Release binary installer framework (merges PR #325, addresses #293)\n\n* feat: add reusable GitHub Release binary installer framework\n\nAddresses #293\n\n* fix: skip executable permissions test on Windows\n\nchmod is a no-op on Windows, so the permission assertion fails.",
          "timestamp": "2026-04-02T17:22:23+01:00",
          "tree_id": "06452b15d9eca8ca3a224b93f9b099137ad248a9",
          "url": "https://github.com/endavis/pyproject-template/commit/75cbe9b37181359365d57b4e54cb59b8a47507fb"
        },
        "date": 1775146967747,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8522999.135197617,
            "unit": "iter/sec",
            "range": "stddev: 2.546878533790938e-8",
            "extra": "mean: 117.32959069188192 nsec\nrounds: 87367"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8749033.081661636,
            "unit": "iter/sec",
            "range": "stddev: 2.4579529090002195e-8",
            "extra": "mean: 114.29834481893144 nsec\nrounds: 87936"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5622823.934611536,
            "unit": "iter/sec",
            "range": "stddev: 1.4188335996232979e-8",
            "extra": "mean: 177.84657880615055 nsec\nrounds: 53987"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1565625.1915514101,
            "unit": "iter/sec",
            "range": "stddev: 3.8308253629604013e-7",
            "extra": "mean: 638.7224767436703 nsec\nrounds: 68106"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 526958.7731716314,
            "unit": "iter/sec",
            "range": "stddev: 4.1064808493592077e-7",
            "extra": "mean: 1.897681661093245 usec\nrounds: 37036"
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
          "id": "56e39e98576f4fa73bbd2a60c2b259d37509853e",
          "message": "fix: restore mutation testing workflow on mutmut 3.x (merges PR #335, addresses #330)\n\nAddresses #330\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-06T17:54:12+01:00",
          "tree_id": "4bcad0b3433995e3b39222b23c4d8f801743d26b",
          "url": "https://github.com/endavis/pyproject-template/commit/56e39e98576f4fa73bbd2a60c2b259d37509853e"
        },
        "date": 1775494482038,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8188607.644204087,
            "unit": "iter/sec",
            "range": "stddev: 3.1032857194504356e-8",
            "extra": "mean: 122.12088348228554 nsec\nrounds: 84382"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8800635.036275884,
            "unit": "iter/sec",
            "range": "stddev: 1.2667434864480236e-8",
            "extra": "mean: 113.62816386295283 nsec\nrounds: 88098"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5380637.971877145,
            "unit": "iter/sec",
            "range": "stddev: 1.6474012294722172e-8",
            "extra": "mean: 185.85156727263134 nsec\nrounds: 54413"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1657278.9116779447,
            "unit": "iter/sec",
            "range": "stddev: 2.7869868516887166e-7",
            "extra": "mean: 603.3987356947239 nsec\nrounds: 54101"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 497353.21045626537,
            "unit": "iter/sec",
            "range": "stddev: 5.370972183307006e-7",
            "extra": "mean: 2.0106435003859993 usec\nrounds: 47195"
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
          "id": "d2c5b22bf3a3a0d32fe2fb4bbee6b33264d26e6e",
          "message": "chore(deps): bump ruff from 0.15.8 to 0.15.9 in the dev-dependencies group across 1 directory (merges PR #331)\n\nchore(deps): bump ruff in the dev-dependencies group\n\nBumps the dev-dependencies group with 1 update: [ruff](https://github.com/astral-sh/ruff).\n\n\nUpdates `ruff` from 0.15.8 to 0.15.9\n- [Release notes](https://github.com/astral-sh/ruff/releases)\n- [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/astral-sh/ruff/compare/0.15.8...0.15.9)\n\n---\nupdated-dependencies:\n- dependency-name: ruff\n  dependency-version: 0.15.9\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n  dependency-group: dev-dependencies\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-07T09:54:02+01:00",
          "tree_id": "a03f41f272508b394fa00a34a1401aa489b97d22",
          "url": "https://github.com/endavis/pyproject-template/commit/d2c5b22bf3a3a0d32fe2fb4bbee6b33264d26e6e"
        },
        "date": 1775552071551,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8421160.937145447,
            "unit": "iter/sec",
            "range": "stddev: 2.4025367732752085e-8",
            "extra": "mean: 118.74847274192742 nsec\nrounds: 87405"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8931462.185339836,
            "unit": "iter/sec",
            "range": "stddev: 1.3187802674667761e-8",
            "extra": "mean: 111.96375008354252 nsec\nrounds: 89598"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5320228.845301308,
            "unit": "iter/sec",
            "range": "stddev: 3.0761476773067336e-8",
            "extra": "mean: 187.96183943913897 nsec\nrounds: 195351"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1678531.1995465136,
            "unit": "iter/sec",
            "range": "stddev: 2.1030741485247953e-7",
            "extra": "mean: 595.758958945874 nsec\nrounds: 50564"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 498886.8807351347,
            "unit": "iter/sec",
            "range": "stddev: 7.034656512977336e-7",
            "extra": "mean: 2.0044624114517706 usec\nrounds: 50667"
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
          "id": "16df0363760787646ce4c5b759824986f09c87c2",
          "message": "chore(deps): bump pyproject-fmt from 2.20.0 to 2.21.0 (merges PR #332)\n\nBumps [pyproject-fmt](https://github.com/tox-dev/toml-fmt) from 2.20.0 to 2.21.0.\n- [Release notes](https://github.com/tox-dev/toml-fmt/releases)\n- [Commits](https://github.com/tox-dev/toml-fmt/compare/pyproject-fmt/2.20.0...pyproject-fmt/2.21.0)\n\n---\nupdated-dependencies:\n- dependency-name: pyproject-fmt\n  dependency-version: 2.21.0\n  dependency-type: direct:production\n  update-type: version-update:semver-minor\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-07T10:02:12+01:00",
          "tree_id": "253ec5c2a99221c56b161ac240e890099b8bf66b",
          "url": "https://github.com/endavis/pyproject-template/commit/16df0363760787646ce4c5b759824986f09c87c2"
        },
        "date": 1775552557022,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8923151.033095391,
            "unit": "iter/sec",
            "range": "stddev: 7.46938303338607e-9",
            "extra": "mean: 112.0680347436757 nsec\nrounds: 86289"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8806622.164555758,
            "unit": "iter/sec",
            "range": "stddev: 2.0821028665560285e-8",
            "extra": "mean: 113.55091444989273 nsec\nrounds: 86686"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5530708.5188584225,
            "unit": "iter/sec",
            "range": "stddev: 2.379011053988079e-8",
            "extra": "mean: 180.8086606969494 nsec\nrounds: 56507"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1527497.9767447992,
            "unit": "iter/sec",
            "range": "stddev: 2.519068610418023e-7",
            "extra": "mean: 654.6653515908854 nsec\nrounds: 63368"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 506086.2069069034,
            "unit": "iter/sec",
            "range": "stddev: 5.2120675369725e-7",
            "extra": "mean: 1.9759479439516796 usec\nrounds: 50023"
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
          "id": "21776b575ef44c06c305f7a9c2fc6afef8a4fddf",
          "message": "chore(deps): bump cyclonedx-bom from 7.2.2 to 7.3.0 (merges PR #333)\n\nBumps [cyclonedx-bom](https://github.com/CycloneDX/cyclonedx-python) from 7.2.2 to 7.3.0.\n- [Release notes](https://github.com/CycloneDX/cyclonedx-python/releases)\n- [Changelog](https://github.com/CycloneDX/cyclonedx-python/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/CycloneDX/cyclonedx-python/compare/v7.2.2...v7.3.0)\n\n---\nupdated-dependencies:\n- dependency-name: cyclonedx-bom\n  dependency-version: 7.3.0\n  dependency-type: direct:production\n  update-type: version-update:semver-minor\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-07T10:07:37+01:00",
          "tree_id": "3dff9cba082505c1fac20d68406de5673fae7fa2",
          "url": "https://github.com/endavis/pyproject-template/commit/21776b575ef44c06c305f7a9c2fc6afef8a4fddf"
        },
        "date": 1775552886406,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8853275.616640233,
            "unit": "iter/sec",
            "range": "stddev: 1.3928187796920135e-8",
            "extra": "mean: 112.95254358967921 nsec\nrounds: 81613"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9114431.933998872,
            "unit": "iter/sec",
            "range": "stddev: 1.508193824508626e-8",
            "extra": "mean: 109.71610817233449 nsec\nrounds: 87712"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5328649.524946965,
            "unit": "iter/sec",
            "range": "stddev: 1.818666036315481e-8",
            "extra": "mean: 187.66480987693646 nsec\nrounds: 52729"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1629888.7049537997,
            "unit": "iter/sec",
            "range": "stddev: 2.7825613111294745e-7",
            "extra": "mean: 613.5388244366941 nsec\nrounds: 57232"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 498819.9265399284,
            "unit": "iter/sec",
            "range": "stddev: 5.247968723480032e-7",
            "extra": "mean: 2.004731460782881 usec\nrounds: 42046"
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
          "id": "efeb6699a56d8d22cd5caf772b7855d770810d9b",
          "message": "chore(deps): bump hypothesis from 6.151.10 to 6.151.11 (merges PR #334)\n\nBumps [hypothesis](https://github.com/HypothesisWorks/hypothesis) from 6.151.10 to 6.151.11.\n- [Release notes](https://github.com/HypothesisWorks/hypothesis/releases)\n- [Commits](https://github.com/HypothesisWorks/hypothesis/compare/hypothesis-python-6.151.10...hypothesis-python-6.151.11)\n\n---\nupdated-dependencies:\n- dependency-name: hypothesis\n  dependency-version: 6.151.11\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-07T11:19:02+01:00",
          "tree_id": "3096a599f870ad1cf7533481f89ddfbce7828afb",
          "url": "https://github.com/endavis/pyproject-template/commit/efeb6699a56d8d22cd5caf772b7855d770810d9b"
        },
        "date": 1775557170022,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8910504.212006671,
            "unit": "iter/sec",
            "range": "stddev: 2.4164888112812132e-8",
            "extra": "mean: 112.22709469712457 nsec\nrounds: 86349"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9045062.538815018,
            "unit": "iter/sec",
            "range": "stddev: 1.0969341281299481e-8",
            "extra": "mean: 110.55755509801139 nsec\nrounds: 89840"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5356564.73393028,
            "unit": "iter/sec",
            "range": "stddev: 2.630806873569133e-8",
            "extra": "mean: 186.68681322297184 nsec\nrounds: 54723"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1686188.8429913237,
            "unit": "iter/sec",
            "range": "stddev: 3.3038133678825744e-7",
            "extra": "mean: 593.053384356396 nsec\nrounds: 53836"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 507540.35160404484,
            "unit": "iter/sec",
            "range": "stddev: 5.561364414438025e-7",
            "extra": "mean: 1.9702866911755323 usec\nrounds: 54693"
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
          "id": "c9b369f4f59f00b359061d13efbbdd201bebd402",
          "message": "docs: add git pull reminder before branching in AGENTS.md Flow (merges PR #336, addresses #329)\n\ndocs: add git pull reminder before branching in Critical Reminders Flow\n\nAddresses #329",
          "timestamp": "2026-04-07T11:33:40+01:00",
          "tree_id": "09eae13965dfeaad51dff82d158b360a6e09df67",
          "url": "https://github.com/endavis/pyproject-template/commit/c9b369f4f59f00b359061d13efbbdd201bebd402"
        },
        "date": 1775558043202,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8957227.68225561,
            "unit": "iter/sec",
            "range": "stddev: 1.1207037630127527e-8",
            "extra": "mean: 111.64168596283574 nsec\nrounds: 82659"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8784388.760727834,
            "unit": "iter/sec",
            "range": "stddev: 1.1135090486265641e-8",
            "extra": "mean: 113.838313312211 nsec\nrounds: 85493"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5986108.902179079,
            "unit": "iter/sec",
            "range": "stddev: 1.5076350352819906e-8",
            "extra": "mean: 167.05342591344728 nsec\nrounds: 59120"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1797381.5093538573,
            "unit": "iter/sec",
            "range": "stddev: 2.3235574789485587e-7",
            "extra": "mean: 556.3649090612327 nsec\nrounds: 56288"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 501490.9140295485,
            "unit": "iter/sec",
            "range": "stddev: 5.093517745268903e-7",
            "extra": "mean: 1.9940540736119472 usec\nrounds: 55258"
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
          "id": "aa6337c7ac254e5e6256ce00c76323987dde24f3",
          "message": "fix: replace Unicode checkmark with ASCII marker in direct-stdout task output (merges PR #337, addresses #328)\n\nAddresses #328",
          "timestamp": "2026-04-07T11:47:05+01:00",
          "tree_id": "3847f038ebd6e4f1bb4a17c5a3b6f2a44b8b5802",
          "url": "https://github.com/endavis/pyproject-template/commit/aa6337c7ac254e5e6256ce00c76323987dde24f3"
        },
        "date": 1775558853127,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8673523.979971722,
            "unit": "iter/sec",
            "range": "stddev: 5.4125648879559805e-8",
            "extra": "mean: 115.29339197183613 nsec\nrounds: 89759"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8881902.121657511,
            "unit": "iter/sec",
            "range": "stddev: 1.4581367936575283e-8",
            "extra": "mean: 112.58849583149687 nsec\nrounds: 89119"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5220907.768633323,
            "unit": "iter/sec",
            "range": "stddev: 1.8265143462219372e-8",
            "extra": "mean: 191.5375724520355 nsec\nrounds: 52897"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1610713.0845057322,
            "unit": "iter/sec",
            "range": "stddev: 2.686554325749458e-7",
            "extra": "mean: 620.8430350628602 nsec\nrounds: 59663"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 482102.1813139261,
            "unit": "iter/sec",
            "range": "stddev: 5.341842307541136e-7",
            "extra": "mean: 2.074249067437509 usec\nrounds: 57101"
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
          "id": "595b68f88c764036ea4f8803951eb5e12c0ebd23",
          "message": "fix: skip benchmark workflow gracefully when tests/benchmarks/ is missing (merges PR #338, addresses #327)\n\nAddresses #327",
          "timestamp": "2026-04-07T12:04:11+01:00",
          "tree_id": "58ef48b43bc7ab62f78add594e98fd195d3a05ac",
          "url": "https://github.com/endavis/pyproject-template/commit/595b68f88c764036ea4f8803951eb5e12c0ebd23"
        },
        "date": 1775559875612,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8356566.650048209,
            "unit": "iter/sec",
            "range": "stddev: 5.413339221445576e-8",
            "extra": "mean: 119.66637039797091 nsec\nrounds: 88332"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9230342.626846008,
            "unit": "iter/sec",
            "range": "stddev: 3.125326230274287e-8",
            "extra": "mean: 108.33834023577283 nsec\nrounds: 87169"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5417779.742981614,
            "unit": "iter/sec",
            "range": "stddev: 1.970699243909538e-8",
            "extra": "mean: 184.5774556072413 nsec\nrounds: 54964"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1651371.5645145136,
            "unit": "iter/sec",
            "range": "stddev: 2.846199764763096e-7",
            "extra": "mean: 605.5572358689546 nsec\nrounds: 58984"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 494490.9043988423,
            "unit": "iter/sec",
            "range": "stddev: 6.659710204075393e-7",
            "extra": "mean: 2.022281888512611 usec\nrounds: 51978"
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
          "id": "117ecd05ad5e548735a23f52e4bedfeddd35b6bf",
          "message": "feat: add archive extraction and custom URL support to install_tools framework (merges PR #339, addresses #326)\n\nAddresses #326",
          "timestamp": "2026-04-07T12:53:09+01:00",
          "tree_id": "80808c89bb37f21b3ea45d610d0497ac172b006b",
          "url": "https://github.com/endavis/pyproject-template/commit/117ecd05ad5e548735a23f52e4bedfeddd35b6bf"
        },
        "date": 1775562815004,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8849484.617671942,
            "unit": "iter/sec",
            "range": "stddev: 8.70657834586307e-9",
            "extra": "mean: 113.0009309246161 nsec\nrounds: 86022"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8279783.304110707,
            "unit": "iter/sec",
            "range": "stddev: 3.79166889830101e-8",
            "extra": "mean: 120.77610769155334 nsec\nrounds: 92115"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5692966.98363091,
            "unit": "iter/sec",
            "range": "stddev: 1.2212629779603913e-8",
            "extra": "mean: 175.65533102076964 nsec\nrounds: 55057"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1852397.2462099444,
            "unit": "iter/sec",
            "range": "stddev: 1.789310268254895e-7",
            "extra": "mean: 539.8410098298448 nsec\nrounds: 59337"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 527780.7014771979,
            "unit": "iter/sec",
            "range": "stddev: 3.4828024319377935e-7",
            "extra": "mean: 1.8947263460015007 usec\nrounds: 48068"
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
          "id": "5cd4ae76328b376f0e3b07968e5f42a4a60273a3",
          "message": "docs: document tooling roles and architectural boundaries (merges PR #347, addresses #340)\n\nAdd a source-of-truth doc for the roles of doit, uv, gh, and git, and\nthe boundary between dev tooling and the published runtime package.\nCodify doit as a development task runner only via a new Scope section\nin ADR-9002, with a current-state callout about #65.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-08T11:47:32+01:00",
          "tree_id": "a6dc5cdcb191afbcac3bec91432e9d87cc6fee90",
          "url": "https://github.com/endavis/pyproject-template/commit/5cd4ae76328b376f0e3b07968e5f42a4a60273a3"
        },
        "date": 1775645280293,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8603078.820334164,
            "unit": "iter/sec",
            "range": "stddev: 3.0149771836452075e-8",
            "extra": "mean: 116.23745648318464 nsec\nrounds: 90827"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9059521.889459325,
            "unit": "iter/sec",
            "range": "stddev: 1.3190719801695913e-8",
            "extra": "mean: 110.38110092360296 nsec\nrounds: 88889"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5352669.0127698975,
            "unit": "iter/sec",
            "range": "stddev: 1.7325246832512503e-8",
            "extra": "mean: 186.82268558251843 nsec\nrounds: 54275"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1684848.121245208,
            "unit": "iter/sec",
            "range": "stddev: 2.9074812718967716e-7",
            "extra": "mean: 593.5253079434469 nsec\nrounds: 58855"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 498847.4507590762,
            "unit": "iter/sec",
            "range": "stddev: 5.219044172125778e-7",
            "extra": "mean: 2.0046208484744987 usec\nrounds: 50795"
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
          "id": "c118c9747f8fde6a7b90d6c6a9ed48ddc406b540",
          "message": "docs: add AI agent architectural conventions guide (merges PR #350, addresses #343)\n\nAdd an AI-facing counterpart to the human-facing tooling-roles doc,\nstating the doit/uv/gh/git layering rules in imperative DO/DO NOT form\nand documenting 5 concrete AI failure modes with correct alternatives.\nCross-link from AGENTS.md (Pre-Action Checks and Sources of Truth\ntables) and AI_SETUP.md so agents reach it via existing paths.\nRestructure the mkdocs Development nav with a nested AI subsection.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-08T12:47:33+01:00",
          "tree_id": "3c7066eff9191d034c6b33e290f4bf1952670729",
          "url": "https://github.com/endavis/pyproject-template/commit/c118c9747f8fde6a7b90d6c6a9ed48ddc406b540"
        },
        "date": 1775648882083,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8717893.552177658,
            "unit": "iter/sec",
            "range": "stddev: 1.310237481377344e-8",
            "extra": "mean: 114.70660819782644 nsec\nrounds: 87169"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8874988.216872536,
            "unit": "iter/sec",
            "range": "stddev: 1.5780549399467695e-8",
            "extra": "mean: 112.67620593556019 nsec\nrounds: 89358"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5388478.786477845,
            "unit": "iter/sec",
            "range": "stddev: 1.5794430146819824e-8",
            "extra": "mean: 185.5811333078747 nsec\nrounds: 54663"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1676340.9409367878,
            "unit": "iter/sec",
            "range": "stddev: 3.464976048455612e-7",
            "extra": "mean: 596.5373603779975 nsec\nrounds: 56584"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 500800.2955021045,
            "unit": "iter/sec",
            "range": "stddev: 8.546480643747749e-7",
            "extra": "mean: 1.996803933586732 usec\nrounds: 50539"
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
          "id": "276259d74765bf2b875f799a2c755c9ddc3aeb20",
          "message": "docs: document slash commands and dual-agent workflow (merges PR #351, addresses #344)\n\nAdd a single reference page covering the ten slash commands that ship\nunder .claude/commands/ and .gemini/commands/, the single-agent and\ndual-agent workflows built on top of them, and how to add new commands.\nCross-link from AGENTS.md Sources of Truth and AI_SETUP.md so\ncontributors can discover the workflow from either entry point.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-08T14:29:07+01:00",
          "tree_id": "5b2178e0637c8b659713aba1a5eda96346854972",
          "url": "https://github.com/endavis/pyproject-template/commit/276259d74765bf2b875f799a2c755c9ddc3aeb20"
        },
        "date": 1775654979923,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8960171.27248787,
            "unit": "iter/sec",
            "range": "stddev: 1.1013030530278131e-8",
            "extra": "mean: 111.6050095013799 nsec\nrounds: 84725"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8904366.17915838,
            "unit": "iter/sec",
            "range": "stddev: 1.2087739400893152e-8",
            "extra": "mean: 112.30445602524824 nsec\nrounds: 87789"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5441290.137402907,
            "unit": "iter/sec",
            "range": "stddev: 1.4174506972934403e-8",
            "extra": "mean: 183.7799445991854 nsec\nrounds: 54873"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1696187.937912317,
            "unit": "iter/sec",
            "range": "stddev: 2.640617399459359e-7",
            "extra": "mean: 589.5573112203643 nsec\nrounds: 56010"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 474162.80983405816,
            "unit": "iter/sec",
            "range": "stddev: 5.249988159412179e-7",
            "extra": "mean: 2.108980247417481 usec\nrounds: 48905"
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
          "id": "6e30481dbd889744cc1af597b8437640cebfd237",
          "message": "docs: clarify AI agent parity, file relationships, and enforcement (merges PR #352, addresses #345)\n\nAdd an agent comparison table, per-agent enforcement-hook callouts, a\nnew \"Context files and precedence\" section, and a Codex parity\nstatement to AI_SETUP.md. Closes the cross-cutting gaps a new adopter\nhits when trying to choose an agent or understand which file wins on\nconflict.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-08T15:26:21+01:00",
          "tree_id": "268fc7f4e4c83ba437d5296a675695775a99591c",
          "url": "https://github.com/endavis/pyproject-template/commit/6e30481dbd889744cc1af597b8437640cebfd237"
        },
        "date": 1775658412215,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 7598526.16335359,
            "unit": "iter/sec",
            "range": "stddev: 4.151512750192131e-8",
            "extra": "mean: 131.60446888014036 nsec\nrounds: 84303"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8928185.7293777,
            "unit": "iter/sec",
            "range": "stddev: 1.197341863933405e-8",
            "extra": "mean: 112.00483841969769 nsec\nrounds: 87944"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5379377.941922918,
            "unit": "iter/sec",
            "range": "stddev: 1.5835023175226202e-8",
            "extra": "mean: 185.89509991605814 nsec\nrounds: 53695"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1655866.486097038,
            "unit": "iter/sec",
            "range": "stddev: 3.0421510320398796e-7",
            "extra": "mean: 603.9134244192907 nsec\nrounds: 35495"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 494458.58990741015,
            "unit": "iter/sec",
            "range": "stddev: 5.57349187828406e-7",
            "extra": "mean: 2.022414051270209 usec\nrounds: 47284"
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
          "id": "dcfd4409c17d886258c1cb0440f436aa95b282f1",
          "message": "docs: add AI agent first-5-minutes walkthrough and clarify Claude as primary agent (merges PR #353, addresses #346)\n\nAdds a narrative First 5 Minutes onboarding walkthrough at\ndocs/development/ai/first-5-minutes.md covering the plan → implement →\nreview → PR → merge loop, and wires it into the AI entry points via\nmkdocs.yml, docs/index.md, docs/development/AI_SETUP.md,\ndocs/development/ai/slash-commands.md, and the AGENTS.md Sources of\nTruth table.\n\nAlso clarifies template framing in README.md, AI_SETUP.md, and\ndocs/index.md to explicitly name Claude Code as the primary agent\n(the only one shipping the full slash-command workflow), with Gemini\nCLI and Codex CLI documented in their narrower supporting roles. This\nframing was added as an in-scope addendum so readers arriving from the\nREADME land on the walkthrough with the correct mental model.\n\nDocumentation-only change. No code, behavior, or APIs affected.\n\nAddresses #346",
          "timestamp": "2026-04-09T10:36:54+01:00",
          "tree_id": "4b8322322f4b5a35b7b3f07c395240d0cf70c8a1",
          "url": "https://github.com/endavis/pyproject-template/commit/dcfd4409c17d886258c1cb0440f436aa95b282f1"
        },
        "date": 1775727446474,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8622254.99896309,
            "unit": "iter/sec",
            "range": "stddev: 5.970779072481284e-8",
            "extra": "mean: 115.97894055792361 nsec\nrounds: 88254"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8908120.049655348,
            "unit": "iter/sec",
            "range": "stddev: 3.832025730262343e-8",
            "extra": "mean: 112.25713106983663 nsec\nrounds: 90654"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5002384.630271373,
            "unit": "iter/sec",
            "range": "stddev: 4.622150363408391e-8",
            "extra": "mean: 199.9046602591515 nsec\nrounds: 52231"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1689085.1912128732,
            "unit": "iter/sec",
            "range": "stddev: 2.4586600183855464e-7",
            "extra": "mean: 592.0364497908687 nsec\nrounds: 59095"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 437345.66725345835,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010477686301166854",
            "extra": "mean: 2.2865208801084616 usec\nrounds: 60129"
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
          "id": "3bd06d1fc91ef7a5f7bdbc677883376f48fc4f65",
          "message": "fix: bump pymdown-extensions to 10.21.2 to fix docs_build crash with pygments 2.20 (merges PR #355, addresses #349)\n\n`doit docs_build` was crashing on every branch with\n`AttributeError: 'NoneType' object has no attribute 'replace'` raised\nfrom `pymdownx/highlight.py` while rendering\n`docs/deployment/production.md`.\n\nRoot cause: `pygments 2.20.0` tightened its handling of a `None`\n`filename` option that `pymdownx.highlight` was passing through.\nUpstream fixed this in `pymdown-extensions 10.21.2`.\n\nFix: add an explicit `pymdown-extensions>=10.21.2` floor to the `dev`\nextra and refresh the lockfile, constrained to that single package via\n`uv lock --upgrade-package pymdown-extensions`. No other dependencies,\nsource code, docs, tests, or CI were touched.\n\nAddresses #349",
          "timestamp": "2026-04-09T11:29:29+01:00",
          "tree_id": "63a3796b22079c17c3ddf8c9b6d76ef9f72dd08d",
          "url": "https://github.com/endavis/pyproject-template/commit/3bd06d1fc91ef7a5f7bdbc677883376f48fc4f65"
        },
        "date": 1775730592351,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9131003.268052824,
            "unit": "iter/sec",
            "range": "stddev: 1.265106393055153e-8",
            "extra": "mean: 109.51699070120351 nsec\nrounds: 86678"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8812841.650818627,
            "unit": "iter/sec",
            "range": "stddev: 1.18042186886375e-8",
            "extra": "mean: 113.47077816916293 nsec\nrounds: 87436"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6331669.98103603,
            "unit": "iter/sec",
            "range": "stddev: 1.589703518779121e-8",
            "extra": "mean: 157.93621635288912 nsec\nrounds: 63304"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1799150.7034678424,
            "unit": "iter/sec",
            "range": "stddev: 2.3300899608509555e-7",
            "extra": "mean: 555.8178078537343 nsec\nrounds: 53482"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 507165.55339728453,
            "unit": "iter/sec",
            "range": "stddev: 4.775070757296934e-7",
            "extra": "mean: 1.9717427441619977 usec\nrounds: 51338"
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
          "id": "0bb725b7128aed0e873f242b538c634f4acdc6fe",
          "message": "feat: add docs_build job to CI to catch mkdocs regressions at PR time (merges PR #356, addresses #354)\n\nPrior to this change, `doit docs_build` was not executed by any CI\nworkflow. That gap allowed the pymdown-extensions / pygments 2.20\nincompatibility tracked in #349 to land on `main` unnoticed until it\nwas reported manually; PR #355 shipped the immediate fix. This PR adds\nthe regression-protection gate that would have caught #349 at PR time.\n\nAdds a new `docs` job to `.github/workflows/ci.yml`, parallel to\n`test`, running on a single OS (`ubuntu-latest`) against the project's\nnewest supported Python version. The `setup` job now exposes a\n`newest` output sourced from `.github/python-versions.json`, which the\n`docs` job consumes so the Python version stays in sync with the rest\nof CI. The job runs `uv run doit docs_build` and is wired through\n`ci-complete`, so a failing docs build blocks the merge gate.\n\nScope: the job runs `mkdocs build` without `--strict`. `main` has an\nexisting backlog of non-fatal mkdocs warnings (unlisted nav files,\nbroken relative links in template/AI docs) that are out of scope here.\nTightening to `--strict` is a potential future improvement once that\nbacklog is cleared. The non-strict gate still catches hard crashes —\nplugin incompatibilities, broken macros, malformed configuration —\nwhich is exactly the class of failure that produced #349.\n\nAddresses #354",
          "timestamp": "2026-04-09T12:39:32+01:00",
          "tree_id": "268829c42a15f6e1b026396fca4d18315be48d13",
          "url": "https://github.com/endavis/pyproject-template/commit/0bb725b7128aed0e873f242b538c634f4acdc6fe"
        },
        "date": 1775734795837,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8228367.802517649,
            "unit": "iter/sec",
            "range": "stddev: 1.188329217323679e-8",
            "extra": "mean: 121.53078520554564 nsec\nrounds: 89518"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8765333.889598027,
            "unit": "iter/sec",
            "range": "stddev: 1.0880275509670654e-8",
            "extra": "mean: 114.0857852758715 nsec\nrounds: 86874"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5447641.792919626,
            "unit": "iter/sec",
            "range": "stddev: 1.6426992055184034e-8",
            "extra": "mean: 183.56566712952997 nsec\nrounds: 52591"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1676802.781443462,
            "unit": "iter/sec",
            "range": "stddev: 3.091344260795183e-7",
            "extra": "mean: 596.3730565494161 nsec\nrounds: 60972"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 503987.27960827295,
            "unit": "iter/sec",
            "range": "stddev: 4.755349057682827e-7",
            "extra": "mean: 1.9841770625188313 usec\nrounds: 57330"
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
          "id": "ec84fb20ee3ce06c1e8b2af37d92fe3abfea1ff7",
          "message": "refactor: move doit from runtime to dev dependencies (merges PR #357, addresses #340, #348)\n\n`doit` is a development task runner, not a runtime CLI surface of the\npublished package. Its prior placement in `[project] dependencies` (per\n#65, as a packaging convenience for template adopters) contradicted the\narchitectural boundary documented in `docs/development/tooling-roles.md`\n(addresses #340, added in PR #347) and in ADR-9002: end users of the\npublished package should never need `doit` installed to use it.\n\nChanges:\n- `pyproject.toml`: `doit>=0.36.0` removed from `[project] dependencies`\n  and added to `[project.optional-dependencies] dev`.\n- `uv.lock`: refreshed to reflect `doit`'s new group placement (now\n  listed under the `dev` extra; no version change).\n- `docs/template/decisions/9002-use-doit-for-task-automation.md`: Scope\n  rephrased so it no longer treats #65's runtime placement as\n  authoritative; #348 added to Related Issues.\n- `docs/development/tooling-roles.md`: \"Current vs Target State\" gap\n  callout replaced with a \"Dependency placement\" section documenting\n  the actual current state.\n\nNot changed: `rich` remains in `[project] dependencies`. Most CLIs\nbuilt on this template use `rich` for user-facing output, which is a\nlegitimate runtime concern.\n\nVerified locally with `doit check` and `doit docs_build`, and by\ninspecting the built wheel's `METADATA` — `Requires-Dist: rich>=13.0`\n(bare runtime) and `Requires-Dist: doit>=0.36.0; extra == 'dev'`, with\nno bare `doit` runtime requirement.\n\nAddresses #348\n\nBREAKING CHANGE: `doit` is no longer a transitive runtime dependency\nof this package. Downstream consumers who relied on `doit` being pulled\nin automatically must now install with the `[dev]` extra (e.g.\n`pip install package_name[dev]` or `uv add 'package_name[dev]'`) to\nget `doit`. In practice no such consumer is expected because this\nproject is a template — downstream users copy the template and manage\ntheir own dependency manifest rather than depending on `package_name`\nas a library.",
          "timestamp": "2026-04-09T14:41:14+01:00",
          "tree_id": "71cdc59a70f0a45b91d093e7300d7b1c4dc11d15",
          "url": "https://github.com/endavis/pyproject-template/commit/ec84fb20ee3ce06c1e8b2af37d92fe3abfea1ff7"
        },
        "date": 1775742101015,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8730003.908370823,
            "unit": "iter/sec",
            "range": "stddev: 1.1250668906963919e-8",
            "extra": "mean: 114.54748594569854 nsec\nrounds: 87874"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8318073.1716223,
            "unit": "iter/sec",
            "range": "stddev: 3.1603572952905394e-8",
            "extra": "mean: 120.22014947062158 nsec\nrounds: 85970"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5388282.23509291,
            "unit": "iter/sec",
            "range": "stddev: 1.3881439822058083e-8",
            "extra": "mean: 185.58790285467612 nsec\nrounds: 53034"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1682758.7725283615,
            "unit": "iter/sec",
            "range": "stddev: 2.5435933917416617e-7",
            "extra": "mean: 594.2622414604858 nsec\nrounds: 52894"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 493192.7661335757,
            "unit": "iter/sec",
            "range": "stddev: 5.244643309267699e-7",
            "extra": "mean: 2.027604759574193 usec\nrounds: 51055"
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
          "id": "8683c3fc8eb1b8e320979522159425a74f2bac2d",
          "message": "feat: add click-based application CLI with greet subcommand (merges PR #358, addresses #341)\n\nThe template previously shipped with an empty `[project.scripts]` block\nand no `cli.py`, leaving contributors with no concrete pattern to copy\nand making the runtime/dev tooling split documented in\n`docs/development/tooling-roles.md` purely aspirational — that file even\nforward-referenced this issue as a TODO. This commit closes the gap:\nreal runtime CLI, real tests, real guide, and an ADR explaining the\nframework choice.\n\nAdded:\n- `src/package_name/cli.py` — click `Group` `main` with a `greet`\n  subcommand and `@click.version_option` wired to installed package\n  metadata. Delegates to `package_name.core.greet`; the CLI is a thin\n  presentation layer over the runtime package.\n- `tests/test_cli.py` — 7 `click.testing.CliRunner` tests covering the\n  default greet, `--name`/`-n`, top-level `--help`, `greet --help`,\n  `--version`, and entry-point importability. In-process, no subprocess.\n- `docs/usage/cli.md` — CLI Guide with entry-point layout, a copyable\n  walkthrough for adding subcommands, and a testing recipe. Linked from\n  `docs/index.md`, `docs/usage/basics.md`, and the Usage section of\n  `mkdocs.yml`.\n- ADR-9014 at `docs/template/decisions/9014-use-click-for-application-cli.md`\n  documenting the choice of `click` over `argparse` (too much boilerplate,\n  no `CliRunner` equivalent) and `typer` (built on click anyway, adds\n  presentation coupling). Registered in `mkdocs.yml` nav.\n- `[project.scripts]` populated with\n  `package-name = \"package_name.cli:main\"`.\n- `click>=8.1` added to `[project] dependencies` as a runtime dep\n  (not dev), so the published wheel's `Requires-Dist:` ships it.\n\nScope note: #341 was originally filed as a doc-only request. Writing a\nguide grounded in real code required the code to exist, so scope was\nexpanded to bundle the feature and the guide in one PR. User explicitly\napproved this in the planning phase; labels were updated from\n`documentation` to `enhancement` + `needs-adr`.\n\nAlso updates `docs/development/tooling-roles.md` to replace its two\n`#341` forward-references with direct links to the new CLI Guide, and\nupdates ADR-9002 to add #341 to its Related Issues, link to ADR-9014\nas a Related Decision, and link to the new CLI Guide as Related\nDocumentation — closing the loop on the dev/runtime tooling split.\n\nAddresses #341",
          "timestamp": "2026-04-09T16:41:16+01:00",
          "tree_id": "2cd1915a7da640cbe3aaacbc384432ff9308b45e",
          "url": "https://github.com/endavis/pyproject-template/commit/8683c3fc8eb1b8e320979522159425a74f2bac2d"
        },
        "date": 1775749302070,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8617235.379328376,
            "unit": "iter/sec",
            "range": "stddev: 1.1763653232805567e-8",
            "extra": "mean: 116.04649936786798 nsec\nrounds: 85456"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8743655.479547612,
            "unit": "iter/sec",
            "range": "stddev: 1.2518456434538744e-8",
            "extra": "mean: 114.36864162124317 nsec\nrounds: 85683"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5334227.510044506,
            "unit": "iter/sec",
            "range": "stddev: 3.096654430351934e-8",
            "extra": "mean: 187.4685693695987 nsec\nrounds: 197239"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1479066.9858821507,
            "unit": "iter/sec",
            "range": "stddev: 5.137784242543308e-7",
            "extra": "mean: 676.101900417699 nsec\nrounds: 54514"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 469264.1564659617,
            "unit": "iter/sec",
            "range": "stddev: 6.968541140622664e-7",
            "extra": "mean: 2.1309959139667116 usec\nrounds: 49437"
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
          "id": "8c2586c7a823b04d30ccb70780a4a200e60385b4",
          "message": "refactor: move install_tools ADR to template decisions directory (merges PR #360, addresses #359)\n\nThe `0001-install-tools-framework-archive-extraction-and-custom-urls.md`\nADR was the only file in `docs/decisions/`, but its subject —\n`install_tools` framework — is template-meta tooling that lives under\n`tools/doit/install_tools.py` and is a feature of the template itself,\nnot of any project built from it. It belonged in the 9000-series\nalongside ADR-9001 through ADR-9014 in `docs/template/decisions/`.\n\nPer the design intent documented in `tests/test_doit_adr.py:66-67`,\n`docs/decisions/` is the scaffold for project-level ADRs (0001-series)\nthat downstream consumers will use after spawning a real project from\nthis template; `docs/template/decisions/` (9XXX series) is for\ntemplate-meta ADRs. The moved file is the only previously-misplaced\nADR — `docs/decisions/`, `tools/doit/adr.py`, and the test all stay\nunchanged because they correctly target project-level ADR creation.\n\nChanges:\n- Created `docs/template/decisions/9015-install-tools-framework-archive-extraction-and-custom-urls.md`\n  with `# ADR-9015` title and corrected relative link to the\n  install-tools-framework doc.\n- Deleted `docs/decisions/0001-install-tools-framework-archive-extraction-and-custom-urls.md`.\n- Updated the inbound reference in `docs/development/install-tools-framework.md`.\n- Added rows for ADR-9014 (leftover from PR #358) and ADR-9015 to the\n  index in `docs/template/decisions/README.md`.\n- Added the ADR-9015 nav entry to `mkdocs.yml`.\n\nAfter this PR, `_get_next_adr_number()` correctly returns `1` because\nthe project-level ADR directory is empty, exactly as the existing test\ndocstring describes.\n\nAddresses #359",
          "timestamp": "2026-04-09T17:01:37+01:00",
          "tree_id": "01947eb9aa10aebc830e61cea828afd977a20dc0",
          "url": "https://github.com/endavis/pyproject-template/commit/8c2586c7a823b04d30ccb70780a4a200e60385b4"
        },
        "date": 1775750524389,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8595818.15381096,
            "unit": "iter/sec",
            "range": "stddev: 1.689819734777366e-8",
            "extra": "mean: 116.33563927322608 nsec\nrounds: 199681"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9014337.511776775,
            "unit": "iter/sec",
            "range": "stddev: 9.27619054998702e-9",
            "extra": "mean: 110.93438632551208 nsec\nrounds: 89510"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5400957.435628896,
            "unit": "iter/sec",
            "range": "stddev: 3.657579336127068e-8",
            "extra": "mean: 185.15235713638955 nsec\nrounds: 54125"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1769818.5778400267,
            "unit": "iter/sec",
            "range": "stddev: 1.6875189056836422e-7",
            "extra": "mean: 565.0296660465892 nsec\nrounds: 57945"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 527772.1890050118,
            "unit": "iter/sec",
            "range": "stddev: 2.895847567981638e-7",
            "extra": "mean: 1.89475690616677 usec\nrounds: 47747"
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
          "id": "52edd7777e47e2c542af0523a30d7d0ae78ebaaf",
          "message": "docs: add end-to-end add-a-feature example (merges PR #361, addresses #342)\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-10T11:10:26+01:00",
          "tree_id": "53b25835a237a373897f8abedac397d368064765",
          "url": "https://github.com/endavis/pyproject-template/commit/52edd7777e47e2c542af0523a30d7d0ae78ebaaf"
        },
        "date": 1775815850008,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8918606.345432783,
            "unit": "iter/sec",
            "range": "stddev: 2.10923144561627e-8",
            "extra": "mean: 112.12514167217391 nsec\nrounds: 89679"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8821717.02479613,
            "unit": "iter/sec",
            "range": "stddev: 1.9504117066951348e-8",
            "extra": "mean: 113.35661721966306 nsec\nrounds: 89119"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5244266.611735369,
            "unit": "iter/sec",
            "range": "stddev: 1.7115615180068864e-8",
            "extra": "mean: 190.68443197800963 nsec\nrounds: 52674"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1691146.5570415123,
            "unit": "iter/sec",
            "range": "stddev: 2.2104588642109136e-7",
            "extra": "mean: 591.3148070084462 nsec\nrounds: 57000"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 505368.5862688608,
            "unit": "iter/sec",
            "range": "stddev: 4.992388396060646e-7",
            "extra": "mean: 1.978753779262391 usec\nrounds: 59337"
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
          "id": "2917df127540228b654e00655cbef4e814faf618",
          "message": "feat: add Copilot CLI command-blocking hook integration (merges PR #363, addresses #362)\n\nfeat: add Copilot/Codex hook integration and fix chained-command detection\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-10T13:39:25+01:00",
          "tree_id": "c95ec0da63dfcb8243d47bb50934db6ca1f3a43d",
          "url": "https://github.com/endavis/pyproject-template/commit/2917df127540228b654e00655cbef4e814faf618"
        },
        "date": 1775824792919,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8196752.698065866,
            "unit": "iter/sec",
            "range": "stddev: 3.175518950237141e-8",
            "extra": "mean: 121.99953284377648 nsec\nrounds: 87551"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9135167.360182611,
            "unit": "iter/sec",
            "range": "stddev: 1.1107443565048612e-8",
            "extra": "mean: 109.46706946592931 nsec\nrounds: 89598"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5348839.292335107,
            "unit": "iter/sec",
            "range": "stddev: 1.5415728780303678e-8",
            "extra": "mean: 186.95644893145345 nsec\nrounds: 53291"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1729845.7270249599,
            "unit": "iter/sec",
            "range": "stddev: 2.4177181910523787e-7",
            "extra": "mean: 578.0862329959502 nsec\nrounds: 60754"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 504013.1105152658,
            "unit": "iter/sec",
            "range": "stddev: 5.1787599356382e-7",
            "extra": "mean: 1.984075372518929 usec\nrounds: 49461"
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
          "id": "dd0ec7d430af5c9f758ebaeebd075d7fa5eadaa6",
          "message": "feat: add doit task to install the gh CLI (merges PR #375, addresses #374)",
          "timestamp": "2026-04-13T12:17:47+01:00",
          "tree_id": "8b2fcac55310b114389b911400492747bd5927e4",
          "url": "https://github.com/endavis/pyproject-template/commit/dd0ec7d430af5c9f758ebaeebd075d7fa5eadaa6"
        },
        "date": 1776079091920,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8581087.020602113,
            "unit": "iter/sec",
            "range": "stddev: 2.5751190275901912e-8",
            "extra": "mean: 116.53535240921408 nsec\nrounds: 88803"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9166862.643092392,
            "unit": "iter/sec",
            "range": "stddev: 1.7998774122287644e-8",
            "extra": "mean: 109.08857685934032 nsec\nrounds: 90490"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5449274.445959907,
            "unit": "iter/sec",
            "range": "stddev: 1.5723793615936977e-8",
            "extra": "mean: 183.51066915732244 nsec\nrounds: 54337"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1694514.6467584528,
            "unit": "iter/sec",
            "range": "stddev: 3.0712950970230005e-7",
            "extra": "mean: 590.1394844317015 nsec\nrounds: 47482"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 494003.90267301217,
            "unit": "iter/sec",
            "range": "stddev: 5.652052109332794e-7",
            "extra": "mean: 2.0242755059000284 usec\nrounds: 54213"
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
          "id": "8a8da85364abc1d1fcd43101cea482ce94c4c615",
          "message": "docs: add GitHub repository settings reference guide (merges PR #377, addresses #376)",
          "timestamp": "2026-04-13T13:21:47+01:00",
          "tree_id": "3afd1530b31dc7601ea1a4eb1e4c4588c079ff8e",
          "url": "https://github.com/endavis/pyproject-template/commit/8a8da85364abc1d1fcd43101cea482ce94c4c615"
        },
        "date": 1776082936772,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9003360.186593488,
            "unit": "iter/sec",
            "range": "stddev: 1.0672303505580667e-8",
            "extra": "mean: 111.06964280836576 nsec\nrounds: 87936"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8840657.665803637,
            "unit": "iter/sec",
            "range": "stddev: 2.3273848750920504e-8",
            "extra": "mean: 113.11375666858802 nsec\nrounds: 89598"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5374890.813389198,
            "unit": "iter/sec",
            "range": "stddev: 1.5789817968329785e-8",
            "extra": "mean: 186.0502910140864 nsec\nrounds: 54396"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1683097.04649939,
            "unit": "iter/sec",
            "range": "stddev: 2.521170024017174e-7",
            "extra": "mean: 594.1428048251064 nsec\nrounds: 57330"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 427539.45243757946,
            "unit": "iter/sec",
            "range": "stddev: 0.000001038059049468629",
            "extra": "mean: 2.338965431841637 usec\nrounds: 47645"
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
          "id": "c1f4ea82014e24025213d821a8fcaca5eba54848",
          "message": "chore(deps): bump actions/github-script from 8 to 9 (merges PR #364)\n\nBumps [actions/github-script](https://github.com/actions/github-script) from 8 to 9.\n- [Release notes](https://github.com/actions/github-script/releases)\n- [Commits](https://github.com/actions/github-script/compare/v8...v9)\n\n---\nupdated-dependencies:\n- dependency-name: actions/github-script\n  dependency-version: '9'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T13:46:28+01:00",
          "tree_id": "e05dc58d0f1e2595dc97cd3608e1e12bed71af61",
          "url": "https://github.com/endavis/pyproject-template/commit/c1f4ea82014e24025213d821a8fcaca5eba54848"
        },
        "date": 1776084418219,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8984407.893298028,
            "unit": "iter/sec",
            "range": "stddev: 1.108519706178409e-8",
            "extra": "mean: 111.30394032376424 nsec\nrounds: 88645"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8802027.288603568,
            "unit": "iter/sec",
            "range": "stddev: 2.262192070698328e-8",
            "extra": "mean: 113.61019083578061 nsec\nrounds: 87405"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5193112.826131728,
            "unit": "iter/sec",
            "range": "stddev: 6.006916067018966e-8",
            "extra": "mean: 192.56273327396298 nsec\nrounds: 53778"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1639555.1086799647,
            "unit": "iter/sec",
            "range": "stddev: 5.188025470826844e-7",
            "extra": "mean: 609.9215541495998 nsec\nrounds: 55516"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 493918.063249,
            "unit": "iter/sec",
            "range": "stddev: 5.1806659576737e-7",
            "extra": "mean: 2.024627310493538 usec\nrounds: 51504"
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
          "id": "1a25adaa9b96c8d20f27fe9fbebde88756e4c3ee",
          "message": "chore(deps): bump the dev-dependencies group across 1 directory with 3 updates (merges PR #365)\n\nchore(deps): bump the dev-dependencies group with 3 updates\n\nBumps the dev-dependencies group with 3 updates: [pytest](https://github.com/pytest-dev/pytest), [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy).\n\n\nUpdates `pytest` from 9.0.2 to 9.0.3\n- [Release notes](https://github.com/pytest-dev/pytest/releases)\n- [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)\n- [Commits](https://github.com/pytest-dev/pytest/compare/9.0.2...9.0.3)\n\nUpdates `ruff` from 0.15.9 to 0.15.10\n- [Release notes](https://github.com/astral-sh/ruff/releases)\n- [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/astral-sh/ruff/compare/0.15.9...0.15.10)\n\nUpdates `mypy` from 1.20.0 to 1.20.1\n- [Changelog](https://github.com/python/mypy/blob/master/CHANGELOG.md)\n- [Commits](https://github.com/python/mypy/compare/v1.20.0...v1.20.1)\n\n---\nupdated-dependencies:\n- dependency-name: pytest\n  dependency-version: 9.0.3\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n  dependency-group: dev-dependencies\n- dependency-name: ruff\n  dependency-version: 0.15.10\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n  dependency-group: dev-dependencies\n- dependency-name: mypy\n  dependency-version: 1.20.1\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n  dependency-group: dev-dependencies\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T13:54:50+01:00",
          "tree_id": "858d9b9d08d13708860f118e175e8bb911e1c037",
          "url": "https://github.com/endavis/pyproject-template/commit/1a25adaa9b96c8d20f27fe9fbebde88756e4c3ee"
        },
        "date": 1776084920668,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8823438.076834874,
            "unit": "iter/sec",
            "range": "stddev: 1.1669195207067856e-8",
            "extra": "mean: 113.3345064919091 nsec\nrounds: 88803"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9038364.486945491,
            "unit": "iter/sec",
            "range": "stddev: 1.2489422403383955e-8",
            "extra": "mean: 110.63948587649283 nsec\nrounds: 89920"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5396056.513323584,
            "unit": "iter/sec",
            "range": "stddev: 1.512519237664658e-8",
            "extra": "mean: 185.32052018559602 nsec\nrounds: 53577"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1653771.2252225727,
            "unit": "iter/sec",
            "range": "stddev: 3.1180877505560744e-7",
            "extra": "mean: 604.6785581635785 nsec\nrounds: 51185"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 489241.1441715675,
            "unit": "iter/sec",
            "range": "stddev: 5.60314013756279e-7",
            "extra": "mean: 2.043981811246274 usec\nrounds: 52395"
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
          "id": "ae5b70008fb131b7ca754f0f0d46d15ffba5cc2f",
          "message": "chore(deps): bump commitizen from 4.13.9 to 4.13.10 (merges PR #366)\n\nBumps [commitizen](https://github.com/commitizen-tools/commitizen) from 4.13.9 to 4.13.10.\n- [Release notes](https://github.com/commitizen-tools/commitizen/releases)\n- [Changelog](https://github.com/commitizen-tools/commitizen/blob/master/CHANGELOG.md)\n- [Commits](https://github.com/commitizen-tools/commitizen/compare/v4.13.9...v4.13.10)\n\n---\nupdated-dependencies:\n- dependency-name: commitizen\n  dependency-version: 4.13.10\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T14:03:26+01:00",
          "tree_id": "5938f4366d892ab6bad1e457229943e138ddd582",
          "url": "https://github.com/endavis/pyproject-template/commit/ae5b70008fb131b7ca754f0f0d46d15ffba5cc2f"
        },
        "date": 1776085435370,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8655021.209753426,
            "unit": "iter/sec",
            "range": "stddev: 2.060483699361325e-8",
            "extra": "mean: 115.53986706272777 nsec\nrounds: 85529"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8828467.91377161,
            "unit": "iter/sec",
            "range": "stddev: 1.1924069162898968e-8",
            "extra": "mean: 113.26993650167665 nsec\nrounds: 45828"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5331547.068058581,
            "unit": "iter/sec",
            "range": "stddev: 3.8156020198996085e-8",
            "extra": "mean: 187.56281942834616 nsec\nrounds: 55795"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1638337.51889919,
            "unit": "iter/sec",
            "range": "stddev: 2.898387400946381e-7",
            "extra": "mean: 610.3748394115437 nsec\nrounds: 35023"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 500935.4556363097,
            "unit": "iter/sec",
            "range": "stddev: 7.754721477223457e-7",
            "extra": "mean: 1.9962651649996646 usec\nrounds: 50033"
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
          "id": "b130283c770d37b261d5514fa80a5ba0d2d9bb5d",
          "message": "chore(deps): update hatch-vcs requirement from >=0.4 to >=0.5.0 (merges PR #367)\n\nUpdates the requirements on [hatch-vcs](https://github.com/ofek/hatch-vcs) to permit the latest version.\n- [Release notes](https://github.com/ofek/hatch-vcs/releases)\n- [Changelog](https://github.com/ofek/hatch-vcs/blob/master/HISTORY.md)\n- [Commits](https://github.com/ofek/hatch-vcs/compare/v0.4.0...v0.5.0)\n\n---\nupdated-dependencies:\n- dependency-name: hatch-vcs\n  dependency-version: 0.5.0\n  dependency-type: direct:development\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T14:06:54+01:00",
          "tree_id": "ce97b584e50e5b1a51d8d6e139b667ba3bfc3a55",
          "url": "https://github.com/endavis/pyproject-template/commit/b130283c770d37b261d5514fa80a5ba0d2d9bb5d"
        },
        "date": 1776085645823,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8991397.454099983,
            "unit": "iter/sec",
            "range": "stddev: 1.1944104450544388e-8",
            "extra": "mean: 111.21741699272903 nsec\nrounds: 87944"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8616626.583695898,
            "unit": "iter/sec",
            "range": "stddev: 3.6341585543239405e-8",
            "extra": "mean: 116.05469847006806 nsec\nrounds: 89759"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5296641.638644942,
            "unit": "iter/sec",
            "range": "stddev: 1.5153754646258106e-8",
            "extra": "mean: 188.79887827484464 nsec\nrounds: 54541"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1659600.6196763178,
            "unit": "iter/sec",
            "range": "stddev: 3.474292419424923e-7",
            "extra": "mean: 602.5546075025185 nsec\nrounds: 55670"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 498695.5057528754,
            "unit": "iter/sec",
            "range": "stddev: 5.766625736403744e-7",
            "extra": "mean: 2.0052316262411676 usec\nrounds: 48738"
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
          "id": "e3484e27fbb14a2ca04496822ddffa003db64e2d",
          "message": "chore(deps): bump hypothesis from 6.151.11 to 6.151.13 (merges PR #368)\n\nBumps [hypothesis](https://github.com/HypothesisWorks/hypothesis) from 6.151.11 to 6.151.13.\n- [Release notes](https://github.com/HypothesisWorks/hypothesis/releases)\n- [Commits](https://github.com/HypothesisWorks/hypothesis/compare/hypothesis-python-6.151.11...hypothesis-python-6.151.13)\n\n---\nupdated-dependencies:\n- dependency-name: hypothesis\n  dependency-version: 6.151.13\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T14:50:34+01:00",
          "tree_id": "717f83382d8f4965674e03f2089143940d2e49e5",
          "url": "https://github.com/endavis/pyproject-template/commit/e3484e27fbb14a2ca04496822ddffa003db64e2d"
        },
        "date": 1776088263806,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8978596.2082261,
            "unit": "iter/sec",
            "range": "stddev: 1.3487826672594877e-8",
            "extra": "mean: 111.37598537773756 nsec\nrounds: 85896"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9037916.165212695,
            "unit": "iter/sec",
            "range": "stddev: 1.9466565536883147e-8",
            "extra": "mean: 110.64497409801616 nsec\nrounds: 86866"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5412612.068012787,
            "unit": "iter/sec",
            "range": "stddev: 1.654179849542548e-8",
            "extra": "mean: 184.75368037361392 nsec\nrounds: 52674"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1648238.808518043,
            "unit": "iter/sec",
            "range": "stddev: 2.7180998642330577e-7",
            "extra": "mean: 606.7081995837214 nsec\nrounds: 56076"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 497071.39970997913,
            "unit": "iter/sec",
            "range": "stddev: 4.893082626202253e-7",
            "extra": "mean: 2.0117834190087365 usec\nrounds: 53121"
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
          "id": "b20d659896178f35c2139e06e6e693521011add5",
          "message": "chore(deps): bump click from 8.3.1 to 8.3.2 (merges PR #369)\n\nBumps [click](https://github.com/pallets/click) from 8.3.1 to 8.3.2.\n- [Release notes](https://github.com/pallets/click/releases)\n- [Changelog](https://github.com/pallets/click/blob/main/CHANGES.rst)\n- [Commits](https://github.com/pallets/click/compare/8.3.1...8.3.2)\n\n---\nupdated-dependencies:\n- dependency-name: click\n  dependency-version: 8.3.2\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T14:55:57+01:00",
          "tree_id": "07b763b080ab583825b6478479424adff953b6ae",
          "url": "https://github.com/endavis/pyproject-template/commit/b20d659896178f35c2139e06e6e693521011add5"
        },
        "date": 1776088587945,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8814471.542569581,
            "unit": "iter/sec",
            "range": "stddev: 1.223978773394729e-8",
            "extra": "mean: 113.44979618692847 nsec\nrounds: 86648"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8860395.882714724,
            "unit": "iter/sec",
            "range": "stddev: 1.1413887618471705e-8",
            "extra": "mean: 112.8617742634781 nsec\nrounds: 87704"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5217933.907867542,
            "unit": "iter/sec",
            "range": "stddev: 4.203881163845909e-8",
            "extra": "mean: 191.64673559628864 nsec\nrounds: 55854"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1530836.7952308152,
            "unit": "iter/sec",
            "range": "stddev: 4.415160833904867e-7",
            "extra": "mean: 653.2374993306996 nsec\nrounds: 57137"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 476223.6364362182,
            "unit": "iter/sec",
            "range": "stddev: 7.891420131888762e-7",
            "extra": "mean: 2.0998537734989817 usec\nrounds: 50285"
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
          "id": "985f16799392d8ddf267cb9923c7622ac2f7294d",
          "message": "chore(deps): update hatchling requirement from >=1.24 to >=1.29.0 (merges PR #370)\n\nUpdates the requirements on [hatchling](https://github.com/pypa/hatch) to permit the latest version.\n- [Release notes](https://github.com/pypa/hatch/releases)\n- [Commits](https://github.com/pypa/hatch/compare/hatchling-v1.24.0...hatchling-v1.29.0)\n\n---\nupdated-dependencies:\n- dependency-name: hatchling\n  dependency-version: 1.29.0\n  dependency-type: direct:development\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T15:29:30+01:00",
          "tree_id": "0da92cdfb592de1780bba1b382dd2dc18d393dc2",
          "url": "https://github.com/endavis/pyproject-template/commit/985f16799392d8ddf267cb9923c7622ac2f7294d"
        },
        "date": 1776090596141,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8881722.054540396,
            "unit": "iter/sec",
            "range": "stddev: 1.2509536260288995e-8",
            "extra": "mean: 112.59077843905206 nsec\nrounds: 86044"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8710192.776103461,
            "unit": "iter/sec",
            "range": "stddev: 2.756664088195535e-8",
            "extra": "mean: 114.808021556482 nsec\nrounds: 198020"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5475827.408410086,
            "unit": "iter/sec",
            "range": "stddev: 1.588388103804424e-8",
            "extra": "mean: 182.62080328977194 nsec\nrounds: 52285"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1705775.3177450802,
            "unit": "iter/sec",
            "range": "stddev: 2.816259623910157e-7",
            "extra": "mean: 586.2436802766806 nsec\nrounds: 56648"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 505156.780268805,
            "unit": "iter/sec",
            "range": "stddev: 7.135691589546185e-7",
            "extra": "mean: 1.979583446287464 usec\nrounds: 56809"
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
          "id": "d8121f8010dae2aaaa70dbd2693a40d090d478b7",
          "message": "chore(deps): bump types-pyyaml from 6.0.12.20250915 to 6.0.12.20260408 (merges PR #371)\n\nBumps [types-pyyaml](https://github.com/python/typeshed) from 6.0.12.20250915 to 6.0.12.20260408.\n- [Commits](https://github.com/python/typeshed/commits)\n\n---\nupdated-dependencies:\n- dependency-name: types-pyyaml\n  dependency-version: 6.0.12.20260408\n  dependency-type: direct:production\n  update-type: version-update:semver-patch\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T15:33:55+01:00",
          "tree_id": "b88640692fc5cc1b95b57fdbbc6777bdebf8733f",
          "url": "https://github.com/endavis/pyproject-template/commit/d8121f8010dae2aaaa70dbd2693a40d090d478b7"
        },
        "date": 1776090861694,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8463254.571107358,
            "unit": "iter/sec",
            "range": "stddev: 1.3195189676541752e-7",
            "extra": "mean: 118.1578542389464 nsec\nrounds: 87321"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9513513.524663735,
            "unit": "iter/sec",
            "range": "stddev: 1.8982747490861136e-8",
            "extra": "mean: 105.11363624043894 nsec\nrounds: 88410"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5394854.604581663,
            "unit": "iter/sec",
            "range": "stddev: 2.2329312320748446e-8",
            "extra": "mean: 185.3618073693283 nsec\nrounds: 50615"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1641238.0553113031,
            "unit": "iter/sec",
            "range": "stddev: 3.0539013645576225e-7",
            "extra": "mean: 609.2961327357988 nsec\nrounds: 60456"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 509706.2179997606,
            "unit": "iter/sec",
            "range": "stddev: 5.05628700745553e-7",
            "extra": "mean: 1.9619144610876018 usec\nrounds: 55390"
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
          "id": "01bd531ab07f3c93496a16b6934da26ece5919be",
          "message": "chore(deps): bump rich from 14.3.3 to 15.0.0 (merges PR #372)\n\nBumps [rich](https://github.com/Textualize/rich) from 14.3.3 to 15.0.0.\n- [Release notes](https://github.com/Textualize/rich/releases)\n- [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)\n- [Commits](https://github.com/Textualize/rich/compare/v14.3.3...v15.0.0)\n\n---\nupdated-dependencies:\n- dependency-name: rich\n  dependency-version: 15.0.0\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T15:44:11+01:00",
          "tree_id": "f97df83a0a41d9f1a379a12c2dca163be5e3711c",
          "url": "https://github.com/endavis/pyproject-template/commit/01bd531ab07f3c93496a16b6934da26ece5919be"
        },
        "date": 1776091480604,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8897842.041761909,
            "unit": "iter/sec",
            "range": "stddev: 1.6215152854072078e-8",
            "extra": "mean: 112.3868006766711 nsec\nrounds: 83949"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8925650.533090027,
            "unit": "iter/sec",
            "range": "stddev: 1.3471017626062184e-8",
            "extra": "mean: 112.03665170316765 nsec\nrounds: 87101"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5548754.375386153,
            "unit": "iter/sec",
            "range": "stddev: 1.4795701978650098e-8",
            "extra": "mean: 180.22062833343696 nsec\nrounds: 53634"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1611430.2758634444,
            "unit": "iter/sec",
            "range": "stddev: 2.5796955903550277e-7",
            "extra": "mean: 620.5667195027568 nsec\nrounds: 55516"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 470677.3138133884,
            "unit": "iter/sec",
            "range": "stddev: 5.110373799409082e-7",
            "extra": "mean: 2.124597830938745 usec\nrounds: 51451"
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
          "id": "f118850932484f3f284328f55f3b63eeca0b12f2",
          "message": "chore(deps): update mkdocstrings[python] requirement from >=0.24 to >=1.0.3 (merges PR #373)\n\nchore(deps): update mkdocstrings[python] requirement\n\nUpdates the requirements on [mkdocstrings[python]](https://github.com/mkdocstrings/mkdocstrings) to permit the latest version.\n- [Release notes](https://github.com/mkdocstrings/mkdocstrings/releases)\n- [Changelog](https://github.com/mkdocstrings/mkdocstrings/blob/main/CHANGELOG.md)\n- [Commits](https://github.com/mkdocstrings/mkdocstrings/compare/0.24.0...1.0.3)\n\n---\nupdated-dependencies:\n- dependency-name: mkdocstrings[python]\n  dependency-version: 1.0.3\n  dependency-type: direct:production\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-13T15:51:38+01:00",
          "tree_id": "c7dfa5fcd70cf79eb32fb83e8245c26943352d02",
          "url": "https://github.com/endavis/pyproject-template/commit/f118850932484f3f284328f55f3b63eeca0b12f2"
        },
        "date": 1776091926719,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8808233.814440994,
            "unit": "iter/sec",
            "range": "stddev: 1.1534542065206672e-8",
            "extra": "mean: 113.53013794439836 nsec\nrounds: 87789"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8969270.765271712,
            "unit": "iter/sec",
            "range": "stddev: 1.3628254849522034e-8",
            "extra": "mean: 111.49178413388061 nsec\nrounds: 91075"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5296789.109793993,
            "unit": "iter/sec",
            "range": "stddev: 1.598485894757639e-8",
            "extra": "mean: 188.79362180966513 nsec\nrounds: 54031"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1685609.678239652,
            "unit": "iter/sec",
            "range": "stddev: 2.7819099635460785e-7",
            "extra": "mean: 593.257153722764 nsec\nrounds: 55146"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 505585.32029916364,
            "unit": "iter/sec",
            "range": "stddev: 5.427884474115154e-7",
            "extra": "mean: 1.9779055282069555 usec\nrounds: 34550"
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
          "id": "8b90cc93069f280fd4132a3d1359e96b9bf61bf0",
          "message": "docs: forbid AI agents from silently fixing failing tests (merges PR #379, addresses #378)\n\ndoc: forbid AI agents from silently fixing failing tests\n\nA failing test is a signal — agents must stop, explain why it broke,\nand discuss with the user whether the code or test should change.\n\nAddresses #378",
          "timestamp": "2026-04-14T11:29:32+01:00",
          "tree_id": "9c4919d7ee31c84f63eadb8a495eb906ab7930e1",
          "url": "https://github.com/endavis/pyproject-template/commit/8b90cc93069f280fd4132a3d1359e96b9bf61bf0"
        },
        "date": 1776162603512,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8123922.221813361,
            "unit": "iter/sec",
            "range": "stddev: 3.441296931510452e-8",
            "extra": "mean: 123.09325135030494 nsec\nrounds: 83879"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8906942.176235404,
            "unit": "iter/sec",
            "range": "stddev: 1.2214452257071995e-7",
            "extra": "mean: 112.27197619718451 nsec\nrounds: 88645"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5285384.107913952,
            "unit": "iter/sec",
            "range": "stddev: 2.0013168475042762e-7",
            "extra": "mean: 189.20100783265158 nsec\nrounds: 53749"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1629995.0016616203,
            "unit": "iter/sec",
            "range": "stddev: 2.89935857279134e-7",
            "extra": "mean: 613.4988137881392 nsec\nrounds: 62384"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 496961.6792873036,
            "unit": "iter/sec",
            "range": "stddev: 5.350091877458823e-7",
            "extra": "mean: 2.0122275855033878 usec\nrounds: 57697"
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
          "id": "afb59ea36e298d1884ac15c8140f618dbd64f7a2",
          "message": "feat: add --auto-close flag to doit pr_merge (merges PR #381, addresses #380)\n\nAdds an opt-in --auto-close flag on task_pr_merge. When set, the task\ncloses each linked issue parsed from \"Addresses #XX\" in the PR body via\n`gh issue close <n> --comment \"Addressed in PR #<pr>\"` after a\nsuccessful merge. Default behavior is unchanged: without the flag, the\ntask continues to print the `gh issue close` reminder commands.\n\nAdds TestCloseLinkedIssues (5 tests) covering multi-issue close, empty\nlists, per-issue failure isolation, comment format, and subprocess\nerrors. Updates AGENTS.md and the doit-tasks / release-and-automation\ndocs to document the new flag.\n\nAddresses #380",
          "timestamp": "2026-04-14T11:57:17+01:00",
          "tree_id": "8f9c45397cbe53db89cfc77477851069f69769f5",
          "url": "https://github.com/endavis/pyproject-template/commit/afb59ea36e298d1884ac15c8140f618dbd64f7a2"
        },
        "date": 1776164267392,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8802938.783085313,
            "unit": "iter/sec",
            "range": "stddev: 7.862307896933996e-9",
            "extra": "mean: 113.59842714361277 nsec\nrounds: 84941"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9015449.34942137,
            "unit": "iter/sec",
            "range": "stddev: 7.859209882906827e-9",
            "extra": "mean: 110.92070525183327 nsec\nrounds: 86267"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5668441.359196727,
            "unit": "iter/sec",
            "range": "stddev: 1.0420785495029767e-8",
            "extra": "mean: 176.41533829710636 nsec\nrounds: 55203"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1594437.9093687679,
            "unit": "iter/sec",
            "range": "stddev: 1.777458425052325e-7",
            "extra": "mean: 627.1802709431918 nsec\nrounds: 59344"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 524655.2294593357,
            "unit": "iter/sec",
            "range": "stddev: 3.3524826228670216e-7",
            "extra": "mean: 1.9060135949288328 usec\nrounds: 27069"
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
          "id": "aff458619c6926cc0edc8eb53bbfa4880ee7d8d9",
          "message": "feat: auto-merge dependabot PRs once required CI checks pass (merges PR #384, addresses #382)\n\nfeat: auto-merge qualifying dependabot PRs once CI passes\n\nAdd a workflow that evaluates each dependabot PR against a JSON\nconfig (update type, sensitive-dependency globs, blocking labels),\nenables native squash auto-merge and applies ready-to-merge for\nqualifying PRs, and posts a sticky status comment otherwise. A\nscheduled job nudges stale qualifying PRs via @dependabot rebase\nto preserve verified signatures. PR-checks is updated to exempt\ndependabot PRs from the issue-link rule. Docs updated in\nAGENTS.md, docs/development/dependabot-automerge.md, and the\nrepo-settings label table.\n\nAddresses #382",
          "timestamp": "2026-04-14T16:23:31+01:00",
          "tree_id": "d5feb9f1f970d1ac6f2c5ee670ff36cec8328335",
          "url": "https://github.com/endavis/pyproject-template/commit/aff458619c6926cc0edc8eb53bbfa4880ee7d8d9"
        },
        "date": 1776180238129,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8936005.226447053,
            "unit": "iter/sec",
            "range": "stddev: 1.3041761768174147e-8",
            "extra": "mean: 111.90682801308063 nsec\nrounds: 87245"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9124274.738070171,
            "unit": "iter/sec",
            "range": "stddev: 1.2315610987728757e-8",
            "extra": "mean: 109.59775200845222 nsec\nrounds: 90245"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5297339.313118607,
            "unit": "iter/sec",
            "range": "stddev: 1.4697599229165958e-8",
            "extra": "mean: 188.77401293202945 nsec\nrounds: 55057"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1674691.5831269096,
            "unit": "iter/sec",
            "range": "stddev: 2.58991165804319e-7",
            "extra": "mean: 597.1248736635104 nsec\nrounds: 56393"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 499122.8706526483,
            "unit": "iter/sec",
            "range": "stddev: 4.84112978183128e-7",
            "extra": "mean: 2.0035146830527113 usec\nrounds: 52203"
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
          "id": "0834c918f71d86923740590524b3cc0003e4804f",
          "message": "feat: have doit pr check branch is up to date with origin/main (merges PR #385, addresses #383)\n\nAdds a pre-flight check in `doit pr` that fetches `origin/main` and aborts\nwith a clear remediation message if the current branch is behind. Prevents\nopening PRs from stale branches (see PR #379 which had to be rebased\npost-hoc after branching from a local `main` 10 commits behind origin).\n\n- `_check_branch_up_to_date()` helper in tools/doit/github.py\n- Wired into `create_pr`; adds `--no-update-check` opt-out\n- Network failures during `git fetch` warn and proceed (don't block)\n- `TestCheckBranchUpToDate` covers pass, abort, fetch-failure, commit-list\n- AGENTS.md Critical Reminders `**Flow:**` line notes the new enforcement\n\nAddresses #383",
          "timestamp": "2026-04-14T17:04:06+01:00",
          "tree_id": "fe94370823e70a68ae928f66a7e46f965fa7105f",
          "url": "https://github.com/endavis/pyproject-template/commit/0834c918f71d86923740590524b3cc0003e4804f"
        },
        "date": 1776182672990,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9059096.137854002,
            "unit": "iter/sec",
            "range": "stddev: 1.1892802962768423e-8",
            "extra": "mean: 110.38628851960596 nsec\nrounds: 89630"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8851432.215457976,
            "unit": "iter/sec",
            "range": "stddev: 1.2837244060657471e-8",
            "extra": "mean: 112.97606711076867 nsec\nrounds: 84696"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6317179.404048325,
            "unit": "iter/sec",
            "range": "stddev: 1.6053647378176864e-8",
            "extra": "mean: 158.2984962179729 nsec\nrounds: 61219"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1733086.608852776,
            "unit": "iter/sec",
            "range": "stddev: 2.538096110714784e-7",
            "extra": "mean: 577.0052084482692 nsec\nrounds: 38975"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 506687.8651695293,
            "unit": "iter/sec",
            "range": "stddev: 4.9089351895934e-7",
            "extra": "mean: 1.973601636710634 usec\nrounds: 39592"
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
          "id": "adb60131a3eda062a20f624bc7254eece29638c1",
          "message": "feat: have doit pr auto-push branch if needed (merges PR #391, addresses #386)\n\nFixes the `aborted: you must first push the current branch to a remote`\nerror that hit PR #385. After the up-to-date check (from PR #385) passes,\n`doit pr` now pushes the branch to origin if no upstream exists, then\ncontinues with the editor/title flow. Push failures surface before the\nuser invests time drafting a PR body.\n\n- `_ensure_branch_pushed()` helper in tools/doit/github.py\n- Wired into `create_pr`; adds `--no-push` opt-out\n- Push failures (protected branch, auth, network) exit 1 with stderr\n- `TestEnsureBranchPushed` covers noop, push, push-failure, --no-push\n- AGENTS.md PR Creation section notes the new behavior\n\nAddresses #386",
          "timestamp": "2026-04-14T17:43:32+01:00",
          "tree_id": "76d181d65019126702a067905c1ce11d756b0db1",
          "url": "https://github.com/endavis/pyproject-template/commit/adb60131a3eda062a20f624bc7254eece29638c1"
        },
        "date": 1776185045020,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8991415.715005107,
            "unit": "iter/sec",
            "range": "stddev: 1.0746578048643328e-8",
            "extra": "mean: 111.21719111832122 nsec\nrounds: 90164"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9105955.463260544,
            "unit": "iter/sec",
            "range": "stddev: 1.7400268969170677e-8",
            "extra": "mean: 109.81823972615092 nsec\nrounds: 90253"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5394487.47378101,
            "unit": "iter/sec",
            "range": "stddev: 2.945190567360026e-8",
            "extra": "mean: 185.37442247485603 nsec\nrounds: 55885"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1658362.6588808533,
            "unit": "iter/sec",
            "range": "stddev: 3.1932391743191486e-7",
            "extra": "mean: 603.0044119992731 nsec\nrounds: 57797"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 505683.03166702535,
            "unit": "iter/sec",
            "range": "stddev: 5.521646753665644e-7",
            "extra": "mean: 1.9775233444227276 usec\nrounds: 21397"
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
          "id": "a21c34c7109169172fa678cfcc3075756a5cdc2a",
          "message": "feat: add plan-mode state hook for sub-agent safety (merges PR #393, addresses #392)\n\nAdds two PostToolUse hooks that maintain .claude/.plan-mode-state on\ndisk so tooling can programmatically detect parent plan-mode state\nbefore spawning sub-agents. Parent plan-mode state propagates to\nspawned sub-agents after the sub-agent's first non-readonly action,\nfreezing it — confirmed via diagnostic probes during the #389 session.\n\n- plan-mode-enter.py writes `active` atomically on EnterPlanMode.\n- plan-mode-exit.py writes `inactive` on ExitPlanMode. PostToolUse\n  (not Pre) ensures rejected ExitPlanMode doesn't clear the flag.\n- .gitignore excludes the state file (transient per-session state).\n- 12 pytest cases cover write/overwrite/missing-dir/malformed-stdin/\n  no-trailing-newline/round-trip.\n- docs/development/ai/plan-mode-hook.md documents the contract, the\n  PostToolUse rationale, and the known stale-state limitation.\n\nFollow-up: #389 will be rebased and revised so /implement reads this\nstate file automatically instead of relying on the user to eyeball\nthe CLI status line.\n\nAddresses #392",
          "timestamp": "2026-04-14T19:01:57+01:00",
          "tree_id": "c537644574af2591aa31dfb3ccdc1b025d2dd104",
          "url": "https://github.com/endavis/pyproject-template/commit/a21c34c7109169172fa678cfcc3075756a5cdc2a"
        },
        "date": 1776189742369,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8947067.611493945,
            "unit": "iter/sec",
            "range": "stddev: 1.040644878947395e-8",
            "extra": "mean: 111.7684635260093 nsec\nrounds: 88254"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8732632.985128624,
            "unit": "iter/sec",
            "range": "stddev: 1.0405798927898115e-8",
            "extra": "mean: 114.51299988250575 nsec\nrounds: 85310"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5164435.881043979,
            "unit": "iter/sec",
            "range": "stddev: 2.6230323281371773e-8",
            "extra": "mean: 193.6319906053035 nsec\nrounds: 194932"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1583349.9138575594,
            "unit": "iter/sec",
            "range": "stddev: 2.6298772424966646e-7",
            "extra": "mean: 631.5723335997614 nsec\nrounds: 55237"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 494246.1635383285,
            "unit": "iter/sec",
            "range": "stddev: 4.82042685776247e-7",
            "extra": "mean: 2.023283282243324 usec\nrounds: 49809"
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
          "id": "8897c6e270272c58b0e298f47e96d76ca6c1bc9d",
          "message": "docs: add plan-mode pre-flight check to /implement (merges PR #394, addresses #389)\n\nAddresses #389\n\nThe /implement command spawns a sub-agent via Task to keep raw tool\noutput out of the main conversation context. Earlier sessions (#382,\n#383) showed the sub-agent freezing mid-execution on its first Write.\nInvestigation during #392 established the cause: parent plan-mode state\npropagates into spawned sub-agents and surfaces as a \"Plan mode is\nactive\" reminder after the first readonly tool call, halting further\nwrites.\n\n#392 landed a PostToolUse hook pair that writes parent plan-mode state\nto .claude/.plan-mode-state. This commit consumes that signal:\n\n- Add Step 0 to .claude/commands/implement.md:\n  - Programmatic check: read .claude/.plan-mode-state and abort with a\n    clear user-facing message if the value is `active`.\n  - Status-line backup check: retained for the stale-state case\n    documented in docs/development/ai/plan-mode-hook.md (plan mode can\n    exit without firing ExitPlanMode, or be entered out-of-band).\n- Update the /implement design note in slash-commands.md to describe\n  the pre-flight check and link to plan-mode-hook.md.\n\nThis supersedes the original #389 proposal to inline the sub-agent;\nthe context-hygiene benefit of the sub-agent hop is preserved while\neliminating the reliability trap.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-15T12:35:10+01:00",
          "tree_id": "cf410640f0ba38de546dd96fbd699b42d5cd439a",
          "url": "https://github.com/endavis/pyproject-template/commit/8897c6e270272c58b0e298f47e96d76ca6c1bc9d"
        },
        "date": 1776252938504,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8864759.8964713,
            "unit": "iter/sec",
            "range": "stddev: 1.2170950021100751e-8",
            "extra": "mean: 112.80621378116054 nsec\nrounds: 83244"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8994834.7287268,
            "unit": "iter/sec",
            "range": "stddev: 1.167172665340785e-8",
            "extra": "mean: 111.1749165113952 nsec\nrounds: 91150"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5659638.366590746,
            "unit": "iter/sec",
            "range": "stddev: 2.3221151164962315e-8",
            "extra": "mean: 176.6897344365803 nsec\nrounds: 57764"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1693059.5053543008,
            "unit": "iter/sec",
            "range": "stddev: 2.5190568904819206e-7",
            "extra": "mean: 590.6466942464219 nsec\nrounds: 47599"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 503428.4542302175,
            "unit": "iter/sec",
            "range": "stddev: 5.264507681164416e-7",
            "extra": "mean: 1.9863795770723376 usec\nrounds: 49513"
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
          "id": "c8c2dd9aefc11f99d799e470495b790c8912e9a6",
          "message": "refactor: add mock_subprocess fixture for test_doit_github.py (merges PR #395, addresses #387)\n\nAddresses #387\n\nTests for helpers in tools.doit.github previously set up\npatch(\"tools.doit.github.subprocess.run\", side_effect=...) inline with\na hand-rolled dispatcher keyed by cmd[:N]. Each test spent ~10 lines on\n\"return X when command is Y\" boilerplate, and the pattern was about to\nspread as more subprocess.run callers get tested.\n\nAdd a mock_subprocess fixture in tests/conftest.py that:\n\n- Patches tools.doit.github.subprocess.run.\n- Dispatches by command prefix (first-registered wins).\n- Accepts dict specs ({stdout, stderr, returncode}), BaseException\n  instances to raise, or callables (cmd) -> MagicMock | Exception for\n  the rare case where behavior varies by a later argument.\n- Raises AssertionError on unknown prefixes, preserving the previous\n  safety net.\n- Yields the underlying MagicMock, so call_count / call_args_list /\n  kwargs assertions continue to work unchanged.\n\nMigrate all 14 tests across TestCloseLinkedIssues,\nTestCheckBranchUpToDate, and TestEnsureBranchPushed to the fixture.\nEvery existing assertion is preserved. Drop the now-unused patch\nimport; keep MagicMock (still referenced by one callable-spec return\ntype). Pure refactor — no behavior change in production code, no\ncoverage change.\n\ntests/test_doit_github.py: 377 -> 348 LOC (-29).\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-15T13:23:30+01:00",
          "tree_id": "c86d536b8a199f5f78bda7480bbe045a6812a799",
          "url": "https://github.com/endavis/pyproject-template/commit/c8c2dd9aefc11f99d799e470495b790c8912e9a6"
        },
        "date": 1776255843898,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9164940.398836277,
            "unit": "iter/sec",
            "range": "stddev: 1.163514130962163e-8",
            "extra": "mean: 109.11145697433837 nsec\nrounds: 80626"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9022669.661208916,
            "unit": "iter/sec",
            "range": "stddev: 1.1969633326292316e-8",
            "extra": "mean: 110.83194193613129 nsec\nrounds: 86491"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5396249.855222565,
            "unit": "iter/sec",
            "range": "stddev: 1.782120418545406e-8",
            "extra": "mean: 185.3138803482545 nsec\nrounds: 53405"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1647105.49579901,
            "unit": "iter/sec",
            "range": "stddev: 2.7470205896761173e-7",
            "extra": "mean: 607.1256531840424 nsec\nrounds: 65450"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 483311.95804501936,
            "unit": "iter/sec",
            "range": "stddev: 5.565427922483743e-7",
            "extra": "mean: 2.069057020738668 usec\nrounds: 61767"
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
          "id": "11fea6c386040eb9b1d765693fc3bd386a68b8cb",
          "message": "feat: add doit labels_sync and declarative .github/labels.yml (merges PR #401, addresses #388)\n\nAddresses #388\n\nIntroduce .github/labels.yml as the source of truth for the\nrepository's GitHub labels, plus a doit labels_sync task that\nreconciles the live label set with it.\n\nMotivation: .github/workflows/dependabot-automerge.yml references\nautomerge-blocked and do-not-merge labels that did not actually\nexist on the repo — applying them via gh pr edit failed with\n\"label does not exist\". More broadly, the repo's active label set\nlived only in the GitHub UI with no way for contributors or forks\nto replicate it.\n\nChanges:\n\n- .github/labels.yml: 15-entry flat list of {name, color,\n  description} covering every label used by issue templates,\n  workflows, release notes, and dependabot automation.\n  automerge-blocked and do-not-merge added in red (B60205).\n\n- tools/doit/github.py: new _load_labels_file, _fetch_github_labels,\n  _reconcile_labels helpers and task_labels_sync task. Options:\n  --dry-run (preview, no API calls), --prune (also delete labels\n  on GitHub absent from the file; off by default because deletion\n  is destructive), --file=<path> (default .github/labels.yml).\n  Color comparison is case-insensitive; running twice is a no-op.\n  All subprocess calls use the existing pattern so tests mock via\n  the mock_subprocess fixture from #387.\n\n- tests/test_doit_github.py: new TestLabelsSync class with 12\n  tests covering create / update / no-change / prune / no-prune /\n  dry-run / malformed YAML / missing file / case-insensitive\n  color comparison / empty description / summary counts / file\n  smoke parse. All use the mock_subprocess fixture.\n\n- AGENTS.md, docs/development/github-repository-settings.md,\n  docs/development/doit-tasks-reference.md: document the new\n  task and point contributors at .github/labels.yml as the\n  declarative source.\n\nADR not required (ops/automation task, not an architectural\ndecision; issue has no needs-adr label).\n\nGitHub default labels (duplicate, good first issue, help wanted,\ninvalid, question, wontfix) are intentionally omitted from\nlabels.yml so --prune removes them from a fresh repo sync.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-15T17:27:23+01:00",
          "tree_id": "1fee6dea81336aae33c1d43e2c571ae22a4f6de5",
          "url": "https://github.com/endavis/pyproject-template/commit/11fea6c386040eb9b1d765693fc3bd386a68b8cb"
        },
        "date": 1776270470034,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8892783.888055557,
            "unit": "iter/sec",
            "range": "stddev: 1.3856552185441612e-8",
            "extra": "mean: 112.45072550825857 nsec\nrounds: 87897"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9187846.34872229,
            "unit": "iter/sec",
            "range": "stddev: 1.2720355000467426e-8",
            "extra": "mean: 108.83943440554654 nsec\nrounds: 86829"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6282431.646922494,
            "unit": "iter/sec",
            "range": "stddev: 1.4831705582674631e-8",
            "extra": "mean: 159.17403581937245 nsec\nrounds: 61866"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1719378.3207410173,
            "unit": "iter/sec",
            "range": "stddev: 2.677481725141494e-7",
            "extra": "mean: 581.6055651841767 nsec\nrounds: 56638"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 509830.3985759726,
            "unit": "iter/sec",
            "range": "stddev: 4.656888905986951e-7",
            "extra": "mean: 1.9614365930182656 usec\nrounds: 47479"
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
          "id": "bd7f27d4ea0eb7c5a7ab8722512dc26cde836dae",
          "message": "refactor: remove plan-mode state hook and /implement Step 0 pre-flight (merges PR #403, addresses #402)\n\nAddresses #402. Resolves #396 locally.\n\nPR #393 added a PostToolUse hook pair that wrote\n`.claude/.plan-mode-state` on `EnterPlanMode` / `ExitPlanMode`.\nPR #394 made `/implement`'s Step 0 read that file and abort on\n`active` as a guard against the sub-agent plan-mode-propagation\ntrap.\n\nIssue #396 documented that plan mode can also be toggled via the\n`/plan` slash command and the Esc-Esc keybinding. Neither path\nemits a tool call, so neither path fires the hooks — the state\nfile stays stale or missing while plan mode is genuinely active.\nStep 0 reading that file produced false-negative \"all clear\"\nsignals that caused the spawned sub-agent to freeze mid-execution\n(observed during work on #388). A signal that is wrong more than\nhalf the time is worse than no signal.\n\nThe long-term fix lives in #397 (custom sub-agent with\n`permissionMode: default`, which breaks propagation at the\nClaude Code layer). This commit clears the broken machinery so\nnothing in the repo trusts the unreliable file.\n\nDeleted:\n- tools/hooks/ai/plan-mode-enter.py\n- tools/hooks/ai/plan-mode-exit.py\n- tests/test_hooks_plan_mode.py\n- docs/development/ai/plan-mode-hook.md\n\nModified:\n- .claude/settings.json: drop the two PostToolUse entries for\n  EnterPlanMode / ExitPlanMode. PreToolUse block-dangerous-commands\n  is untouched.\n- .gitignore: drop the `.claude/.plan-mode-state` entry.\n- .claude/commands/implement.md: revert Step 0 to a single\n  preamble warning telling the user to glance at the CLI status\n  line before running. Drop the state-file `cat` snippet, the\n  Step 0 heading, and the link to the deleted plan-mode-hook.md.\n- docs/development/ai/slash-commands.md: update the /implement\n  design note to match.\n- docs/TABLE_OF_CONTENTS.md: drop Plan-Mode State Hook entries.\n\nPost-merge manual step for existing clones: delete any local\n`.claude/.plan-mode-state` file — it is now orphaned (no code\nwrites to it, no longer gitignored).\n\nHook scripts are resurrectable from git history if upstream ever\nfixes hook firing for the `/plan` command and Esc-Esc keybinding.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-15T18:20:32+01:00",
          "tree_id": "1ec3785f07178128054e27631fc395639966f72e",
          "url": "https://github.com/endavis/pyproject-template/commit/bd7f27d4ea0eb7c5a7ab8722512dc26cde836dae"
        },
        "date": 1776273657762,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9134072.84576081,
            "unit": "iter/sec",
            "range": "stddev: 1.197623547753114e-8",
            "extra": "mean: 109.48018664686994 nsec\nrounds: 79347"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8942265.487730986,
            "unit": "iter/sec",
            "range": "stddev: 1.2295340520161149e-8",
            "extra": "mean: 111.82848478073316 nsec\nrounds: 86641"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5016457.030482852,
            "unit": "iter/sec",
            "range": "stddev: 4.6354575229330856e-8",
            "extra": "mean: 199.34387834350622 nsec\nrounds: 197629"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1650759.7531544769,
            "unit": "iter/sec",
            "range": "stddev: 2.9948205038382213e-7",
            "extra": "mean: 605.7816699789753 nsec\nrounds: 64604"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 491234.895843326,
            "unit": "iter/sec",
            "range": "stddev: 4.964391213785693e-7",
            "extra": "mean: 2.0356859996341528 usec\nrounds: 56777"
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
          "id": "5050f50ba2d6e2081da72098d17901c33e112251",
          "message": "feat: add PostToolUse hook to run ruff --fix on edited Python files (merges PR #404, addresses #390)\n\nAddresses #390\n\nClaude Code's Edit / Write / MultiEdit tools leave trivial ruff\nfindings (F401 unused imports, F841 unused locals, I import\nordering) to surface at `doit check` time — often many turns\nafter the edit. The agent then re-opens the file and fixes what\na single `ruff --fix` pass would have cleaned up automatically.\nThe stale diagnostics that result also confuse Pyright follow-up\nruns.\n\nAdds a PostToolUse hook wired in .claude/settings.json for\nmatcher `Edit|Write|MultiEdit`. After each such tool call the\nhook:\n\n- Reads the JSON payload from stdin.\n- Extracts tool_input.file_path and normalizes it against\n  $CLAUDE_PROJECT_DIR.\n- Returns early for non-Python files, paths outside\n  src/ / tests/ / tools/ / bootstrap.py, and missing files.\n- Otherwise runs `uv run ruff check --fix\n  --select F401,F841,I --quiet <path>` followed by\n  `uv run ruff format --quiet <path>`.\n- Always exits 0 — a broken hook must never block a tool call.\n\nScope of fixed rules is deliberately narrow: only the three\ncases where auto-fix requires no judgment. Other findings still\nsurface at `doit check` time.\n\nFiles:\n- tools/hooks/ai/ruff-fix-on-edit.py: new hook script\n  (143 LOC, mode 0755). Module-level run_ruff() so tests can\n  patch it. Every branch wraps in try/except and returns 0.\n  B110 suppressed with nosec + justification: by design the\n  hook swallows all exceptions because surfacing them would\n  block the originating tool call.\n- .claude/settings.json: added PostToolUse block matching\n  Edit|Write|MultiEdit. Existing PreToolUse Bash\n  block-dangerous-commands entry untouched.\n- tests/test_hook_ruff_fix.py: 12 pytest cases covering\n  in-scope / out-of-scope / missing file / malformed stdin /\n  ruff failure / ruff timeout / absolute path branches.\n  importlib loads the hyphen-named hook module.\n- docs/development/ai/ruff-fix-hook.md: scope, rules, how to\n  disable locally, consecutive-edit caveat.\n- docs/TABLE_OF_CONTENTS.md: auto-regenerated.\n\nActivation: the hook takes effect only in fresh Claude Code\nsessions started after merge. Restart existing sessions to pick\nup the new settings.\n\nKnown limitation: consecutive Edit calls on the same file may\nsee their `old_string` go stale if the hook reorders imports or\nremoves a line. Mitigation is editorial — use Write for large\nrewrites, or re-read between edits.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-15T23:59:58+01:00",
          "tree_id": "daf74f07990f0c7238453cab31d67c6f04287e9f",
          "url": "https://github.com/endavis/pyproject-template/commit/5050f50ba2d6e2081da72098d17901c33e112251"
        },
        "date": 1776294028515,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8950069.822632287,
            "unit": "iter/sec",
            "range": "stddev: 1.0967895038956872e-8",
            "extra": "mean: 111.73097191613778 nsec\nrounds: 87559"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8993958.650638746,
            "unit": "iter/sec",
            "range": "stddev: 1.0648072396590221e-8",
            "extra": "mean: 111.18574577046566 nsec\nrounds: 85529"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5387959.673317242,
            "unit": "iter/sec",
            "range": "stddev: 1.4400413724017465e-8",
            "extra": "mean: 185.59901347300232 nsec\nrounds: 53663"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1637661.1896897177,
            "unit": "iter/sec",
            "range": "stddev: 3.265394027653474e-7",
            "extra": "mean: 610.6269149539208 nsec\nrounds: 58748"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 493862.647174937,
            "unit": "iter/sec",
            "range": "stddev: 5.389976968668891e-7",
            "extra": "mean: 2.0248544928844927 usec\nrounds: 50513"
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
          "id": "f6c3a7cebce8ee9cfc9af4784ebc300352fdbf15",
          "message": "refactor: have /implement spawn a custom implement-worker subagent with permissionMode: default (merges PR #405, addresses #397)\n\nAddresses #397\n\n/implement currently spawns a sub-agent via the Task tool with\n`subagent_type: \"general-purpose\"`. When the parent session is\nin plan mode, the sub-agent inherits plan-mode constraints and\nfreezes on its first non-readonly action.\n\nThe prior hook-based workaround (PRs #393 / #394) was removed in\nPR #403 (see #402) because plan-mode entry via the `/plan` slash\ncommand or Esc-Esc keybinding does not fire the PostToolUse\nhooks (see #396 and the upstream observability gap).\n\nPer the Claude Code sub-agents precedence rules, parent\n`bypassPermissions` and `auto` override child `permissionMode`\nfrontmatter — but plan mode is NOT in that precedence list. A\nchild with `permissionMode: default` should escape parent plan\nmode and let the sub-agent write files without freezing.\n\nChanges:\n\n- .claude/agents/implement-worker.md (new, 67 lines): custom\n  Claude Code sub-agent. Frontmatter: `name: implement-worker`,\n  `tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite`\n  (minimum needed; `Task` omitted to prevent nested-subagent\n  recursion), and `permissionMode: default`. Body carries the\n  implementation prompt: project-rules reads, plan fetch via\n  `gh api`, implementation constraints (no branch switch, no\n  commit, no plan mode, type-annotated code), run `doit check`,\n  return summary.\n\n- .claude/commands/implement.md: Step 3 shrunk from ~30 lines\n  to a short paragraph invoking\n  `subagent_type: \"implement-worker\"`. The long inline prompt is\n  gone — the custom sub-agent carries those instructions\n  intrinsically. Step 0 preamble (plan-mode trap warning),\n  Step 1, Step 2, Step 4 preserved verbatim.\n\n- docs/development/ai/slash-commands.md: /implement design note\n  updated to mention the custom sub-agent, the `permissionMode:\n  default` override rationale, and that the status-line preamble\n  remains as belt-and-suspenders.\n\nThe status-line preamble warning is retained as\nbelt-and-suspenders until the override is empirically verified\non this Claude Code version. Claude Code loads sub-agents at\nsession start, so the empirical test requires a fresh session\nafter merge.\n\nIssue #4462 has a v2.1.90 Bedrock observation that the Agent\ntool's `mode` parameter had no effect against a settings.json\n`defaultMode: \"plan\"`. That's a different code path than\nfrontmatter `permissionMode`, but it is a counter-signal worth\nchecking post-merge. If the override turns out not to work on\nour version, the `tools` restriction and context hygiene of the\ncustom sub-agent are still useful on their own.\n\nCo-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-16T00:38:25+01:00",
          "tree_id": "e2a3284da2eab2ec19c7c1928208ad135a9c5907",
          "url": "https://github.com/endavis/pyproject-template/commit/f6c3a7cebce8ee9cfc9af4784ebc300352fdbf15"
        },
        "date": 1776296334189,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8772015.544457098,
            "unit": "iter/sec",
            "range": "stddev: 8.457276408181708e-9",
            "extra": "mean: 113.99888599512167 nsec\nrounds: 87944"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8999254.724433258,
            "unit": "iter/sec",
            "range": "stddev: 7.965940390145962e-9",
            "extra": "mean: 111.12031280601144 nsec\nrounds: 86859"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5622040.238530518,
            "unit": "iter/sec",
            "range": "stddev: 1.0150084514848379e-8",
            "extra": "mean: 177.8713701027118 nsec\nrounds: 54828"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1629027.5266648133,
            "unit": "iter/sec",
            "range": "stddev: 2.018390339596025e-7",
            "extra": "mean: 613.863169057277 nsec\nrounds: 62442"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 511800.45779523876,
            "unit": "iter/sec",
            "range": "stddev: 3.735234916250816e-7",
            "extra": "mean: 1.9538864898789916 usec\nrounds: 50762"
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
          "id": "3a7466522fc2e3eaebdea0088316a13e12f333b3",
          "message": "fix: use tmp/agents/claude/ for finalize PR body temp file (merges PR #407, addresses #406)\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-04-16T15:12:23+01:00",
          "tree_id": "f31cea99569b6df6486f4bf1bdd0c9516013ec9a",
          "url": "https://github.com/endavis/pyproject-template/commit/3a7466522fc2e3eaebdea0088316a13e12f333b3"
        },
        "date": 1776348779705,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8859108.65726289,
            "unit": "iter/sec",
            "range": "stddev: 1.3937995845670141e-8",
            "extra": "mean: 112.87817304060022 nsec\nrounds: 87101"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8665131.94469591,
            "unit": "iter/sec",
            "range": "stddev: 2.681596723417529e-8",
            "extra": "mean: 115.40505169250407 nsec\nrounds: 90245"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5367511.282126211,
            "unit": "iter/sec",
            "range": "stddev: 1.7840631226359138e-8",
            "extra": "mean: 186.30608254704478 nsec\nrounds: 53836"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1654631.9996624195,
            "unit": "iter/sec",
            "range": "stddev: 2.396800529661928e-7",
            "extra": "mean: 604.3639916331979 nsec\nrounds: 57831"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 496427.55015695625,
            "unit": "iter/sec",
            "range": "stddev: 5.002397451136699e-7",
            "extra": "mean: 2.0143926332932742 usec\nrounds: 46751"
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
          "id": "a6bf552d514f036fa962d8b32b2e8a3e901a9001",
          "message": "docs: add GitHub Copilot CLI workflow support and .copilot/ config directory (merges PR #408, addresses #400)\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-04-16T17:29:24+01:00",
          "tree_id": "ff57abb31c77b00dfc0a77ec36fd800ad4daa944",
          "url": "https://github.com/endavis/pyproject-template/commit/a6bf552d514f036fa962d8b32b2e8a3e901a9001"
        },
        "date": 1776356998528,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8365566.114254826,
            "unit": "iter/sec",
            "range": "stddev: 1.521422887107587e-8",
            "extra": "mean: 119.5376363466917 nsec\nrounds: 196156"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8543677.621701593,
            "unit": "iter/sec",
            "range": "stddev: 9.380139184867386e-9",
            "extra": "mean: 117.04561481345266 nsec\nrounds: 84977"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6249117.407714756,
            "unit": "iter/sec",
            "range": "stddev: 1.2489807655211146e-8",
            "extra": "mean: 160.02259755361047 nsec\nrounds: 61889"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 2276694.074892107,
            "unit": "iter/sec",
            "range": "stddev: 1.8164184321949347e-7",
            "extra": "mean: 439.23336517990026 nsec\nrounds: 59649"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 657667.7604501287,
            "unit": "iter/sec",
            "range": "stddev: 3.899036468606324e-7",
            "extra": "mean: 1.5205245872407798 usec\nrounds: 50636"
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
          "id": "64c7aca0128313e98b49143f4d91e00346f8847b",
          "message": "docs: complete Copilot CLI coverage in AI_SETUP, enforcement-principles, first-5-minutes (merges PR #410, addresses #409)\n\nPR #408 landed the initial Copilot CLI integration, but three AI agent\ndocs still described a three-CLI world (Claude, Gemini, Codex). Update\nAI_SETUP.md, enforcement-principles.md, and first-5-minutes.md so they\ndescribe the four-CLI reality already shipped on main. Also link issue\n#409 from ADR 9005.\n\nAddresses #409\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-17T11:45:40+01:00",
          "tree_id": "c844871422974bb8919882ef30140f420387c6d1",
          "url": "https://github.com/endavis/pyproject-template/commit/64c7aca0128313e98b49143f4d91e00346f8847b"
        },
        "date": 1776422769587,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8562836.129519502,
            "unit": "iter/sec",
            "range": "stddev: 2.3121431647969108e-8",
            "extra": "mean: 116.78373670524911 nsec\nrounds: 87628"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9027041.071723886,
            "unit": "iter/sec",
            "range": "stddev: 9.471719171650841e-9",
            "extra": "mean: 110.77827075943844 nsec\nrounds: 86431"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5900646.806512897,
            "unit": "iter/sec",
            "range": "stddev: 1.932018124509351e-8",
            "extra": "mean: 169.47294640584832 nsec\nrounds: 58831"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1631491.227704628,
            "unit": "iter/sec",
            "range": "stddev: 2.4245850200897705e-7",
            "extra": "mean: 612.9361795018148 nsec\nrounds: 57176"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 529619.2333146837,
            "unit": "iter/sec",
            "range": "stddev: 3.5796758218488573e-7",
            "extra": "mean: 1.8881489513539444 usec\nrounds: 51970"
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
          "id": "52a8b95de44a160810309368a0908b5763d5eb24",
          "message": "refactor: gate codecov upload on needs.setup.outputs.newest in ci.yml (merges PR #412, addresses #411)\n\nSwitch the Codecov upload `if:` expression from the hardcoded\n`'3.12'` (the current oldest Python) to the dynamic\n`needs.setup.outputs.newest` output from the setup job, matching the\npattern already used by the docs job at ci.yml:142.\n\nThis makes the filter self-updating: future bumps to\n.github/python-versions.json automatically move the upload to the\nnewest row without a CI edit, and coverage uploads now come from the\nnewest supported Python (conventional) rather than the oldest.\n\nAddresses #411\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-17T15:57:29+01:00",
          "tree_id": "ba4c72e35a22406e2f41bd2bf8be8f3535d26c23",
          "url": "https://github.com/endavis/pyproject-template/commit/52a8b95de44a160810309368a0908b5763d5eb24"
        },
        "date": 1776437872614,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8909728.057664638,
            "unit": "iter/sec",
            "range": "stddev: 1.2150521351866817e-8",
            "extra": "mean: 112.23687115116212 nsec\nrounds: 85092"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8952175.698749807,
            "unit": "iter/sec",
            "range": "stddev: 1.0400991245146157e-8",
            "extra": "mean: 111.70468874283293 nsec\nrounds: 87789"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5370011.620782972,
            "unit": "iter/sec",
            "range": "stddev: 2.928742298191984e-8",
            "extra": "mean: 186.21933631015037 nsec\nrounds: 55764"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1646371.5898317238,
            "unit": "iter/sec",
            "range": "stddev: 2.676404276087878e-7",
            "extra": "mean: 607.396292657243 nsec\nrounds: 56428"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 499727.3597092969,
            "unit": "iter/sec",
            "range": "stddev: 4.935421592857859e-7",
            "extra": "mean: 2.0010911561490716 usec\nrounds: 51878"
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
          "id": "574ccb9da0a0c49ae55c009485ebd5641fc410fe",
          "message": "refactor: extract python-versions.json reader into a reusable composite action (merges PR #414, addresses #413)\n\nIntroduce .github/actions/python-versions/action.yml so every workflow\nthat selects a Python version reads .github/python-versions.json through\na single composite action instead of hardcoding literals. Builds on the\none-shot fix from #411/#412 and generalizes it across the remaining five\nworkflows.\n\nThree workflows flip from the hardcoded oldest (3.12) to newest\n(breaking-change-detection, testpypi, release) — consistency cleanup\nconfirmed during planning; build/analyze jobs converge on newest.\n\nAlso dogfoods the action in ci.yml's setup job, replacing the inline\njq parsing and binding OLDEST/NEWEST as env vars for the matrix script.\nADR-9013's Related Issues section updated to link #413.\n\nAddresses #413\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-17T16:24:06+01:00",
          "tree_id": "70ecb5d433a9c246a06461360c3aa471c7af4aa3",
          "url": "https://github.com/endavis/pyproject-template/commit/574ccb9da0a0c49ae55c009485ebd5641fc410fe"
        },
        "date": 1776439478594,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8610009.53336079,
            "unit": "iter/sec",
            "range": "stddev: 5.94529197632741e-8",
            "extra": "mean: 116.14388998355321 nsec\nrounds: 82224"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8562673.617469797,
            "unit": "iter/sec",
            "range": "stddev: 2.8872380019441372e-8",
            "extra": "mean: 116.78595315834217 nsec\nrounds: 194175"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5250127.64033907,
            "unit": "iter/sec",
            "range": "stddev: 2.597458034379573e-8",
            "extra": "mean: 190.4715596467702 nsec\nrounds: 53666"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1521370.1325201516,
            "unit": "iter/sec",
            "range": "stddev: 4.109523105223309e-7",
            "extra": "mean: 657.3022426459094 nsec\nrounds: 47667"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 484241.6411644701,
            "unit": "iter/sec",
            "range": "stddev: 6.969525422532025e-7",
            "extra": "mean: 2.065084691178707 usec\nrounds: 47195"
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
          "id": "652bb6ea675d1a6e359cced3ae2c872cbf7c0914",
          "message": "chore: add actionlint pre-commit hook for GitHub Actions workflows (merges PR #416, addresses #415)\n\nAdds rhysd/actionlint@v1.7.12 as a pre-commit hook to catch workflow\nerrors locally before they reach CI. Running it across the 9 workflows\nplus the composite action surfaced one real issue, fixed here:\ncodecov/codecov-action@v6 renamed its input from `file:` to `files:`,\nand the stale name was being silently ignored.\n\nUpdates ADR-9009 and the pre-commit hook tables in the dev docs.\n\nAddresses #415\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-18T18:46:42+01:00",
          "tree_id": "9fdf723202bbef1604ad3c52a7e36771943cb0c4",
          "url": "https://github.com/endavis/pyproject-template/commit/652bb6ea675d1a6e359cced3ae2c872cbf7c0914"
        },
        "date": 1776534432032,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8698299.482443815,
            "unit": "iter/sec",
            "range": "stddev: 5.6679509711642024e-8",
            "extra": "mean: 114.96500000009736 nsec\nrounds: 86874"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8888175.824147947,
            "unit": "iter/sec",
            "range": "stddev: 1.1568306428415912e-8",
            "extra": "mean: 112.50902544964715 nsec\nrounds: 88410"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5421544.912571362,
            "unit": "iter/sec",
            "range": "stddev: 1.744927005745406e-8",
            "extra": "mean: 184.4492697425085 nsec\nrounds: 55857"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1672994.839887419,
            "unit": "iter/sec",
            "range": "stddev: 3.237958521199245e-7",
            "extra": "mean: 597.7304748096492 nsec\nrounds: 55390"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 496559.7363908004,
            "unit": "iter/sec",
            "range": "stddev: 6.704978981253124e-7",
            "extra": "mean: 2.0138563937310137 usec\nrounds: 46147"
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
          "id": "78c96cd4670b78f887cd7a36b7b1f988829e3794",
          "message": "fix: label dependabot PRs before calling gh pr merge (merges PR #432, addresses #423)\n\n* fix: apply ready-to-merge label before gh pr merge in dependabot auto-merge workflow\n\nAddresses #423\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* fix: use utf-8 encoding when reading workflow yaml in test\n\nWindows defaults Path.read_text() to cp1252, which cannot decode the\nemoji bytes (✅ ⏸️ 🛑 ⚠️) in the sticky-comment bodies. Explicit utf-8\nmakes the test cross-platform.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-20T13:44:12+01:00",
          "tree_id": "04cff33908303057e2cfdaa0adcb563fc72e040f",
          "url": "https://github.com/endavis/pyproject-template/commit/78c96cd4670b78f887cd7a36b7b1f988829e3794"
        },
        "date": 1776689082773,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8894663.591378309,
            "unit": "iter/sec",
            "range": "stddev: 8.655709562989438e-9",
            "extra": "mean: 112.42696137145765 nsec\nrounds: 46883"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8933784.919181269,
            "unit": "iter/sec",
            "range": "stddev: 1.1507718538183237e-8",
            "extra": "mean: 111.9346401381291 nsec\nrounds: 89840"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5523907.428409524,
            "unit": "iter/sec",
            "range": "stddev: 1.579743607630602e-8",
            "extra": "mean: 181.03127414065406 nsec\nrounds: 54366"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1629016.364461375,
            "unit": "iter/sec",
            "range": "stddev: 2.4991434255433115e-7",
            "extra": "mean: 613.8673753167877 nsec\nrounds: 53150"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 504431.6333506637,
            "unit": "iter/sec",
            "range": "stddev: 4.98060405853557e-7",
            "extra": "mean: 1.9824292012726212 usec\nrounds: 48080"
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
          "id": "b07184a52b3ac96530a6dca0f778ae57f8ef8d60",
          "message": "refactor: convert CodeQL from default setup to advanced workflow (merges PR #433, addresses #431)\n\nAddresses #431\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-20T14:49:30+01:00",
          "tree_id": "b85bd8cddde2ad934e6458918e0a21eb27a95e69",
          "url": "https://github.com/endavis/pyproject-template/commit/b07184a52b3ac96530a6dca0f778ae57f8ef8d60"
        },
        "date": 1776692997679,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8809796.912887633,
            "unit": "iter/sec",
            "range": "stddev: 1.3286389640671801e-8",
            "extra": "mean: 113.5099945989816 nsec\nrounds: 88874"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8617973.138311788,
            "unit": "iter/sec",
            "range": "stddev: 3.373552708883145e-8",
            "extra": "mean: 116.036564973083 nsec\nrounds: 87944"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5500613.986733156,
            "unit": "iter/sec",
            "range": "stddev: 2.2398901936495137e-8",
            "extra": "mean: 181.79788700168461 nsec\nrounds: 54160"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1674778.85693059,
            "unit": "iter/sec",
            "range": "stddev: 2.9759259132657126e-7",
            "extra": "mean: 597.0937571021917 nsec\nrounds: 57297"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 459421.20678077126,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022073206101613806",
            "extra": "mean: 2.17665180718831 usec\nrounds: 49194"
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
          "id": "2e3c9d0d0da7b001f25fa7d7a54868582785cca7",
          "message": "refactor: dedupe dependabot workflow runs via concurrency and label-split (merges PR #434, addresses #424)\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-20T20:02:56+01:00",
          "tree_id": "b0bb86ecbb40622f612d4325bb6138296dc6ba03",
          "url": "https://github.com/endavis/pyproject-template/commit/2e3c9d0d0da7b001f25fa7d7a54868582785cca7"
        },
        "date": 1776711809574,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8949110.113471191,
            "unit": "iter/sec",
            "range": "stddev: 1.3196404498810181e-8",
            "extra": "mean: 111.7429540278747 nsec\nrounds: 87704"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8933340.856427992,
            "unit": "iter/sec",
            "range": "stddev: 1.1363258155747303e-8",
            "extra": "mean: 111.94020423842322 nsec\nrounds: 87789"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5411543.180164302,
            "unit": "iter/sec",
            "range": "stddev: 1.5376208110788467e-8",
            "extra": "mean: 184.7901729150831 nsec\nrounds: 54304"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1702212.1825420493,
            "unit": "iter/sec",
            "range": "stddev: 3.1718594305358155e-7",
            "extra": "mean: 587.4708278180809 nsec\nrounds: 52533"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 498378.06859427475,
            "unit": "iter/sec",
            "range": "stddev: 5.067175388519256e-7",
            "extra": "mean: 2.0065088394049924 usec\nrounds: 45309"
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
          "id": "dae322d1787420bbebdbbfd14d0f88d2250855d8",
          "message": "chore(deps): bump dependabot/fetch-metadata from 2 to 3 (#418)\n\nBumps [dependabot/fetch-metadata](https://github.com/dependabot/fetch-metadata) from 2 to 3.\n- [Release notes](https://github.com/dependabot/fetch-metadata/releases)\n- [Commits](https://github.com/dependabot/fetch-metadata/compare/v2...v3)\n\n---\nupdated-dependencies:\n- dependency-name: dependabot/fetch-metadata\n  dependency-version: '3'\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-21T00:06:02Z",
          "tree_id": "ea0f2110304c0582ea7f75e5ba38b0c62328fa99",
          "url": "https://github.com/endavis/pyproject-template/commit/dae322d1787420bbebdbbfd14d0f88d2250855d8"
        },
        "date": 1776729986553,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9003467.294311205,
            "unit": "iter/sec",
            "range": "stddev: 1.3432405457332195e-8",
            "extra": "mean: 111.06832149341453 nsec\nrounds: 91075"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8833651.271657273,
            "unit": "iter/sec",
            "range": "stddev: 2.4158066251608617e-8",
            "extra": "mean: 113.20347263520523 nsec\nrounds: 87101"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 4864279.58722121,
            "unit": "iter/sec",
            "range": "stddev: 7.776879887004423e-8",
            "extra": "mean: 205.58028831793865 nsec\nrounds: 188680"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1669549.9749210612,
            "unit": "iter/sec",
            "range": "stddev: 3.027500956004537e-7",
            "extra": "mean: 598.9638016359957 nsec\nrounds: 61163"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 495829.3047571126,
            "unit": "iter/sec",
            "range": "stddev: 4.998260302570933e-7",
            "extra": "mean: 2.016823109093685 usec\nrounds: 55701"
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
          "id": "e2df00a136336fa95b700025f69644507bfacab3",
          "message": "feat: stream subprocess output during release tasks instead of silent capture (merges PR #435)\n\nAdds _child_env, run_streamed, and run_teed to tools/doit/base.py and swaps\n13 call sites in tools/doit/release.py from capture_output=True to the\nappropriate streaming helper. run_streamed inherits stdout/stderr (right\nfor long steps whose output isn't parsed); run_teed pipes + tees + buffers\n(right for steps that need both live output and parseable output, like\ncz bump --get-next whose output gets regex-parsed for the version).\n\nrun_teed includes try/except(kill)/finally(close+wait) so a broken parent\nstdout doesn't leave zombie children. PYTHONUNBUFFERED=1 is set on child\nenvironments so Python children flush line-by-line to pipes.\n\nAdds tests/test_doit_release.py with 23 tests covering stdout/stderr\nbehavior, env passing, cwd, exception cleanup, and a timing-based\nregression test that locks in line-by-line streaming.\n\nAddresses #425.\n\nCross-repo port from endavis/pynetappfoundry#633.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T04:51:41+01:00",
          "tree_id": "2c6cce7196da9453c1303d152bd6a874279ba2d9",
          "url": "https://github.com/endavis/pyproject-template/commit/e2df00a136336fa95b700025f69644507bfacab3"
        },
        "date": 1776743524038,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8830660.163332721,
            "unit": "iter/sec",
            "range": "stddev: 1.0884978878604164e-8",
            "extra": "mean: 113.24181675026621 nsec\nrounds: 83809"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8609954.571860276,
            "unit": "iter/sec",
            "range": "stddev: 2.2807985127850733e-8",
            "extra": "mean: 116.14463138612575 nsec\nrounds: 86866"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5196793.724965828,
            "unit": "iter/sec",
            "range": "stddev: 1.478049557518121e-8",
            "extra": "mean: 192.42634072542018 nsec\nrounds: 51584"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1615028.1915366114,
            "unit": "iter/sec",
            "range": "stddev: 3.154747935892077e-7",
            "extra": "mean: 619.1842379225309 nsec\nrounds: 53724"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 490664.3926049786,
            "unit": "iter/sec",
            "range": "stddev: 4.95333572533975e-7",
            "extra": "mean: 2.038052923895528 usec\nrounds: 52925"
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
          "id": "1778be083cb493b2cf3e7d7c1b774c65f2f7e563",
          "message": "fix: enable PR-based pre-releases via regex widen and --prerelease flag (merges PR #436, addresses #426)\n\n* fix: enable PR-based pre-releases via regex widen and --prerelease flag\n\nTwo phases of #426 ported as one PR. Phase C (consolidation + ADR)\ndeferred for a dedicated upstream rewrite.\n\nPhase A — task_release_tag's inline version regex only matched production\nversions, silently failing on pre-release tags (v0.1.0a0 PEP440 or\nv0.1.0-alpha.0 semver). Widen to a module-level _VERSION_PATTERN covering\nboth shapes; extract _extract_version_from_release_pr(pr_title,\nbranch_name) as a named helper.\n\nPhase B — task_release_pr had no way to request a pre-release. Add a\n--prerelease=alpha|beta|rc parameter validated at task entry (mutual-\nexclusion with --increment, allowed-values check). Extract pure helper\n_build_cz_get_next_cmd(increment, prerelease) so the flag flow through\nto cz bump --get-next is testable.\n\nAdds 18 parametrized regression tests across TestExtractVersionFromReleasePR\n(11) and TestBuildCzGetNextCmd (7).\n\nAddresses #426 (Phases A and B).\n\nCross-repo port from endavis/pynetappfoundry#634 (Phase A) and\nendavis/pynetappfoundry#637 (Phase B). Phase C (downstream #638) deferred.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* refactor: consolidate release tasks around the PR-based flow\n\nPhase C of the #426 fix. Phase A widened the release_tag version regex,\nPhase B added --prerelease to task_release_pr (both folded into the\nprior commit on this branch). This phase consolidates the release task\nsurface from three to one:\n\n- Delete task_release_dev (direct-to-main, blocked by no-commit-to-main).\n- Delete the old task_release (also direct-to-main).\n- Rename task_release_pr -> task_release. The PR-based flow is now the\n  single supported entry point.\n\nUpdates the prose-heavy docs (CONTRIBUTING, AGENTS, release-and-automation,\ndoit-tasks-reference, template/migration) and the configure.py template\nhint to match. Drops the now-stale release_dev / release_pr entries from\nthe AI command-blocking hook and its tests.\n\nRecords the architectural decision in ADR-0001 (PR-based release is the\nonly supported flow). Note: downstream pynetappfoundry numbered this\nADR-0016 in their own ADR sequence; renumbered to 0001 here as upstream\nhas no prior ADRs.\n\nAddresses #426 (Phase C; Phases A and B are in the prior commit).\n\nCross-repo port from endavis/pynetappfoundry#638. Phases A and B in\nthis same branch from endavis/pynetappfoundry#634 and #637.\n\nBREAKING CHANGE: doit release no longer commits directly to main; it\nopens a release PR that a reviewer merges, after which doit release_tag\ntags main. doit release_dev and doit release_pr are removed.\nMigration:\n  - doit release (old direct-to-main) -> doit release + merge PR +\n    doit release_tag\n  - doit release_dev --type=alpha      -> doit release --prerelease=alpha\n  - doit release_pr                    -> doit release\n  - doit release_tag                   -> doit release_tag (unchanged)\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T04:58:36+01:00",
          "tree_id": "171e2581f288eee03bbbd633784eb0e48d7956bd",
          "url": "https://github.com/endavis/pyproject-template/commit/1778be083cb493b2cf3e7d7c1b774c65f2f7e563"
        },
        "date": 1776743943991,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8815004.370061753,
            "unit": "iter/sec",
            "range": "stddev: 1.5816645392603842e-8",
            "extra": "mean: 113.44293865540018 nsec\nrounds: 87033"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9015453.232700862,
            "unit": "iter/sec",
            "range": "stddev: 8.278895643703203e-9",
            "extra": "mean: 110.92065747430189 nsec\nrounds: 88551"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 4961403.068271944,
            "unit": "iter/sec",
            "range": "stddev: 6.495226661240218e-8",
            "extra": "mean: 201.55588776791316 nsec\nrounds: 54316"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1524610.6522481872,
            "unit": "iter/sec",
            "range": "stddev: 3.288529180075144e-7",
            "extra": "mean: 655.9051640662502 nsec\nrounds: 65007"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 516599.3286777358,
            "unit": "iter/sec",
            "range": "stddev: 4.5816479844215253e-7",
            "extra": "mean: 1.9357361585419681 usec\nrounds: 55901"
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
          "id": "f0752ba555d9dbb02017cf8c961f2ec473c11bfe",
          "message": "fix: bound validate_merge_commits walk when no tags exist (merges PR #438, addresses #437)\n\nThe no-tag fallback walked full HEAD, surfacing merges inherited from\npre-project ancestor repos and blocking doit release on any repo\nbefore its first tag. Mirror the sibling validate_issue_links helper:\nfall back to HEAD~10..HEAD so only the last 10 commits are scanned.\n\nAdds regression tests using monkeypatched subprocess.run.\n\nAddresses #437.\n\nCross-repo port from endavis/pynetappfoundry#640.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T05:16:57+01:00",
          "tree_id": "75fa2b2a48ea55eb568479e08d8dbb268909a9a1",
          "url": "https://github.com/endavis/pyproject-template/commit/f0752ba555d9dbb02017cf8c961f2ec473c11bfe"
        },
        "date": 1776745041932,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8769592.49110437,
            "unit": "iter/sec",
            "range": "stddev: 1.2430702936154748e-8",
            "extra": "mean: 114.03038408162888 nsec\nrounds: 87169"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8892754.298293255,
            "unit": "iter/sec",
            "range": "stddev: 1.219666876008844e-8",
            "extra": "mean: 112.45109967694995 nsec\nrounds: 87944"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5164361.847766708,
            "unit": "iter/sec",
            "range": "stddev: 1.8505976445353168e-8",
            "extra": "mean: 193.63476640050754 nsec\nrounds: 51905"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1626479.3575383446,
            "unit": "iter/sec",
            "range": "stddev: 3.089471284283661e-7",
            "extra": "mean: 614.8248948658575 nsec\nrounds: 59450"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 487895.4510412123,
            "unit": "iter/sec",
            "range": "stddev: 5.930579059963296e-7",
            "extra": "mean: 2.0496194376600787 usec\nrounds: 50181"
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
          "id": "bdfe2041c213aefdfc8efa7632fceb8644332a80",
          "message": "fix: complete release task wiring (cz --yes, action params, gh search) (merges PR #440, addresses #439)\n\nThree task-internal wiring bugs in the PR-based release flow, all\ndiscovered downstream in sequence as end-to-end TestPyPI verification\ngot further into the chain. Combined here as one upstream PR because\neach bug only became visible after the prior one was fixed.\n\n1. cz bump --get-next interactivity + version pollution. The command\n   prompts on a tagless repo and (with capture_output) the prompt can't\n   reach stdin — cz dumps diagnostic text + Cancelled by user into\n   stdout and the task interpolates the whole blob into the\n   release/v<version> branch name. Pass --yes; add a defensive\n   _extract_next_version_from_cz_output helper that scans stdout from\n   the last line backward and returns only lines fully matching the\n   version pattern.\n\n2. --prerelease and --increment CLI flags silently dropped. doit's\n   params parsing populates the action function's kwargs, not the outer\n   task-creator's parameters. task_release(increment, prerelease) had\n   the values on the wrong function and create_release_pr() took no\n   args, so doit had nowhere to deliver parsed values. Move the kwargs\n   onto create_release_pr matching params[n][\"name\"]. Adds two\n   regression tests pinning the action signature.\n\n3. release_tag gh search uses colon qualifier syntax. The search\n   \"release: v in:title\" is parsed by GitHub as the qualifier \"release:\"\n   followed by \"v in:title\" and returns zero matches even when a\n   merged release PR exists. Swap to \"head:release/\" — GitHub's built-in\n   head-branch prefix qualifier.\n\nAdds 12 new test cases across TestExtractNextVersionFromCzOutput (9),\nTestTaskReleaseActionSignature (2), and TestReleaseTagGhSearch (1).\n\nAddresses #439.\n\nCross-repo port from endavis/pynetappfoundry#642 (cz --yes), #651\n(action params), #658 (gh search).\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T05:27:28+01:00",
          "tree_id": "5baff66ce7546252aa383f0056c0c7bd8680c9a6",
          "url": "https://github.com/endavis/pyproject-template/commit/bdfe2041c213aefdfc8efa7632fceb8644332a80"
        },
        "date": 1776745673874,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8530334.497524159,
            "unit": "iter/sec",
            "range": "stddev: 1.1425306829706481e-8",
            "extra": "mean: 117.22869722051809 nsec\nrounds: 87321"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8937174.282605726,
            "unit": "iter/sec",
            "range": "stddev: 1.2563543862264797e-8",
            "extra": "mean: 111.89218967635928 nsec\nrounds: 86716"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5199403.847253671,
            "unit": "iter/sec",
            "range": "stddev: 3.545258203983522e-8",
            "extra": "mean: 192.3297419045841 nsec\nrounds: 177905"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1666265.843590178,
            "unit": "iter/sec",
            "range": "stddev: 2.6707923144754335e-7",
            "extra": "mean: 600.1443310182575 nsec\nrounds: 55054"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 500762.07211209903,
            "unit": "iter/sec",
            "range": "stddev: 5.791727735232755e-7",
            "extra": "mean: 1.9969563505123908 usec\nrounds: 26667"
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
          "id": "3b1a5a2e9c2766ed44a83bab3257877f54cb2d06",
          "message": "fix: accept release as a conventional type in all three validators (merges PR #442, addresses #441)\n\nThree validators in this template rejected release as a conventional-\ncommit type, blocking the release flow at multiple gates:\n\n1. CI title check (.github/workflows/pr-checks.yml) — Validate PR\n   Title Format regex was the 8 standard types only. Release PRs\n   titled \"release: v<version>\" failed the check.\n2. Governance check (validate_merge_commits in release.py) — same\n   regex. Merge commits of release PRs failed the next release's\n   governance validation.\n3. doit pr_merge title check (github.py) — same regex. Release PRs\n   couldn't be merged through the doit wrapper.\n\nExtend the regex in all three to accept release. Hoist pr_merge's\ninline regex into module-level _PR_TITLE_PATTERN for testability.\nSync the documented Valid Types list in release-and-automation.md.\n\nNote: the test_release_type_merge_commit_passes regression test from\ndownstream PR #654 depends on TestValidateMergeCommits which is in\nPR #438 (not this branch's chain). Will be added when this and #438\nboth land and someone rebases.\n\n19 new test cases for _PR_TITLE_PATTERN covering all 8 standard types\nplus release variants and rejection of malformed titles.\n\nAddresses #441.\n\nCross-repo port from endavis/pynetappfoundry#654 (CI + governance) and\n#656 (pr_merge).\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T05:33:09+01:00",
          "tree_id": "ca032de98e54e355c9d8312ee17e9d598f4c0111",
          "url": "https://github.com/endavis/pyproject-template/commit/3b1a5a2e9c2766ed44a83bab3257877f54cb2d06"
        },
        "date": 1776746015800,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8954894.985300254,
            "unit": "iter/sec",
            "range": "stddev: 1.201852798748485e-8",
            "extra": "mean: 111.67076795892437 nsec\nrounds: 87101"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8788013.495752625,
            "unit": "iter/sec",
            "range": "stddev: 1.593130817941715e-8",
            "extra": "mean: 113.79135916021458 nsec\nrounds: 87635"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5005731.182824398,
            "unit": "iter/sec",
            "range": "stddev: 4.859868560628586e-8",
            "extra": "mean: 199.77101515782297 nsec\nrounds: 184129"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1611203.0546095283,
            "unit": "iter/sec",
            "range": "stddev: 3.5462154966516427e-7",
            "extra": "mean: 620.6542354416948 nsec\nrounds: 56712"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 454411.8355348535,
            "unit": "iter/sec",
            "range": "stddev: 9.762828868059498e-7",
            "extra": "mean: 2.2006469061770284 usec\nrounds: 54334"
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
          "id": "0400ae95831060066688c38e4bf35d0eb1ff74a9",
          "message": "fix: align release pipeline workflows with PEP440 tags and twine (merges PR #444, addresses #443)\n\nTwo workflow-YAML defects in the release pipeline that block actual\npublish to PyPI/TestPyPI.\n\n1. testpypi.yml tag trigger uses semver glob (v*-[a-zA-Z]*), which\n   requires a literal dash before the pre-release type. commitizen\n   (used by doit release --prerelease=...) emits PEP440 tags with no\n   dash: v0.1.0a0, v0.1.0b1, v0.1.0rc0, v0.1.0.dev2. Pushing a PEP440\n   pre-release tag does nothing; no workflow triggers.\n\n   Replace the semver glob with four PEP440 globs covering alpha, beta,\n   rc, dev. PEP440-only chosen over both-formats because PyPI expects\n   PEP440 natively and commitizen is the only tag source.\n\n2. release.yml builds SBOMs into dist/ alongside the wheels and uploads\n   the entire directory as one artifact. The publish jobs hand\n   packages-dir: dist to pypa/gh-action-pypi-publish, which calls twine.\n   Twine inspects every file in packages-dir and rejects sbom.json with\n   \"InvalidDistribution: Unknown distribution format\". publish-testpypi\n   and publish both fail; github-release is skipped.\n\n   Split the build output into two artifacts: dist (wheels + sdist\n   only, consumed by the publish jobs) and sbom (consumed by\n   github-release). Publish jobs are unchanged; github-release\n   downloads sbom into dist/ so the existing gh release upload line\n   keeps working.\n\nAdds 6 structural-YAML regression tests (4 in TestPushTagTriggers, 3 in\nTestBuildArtifactsSeparation, minus 1 since one was a delta) plus\nsynced docs in release-and-automation.md and CONTRIBUTING.md.\n\nAddresses #443.\n\nCross-repo port from endavis/pynetappfoundry#660 (testpypi.yml PEP440)\nand #666 (release.yml split SBOMs).\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T05:39:14+01:00",
          "tree_id": "0bd2f397767679a01bea0141cdcc8059557a5ebc",
          "url": "https://github.com/endavis/pyproject-template/commit/0400ae95831060066688c38e4bf35d0eb1ff74a9"
        },
        "date": 1776746380246,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8340996.136511147,
            "unit": "iter/sec",
            "range": "stddev: 3.171310020032765e-8",
            "extra": "mean: 119.88975700668263 nsec\nrounds: 83459"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8820633.514706725,
            "unit": "iter/sec",
            "range": "stddev: 2.255810761077298e-8",
            "extra": "mean: 113.37054173407054 nsec\nrounds: 87866"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5405985.679874709,
            "unit": "iter/sec",
            "range": "stddev: 9.735174908044425e-8",
            "extra": "mean: 184.9801422380343 nsec\nrounds: 53291"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1666165.9526902956,
            "unit": "iter/sec",
            "range": "stddev: 4.884092102891794e-7",
            "extra": "mean: 600.180311202097 nsec\nrounds: 56042"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 491125.20565219526,
            "unit": "iter/sec",
            "range": "stddev: 5.378189702529362e-7",
            "extra": "mean: 2.0361406592276987 usec\nrounds: 54337"
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
          "id": "446866f4f628a39672861ed3662f4e6d2842dc76",
          "message": "fix: drop obsolete assume-unchanged step from install_dev (merges PR #446, addresses #445)\n\ntask_install_dev ran git update-index --assume-unchanged on\nsrc/package_name/_version.py after uv sync. That command requires the\nfile to be tracked, but _version.py is correctly gitignored and\nuntracked in this template (its own header says \"don't track in\nversion control\"). doit install_dev fails on a fresh clone with:\n\n    fatal: Unable to mark file src/package_name/_version.py\n\nThe assume-unchanged step dates to when _version.py was incorrectly\ntracked. Now that it isn't, the workaround is obsolete and breaks the\ninstall task.\n\nRemove the action from task_install_dev. Drop the matching docstring\nsentence. Sync doit-tasks-reference.md's install_dev entry to remove\nthe assume-unchanged description and add a note explaining _version.py\nis a build-time artifact that's gitignored and untracked.\n\nReplace the two existing tests\n(test_actions_contain_assume_unchanged, test_uv_sync_runs_before_assume_unchanged)\nwith a single regression test asserting assume-unchanged does NOT\nappear in the action list.\n\nAddresses #445.\n\nCross-repo context: downstream endavis/pynetappfoundry had the inverse\nbug — _version.py was incorrectly tracked, the workaround silenced its\ndirty-tree symptom, and TestPyPI eventually rejected the resulting\nlocal-version suffix. Downstream PR #662 untracked the file and\nremoved the install_dev workaround in one commit. Upstream already has\nthe file untracked, so only the install_dev cleanup applies here.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T05:43:07+01:00",
          "tree_id": "292c64b89a34e3b945ddcf36ef4fd1879cc09c42",
          "url": "https://github.com/endavis/pyproject-template/commit/446866f4f628a39672861ed3662f4e6d2842dc76"
        },
        "date": 1776746609966,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9044830.16403809,
            "unit": "iter/sec",
            "range": "stddev: 1.1147328270965212e-8",
            "extra": "mean: 110.56039548160486 nsec\nrounds: 85339"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8775985.448193187,
            "unit": "iter/sec",
            "range": "stddev: 1.1401400352016784e-8",
            "extra": "mean: 113.9473174725787 nsec\nrounds: 84905"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6476256.154160645,
            "unit": "iter/sec",
            "range": "stddev: 1.5371286809218592e-8",
            "extra": "mean: 154.41019876237507 nsec\nrounds: 63040"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1776134.263822376,
            "unit": "iter/sec",
            "range": "stddev: 2.1812781953261713e-7",
            "extra": "mean: 563.020499276853 nsec\nrounds: 57124"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 504933.1704986517,
            "unit": "iter/sec",
            "range": "stddev: 4.3799604030312266e-7",
            "extra": "mean: 1.9804601052698523 usec\nrounds: 47124"
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
          "id": "302da19556f12b9b1c79497c1b93f427accecb36",
          "message": "refactor: enforce explicit UTF-8 encoding for all text-mode file I/O (merges PR #449, addresses #430)\n\n* refactor: add encoding=\"utf-8\" to production text-mode file I/O\n\nText-mode file I/O in tools/, examples/, and bootstrap.py relied on\nlocale.getpreferredencoding() for decoding. On Windows this is cp1252,\nwhich raises UnicodeDecodeError on any non-cp1252 character (emoji,\ncurly quotes, em dashes) the moment such content lands in a file these\ncallers read or write.\n\nAdd encoding=\"utf-8\" to every text-mode read_text(), write_text(), and\nopen() call in production code. Binary-mode calls (.open(\"rb\"),\ntarfile.open(), urlopen()) are intentionally untouched.\n\nsrc/ was already clean. This is the first of a three-part sweep;\ntests follow in the next commit and a ruff guardrail prevents\nregression in the one after.\n\nAddresses #430\n\n* refactor: add encoding=\"utf-8\" to test text-mode file I/O\n\nMirror the production-code pass across the test suite. Every\ntext-mode read_text(), write_text(), and open() call in tests/ now\nspecifies encoding=\"utf-8\".\n\nThe highlighted site is tests/test_benchmark_workflow.py: it reads\n.github/workflows/benchmark.yml with no encoding, so a single emoji\nadded to that workflow would silently break this test on Windows CI.\nReuse the inline comment pattern from tests/test_doit_release.py:665\nso a future reader immediately sees why encoding=\"utf-8\" is not\noptional there.\n\nAddresses #430\n\n* refactor: enable ruff PLW1514 to require explicit encoding\n\nAdd PLW1514 (unspecified-encoding) to the [tool.ruff.lint] select\nlist so every future text-mode read_text(), write_text(), open(), and\ntempfile.NamedTemporaryFile() call must pass encoding= explicitly.\n\nPLW1514 is a preview rule, so enable preview mode and pair it with\nexplicit-preview-rules = true; that combination pulls in only the\nexact codes listed in select, keeping the rest of the preview\nruleset out of CI.\n\nEnabling the rule also surfaced two tempfile.NamedTemporaryFile sites\nmissed by the pathlib-focused audit — tools/doit/adr.py and\ntools/doit/github.py — which are fixed here so doit check stays\ngreen.\n\nAddresses #430\n\n* docs: document explicit UTF-8 file I/O convention\n\nRecord the repo convention of always passing encoding=\"utf-8\" to\ntext-mode file I/O under the Python Standards section of\nCONTRIBUTING.md, and note that ruff's PLW1514 enforces it. Include\nthe list of binary-mode calls that are exempt (and cannot accept an\nencoding kwarg) so readers do not get tripped up when PLW1514\nappears clean.\n\nAddresses #430\n\n* docs: propagate utf-8 encoding convention to code examples\n\nUpdate the two code snippets in docs/ that illustrate file I/O so they\nmodel the project convention codified in CONTRIBUTING.md and enforced\nby ruff PLW1514: the open() example in coding-standards.md and the\ntmp_path.write_text() example in ci-cd-testing.md now pass\nencoding=\"utf-8\".\n\nAddresses #430",
          "timestamp": "2026-04-21T13:26:27+01:00",
          "tree_id": "ec8ae147aec3fa8d4b515a087bcd2227e5e6336e",
          "url": "https://github.com/endavis/pyproject-template/commit/302da19556f12b9b1c79497c1b93f427accecb36"
        },
        "date": 1776774417067,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8869193.446969496,
            "unit": "iter/sec",
            "range": "stddev: 1.1177602913765396e-8",
            "extra": "mean: 112.74982398108466 nsec\nrounds: 87093"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9022416.46785514,
            "unit": "iter/sec",
            "range": "stddev: 1.1176429782284787e-8",
            "extra": "mean: 110.83505217951058 nsec\nrounds: 88637"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5276552.456157744,
            "unit": "iter/sec",
            "range": "stddev: 1.491488264915281e-8",
            "extra": "mean: 189.51768381133002 nsec\nrounds: 53778"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1686048.1087935392,
            "unit": "iter/sec",
            "range": "stddev: 2.73613106991902e-7",
            "extra": "mean: 593.1028864387241 nsec\nrounds: 57199"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 493909.48561723385,
            "unit": "iter/sec",
            "range": "stddev: 5.244431709792189e-7",
            "extra": "mean: 2.0246624718096067 usec\nrounds: 49584"
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
          "id": "4934019344dc1fc28f7fbf221ed6705c9647d77b",
          "message": "fix: refuse doit release --prerelease on tagless repos (merges PR #450, addresses #448)\n\ncz bump --get-next --yes --prerelease alpha on a tagless repo silently\nreturns the first-version default (0.1.0) and drops --prerelease entirely\nbecause it has no anchor to bump from. The task then happily creates\nrelease/v0.1.0 and opens a production release PR when an alpha was\nrequested — if the user doesn't notice, running release_tag would push\nstraight to PyPI instead of TestPyPI.\n\nAdd a pre-flight guard in task_release: if --prerelease is set and the\nrepo has no v* tags, exit 1 with a red error banner plus two-option\nguidance (seed a baseline tag and retry, or drop --prerelease for a\nproduction first release). New helper _repo_has_version_tags() shells\nout to git tag --list v* and powers the check.\n\nFour new tests in TestRepoHasVersionTags cover empty output,\nwhitespace-only output, single tag, and multiple tags using the\nsubprocess monkeypatch pattern from #437.\n\nAddresses #448.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T13:35:12+01:00",
          "tree_id": "425c57d7e6ba411de2120b776e0fd67d2d70c2fd",
          "url": "https://github.com/endavis/pyproject-template/commit/4934019344dc1fc28f7fbf221ed6705c9647d77b"
        },
        "date": 1776774941277,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8682927.088663163,
            "unit": "iter/sec",
            "range": "stddev: 1.5905944834902313e-8",
            "extra": "mean: 115.16853588528309 nsec\nrounds: 87459"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8945130.447594747,
            "unit": "iter/sec",
            "range": "stddev: 3.3407270487440015e-8",
            "extra": "mean: 111.7926681850559 nsec\nrounds: 89574"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5725190.520709826,
            "unit": "iter/sec",
            "range": "stddev: 9.703123758972309e-9",
            "extra": "mean: 174.6666763983982 nsec\nrounds: 56174"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1574408.3153830986,
            "unit": "iter/sec",
            "range": "stddev: 1.4026412215422724e-7",
            "extra": "mean: 635.1592469560042 nsec\nrounds: 62626"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 526865.0531751502,
            "unit": "iter/sec",
            "range": "stddev: 2.9016578602814746e-7",
            "extra": "mean: 1.8980192251763595 usec\nrounds: 48114"
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
          "id": "3ded4082f90788b12930fca329d647c2bad845b3",
          "message": "feat: auto-seed v0.0.0 baseline tag in template bootstrap (merges PR #451, addresses #447)\n\ndoit release --prerelease=alpha|beta|rc requires a v* anchor tag so\ncommitizen can compute the pre-release version. After #448 landed, the\ntask refuses on a tagless repo instead of silently producing a\nproduction version — closing the footgun but leaving a one-time\npapercut for anyone bootstrapping a new project that wants to cut a\npre-release before their first production release.\n\nShip the papercut fix in two layers:\n\n1. tools/pyproject_template/configure.py now auto-seeds v0.0.0 on the\n   root commit. Helpers _git_has_version_tag and _git_root_commit check\n   preconditions; seed_baseline_tag is idempotent (skips if any v* tag\n   exists) and degrades gracefully (with a visible Logger message) when\n   outside a git repo or with no commits yet — the user can then seed\n   manually with `git tag v0.0.0 <root-commit>` after the first commit.\n\n2. docs/development/release-and-automation.md gets a new \"Before your\n   first pre-release\" subsection with the manual seeding commands for\n   existing projects that predate the auto-seed. The release task entry\n   in doit-tasks-reference.md cross-links there under Requirements.\n\nThree tests in TestSeedBaselineTag cover the two AC cases (no tags, tag\nexists) plus a safe-no-op fall-through for the not-a-git-repo case.\nUses real tmp_path git repos with env-seeded author/committer so no\nuser git config is assumed.\n\nAddresses #447.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T13:57:46+01:00",
          "tree_id": "e518477f4b270c42c68b95600dc1bf48ab98e15e",
          "url": "https://github.com/endavis/pyproject-template/commit/3ded4082f90788b12930fca329d647c2bad845b3"
        },
        "date": 1776776293063,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8677717.344655903,
            "unit": "iter/sec",
            "range": "stddev: 1.2266883872817205e-8",
            "extra": "mean: 115.23767832975582 nsec\nrounds: 82768"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8518083.069478335,
            "unit": "iter/sec",
            "range": "stddev: 1.633459570914269e-8",
            "extra": "mean: 117.39730545516295 nsec\nrounds: 82693"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 4840672.706715344,
            "unit": "iter/sec",
            "range": "stddev: 6.736563436043743e-8",
            "extra": "mean: 206.58285750505812 nsec\nrounds: 191205"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1656058.7148774636,
            "unit": "iter/sec",
            "range": "stddev: 3.8033982243068255e-7",
            "extra": "mean: 603.8433245248751 nsec\nrounds: 54131"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 477604.36346452456,
            "unit": "iter/sec",
            "range": "stddev: 7.694173400848157e-7",
            "extra": "mean: 2.093783215768877 usec\nrounds: 48057"
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
          "id": "81f88c60d996ba05ad69677334ee9d3b1b111ed2",
          "message": "feat: add doit tasks to create GitHub environments for PyPI trusted publishing (merges PR #452, addresses #417)\n\n* feat: add doit env_create, env_list, publish_setup tasks\n\nAdd three idempotent doit tasks and their GitHub API helpers to\n``tools/doit/github.py``:\n\n- ``env_create --name=<name>``: create a GitHub environment by name,\n  skipping when it already exists.\n- ``env_list``: list existing environments (sorted alphabetically).\n- ``publish_setup``: create the ``testpypi`` and ``pypi`` environments\n  required for PyPI trusted publishing and print the manual\n  follow-up steps (registering the project on PyPI/TestPyPI) that\n  cannot be automated.\n\nAddresses #417\n\n* test: cover env helpers and tasks via mock_subprocess\n\nAdd 18 tests covering the new ``_gh_repo_slug``, ``_gh_env_exists``,\n``_gh_env_create``, ``_gh_env_list`` helpers and the ``env_create``,\n``env_list``, ``publish_setup`` tasks. Tests use the existing\nprefix-dispatch ``mock_subprocess`` fixture and verify command\nconstruction, the existing-vs-missing-env branches, and idempotence\nof ``publish_setup``.\n\nAddresses #417\n\n* docs: document doit env_create / env_list / publish_setup\n\nAdd a \"GitHub Environments & Trusted Publishing\" section to\n``release-and-automation.md`` that explains the role of the\n``testpypi`` and ``pypi`` environments for OIDC publishing, presents\n``doit publish_setup`` as the one-step bootstrap, and calls out the\nmanual trusted-publisher registration step with links to the PyPI and\nTestPyPI management pages.\n\nAdd matching entries for ``env_create``, ``env_list``, and\n``publish_setup`` to ``doit-tasks-reference.md``, and update the\nGitHub Workflow task category row to include them.\n\nAddresses #417\n\n* docs: point env/publish guides to doit publish_setup\n\nUpdate the two docs pages that still told readers to create the\n``testpypi`` and ``pypi`` environments manually through the GitHub\nSettings UI: ``github-repository-settings.md`` (the OIDC trusted\npublisher section and the summary of manual steps) and\n``new-project.md`` (the post-configure and manual-setup Step 5\nchecklists). Each now points at ``doit publish_setup`` as the one-step\nbootstrap and cross-links the new \"GitHub Environments & Trusted\nPublishing\" section in the release automation guide.\n\nAddresses #417",
          "timestamp": "2026-04-21T16:13:05+01:00",
          "tree_id": "aa418afab15bed1951b8167179699c73e41bc20b",
          "url": "https://github.com/endavis/pyproject-template/commit/81f88c60d996ba05ad69677334ee9d3b1b111ed2"
        },
        "date": 1776784413803,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8927384.828237219,
            "unit": "iter/sec",
            "range": "stddev: 1.4592833598102395e-8",
            "extra": "mean: 112.01488669302248 nsec\nrounds: 87329"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8986804.407048628,
            "unit": "iter/sec",
            "range": "stddev: 1.0691944053683434e-8",
            "extra": "mean: 111.27425886955649 nsec\nrounds: 89350"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5401705.381754986,
            "unit": "iter/sec",
            "range": "stddev: 1.5820731743039602e-8",
            "extra": "mean: 185.12672004986416 nsec\nrounds: 54574"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1652310.0391105174,
            "unit": "iter/sec",
            "range": "stddev: 2.8396203400816643e-7",
            "extra": "mean: 605.2132931046807 nsec\nrounds: 37779"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 502786.41791054734,
            "unit": "iter/sec",
            "range": "stddev: 4.6768400892726994e-7",
            "extra": "mean: 1.988916097128769 usec\nrounds: 51798"
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
          "id": "4c1d3a9b6d7afe70f9bfea461786d310ef98058d",
          "message": "refactor: use App token for ready-to-merge label to trigger Merge Gate (merges PR #453, addresses #428)\n\nGitHub's loop-prevention rule suppresses downstream workflows for events\nproduced by GITHUB_TOKEN, so the labeled event never fired the Merge Gate\nafter dependabot-automerge applied the ready-to-merge label. The gate\nstayed red and auto-merge never fired.\n\nGenerate a GitHub App token (conditional on vars.RELEASE_APP_ID) and use\nit for the label step, falling back to GITHUB_TOKEN when the App is not\nconfigured. Expose APP_TOKEN_CONFIGURED to the sticky comment so the\nuser sees a distinct message when falling back, pointing at the manual\nrelabel workaround. Keep the merge step on GITHUB_TOKEN (it does not\ntrigger downstream workflows). Drop the job-level GH_TOKEN so the token\nchoice is explicit on each step.\n\nAddresses #428\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T17:32:06+01:00",
          "tree_id": "0b4a65ce9ec049fc7a6ff999ff3c829400a3d76e",
          "url": "https://github.com/endavis/pyproject-template/commit/4c1d3a9b6d7afe70f9bfea461786d310ef98058d"
        },
        "date": 1776789151557,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8155846.227839877,
            "unit": "iter/sec",
            "range": "stddev: 4.017715073377181e-8",
            "extra": "mean: 122.61143381866528 nsec\nrounds: 198847"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8864543.6181714,
            "unit": "iter/sec",
            "range": "stddev: 1.5014532593671498e-8",
            "extra": "mean: 112.80896604198588 nsec\nrounds: 88021"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5298893.190022371,
            "unit": "iter/sec",
            "range": "stddev: 1.903004471342153e-8",
            "extra": "mean: 188.71865579079133 nsec\nrounds: 53206"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1670140.32883412,
            "unit": "iter/sec",
            "range": "stddev: 2.570944367985483e-7",
            "extra": "mean: 598.7520825259475 nsec\nrounds: 52340"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 493710.5733625546,
            "unit": "iter/sec",
            "range": "stddev: 5.204472556737453e-7",
            "extra": "mean: 2.0254781930012533 usec\nrounds: 47416"
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
          "id": "3a8caa73b34617ab1afcf7e8dcd04b2ad629c2a9",
          "message": "docs: document allow_auto_merge as a required repository setting (merges PR #454, addresses #427)\n\ndoc: document allow_auto_merge as a required repository setting\n\nThe setting is required by the dependabot auto-merge workflow's\n`Enable auto-merge (squash)` step but was only copied implicitly via\n`configure_repository_settings()` and absent from the Repository\nSettings table, so operators discovered it via a workflow failure\n(\"Pull request Auto merge is not allowed for this repository\") rather\nthan the docs. Bugs #419 and #423 both traced to this gap.\n\nAdd an explicit \"Allow auto-merge | Yes\" row to the settings table,\nturn the inline `allow_auto_merge` reference in dependabot-automerge.md\ninto a bidirectional link, and add a header comment to\n`.github/workflows/dependabot-automerge.yml` so readers of the YAML can\nfind the setting requirement.\n\nAddresses #427\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T17:47:07+01:00",
          "tree_id": "0e005dcc9b71b6bff43a6459f85c46a03f831f74",
          "url": "https://github.com/endavis/pyproject-template/commit/3a8caa73b34617ab1afcf7e8dcd04b2ad629c2a9"
        },
        "date": 1776790053423,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9075472.76435698,
            "unit": "iter/sec",
            "range": "stddev: 1.1935341756584096e-8",
            "extra": "mean: 110.18709724163361 nsec\nrounds: 88285"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8844583.930798218,
            "unit": "iter/sec",
            "range": "stddev: 1.1385372435499374e-8",
            "extra": "mean: 113.06354350008986 nsec\nrounds: 89310"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6349358.859343391,
            "unit": "iter/sec",
            "range": "stddev: 1.4427901787757871e-8",
            "extra": "mean: 157.49621688628474 nsec\nrounds: 62097"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1779456.4174981783,
            "unit": "iter/sec",
            "range": "stddev: 2.705714423782453e-7",
            "extra": "mean: 561.9693689413012 nsec\nrounds: 56348"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 505147.0828181149,
            "unit": "iter/sec",
            "range": "stddev: 5.073156767397916e-7",
            "extra": "mean: 1.9796214489079087 usec\nrounds: 44916"
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
          "id": "2745e5d7262fcdd17944b489f84e8937931cdc68",
          "message": "refactor: normalize \"doc\" to \"docs\" across tooling, tests, and docs (merges PR #456, addresses #455)\n\nRename the doit issue-type flag from \"doc\" to \"docs\" so a single\nspelling is used everywhere the word acts as a type identifier or\nConventional Commits prefix. Also fix the AGENTS.md documentation\nexample that was using an invalid `doc:` title prefix (the PR-title\nvalidator requires `docs:`).\n\nThe ISSUE_TYPE_TO_FILE mapping key changes from \"doc\" to \"docs\" and\ndownstream docstrings, help strings, tests, and documentation are\nflipped to match. A new regression test asserts that the legacy \"doc\"\nkey now raises ValueError.\n\nThe `.github/ISSUE_TEMPLATE/documentation.yml` filename is kept as-is\nbecause it is user-visible in the GitHub \"New Issue\" picker, where the\nfull word is appropriate.\n\nBREAKING CHANGE: `doit issue --type=doc` no longer works. Use\n`doit issue --type=docs` instead. The CLI now raises\n`ValueError: Invalid issue type` for the old flag value. Update any\nlocal scripts, shell aliases, or automation that invoke\n`doit issue --type=doc`.\n\nAddresses #455\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T18:42:08+01:00",
          "tree_id": "984eac8a1d2c2a97c77bd13972ae039ee2dd26bc",
          "url": "https://github.com/endavis/pyproject-template/commit/2745e5d7262fcdd17944b489f84e8937931cdc68"
        },
        "date": 1776793352845,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8808605.533461247,
            "unit": "iter/sec",
            "range": "stddev: 1.2350109211215638e-8",
            "extra": "mean: 113.52534702584879 nsec\nrounds: 88567"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8906534.710612835,
            "unit": "iter/sec",
            "range": "stddev: 1.1366374784499495e-8",
            "extra": "mean: 112.27711253495947 nsec\nrounds: 87866"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5485771.76086242,
            "unit": "iter/sec",
            "range": "stddev: 1.747681410571193e-8",
            "extra": "mean: 182.289756773036 nsec\nrounds: 55298"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1667361.3642500413,
            "unit": "iter/sec",
            "range": "stddev: 3.1866558971115554e-7",
            "extra": "mean: 599.7500130691752 nsec\nrounds: 57003"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 496042.06837297144,
            "unit": "iter/sec",
            "range": "stddev: 5.370697505935341e-7",
            "extra": "mean: 2.01595804823575 usec\nrounds: 55826"
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
          "id": "d6fa39c22b3c0752da7c862e13896198388d5b99",
          "message": "fix: bump lxml to 6.1.0 in uv.lock to resolve CVE-2026-41066 (merges PR #460, addresses #459)\n\nlxml 6.0.2 is a transitive dep (via cyclonedx-python-lib) flagged by\npip-audit with CVE-2026-41066. The fix version is 6.1.0. Ran\n`uv lock --upgrade-package lxml`; no pyproject.toml change required.\n`pip-audit` now reports \"No known vulnerabilities found\".\n\nAddresses #459",
          "timestamp": "2026-04-22T12:55:02+01:00",
          "tree_id": "450856bd2a5efc2265315e00cabf60674ed5addd",
          "url": "https://github.com/endavis/pyproject-template/commit/d6fa39c22b3c0752da7c862e13896198388d5b99"
        },
        "date": 1776858925795,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8960697.176219767,
            "unit": "iter/sec",
            "range": "stddev: 1.7414690323269546e-8",
            "extra": "mean: 111.59845939820813 nsec\nrounds: 193874"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8976935.481433924,
            "unit": "iter/sec",
            "range": "stddev: 1.1675511607456616e-8",
            "extra": "mean: 111.3965898572177 nsec\nrounds: 87055"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6405683.9275640985,
            "unit": "iter/sec",
            "range": "stddev: 2.366919150600981e-8",
            "extra": "mean: 156.111355369398 nsec\nrounds: 62957"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1754607.00529653,
            "unit": "iter/sec",
            "range": "stddev: 2.514838713157857e-7",
            "extra": "mean: 569.9281930263348 nsec\nrounds: 54744"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 501200.3584156266,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013581101971931606",
            "extra": "mean: 1.9952100656135956 usec\nrounds: 45243"
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
          "id": "f4950470b2331ff771111a90b17868756490f4a8",
          "message": "fix: tolerate single-# plan headers in /implement grep (merges PR #458, addresses #457)\n\nRelax plan-comment detection in /plan-issue, /plan-both, /implement,\n/where-am-i, and the implement-worker agent to accept both\n`# Implementation Plan for ...` and `## Implementation Plan for ...`.\nFour grep patterns switch to `grep -E \"^#+ Implementation Plan for\"`;\nthe jq filter in implement-worker switches to\n`test(\"^#+ Implementation Plan for\"; \"m\")`. Planner/template files are\nunchanged — canonical emitted form remains `##`.\n\nAddresses #457",
          "timestamp": "2026-04-22T13:03:47+01:00",
          "tree_id": "15f37195a110bc33527b52ab7342259a3287f943",
          "url": "https://github.com/endavis/pyproject-template/commit/f4950470b2331ff771111a90b17868756490f4a8"
        },
        "date": 1776859450494,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8849736.707781356,
            "unit": "iter/sec",
            "range": "stddev: 2.3383636579650982e-8",
            "extra": "mean: 112.99771202466674 nsec\nrounds: 88834"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9193552.866150148,
            "unit": "iter/sec",
            "range": "stddev: 1.1811597041049277e-8",
            "extra": "mean: 108.77187683141649 nsec\nrounds: 88724"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5726886.44151537,
            "unit": "iter/sec",
            "range": "stddev: 4.098177673035811e-8",
            "extra": "mean: 174.61495180885646 nsec\nrounds: 60592"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1663213.4580226887,
            "unit": "iter/sec",
            "range": "stddev: 3.334990846495017e-7",
            "extra": "mean: 601.2457361840073 nsec\nrounds: 51128"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 478996.24043582607,
            "unit": "iter/sec",
            "range": "stddev: 6.401310747098499e-7",
            "extra": "mean: 2.087699058118131 usec\nrounds: 48521"
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
          "id": "30ae0b1a868cbd2750b48a4b0cd9d0d91814007d",
          "message": "fix: unify ADR directories under docs/decisions and add doit adr --template (merges PR #462, addresses #461)\n\n* chore: remove misplaced downstream ADR from docs/decisions/\n\nThe file docs/decisions/0001-pr-based-release-is-the-only-supported-flow.md\ndocuments a release-workflow decision made in a downstream consumer of the\ntemplate and references issues #632/#634/#637 that do not exist in this\nrepository. Its own text (\"intentional drift between this repo and the\nupstream template\") confirms it was committed back to the template by\nmistake.\n\nDeleting the file restores the design invariant asserted by\ntests/test_doit_adr.py (\"docs/decisions/ starts empty and the next number\nshould be 1\") and by docs/template/decisions/README.md. This commit is\nscoped to the deletion only; the broader directory unification lands in\na follow-up commit on the same branch.\n\nAddresses #461.\n\n* refactor: unify template ADRs into docs/decisions/\n\nCollapses docs/template/decisions/ into docs/decisions/ so all ADRs —\ntemplate-meta (9XXX) and project-level (0001+) — live in a single\ndirectory. The numeric prefix alone encodes ownership; the physical\ndirectory split added no information and produced contradictory\nguidance across the repo (issue #461).\n\nChanges:\n- git mv 9001-9015 ADR files from docs/template/decisions/ into\n  docs/decisions/.\n- Delete docs/template/decisions/ (README.md removed; directory\n  collapses with the renames).\n- Rewrite docs/decisions/README.md to describe the two-series\n  convention, update the creation instructions, and list 9001-9015 in\n  an index with a reserved section for 0001+.\n- Drop _copy_template_adrs() and the opt-in prompt from\n  tools/pyproject_template/manage.py; downstream projects now inherit\n  9XXX ADRs via the clone. Remove the now-unused prompt_confirm import\n  (the only caller in this module was the removed prompt).\n- Delete the TestCopyTemplateAdrs class and\n  test_create_with_yes_skips_adr_prompt — they exercised the removed\n  copy path.\n- Update inbound links to docs/template/decisions/ across\n  architectural-conventions.md, install-tools-framework.md,\n  tooling-roles.md, add-a-feature.md, cli.md, and mkdocs.yml so they\n  point at docs/decisions/ instead.\n- Regenerate docs/TABLE_OF_CONTENTS.md so entries reflect the new\n  paths.\n- Update the test_doit_adr.py smoke-test docstring to reflect the\n  unified layout (no assertion changes).\n\nAddresses #461.\n\n* feat(doit): add --template flag to doit adr for 9XXX series\n\nBefore this commit, doit adr could only create project-level (0XXX)\nADRs and the 9XXX template-meta ADRs had to be authored by hand. The\ncontradiction was flagged by issue #461.\n\nChanges:\n- Add TEMPLATE_SERIES_FLOOR = 9001 and refactor _get_next_adr_number()\n  to take a template bool. It scans the shared docs/decisions/\n  directory with different regexes (^0\\d{3}-.*\\.md$ for the project\n  series, ^9\\d{3}-.*\\.md$ for the template series) and returns\n  max + 1, falling back to the series floor (1 for project, 9001 for\n  template) when none exist.\n- Thread a template parameter through create_adr() and expose it as a\n  --template boolean flag on the doit adr task.\n- Update the task docstring with both project and template\n  invocations, and print the series in the status output so the user\n  can see which series a new ADR will land in.\n- Replace the integration-style _get_next_adr_number tests with\n  monkeypatched tmp_path tests that cover both series, the floor\n  behavior for the template series, series isolation within the\n  shared directory, and the ignore list (README.md,\n  adr-template.md). Keep a smoke test against the real ADR_DIR.\n- Document --template in docs/development/doit-tasks-reference.md.\n\nAddresses #461.\n\n* docs(adr): add ADR-9016 recording the unified-directory decision\n\nADR-9016 documents the decision to collapse docs/template/decisions/\ninto docs/decisions/ and drop the opt-in ADR-copy prompt from the\nproject-setup flow. It is the dogfood case for the new\ndoit adr --template flag: the ADR was created by running\n\n    doit adr --title=\"Unify ADR directories under docs/decisions\" \\\n             --template --body-file=<body>\n\nand renamed to docs/decisions/9016-unify-adr-directories.md so the\nfilename matches the planned slug.\n\nAlso updates:\n- docs/decisions/README.md — adds 9016 to the template-meta index.\n- mkdocs.yml — adds 9016 to the Decisions nav.\n- docs/TABLE_OF_CONTENTS.md — regenerated by pre-commit hook.\n\nAddresses #461.\n\n* chore: discard unused yes param in action_create_project\n\nThe refactor in commit 8f39d5e removed the opt-in ADR-copy prompt,\nwhich was the only consumer of the `yes` parameter in\naction_create_project. The parameter is retained in the signature\nbecause run_action() dispatches uniformly to every action_*\nfunction with `yes=yes`. A `del yes` discard documents the intent\nand silences the pyright \"not accessed\" hint without touching the\ndispatcher pattern.\n\nAddresses #461.",
          "timestamp": "2026-04-22T14:33:52+01:00",
          "tree_id": "517407699606fc11c645e923f7df0b4e2fbc19c4",
          "url": "https://github.com/endavis/pyproject-template/commit/30ae0b1a868cbd2750b48a4b0cd9d0d91814007d"
        },
        "date": 1776864858259,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9049281.871065225,
            "unit": "iter/sec",
            "range": "stddev: 1.1894450993153866e-8",
            "extra": "mean: 110.50600636029102 nsec\nrounds: 88363"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8895269.614670109,
            "unit": "iter/sec",
            "range": "stddev: 1.1629866767431508e-8",
            "extra": "mean: 112.41930186700543 nsec\nrounds: 86230"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6270736.262686813,
            "unit": "iter/sec",
            "range": "stddev: 1.4834368082735373e-8",
            "extra": "mean: 159.47090710071282 nsec\nrounds: 63036"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1766444.93785802,
            "unit": "iter/sec",
            "range": "stddev: 2.7037346950083607e-7",
            "extra": "mean: 566.108786392512 nsec\nrounds: 56542"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 438528.84517336515,
            "unit": "iter/sec",
            "range": "stddev: 7.832260840285224e-7",
            "extra": "mean: 2.280351705495374 usec\nrounds: 52888"
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
          "id": "74ed41ff858c0409bbdfaeba8ebb6be314bb861c",
          "message": "fix: auto-remove template management suite from spawned projects (merges PR #466, addresses #465)\n\n* feat(spawn): auto-remove template management suite from spawned projects\n\nAdd `cleanup_template_suite()` to `RepositorySetup` and wire it into\n`run()` between `setup_development_environment()` and\n`print_manual_steps()`. The method invokes\n`cleanup_template_files(CleanupMode.ALL, root=Path.cwd())`, then stages,\ncommits, and pushes the deletions so the consumer's default branch\nreflects a clean tree.\n\nThis honors the two-flow design already documented in `bootstrap.py`'s\nown module docstring: default spawn ships a clean consumer tree;\n`bootstrap.py --sync` re-installs the template management suite for\nprojects that want ongoing template sync.\n\nDefensive behavior mirrors `configure_placeholders()`:\n- `--no-verify` on the commit to bypass the no-commit-to-main pre-commit\n  hook that blocks fresh spawns whose only branch is main.\n- Exceptions are logged as warnings and swallowed so a cleanup failure\n  does not block the user from using their freshly spawned repository.\n- Early return when `cleanup_template_files` reports no deletions,\n  avoiding an empty commit if a consumer re-runs setup on a project\n  that has already been cleaned.\n\nAlso removes the now-obsolete \"Cleanup Recommendations\" manual-steps\nblock from `print_manual_steps()` and replaces it with a one-liner\npointing to `bootstrap.py --sync` for re-installation.\n\nTests cover (7 new cases in `TestCleanupTemplateSuite` and\n`TestRunOrder`):\n- `CleanupMode.ALL` is the mode passed to `cleanup_template_files`.\n- `Path.cwd()` is the root argument.\n- Successful cleanup stages (`git add -A`), commits with\n  `--no-verify` and the expected subject, and pushes.\n- Empty `CleanupResult` skips the git path entirely.\n- `OSError` from the cleanup helper is caught and surfaced as a\n  warning without re-raising.\n- `subprocess.CalledProcessError` during commit is caught the same way.\n- `run()` calls `cleanup_template_suite()` after\n  `setup_development_environment` and before `print_manual_steps`.\n\nAddresses #465\n\n* docs: describe auto-cleanup of template suite and --sync re-install path\n\nUpdate the three consumer-facing template docs to reflect the new\ndefault behavior introduced in the sibling code change:\n\n- `docs/template/new-project.md`: add step 7 (\"Removes the template\n  management suite\") to the \"What It Does\" list and a post-setup note\n  pointing to `bootstrap.py --sync` as the re-install path.\n- `docs/template/index.md`: cross-reference the new default behavior\n  from the template overview and link to the updates guide.\n- `docs/template/updates.md`: add a callout for consumers who spawned a\n  clean tree and later want the template-sync suite back, documenting\n  the `bootstrap.py --sync` command.\n\nAddresses #465",
          "timestamp": "2026-04-22T16:36:00+01:00",
          "tree_id": "ae14a2293c5d4b712a8bc52326ee26b749310eaa",
          "url": "https://github.com/endavis/pyproject-template/commit/74ed41ff858c0409bbdfaeba8ebb6be314bb861c"
        },
        "date": 1776872193546,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 11611614.126577113,
            "unit": "iter/sec",
            "range": "stddev: 8.745450339818214e-9",
            "extra": "mean: 86.12067100224775 nsec\nrounds: 114247"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 11655830.941588696,
            "unit": "iter/sec",
            "range": "stddev: 7.762083561978943e-9",
            "extra": "mean: 85.79396913110165 nsec\nrounds: 111309"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 8356228.3479883205,
            "unit": "iter/sec",
            "range": "stddev: 1.1662833503807056e-8",
            "extra": "mean: 119.67121509319932 nsec\nrounds: 82183"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 2238835.2070899555,
            "unit": "iter/sec",
            "range": "stddev: 2.3786986938911558e-7",
            "extra": "mean: 446.66083364831616 nsec\nrounds: 61032"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 655890.6823411119,
            "unit": "iter/sec",
            "range": "stddev: 3.364506870569772e-7",
            "extra": "mean: 1.524644314858441 usec\nrounds: 50078"
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
          "id": "13638e1390dfeb98e2d89441b67a50338a05ff19",
          "message": "fix: consolidate template-only tests into tests/template/ and strip them during spawn (merges PR #467, addresses #463)\n\n* refactor(tests): consolidate template-only tests into tests/template/ and use pytest pythonpath\n\nMove 16 template-infrastructure test files (9 top-level `test_doit_*.py`,\n`test_templates.py`, `test_properties.py`, plus 7 files from\n`tests/pyproject_template/`) into a single `tests/template/` directory.\n\nRetire the fragile `sys.path.insert` hack in the deleted\n`tests/pyproject_template/conftest.py` in favour of a standard\n`pythonpath = [\".\"]` entry under `[tool.pytest.ini_options]` in\n`pyproject.toml`. This makes `uv run pytest tests/template/test_doit_adr.py`\n(single-file invocation) work as well as full-suite runs, closing the\ndiscrepancy flagged in issue #463.\n\nMechanical fixups forced by the move (tests/template/ is one level deeper\nthan tests/):\n- test_doit_github.py: extra .parent on repo-labels lookup.\n- test_templates.py: extra .parent on ISSUE_TEMPLATE lookup.\n- test_properties.py: drop the now-redundant sys.path.insert block.\n\nAddresses #463\n\n* fix(spawn): remove tests/template/ during configure_placeholders\n\nReroute the template-only tests removal in the spawn flow to point at the\nconsolidated `tests/template/` directory introduced by the preceding\nrefactor commit. Both spawn entry points (`setup_repo.py` and\n`configure.py`) are updated so fresh consumer projects ship without the\ntemplate-infrastructure tests and pass `doit check` cleanly.\n\nAlso rename the existing configure-side regression test to reflect the\nnew path and add two new unit tests for\n`RepositorySetup.configure_placeholders()`: one asserting\n`tests/template/` is removed when present, and one asserting the call\nis a no-op (does not raise) when the directory is absent.\n\nAddresses #463\n\n* docs: fix stale test path in hypothesis debugging example\n\ntests/test_properties.py moved to tests/template/test_properties.py in\ncommit 69e32a2 as part of the template-only tests consolidation. The\nHypothesis seed-reproduction example in ci-cd-testing.md still referenced\nthe old path; update it.\n\nAddresses #463",
          "timestamp": "2026-04-22T17:18:56+01:00",
          "tree_id": "517c2146f373653bd7a6619ec866f1f56e26c5e1",
          "url": "https://github.com/endavis/pyproject-template/commit/13638e1390dfeb98e2d89441b67a50338a05ff19"
        },
        "date": 1776874771249,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8980827.061538553,
            "unit": "iter/sec",
            "range": "stddev: 1.0317562198754444e-8",
            "extra": "mean: 111.34831938615291 nsec\nrounds: 90580"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8766724.418394744,
            "unit": "iter/sec",
            "range": "stddev: 2.3229298468925885e-8",
            "extra": "mean: 114.06768962666992 nsec\nrounds: 89518"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5126349.083268572,
            "unit": "iter/sec",
            "range": "stddev: 5.657507948649673e-8",
            "extra": "mean: 195.07060166148457 nsec\nrounds: 198847"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1586705.6735814747,
            "unit": "iter/sec",
            "range": "stddev: 3.1810483468009735e-7",
            "extra": "mean: 630.236606983842 nsec\nrounds: 59770"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 449855.51309833024,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011576275812803848",
            "extra": "mean: 2.222935966956613 usec\nrounds: 56424"
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
          "id": "0cdab3e349b2bfd8007acb713b136b134bf0700e",
          "message": "fix: scope placeholder replacement with marker tokens and word-boundary regex (merges PR #468, addresses #464)\n\n* refactor(spawn): teach update_file three replacement modes\n\nAddresses #464.\n\nPreviously ``update_file()`` applied a blind ``str.replace`` for every\n``(old, new)`` pair with a single regex guard for ``package_name``. This\nleft identifier substrings (``validate_package_name``) vulnerable and\nmade prose files with the word ``username`` or ``package_name`` prone to\naccidental rewrites.\n\nThe function now distinguishes three modes per pair:\n\n1. Marker tokens (``__FOO__``): blind replace. Collision-proof by\n   construction.\n2. Identifier-like literals in ``.py`` files: word-boundary regex,\n   plus the existing ``(?!\\s*=)`` guard on ``package_name`` to preserve\n   kwargs / TOML-keys.\n3. Everything else: blind replace (current default).\n\nThe replacements dicts in both ``setup_repo.py`` and ``configure.py``\ngain the new ``__FOO__`` marker entries alongside the existing literal\nentries. Markers are the canonical form for new prose files; literals\nremain to support runtime-critical files (pyproject.toml, workflows,\nLICENSE, etc.) and downstream consumer projects that have not yet\nmigrated.\n\nThe existing ``test_package_name_preserves_toml_keys`` fixture is\nupdated to use a ``.py`` file, reflecting that the ``(?!\\s*=)`` guard\nnow scopes to Python source. Commit 3 adds a full ``TestUpdateFileModes``\nclass covering the three modes.\n\nCo-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* refactor(template): switch prose files to marker tokens\n\nConverts literal placeholder tokens to __FOO__ markers in 25 prose\nfiles so substring collisions (e.g. validate_package_name being\ncorrupted to validate_<user_pkg>) are structurally impossible when\nupdate_file() processes them. The three-mode update_file() added in\ncommit 5a25c18 already handles the new markers via the blind-replace\npath; this commit is the mechanical corpus migration.\n\nMarker token map:\n  package_name           -> __PACKAGE_NAME__\n  package-name           -> __PYPI_NAME__\n  Package Name           -> __PROJECT_NAME__\n  username               -> __GH_OWNER__\n  Your Name              -> __AUTHOR_NAME__\n  your.email@example.com -> __AUTHOR_EMAIL__\n  A short description... -> __DESCRIPTION__\n  https://github.com/username/package_name -> __REPO_URL__\n\nFiles converted: README, CHANGELOG, .github/CONTRIBUTING.md,\n.github/SECURITY.md, .claude/CLAUDE.md, .claude/lsp-setup.md, and\ndocs/** except runtime-critical files. Runtime-critical files\n(pyproject.toml, mkdocs.yml, dodo.py, workflows, LICENSE, .envrc,\n.pre-commit-config.yaml) and Python source/tests keep literal\nplaceholders per the hybrid plan decided in the #464 plan.\n\nAdds a \"Placeholder Markers\" note to docs/template/tools-reference.md\nexplaining the convention.\n\nA handful of template-internal docs (docs/template/tools-reference.md,\nnew-project.md, migration.md) had spots where the script corrupted\ndocumentation referring to the template's own `src/package_name/`\ndirectory as a literal path, or to prompt-label prose like \"GitHub\nusername\". Those were manually reverted to literals.\n\nAddresses #464\n\n* test(spawn): cover update_file's three replacement modes\n\nAdds TestUpdateFileModes class to tests/template/test_utils.py with\n6 tests exercising the three-mode update_file() logic introduced in\ncommit 5a25c18:\n\n1. test_marker_replacement_is_blind — __PACKAGE_NAME__ replaces\n   anywhere in a file regardless of surrounding chars.\n2. test_literal_in_python_code_protects_identifiers —\n   validate_package_name survives when the literal 'package_name' is\n   replaced in a .py file (the core #464 bug).\n3. test_literal_username_in_python_code_protects_identifiers —\n   my_username survives; bare username is replaced.\n4. test_literal_in_non_python_file_is_blind — documents that prose\n   files still get blind replace for literal tokens (rationale for\n   the marker migration in commit 96f86cc).\n5. test_python_identifier_hyphen_case — verifies that \\\\b boundaries\n   work around hyphens in package-name.\n6. test_marker_does_not_interfere_with_literal — marker and literal\n   replacements for the same concept coexist cleanly when both are\n   present in the replacements dict.\n\nAddresses #464\n\n* fix(docs): revert marker usage in mkdocs-evaluated links and mkdocstrings directives\n\ndocs_build failed on HEAD because three classes of marker leaked into\nelements mkdocs evaluates at template-build time:\n\n1. docs/reference/api.md uses mkdocstrings directives\n   (``::: package_name``) that actually import the module at build\n   time. __PACKAGE_NAME__ is not an importable module on the template\n   repo, so the build aborted with ModuleNotFoundError. Reverted every\n   occurrence in api.md back to the literal package_name (the\n   template's own package directory). Word-boundary regex in\n   update_file() substitutes correctly at spawn time.\n\n2. docs/development/install-tools-framework.md and docs/usage/basics.md\n   had __REPO_URL__ in markdown link targets. mkdocs resolves those as\n   relative paths, so the build warned/failed. Reverted to the literal\n   https://github.com/username/package_name URL which the existing\n   URL-pattern entry in the replacements dict handles at spawn time.\n\n3. README.md, CHANGELOG.md, .github/SECURITY.md, .github/CONTRIBUTING.md,\n   docs/getting-started/installation.md, and .claude/lsp-setup.md also\n   had __REPO_URL__ references. These aren't in the mkdocs nav so\n   they didn't fail the docs_build, but they render as broken links on\n   GitHub in the pre-spawn template view. Reverted for consistency.\n\nClassification: these specific URL/module tokens never needed markers.\nMarkers are for identifier-like literals (package_name, username,\npackage-name) that can collide with longer identifiers. Full URLs and\nimportable module names are specific enough to be safely handled by\nblind replace (URLs) or word-boundary regex (identifiers in .py).\n\nAddresses #464\n\n---------\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-22T20:09:59+01:00",
          "tree_id": "bcf9620c1aee953da3738e14737af47c153c8790",
          "url": "https://github.com/endavis/pyproject-template/commit/0cdab3e349b2bfd8007acb713b136b134bf0700e"
        },
        "date": 1776885031706,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8877922.587879457,
            "unit": "iter/sec",
            "range": "stddev: 2.8519633673246574e-8",
            "extra": "mean: 112.63896368788407 nsec\nrounds: 85756"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8879160.103689007,
            "unit": "iter/sec",
            "range": "stddev: 1.1875583458985043e-8",
            "extra": "mean: 112.62326484962601 nsec\nrounds: 88488"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5310524.945585784,
            "unit": "iter/sec",
            "range": "stddev: 1.641281141395488e-8",
            "extra": "mean: 188.30530131135535 nsec\nrounds: 53234"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1652465.3594450813,
            "unit": "iter/sec",
            "range": "stddev: 2.949118948737411e-7",
            "extra": "mean: 605.1564072337424 nsec\nrounds: 52261"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 487497.8165359499,
            "unit": "iter/sec",
            "range": "stddev: 6.074488466884264e-7",
            "extra": "mean: 2.0512912388116433 usec\nrounds: 47037"
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
          "id": "c8d1bf4ab2f779b6196f65a87d00f4eb2981169d",
          "message": "fix: scrub bootstrap.py refs and template docs during spawn cleanup (merges PR #471, addresses #469)\n\nSpawn cleanup deletes bootstrap.py and the template management suite,\nbut several doit task commands hardcoded bootstrap.py and three\nuser-visible files still referenced template-only machinery, causing\n`doit check` to fail in spawned repos.\n\nAdd `optional_root_files()` in tools/doit/base.py and route the six\naffected task actions (lint/format/format_check/type_check, security,\nspell_check) through it so bootstrap.py is included only when present.\nBroaden cleanup: add `scrub_template_references()` that rewrites\npyproject.toml (mypy override), README.md (template-setup sections),\nand docs/development/doit-tasks-reference.md (template_clean section\n+ TOC row) under CleanupMode.ALL, and add tools/doit/template_clean.py\nto ALL_TEMPLATE_FILES. Finally, wire a post-cleanup `doit check` into\nRepositorySetup.run() via verify_post_cleanup() so future regressions\nsurface inside the wizard with a lenient diagnostic (no sys.exit).\n\nSame family as #463, #464, #465.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T12:35:53+01:00",
          "tree_id": "8277ce4e1ac0cdd252df4bb0c4752a7a0c3b1056",
          "url": "https://github.com/endavis/pyproject-template/commit/c8d1bf4ab2f779b6196f65a87d00f4eb2981169d"
        },
        "date": 1776944189082,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 11672291.813334087,
            "unit": "iter/sec",
            "range": "stddev: 9.754810105636952e-9",
            "extra": "mean: 85.67297802284459 nsec\nrounds: 111161"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 11940274.664109135,
            "unit": "iter/sec",
            "range": "stddev: 1.0615268209779845e-8",
            "extra": "mean: 83.75016723910598 nsec\nrounds: 108886"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 8129015.333066312,
            "unit": "iter/sec",
            "range": "stddev: 1.7406369943650563e-8",
            "extra": "mean: 123.01612914079645 nsec\nrounds: 77280"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 2291450.6334428703,
            "unit": "iter/sec",
            "range": "stddev: 1.7313407104438007e-7",
            "extra": "mean: 436.4047758242624 nsec\nrounds: 68344"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 655706.0437388292,
            "unit": "iter/sec",
            "range": "stddev: 3.552133963445774e-7",
            "extra": "mean: 1.5250736355852543 usec\nrounds: 59971"
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
          "id": "b99d5115f10369365570f72cfbaba2af180a82d9",
          "message": "fix: fall back to --global in get_git_config when CWD has no repo (merges PR #472, addresses #470)\n\nThe unscoped `git config <key>` lookup exits non-zero when the CWD is\nnot inside a git repository, even for keys set in ~/.gitconfig. That\nbroke bootstrap.py's required-field loop on piped stdin when run from\noutside a repo. Retry with `git config --global <key>` on failure so\nuser.name / user.email resolve from global identity regardless of CWD.\nBoth calls remain inside the existing exception guard; signature and\nthe three existing callers are unchanged.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T12:58:50+01:00",
          "tree_id": "8dec5ff80a205eb9133108e50d7cda544e8c5b35",
          "url": "https://github.com/endavis/pyproject-template/commit/b99d5115f10369365570f72cfbaba2af180a82d9"
        },
        "date": 1776945554185,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8937302.074787853,
            "unit": "iter/sec",
            "range": "stddev: 1.1856976164573614e-8",
            "extra": "mean: 111.89058975873738 nsec\nrounds: 86866"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9025474.881040048,
            "unit": "iter/sec",
            "range": "stddev: 1.1673123890627577e-8",
            "extra": "mean: 110.7974941131037 nsec\nrounds: 88332"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5248667.756204017,
            "unit": "iter/sec",
            "range": "stddev: 2.88418121617978e-8",
            "extra": "mean: 190.52453812074168 nsec\nrounds: 198020"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1583223.0180179977,
            "unit": "iter/sec",
            "range": "stddev: 3.2618808119713507e-7",
            "extra": "mean: 631.6229543276082 nsec\nrounds: 55667"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 486495.0511236196,
            "unit": "iter/sec",
            "range": "stddev: 4.967043724375519e-7",
            "extra": "mean: 2.055519367957347 usec\nrounds: 51451"
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
          "id": "4e405b0143c1afeecf3596fe16b207b2dc0afe89",
          "message": "fix: scrub remaining pyproject/README template refs in spawn cleanup (#469 follow-up) (merges PR #473, addresses #469)\n\nfix: scrub remaining pyproject.toml/README template refs in spawn cleanup (#469 follow-up)\n\nThe first pass of scrub_template_references missed several stale\ntools/pyproject_template/ references that the spawn wizard leaves\nbehind after CleanupMode.ALL. Root cause has two parts:\n\n1. `doit fmt_pyproject` runs before cleanup in setup_repo.run() and\n   rewrites `[[tool.mypy.overrides]]` stanzas into an inline-array\n   `overrides = [...]` list. The original regex only matched stanza\n   form, so the tools.pyproject_template.* override survived.\n2. The original regex scope didn't cover three additional pyproject\n   fragments (ruff per-file-ignores block, mypy exclude entry + its\n   explanatory comment) and the two README subsections under\n   `## Versioning & Releases` (`### Migrating an Existing Project`,\n   `### Keeping Up to Date`).\n\nAdd four new patterns (post-fmt inline override, ruff per-file block,\nmypy exclude comment, mypy exclude entry) plus one more README pattern\nfor the subsections. Keep the existing stanza-form pattern as a\nharmless fallback for downstream users who invoke the scrubber before\nfmt_pyproject normalizes the file. Refactor scrub_template_references\nto apply every pattern for a given file unconditionally (re.sub is a\nno-op on no match) and detect change via content comparison — simpler\nthan per-pattern search/sub.\n\nNew tests in TestScrubTemplateReferences cover each new pattern plus a\nrealistic post-fmt_pyproject fixture that exercises every pattern in\none file. Idempotency test now exercises all patterns end-to-end.\n\nAll doit check gates green (39 cleanup tests pass).\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T17:44:15+01:00",
          "tree_id": "c00beab7bdd8b6067194f6f8fb21c18f0e1e1719",
          "url": "https://github.com/endavis/pyproject-template/commit/4e405b0143c1afeecf3596fe16b207b2dc0afe89"
        },
        "date": 1776962687223,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8869422.947702967,
            "unit": "iter/sec",
            "range": "stddev: 8.728884181040633e-9",
            "extra": "mean: 112.74690652326863 nsec\nrounds: 88803"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8988686.169354666,
            "unit": "iter/sec",
            "range": "stddev: 9.415759554307616e-9",
            "extra": "mean: 111.25096384044679 nsec\nrounds: 87805"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5539846.717842222,
            "unit": "iter/sec",
            "range": "stddev: 1.1519115869193284e-8",
            "extra": "mean: 180.51040957131417 nsec\nrounds: 54789"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1626868.600568541,
            "unit": "iter/sec",
            "range": "stddev: 1.6719311478905764e-7",
            "extra": "mean: 614.6777924477309 nsec\nrounds: 34065"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 528750.848346915,
            "unit": "iter/sec",
            "range": "stddev: 2.813859263293326e-7",
            "extra": "mean: 1.8912499206883489 usec\nrounds: 31518"
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
          "id": "a734f58c5f52a52d2a78b1b50be5229f697f7bf9",
          "message": "fix: allow --prerelease + --increment on doit release (merges PR #476, addresses #475)\n\nThe task rejected --prerelease combined with --increment with a custom\nerror, but cz bump accepts both (and recommends --increment when\nconventional-commit hints are thin). That false-mutex blocked the\nfirst-pre-release-on-a-fresh-repo path that PR #436 was built for.\n\nDrop the 7-line mutex block; cz handles flag precedence. Update the\ntask docstring and every doc that claimed the flags were mutually\nexclusive. New TestCreateReleasePrValidation tests cover the accepted\ncombination and guard the still-enforced allowed-values check.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T18:46:41+01:00",
          "tree_id": "38e612fa8a1ad7a89800935d0c2f638c88efe6a7",
          "url": "https://github.com/endavis/pyproject-template/commit/a734f58c5f52a52d2a78b1b50be5229f697f7bf9"
        },
        "date": 1776966435403,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9017038.38874197,
            "unit": "iter/sec",
            "range": "stddev: 1.0876187217580132e-8",
            "extra": "mean: 110.90115810625012 nsec\nrounds: 88567"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9049660.043027055,
            "unit": "iter/sec",
            "range": "stddev: 1.0697158599280921e-8",
            "extra": "mean: 110.50138847707545 nsec\nrounds: 89040"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5620800.248968445,
            "unit": "iter/sec",
            "range": "stddev: 1.3752794467829103e-8",
            "extra": "mean: 177.91060982526903 nsec\nrounds: 56262"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1678403.8323711548,
            "unit": "iter/sec",
            "range": "stddev: 2.1402248254637435e-7",
            "extra": "mean: 595.8041686470985 nsec\nrounds: 39437"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 491292.6591862352,
            "unit": "iter/sec",
            "range": "stddev: 4.989511690659913e-7",
            "extra": "mean: 2.035446655474915 usec\nrounds: 61159"
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
          "id": "7a13c9384b1b94446836eabaa20ca0800d185369",
          "message": "fix: document three trusted-publisher registrations in publish_setup (merges PR #480, addresses #479)\n\nPyPI scopes trusted publishers per (owner, repo, workflow, env), so the\ntemplate needs three registrations, not two: testpypi.yml x testpypi,\nrelease.yml x testpypi (the canary), and release.yml x pypi. Missing\nthe second caused first-production-release 403s at the TestPyPI canary\nstep. Update the publish_setup panel and the four docs pages that\ndescribe setup, and pin the output shape with a new test.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T19:56:08+01:00",
          "tree_id": "374a34f37a15383bdc71f17e1ae1877182579579",
          "url": "https://github.com/endavis/pyproject-template/commit/7a13c9384b1b94446836eabaa20ca0800d185369"
        },
        "date": 1776970595741,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8764250.530948225,
            "unit": "iter/sec",
            "range": "stddev: 9.24205047995221e-9",
            "extra": "mean: 114.09988754529677 nsec\nrounds: 87413"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8851821.77995255,
            "unit": "iter/sec",
            "range": "stddev: 1.7998920395871584e-8",
            "extra": "mean: 112.9710950874296 nsec\nrounds: 86678"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5795506.938434137,
            "unit": "iter/sec",
            "range": "stddev: 2.5157274183822355e-8",
            "extra": "mean: 172.54745971716247 nsec\nrounds: 56848"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1599449.363347038,
            "unit": "iter/sec",
            "range": "stddev: 2.2465467665726227e-7",
            "extra": "mean: 625.2151664916613 nsec\nrounds: 61148"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 519624.0417755779,
            "unit": "iter/sec",
            "range": "stddev: 3.0280351130778707e-7",
            "extra": "mean: 1.9244683070917132 usec\nrounds: 50516"
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
          "id": "a06ef07e80b7bd534e3c2666bf9ceffe12267382",
          "message": "chore: bump pip 26.0.1 -> 26.1 in uv.lock (merges PR #484, addresses #483)\n\nchore: bump pip 26.0.1 -> 26.1 in uv.lock to clear CVE-2026-3219\n\nAddresses #483",
          "timestamp": "2026-04-27T10:57:10+01:00",
          "tree_id": "0a015647dfe8e0fac864764a859efe2a0244064b",
          "url": "https://github.com/endavis/pyproject-template/commit/a06ef07e80b7bd534e3c2666bf9ceffe12267382"
        },
        "date": 1777283859257,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8836766.50279608,
            "unit": "iter/sec",
            "range": "stddev: 2.0117201763812786e-8",
            "extra": "mean: 113.16356494013796 nsec\nrounds: 88669"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8920001.66542869,
            "unit": "iter/sec",
            "range": "stddev: 7.712802404543577e-9",
            "extra": "mean: 112.10760238708325 nsec\nrounds: 87291"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5683477.984933384,
            "unit": "iter/sec",
            "range": "stddev: 9.912480212800202e-9",
            "extra": "mean: 175.9486009536678 nsec\nrounds: 55009"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1603189.988384386,
            "unit": "iter/sec",
            "range": "stddev: 1.742529696531784e-7",
            "extra": "mean: 623.7563902253092 nsec\nrounds: 65215"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 525276.7438034714,
            "unit": "iter/sec",
            "range": "stddev: 2.9440843945797626e-7",
            "extra": "mean: 1.9037583746028988 usec\nrounds: 45227"
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
          "id": "9161946d74b7b0f06da1007268169301a354d6b7",
          "message": "feat: add Codex workflow skills (merges PR #482, addresses #399)",
          "timestamp": "2026-04-27T11:00:26+01:00",
          "tree_id": "949fda09c46856ea311567d1f48493f5874c25eb",
          "url": "https://github.com/endavis/pyproject-template/commit/9161946d74b7b0f06da1007268169301a354d6b7"
        },
        "date": 1777284049831,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8783285.978339607,
            "unit": "iter/sec",
            "range": "stddev: 1.0588204896125447e-8",
            "extra": "mean: 113.8526062416836 nsec\nrounds: 87559"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8990423.898717098,
            "unit": "iter/sec",
            "range": "stddev: 1.1468747902931539e-8",
            "extra": "mean: 111.22946050883056 nsec\nrounds: 86044"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5375291.647863249,
            "unit": "iter/sec",
            "range": "stddev: 1.4784119564680035e-8",
            "extra": "mean: 186.03641727933285 nsec\nrounds: 56552"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1681195.251831104,
            "unit": "iter/sec",
            "range": "stddev: 2.8764071874107046e-7",
            "extra": "mean: 594.8149085662907 nsec\nrounds: 63212"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 488652.70168619335,
            "unit": "iter/sec",
            "range": "stddev: 5.062361282959507e-7",
            "extra": "mean: 2.046443203013717 usec\nrounds: 50927"
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
          "id": "060bba8fd1457928f80f3f24d766751ecb2d2c89",
          "message": "feat: add Gemini-native /implement and /finalize plus split planner (merges PR #491, addresses #398)\n\nAdds standalone Gemini-native implementations of /implement and\n/finalize under .gemini/commands/, completing the Gemini-first\nissue-to-PR workflow. The new commands share the GitHub-artifact\ncontract (plan comment header, branch naming, PR body) with the\nClaude versions, so users can switch agents mid-workflow.\n\nSplits the existing Gemini /plan-issue into two commands so that\nstandalone use posts plans directly to GitHub (matching Claude's\n/plan-issue) without producing duplicate comments under dual-agent\norchestration:\n  - /plan-issue: interactive, posts on user approval (standalone)\n  - /plan-issue-stdout: output-only (used by Claude's /plan-both)\n\nUpdates Claude's /plan-both to invoke the stdout-only variant.\n\nAlso enables auto-approval in .gemini/settings.json so /implement\ncan run end-to-end without per-tool prompts, refreshes the AI\nConfig Directories table in AGENTS.md, and updates the slash-\ncommands and AI_SETUP docs.\n\nAddresses #398",
          "timestamp": "2026-04-27T12:38:36+01:00",
          "tree_id": "8589fd2e451828a82f2dad7c426f41bf187be0c1",
          "url": "https://github.com/endavis/pyproject-template/commit/060bba8fd1457928f80f3f24d766751ecb2d2c89"
        },
        "date": 1777289941210,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 9042031.733264184,
            "unit": "iter/sec",
            "range": "stddev: 1.2460525145695686e-8",
            "extra": "mean: 110.59461296968915 nsec\nrounds: 88598"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8922371.825736232,
            "unit": "iter/sec",
            "range": "stddev: 1.3756966446605379e-8",
            "extra": "mean: 112.07782185399842 nsec\nrounds: 88130"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 6257958.318520836,
            "unit": "iter/sec",
            "range": "stddev: 1.7560482095103153e-8",
            "extra": "mean: 159.7965261354386 nsec\nrounds: 64375"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1739220.0878585025,
            "unit": "iter/sec",
            "range": "stddev: 3.4160216463231476e-7",
            "extra": "mean: 574.970359979741 nsec\nrounds: 55938"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 508878.4719374236,
            "unit": "iter/sec",
            "range": "stddev: 4.895098797260434e-7",
            "extra": "mean: 1.9651057278818609 usec\nrounds: 49826"
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
          "id": "5c892fe705ec2a6989d8cbca734eb79d9dfcf69a",
          "message": "fix: use App token in request-rebase job for dependabot push-access check (merges PR #493, addresses #492)\n\nThe request-rebase job in dependabot-automerge.yml posted @dependabot\nrebase comments using GITHUB_TOKEN, which authenticates as\ngithub-actions[bot]. Dependabot's command parser rejects comments from\nthat actor with \"Sorry, only users with push access can use that\ncommand\", so stale dependabot PRs never actually got rebased.\n\nMirror the App-token / GITHUB_TOKEN fallback pattern that the\nenable-automerge job already uses: mint an App installation token when\nvars.RELEASE_APP_ID is set and pass it to actions/github-script@v9 via\nits github-token input. The App's installation token grants Contents:\nwrite, which dependabot accepts as push access.\n\nThe job-level env: GH_TOKEN was unused (the script uses the GitHub API\nclient from actions/github-script, not the gh CLI) and is removed.\n\nAddresses #492",
          "timestamp": "2026-04-27T13:15:26+01:00",
          "tree_id": "9e377133b9bbacb99f0e96343ad19b523ca8b861",
          "url": "https://github.com/endavis/pyproject-template/commit/5c892fe705ec2a6989d8cbca734eb79d9dfcf69a"
        },
        "date": 1777292156752,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8662570.774516026,
            "unit": "iter/sec",
            "range": "stddev: 2.386120875338903e-8",
            "extra": "mean: 115.43917227687754 nsec\nrounds: 88387"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9001398.419317756,
            "unit": "iter/sec",
            "range": "stddev: 7.965962696487028e-9",
            "extra": "mean: 111.09384935721945 nsec\nrounds: 87651"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5600873.381871828,
            "unit": "iter/sec",
            "range": "stddev: 1.0557638190110912e-8",
            "extra": "mean: 178.54358272705622 nsec\nrounds: 54813"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1595950.8806432656,
            "unit": "iter/sec",
            "range": "stddev: 2.07498121871943e-7",
            "extra": "mean: 626.5857001795313 nsec\nrounds: 59609"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 494459.1803624401,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016814543749134194",
            "extra": "mean: 2.0224116362183766 usec\nrounds: 49449"
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
          "id": "621fce1484e480f413f7ba772d413290c7da096b",
          "message": "chore: add 7-day cooldown to dependabot uv updates for supply-chain hardening (merges PR #495, addresses #494)\n\nchore: add 7-day cooldown to dependabot uv updates\n\nDefends the auto-merge path against supply-chain attacks where a\ncompromised maintainer publishes a malicious patch or minor that gets\ndetected and yanked within hours to days. Dependabot's native cooldown\ndelays version-update PRs until the new version has aged for\ndefault-days: 7, so a malicious release pulled within the window never\nproduces a PR for auto-merge to act on.\n\nSecurity-update PRs (advisory-driven) bypass cooldown, per the\ndependabot documentation, so CVE patching latency is unchanged.\n\nThe github-actions ecosystem is not covered — dependabot's cooldown\nonly supports SemVer ecosystems and explicitly excludes github-actions.\nHardening action bumps is tracked separately.\n\nDocumentation in docs/development/dependabot-automerge.md gains a\nVersion-update cooldown section covering the configuration, the\nsecurity-update bypass, and the github-actions non-coverage.\n\nAddresses #494",
          "timestamp": "2026-04-27T13:51:02+01:00",
          "tree_id": "7b4312319b53f13ca79935399791302b12010965",
          "url": "https://github.com/endavis/pyproject-template/commit/621fce1484e480f413f7ba772d413290c7da096b"
        },
        "date": 1777294293056,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8835419.978303624,
            "unit": "iter/sec",
            "range": "stddev: 1.073804784036492e-8",
            "extra": "mean: 113.1808111505297 nsec\nrounds: 84374"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8894103.352727389,
            "unit": "iter/sec",
            "range": "stddev: 1.0604410697044906e-8",
            "extra": "mean: 112.43404313413433 nsec\nrounds: 86799"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5375805.984308913,
            "unit": "iter/sec",
            "range": "stddev: 1.864057645403138e-8",
            "extra": "mean: 186.01861803027015 nsec\nrounds: 55609"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1659571.789762989,
            "unit": "iter/sec",
            "range": "stddev: 3.291765335125501e-7",
            "extra": "mean: 602.5650750202343 nsec\nrounds: 44902"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 498105.45989886235,
            "unit": "iter/sec",
            "range": "stddev: 5.629510235470835e-7",
            "extra": "mean: 2.0076069838765562 usec\nrounds: 56616"
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
          "id": "23b85bfe3c2233b7aca180ed3ab7d7498ce63b99",
          "message": "chore: remove broken request-rebase job from dependabot-automerge workflow (merges PR #497, addresses #496)\n\nchore: remove broken request-rebase job from dependabot-automerge\n\nThe request-rebase job posted @dependabot rebase on stale PRs, but\ndependabot's command parser rejects all GitHub App actors regardless\nof permissions (upstream issue dependabot/dependabot-core#9147). PR\n#493's App-token wiring made the comment author correct but could not\naddress the underlying authz check; end-to-end validation confirmed\nthe comment is still rejected with \"Sorry, only users with push access\ncan use that command.\"\n\nSince no path forward avoids either re-introducing a PAT (reversing\nthe project's App-only stance) or stripping dependabot's verified\ncommit signatures (forbidden by AGENTS.md), the job is removed.\nMaintainers post @dependabot rebase manually as themselves to unstick\nstale PRs.\n\nRemoved:\n- request-rebase job (Generate App token step + the github-script\n  rebase loop) from .github/workflows/dependabot-automerge.yml\n- schedule: cron and workflow_dispatch: triggers from the workflow's\n  on: block, since they only existed to fire that job (the surviving\n  jobs gate on pull_request_target events)\n\nUpdated:\n- docs/development/dependabot-automerge.md: replaced \"Rebase handling\n  for stale PRs\" with \"Stale PRs\", documenting the manual unstick path\n  and an IMPORTANT callout linking to dependabot/dependabot-core#9147\n- tests/test_dependabot_automerge_workflow.py: inverted the trigger\n  test (renamed to test_schedule_and_workflow_dispatch_absent) so it\n  pins the intentional removal; updated stale docstring in\n  test_concurrency_group_keyed_on_pr_number_or_ref\n\nThe enable-automerge job's App-token usage from #493 is unaffected.\nThat fix correctly addressed the original bug — GitHub Apps can author\nlabeled events that trigger downstream workflows, so the require-label\nMerge Gate flip works as intended. Only the @dependabot rebase comment\npath was blocked.\n\nAddresses #496",
          "timestamp": "2026-04-27T15:27:34+01:00",
          "tree_id": "64804674fdcc87968008686969c01cf6e828a237",
          "url": "https://github.com/endavis/pyproject-template/commit/23b85bfe3c2233b7aca180ed3ab7d7498ce63b99"
        },
        "date": 1777300087520,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8871656.400672192,
            "unit": "iter/sec",
            "range": "stddev: 1.0963982283286618e-8",
            "extra": "mean: 112.71852231836115 nsec\nrounds: 88402"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8815423.604027212,
            "unit": "iter/sec",
            "range": "stddev: 1.1811419228295288e-8",
            "extra": "mean: 113.43754366417093 nsec\nrounds: 87944"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5133930.035578468,
            "unit": "iter/sec",
            "range": "stddev: 2.8839001503834326e-8",
            "extra": "mean: 194.7825531454335 nsec\nrounds: 197239"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1610744.1791078888,
            "unit": "iter/sec",
            "range": "stddev: 2.9835433480807633e-7",
            "extra": "mean: 620.8310500019005 nsec\nrounds: 62190"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 488539.30932370515,
            "unit": "iter/sec",
            "range": "stddev: 5.536331109355924e-7",
            "extra": "mean: 2.0469181924875612 usec\nrounds: 50081"
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
          "id": "225184c05d1fef8d0627830a3f61e5bd7964086f",
          "message": "docs: clarify GitHub App vs PAT setup and credential scope in CONTRIBUTING.md (merges PR #499, addresses #498)\n\ndocs: clarify GitHub App vs PAT setup and credential scope\n\nRestructure the \"Setting Up Release Permissions\" section of\n.github/CONTRIBUTING.md to fix three confusions in the existing copy:\n\n1. The \"personal vs organization\" framing is misleading — a GitHub\n   App works just as well on a personal account. The real decision\n   axis is CI-driven vs local-only releases and whether you want\n   full dependabot auto-merge automation.\n\n2. The previous \"Store Secrets\" step did not specify repository\n   scope vs environment scope. Storing the App credentials in an\n   environment makes vars.RELEASE_APP_ID and the private-key secret\n   silently resolve to empty strings, because the enable-automerge\n   job in dependabot-automerge.yml does not declare an environment.\n   This is the failure mode this session debugged for #492 / #493.\n\n3. Step 5 was titled \"Update Workflows (if using CI-based releases)\",\n   which implied the App credentials are required for release.yml.\n   They are not — release.yml uses PyPI trusted publishing (OIDC)\n   and GITHUB_TOKEN. The snippet documents an optional CI-driven\n   tag-push extension not currently used by this template.\n\nAlso tightens the PAT path to its actual remaining use case\n(local-only releases from a maintainer's laptop) by dropping the\nobsolete CI-as-PAT subsections.\n\nChanges:\n- Add \"Which path should I use?\" decision callout with a small table.\n- Rename \"Organization Repositories: GitHub App (Recommended)\" to\n  \"Recommended: GitHub App\". Add a NOTE callout clarifying release.yml\n  uses OIDC + GITHUB_TOKEN.\n- Rename step 4 to \"Store Credentials at the Repository Scope\" with a\n  WARNING callout describing the environment-scope failure chain.\n- Rename step 5 to \"Optional: CI-Driven Tag-Push Flow (not used by\n  this template's release.yml)\" with explanatory context.\n- Rename \"Personal Repositories: PAT\" to \"Alternative: Fine-Grained\n  PAT (local-only releases)\" with an explicit usage guard. Drop the\n  obsolete \"Store as Secret (for CI-based releases)\" and \"Update\n  Workflows\" subsections.\n- Update the cross-link anchor in dependabot-automerge.md:118 to\n  match the renamed heading.\n\nAddresses #498",
          "timestamp": "2026-04-27T15:36:34+01:00",
          "tree_id": "278245df9b526f56354c4500e607a7594442446f",
          "url": "https://github.com/endavis/pyproject-template/commit/225184c05d1fef8d0627830a3f61e5bd7964086f"
        },
        "date": 1777300627103,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8721936.269372016,
            "unit": "iter/sec",
            "range": "stddev: 1.2671949075403445e-8",
            "extra": "mean: 114.65344037328084 nsec\nrounds: 88098"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 7939438.766132711,
            "unit": "iter/sec",
            "range": "stddev: 4.278691802458254e-8",
            "extra": "mean: 125.9534873252884 nsec\nrounds: 90654"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5211831.863395402,
            "unit": "iter/sec",
            "range": "stddev: 2.593757497414789e-8",
            "extra": "mean: 191.87111676095407 nsec\nrounds: 54873"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1646022.1569498873,
            "unit": "iter/sec",
            "range": "stddev: 5.190232500833297e-7",
            "extra": "mean: 607.525236387474 nsec\nrounds: 55733"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 490022.9732917638,
            "unit": "iter/sec",
            "range": "stddev: 0.000001953490893777944",
            "extra": "mean: 2.0407206488349505 usec\nrounds: 54870"
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
          "id": "dbcf586562fbb4ce8d8de10db4505c600943b2f1",
          "message": "chore: upgrade github/codeql-action from v3 to v4 (supersedes #485) (merges PR #501, addresses #500)\n\nchore: upgrade github/codeql-action from v3 to v4\n\nBumps github/codeql-action from @v3 to @v4 in\n.github/workflows/codeql.yml and updates the corresponding pinned-\nversion assertions in tests/test_codeql_workflow.py.\n\nThe v3 -> v4 upgrade is a pure Node runtime bump (init/action.yml\nusing: node20 -> node24). v3.x.y and v4.x.y minor releases ship in\nlockstep with identical inputs and behaviors. GitHub-hosted runners\nalready support node24, so no project-specific impact.\n\nThe version pin in the tests is a deliberate guard rail: it forces a\nhuman to consciously update the test alongside any major bump rather\nthan letting an unreviewed major version change ride a green CI.\nThis commit keeps that pattern (just rolled forward) so the next\nmajor bump triggers the same review loop.\n\nSupersedes dependabot PR #485, which couldn't merge alone because of\nthe test pin. Dependabot will auto-close #485 once main reaches v4.\n\nAddresses #500",
          "timestamp": "2026-04-28T11:32:57+01:00",
          "tree_id": "c5b3b5dbbd1ba964393f0d7872cbb9a41191388a",
          "url": "https://github.com/endavis/pyproject-template/commit/dbcf586562fbb4ce8d8de10db4505c600943b2f1"
        },
        "date": 1777372410857,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8403548.52493715,
            "unit": "iter/sec",
            "range": "stddev: 1.1260921937450317e-8",
            "extra": "mean: 118.99734939740578 nsec\nrounds: 84660"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8401341.289667554,
            "unit": "iter/sec",
            "range": "stddev: 1.1847235075565985e-8",
            "extra": "mean: 119.02861287516752 nsec\nrounds: 80620"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5770596.72993564,
            "unit": "iter/sec",
            "range": "stddev: 1.4901191327121325e-8",
            "extra": "mean: 173.29230351730942 nsec\nrounds: 56010"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1716832.5304943165,
            "unit": "iter/sec",
            "range": "stddev: 2.725210380204795e-7",
            "extra": "mean: 582.4679939586632 nsec\nrounds: 57661"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 501440.8016533855,
            "unit": "iter/sec",
            "range": "stddev: 5.289453573305068e-7",
            "extra": "mean: 1.9942533529436188 usec\nrounds: 49658"
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
          "id": "4bdbbc52ae867e483a12e963bbd7fd3359da3ca1",
          "message": "fix: scrub remaining tools/pyproject_template/ refs in three docs files (merges PR #502, addresses #474)\n\nAddresses #474\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-28T13:05:34+01:00",
          "tree_id": "5f5475c5dcbb948f58e93349109d35473e25e791",
          "url": "https://github.com/endavis/pyproject-template/commit/4bdbbc52ae867e483a12e963bbd7fd3359da3ca1"
        },
        "date": 1777378125317,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8312624.705514235,
            "unit": "iter/sec",
            "range": "stddev: 1.1556081184268175e-8",
            "extra": "mean: 120.29894713478926 nsec\nrounds: 83382"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8481247.888079878,
            "unit": "iter/sec",
            "range": "stddev: 1.256368722927465e-8",
            "extra": "mean: 117.90717748097752 nsec\nrounds: 83181"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5604961.051787447,
            "unit": "iter/sec",
            "range": "stddev: 3.4160740596458374e-8",
            "extra": "mean: 178.41337178981746 nsec\nrounds: 137476"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1686958.5602515657,
            "unit": "iter/sec",
            "range": "stddev: 2.712297819443368e-7",
            "extra": "mean: 592.7827888379643 nsec\nrounds: 42728"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 508373.5618681299,
            "unit": "iter/sec",
            "range": "stddev: 5.25665411682485e-7",
            "extra": "mean: 1.9670574455628282 usec\nrounds: 53320"
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
          "id": "b1f4bc7860328b315c2a6ee61c08da6697c92021",
          "message": "chore: declare least-privilege permissions in pr-checks.yml (merges PR #504, addresses #503)\n\nAdd a top-level `permissions:` block (`contents: read`, `pull-requests:\nread`) to .github/workflows/pr-checks.yml so the workflow's GITHUB_TOKEN\nno longer inherits the repository-default scopes. Resolves CodeQL alerts\n#2, #5, and #18 (one per job).\n\nAlso update the workflow permissions table in\ndocs/development/github-repository-settings.md so the PR Validation row\nreflects the now-declared permissions instead of \"Default\".\n\nAddresses #503\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-28T13:33:34+01:00",
          "tree_id": "0ae3ec38d45d749f2e648d2123fa879849e7e986",
          "url": "https://github.com/endavis/pyproject-template/commit/b1f4bc7860328b315c2a6ee61c08da6697c92021"
        },
        "date": 1777379639672,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8726945.519617554,
            "unit": "iter/sec",
            "range": "stddev: 1.4673352496955112e-8",
            "extra": "mean: 114.58762951505437 nsec\nrounds: 86708"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 9022434.431089697,
            "unit": "iter/sec",
            "range": "stddev: 1.0118369431447756e-8",
            "extra": "mean: 110.8348315122334 nsec\nrounds: 87306"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5532229.809695738,
            "unit": "iter/sec",
            "range": "stddev: 1.4609043405413034e-8",
            "extra": "mean: 180.75894068019528 nsec\nrounds: 53591"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1610350.4711546428,
            "unit": "iter/sec",
            "range": "stddev: 2.7007804183759036e-7",
            "extra": "mean: 620.9828344279533 nsec\nrounds: 42527"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 532113.0486565591,
            "unit": "iter/sec",
            "range": "stddev: 2.9855008771839165e-7",
            "extra": "mean: 1.879299901636933 usec\nrounds: 35575"
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
          "id": "5dace4a7dddfe5a3479d62401211527cdae15514",
          "message": "fix: resolve PyPI name at runtime in doit release_tag printout (merges PR #505, addresses #478)\n\nAddresses #478",
          "timestamp": "2026-04-28T14:59:21+01:00",
          "tree_id": "1d19610575d0459af96f16284585cc56d32d506d",
          "url": "https://github.com/endavis/pyproject-template/commit/5dace4a7dddfe5a3479d62401211527cdae15514"
        },
        "date": 1777384794720,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8228294.094465139,
            "unit": "iter/sec",
            "range": "stddev: 1.1399923945258861e-8",
            "extra": "mean: 121.5318738634612 nsec\nrounds: 83592"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8325075.553319521,
            "unit": "iter/sec",
            "range": "stddev: 1.625261913656851e-8",
            "extra": "mean: 120.11902998300867 nsec\nrounds: 81813"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5731803.826227103,
            "unit": "iter/sec",
            "range": "stddev: 1.552313658576221e-8",
            "extra": "mean: 174.46514750283052 nsec\nrounds: 57931"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1673348.9643495698,
            "unit": "iter/sec",
            "range": "stddev: 2.6502297093572815e-7",
            "extra": "mean: 597.6039793879454 nsec\nrounds: 66191"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 499326.3587497628,
            "unit": "iter/sec",
            "range": "stddev: 4.999523921875075e-7",
            "extra": "mean: 2.0026982002389135 usec\nrounds: 55729"
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
          "id": "f50d7175775ddd2f0da7b02234a5342a5fec3385",
          "message": "feat: support per-platform extract_binaries in install_tool framework (merges PR #506, addresses #477)\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-28T16:25:55+01:00",
          "tree_id": "c30cc172e3c8932ab204c570d4c55ff4485d39df",
          "url": "https://github.com/endavis/pyproject-template/commit/f50d7175775ddd2f0da7b02234a5342a5fec3385"
        },
        "date": 1777389987407,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8276998.164510086,
            "unit": "iter/sec",
            "range": "stddev: 2.0729077345804203e-8",
            "extra": "mean: 120.81674782625613 nsec\nrounds: 85100"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8268672.978686494,
            "unit": "iter/sec",
            "range": "stddev: 1.294656102088297e-8",
            "extra": "mean: 120.93839030490396 nsec\nrounds: 82556"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5174877.0574741345,
            "unit": "iter/sec",
            "range": "stddev: 5.341913467430911e-8",
            "extra": "mean: 193.24130581144695 nsec\nrounds: 57627"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1641322.4800984114,
            "unit": "iter/sec",
            "range": "stddev: 3.7866311436548106e-7",
            "extra": "mean: 609.2647923399193 nsec\nrounds: 52392"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 486257.3199359727,
            "unit": "iter/sec",
            "range": "stddev: 7.988934610955861e-7",
            "extra": "mean: 2.056524311308411 usec\nrounds: 45740"
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
          "id": "170df8c909cd3199c4dfeb866f3494cc989ea61c",
          "message": "chore: add sync-exclude mechanism for downstream template drift (merges PR #507, addresses #481)\n\nAddresses #481\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-28T17:35:58+01:00",
          "tree_id": "f81bdc552430604425379b96ceea9f769b6d82ec",
          "url": "https://github.com/endavis/pyproject-template/commit/170df8c909cd3199c4dfeb866f3494cc989ea61c"
        },
        "date": 1777394197349,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_default",
            "value": 8326680.136383714,
            "unit": "iter/sec",
            "range": "stddev: 1.2862198862006787e-8",
            "extra": "mean: 120.09588258716288 nsec\nrounds: 82768"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_with_name",
            "value": 8203376.5112844,
            "unit": "iter/sec",
            "range": "stddev: 1.8876631211486332e-8",
            "extra": "mean: 121.90102436776125 nsec\nrounds: 84374"
          },
          {
            "name": "tests/benchmarks/test_bench_core.py::test_bench_greet_long_name",
            "value": 5755646.241049026,
            "unit": "iter/sec",
            "range": "stddev: 1.5097290608602453e-8",
            "extra": "mean: 173.74243623036492 nsec\nrounds: 58648"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_get_logger",
            "value": 1682359.9658637932,
            "unit": "iter/sec",
            "range": "stddev: 2.4063233340292515e-7",
            "extra": "mean: 594.4031124674075 nsec\nrounds: 60787"
          },
          {
            "name": "tests/benchmarks/test_bench_logging.py::test_bench_setup_logging",
            "value": 491807.86625832634,
            "unit": "iter/sec",
            "range": "stddev: 5.068737780936561e-7",
            "extra": "mean: 2.0333143664577773 usec\nrounds: 50667"
          }
        ]
      }
    ]
  }
}
window.BENCHMARK_DATA = {
  "lastUpdate": 1775128042139,
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
      }
    ]
  }
}
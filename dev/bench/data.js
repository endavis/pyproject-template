window.BENCHMARK_DATA = {
  "lastUpdate": 1775559875887,
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
      }
    ]
  }
}
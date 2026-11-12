# statcat-serve

[![PyPI](https://img.shields.io/pypi/v/statcat-serve)](https://pypi.org/project/statcat-serve/)
[![Python](https://img.shields.io/pypi/pyversions/statcat-serve)](https://pypi.org/project/statcat-serve/)
[![License](https://img.shields.io/pypi/l/statcat-serve)](LICENSE)
[![Docs](https://github.com/StatCat-Suite/statcat-serve/actions/workflows/docs.yml/badge.svg)](https://statcat-suite.github.io/statcat-serve/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> **Note:** This library has been written extensively with AI assistance
> (Claude Code). Users who are not comfortable with AI-generated code should
> take that into account before adopting it.

**statcat-serve** is the [StatCat Suite](https://statcat-suite.github.io/)'s
serving program. It serves a catalog of products and editions over SDMX-REST:
it polls the Inventory, pulls and attaches each product's live edition, routes
each request to the edition that answers it, and stores rendered results.

```python
import statcat_serve
```

## Status

The repository is a skeleton; Phase 6 of the sharded catalog builds it. Today
it holds the package `statcat_serve` with its version, the suite's tooling and
the docs site's sources. The PyPI and Docs badges above resolve after the
first release and the first docs deployment.

- [The sharded catalog plan](https://statcat-suite.github.io/sdmxlib/design/sharded-bundle-catalog-plan/)
  lists the work: Phase 6 (the router, pulls, pools and readiness, the result
  store, pre-materialisation), Phase 8 (Kubernetes manifests in `deploy/`) and
  Phase 9 (rollout and restore drills).
- [The suite's architecture page](https://statcat-suite.github.io/architecture/)
  describes products, editions and the Inventory.

statcat-serve depends on [sdmxlib](https://github.com/StatCat-Suite/sdmxlib),
[sdmxlib-rest](https://github.com/StatCat-Suite/sdmxlib-rest) and
[statcatlib](https://github.com/StatCat-Suite/statcatlib). None of them
imports it.

## Installation

Requires Python 3.14+. Managed with [uv](https://docs.astral.sh/uv/).
statcat-serve has no release yet. After the first release:

```bash
uv add statcat-serve
# or: pip install statcat-serve
```

statcat-serve is pre-1.0: until 1.0, a minor release may break the API.

## Development

Run once per clone. It installs a pre-push hook that runs the full gate, and
the hook is the only gate, since the repository has no GitHub Actions workflow:

```bash
just hooks-install     # git config core.hooksPath .githooks
```

```bash
just ci                # full gate: index guard + lint + format + docstrings + prose + Any ratchet + pyrefly + unit tests + strict docs build
just test              # unit tests
just lint              # ruff check
just fmt               # ruff format + ruff check --fix
just typecheck         # pyrefly
just check-indexes     # only public PyPI is named anywhere in the repo
just docs              # local docs server
```

The integration and object-store test tiers that statcatlib runs return here
when Phase 6 writes their first tests.

The repository is private for now. Private repositories use the organisation's
GitHub Actions minutes, and GitHub Pages needs a public repository, so
`.github/workflows/docs.yml` arrives when the repository is made public. Until
then `just ci` builds the docs site with `mkdocs build --strict`, and nothing
deploys it.

`uv.lock` is not committed: consumers resolve against `pyproject.toml`, and a
lockfile would record whichever index resolved it. `just check-indexes` fails
the build if a non-public package index is named in any tracked file.

## License

Apache-2.0. See [LICENSE](LICENSE).

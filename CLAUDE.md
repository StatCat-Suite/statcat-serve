# statcat-serve

The StatCat Suite's serving program: an SDMX-REST service over a sharded
catalog of products and editions. The import name is `statcat_serve`.

## Status

The repository is a skeleton. `src/statcat_serve/__init__.py` holds the
package docstring and `__version__`, and `tests/test_version.py` is the one
test of the package. Phase 6 of the sharded catalog plan builds the serving
code; Phases 8 and 9 add `deploy/`. The plan is
`docs/design/sharded-bundle-catalog-plan.md` in sdmxlib, published at
<https://statcat-suite.github.io/sdmxlib/design/sharded-bundle-catalog-plan/>.
Its decision Q8 (2026-11-03) created this repository.

## What the package will hold

- **Router**: a `ShardRouter` over one `EditionEngine`, with single-flight
  attaches per product and LRU eviction.
- **Inventory polling and pulls**: a `LiveInventory`, and the pull of each
  edition's required tier.
- **Pools and readiness**: pool configuration, `/ready`, `/live` and `preStop`.
- **Result store**: rendered responses under `results/`, their keys and their
  garbage collection.
- **Pre-materialisation**: a command that renders each embargoed edition's
  release set. It reads embargoed editions through statcatlib's
  `EmbargoReader`.
- **Preview wiring**: the service that serves the `EmbargoReader` preview
  through sdmxlib-rest.
- **`deploy/`**: reference Kubernetes manifests (Phase 8) and the rollout and
  restore drills (Phase 9).

## Place in the suite

- statcat-serve depends on sdmxlib, sdmxlib-rest and statcatlib. None of them
  imports it.
- sdmxlib owns the edition format, the Inventory documents and their reader.
  statcatlib owns the catalog model, the Inventory writer and `EmbargoReader`.
  sdmxlib-rest is the generic SDMX-REST service, and never imports statcatlib.
- Phase 6 adds four seams to sdmxlib-rest for this package: a per-request
  catalog resolver, the ETag set by the route, routing refusals mapped to 404
  and 503, and a published `RENDER_VERSION`. A change those seams need goes in
  an issue on StatCat-Suite/sdmxlib-rest.
- The hub (github.com/StatCat-Suite/statcat-suite.github.io) holds the suite's
  conventions (`docs/conventions.md`), the docs-site block (`docs/sites.md`)
  and the designs that change a contract between repositories.

## Writing style

These rules cover all prose written for this repo: comments, docstrings,
documentation, CHANGELOG and `docs/upgrading.md` entries, commit messages,
issues, PRs and milestones. The section is shared across the StatCat-Suite
repos (GH-58); change it in all three or none.

Write in plain language. State claims directly, in the order the reader
needs them. Use subject-verb-object sentences, concrete nouns, and the
actual number, name, or mechanism instead of an allusion to it.

Follow these rules from Strunk & White:

- Put statements in positive form.
- Use definite, specific, concrete language.
- Omit needless words.

Avoid these constructions everywhere (sentences, headings, titles, lists):

- Contrast by negation: "not X, but Y", "it's not about X, it's about Y",
  "X isn't the problem; Y is". State Y. Mention X only if someone
  actually holds that view.
- Hook clauses that read like half a question: "what X doesn't tell you",
  "the part nobody mentions", "the evidence Y lacks", "why this matters".
  State the fact the clause points at.
- Colon reveals: "The real issue: ...", "Here's the thing: ...",
  "The short version: ...". Drop the setup and write the sentence.
- Punchline structure: ending a sentence or list on a twist, a dramatic
  final item, or a short fragment for emphasis.
- Rhetorical questions that the text then answers.
- Framing work or ideas by what is missing when you can name what is
  present or proposed.

Titles (milestones, issues, PRs, headings):

- Name the deliverable or scope as a plain noun phrase or imperative.
  A reader should know from the title alone what gets merged or decided.
- Use a colon only to separate a component name from the work item
  (e.g. "Query DSL: add DuckDB backend"), never to introduce a hook.

Examples:

```text
Bad:  Conformance evidence: what the green checks do not prove
Good: Conformance: add negative and edge-case test fixtures

Bad:  Query DSL: a second backend, and the evidence the first one lacks
Good: Query DSL: add second backend; add validation tests for SQL backend

Bad:  The green checks tell you less than you'd think.
Good: The green checks only cover valid inputs; there are no tests
      for malformed DSDs or constraint violations.

Bad:  The problem isn't performance — it's correctness.
Good: The cache returns stale codelists after a version bump.

Bad:  Here's what the benchmark doesn't show: cold-start latency.
Good: The benchmark measures warm queries only; cold-start latency
      is untested.
```

Before finishing, reread the output. Rewrite any sentence that delays its
point, contrasts with a claim nobody made, or alludes to a fact instead of
stating it.


## Tooling

- **Package manager**: `uv`. Install instructions (README, docs, CLI and error
  messages) say `uv add <pkg>` first and `pip install <pkg>` second, as the
  fallback. Quote extras.
- **Command runner**: `just`
- **Type checker**: `pyrefly`, the only one: `preset = "all"` minus a
  deny-list in `pyrefly.toml`, over `src` and `tests`. Suppressions are
  `# pyrefly: ignore[kind]` only; its `unused-ignore` reports a dead one.
  ruff, pyrefly and pydoclint are capped in `pyproject.toml`, so a checker
  release reaches the gate only through a PR that bumps it.
- **Linter/formatter**: `ruff`. SLF001 (private-member-access) is off
  suite-wide: it cannot see package boundaries, so a module reading its own
  package's underscored helpers is flagged at every site. Do not add
  `# noqa: SLF001`; the rule is not selected.
- **`Any`**: `src/` carries zero `Any`-annotated parameters or locals, and an
  `Any` parameter anywhere is a finding. `just check-any` holds the count at
  the baseline in `tools/any_baseline.txt`, which is 0.
- **Docstrings**: plain Google style, checked by `just check-docstrings`.
- **Suite dependencies**: every suite library is pre-1.0, so a minor bump may
  break. `pyproject.toml` caps each suite dependency below its next minor
  (`sdmxlib>=0.88,<0.89`, `sdmxlib-rest>=0.10.3,<0.11`,
  `statcatlib>=0.18,<0.19`), and the PR that adopts a new minor raises the cap.
- **Testing**: `pytest`
- the `ruff.toml` file will NEVER be changed to fix a linting error. If a fix can't be made ask the user to change it.
- `ruff.toml` and `pyrefly.toml` are copied from statcatlib. The owner signs
  off on every change to either file.

## Commands

```bash
just ci                        # the gate: index guard + lint + fmt + docstrings + prose + Any + typecheck + unit tests + docs
just typecheck                 # pyrefly over src/ and tests/
just lint                      # ruff check src tests tools
just fmt                       # ruff format + ruff check --fix
just check-docstrings          # Google sections, no RST roles, pydoclint
just check-prose               # no question headings, no banned hook phrases
just check-any                 # the `Any` ratchet (tools/count_any.py)
just check-indexes             # only public PyPI named in tracked files; uv.lock is gitignored
just coverage                  # unit tests with coverage; fails under 85% (pyproject.toml)
```

### `just ci` is the gate, and it runs locally

The one GitHub Actions workflow, `.github/workflows/docs.yml`, deploys the
docs site and runs no tests or lint, so a change merges on a green `just ci`.
Never dispatch or re-run a GitHub Actions workflow: the organisation's Actions
minutes are scarce.

The gate selects tests by marker (`-m unit`), so **every test file needs a
`pytestmark`**: a file without one never runs in `just ci`. statcatlib's
`integration`, `stores` and `live` tiers have no test here yet. Each tier's
recipe and marker return when Phase 6 writes its first test, and
`test-integration` and `test-stores` then join `ci`.

pytest runs with `strict = true` and `filterwarnings = ["error"]`, and no
ignore list. A test that sets up a situation the code warns about asserts the
warning with `pytest.warns(match=...)`.

**The pre-push hook is the only gate for tests and lint**: `just hooks-install` runs
`git config core.hooksPath .githooks`, and every `git push` then runs
`just ci` first. `core.hooksPath` is per-clone and cannot be set by a commit,
so a fresh clone must run `just hooks-install` before its first push. Bypass
with `git push --no-verify`, sparingly, and say why.

`just ci` ends with `docs-build`, which is `mkdocs build --strict`: it fails
on broken links and pages missing from the nav.

### The docs site

`mkdocs.yml` carries the StatCat Suite block between its "Suite configuration"
markers, copied from the hub's `docs/sites.md`. The hub also serves the
stylesheet and favicon the block names by URL. Change the block in the hub
first, then here; never only here.

The repository is public. `.github/workflows/docs.yml` (statcatlib's is the
model) runs `just docs-build` and deploys the site to
<https://statcat-suite.github.io/statcat-serve/> on each push to `main` that
changes the site's sources. The hub's `docs/sites.md` lists the steps for
adding the site.

### Designs

Current designs and RFCs live in `docs/design/`, are listed in
`docs/design/SITEMAP.md` and appear in the site nav under "Design". EGM review
reports for a design go in `docs/design/egm/<feature>/`. A design that changes
a contract between repositories lives in the hub's `docs/design/`, and the
local design links it.

## Git / GitHub

- git commit/push/merge etc. will NEVER be done without asking.
- The project always uses conventional commits for commit messages. git-cliff
  builds `CHANGELOG.md` from them, one entry per commit.
- Nothing is signed with Claude: commit messages carry no `Co-Authored-By`
  trailer, and PR descriptions, issues and comments carry no "Generated with
  Claude Code" footer. The README's note discloses AI use once for the project.
- `main` is protected: changes arrive through a PR, merged with a merge commit
  (`gh pr merge --merge`). The hub's `docs/conventions.md` describes the
  ruleset.
- The project lives at github.com/StatCat-Suite/statcat-serve; use `gh` for
  the API.
- Releases go through a PR: `just release-1-preview` … `release-5-pypi`.
- Write a GitHub issue or PR as `GH-N`, and one in another repository as
  `StatCat-Suite/<repo>#N`.

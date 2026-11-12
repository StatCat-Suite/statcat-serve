# statcat-serve

statcat-serve is the StatCat Suite's serving program. It serves a catalog of
products and editions over SDMX-REST: it polls the Inventory, pulls and
attaches each product's live edition, routes each request to the edition
that answers it, and stores rendered results.

## Status

The repository is a skeleton. It holds the package `statcat_serve` with its
version, the suite's tooling and this site. Phase 6 of the
[sharded catalog plan](https://statcat-suite.github.io/sdmxlib/design/sharded-bundle-catalog-plan/)
builds the serving code, and Phases 8 and 9 add `deploy/`.

## What the package will hold

The plan's decision Q8 (2026-11-03) assigns these parts to statcat-serve:

| Part | Phase | What it does |
| --- | --- | --- |
| Router | 6 | A `ShardRouter` over one `EditionEngine`. It attaches a product's live edition once for concurrent first requests, evicts by LRU, and resolves a dataflow or a full artefact through the Inventory's leaves. |
| Inventory polling and pulls | 6 | A `LiveInventory` that follows `CURRENT`, and a pull of each edition's required tier, checked on open. |
| Pools and readiness | 6 | The `hot`, `base` and `search` pools. `/ready` answers ready once every pinned live edition is attached; `/live` is the liveness probe. |
| Result store | 6 | Rendered responses under `results/`, keyed by the edition's fingerprints and the render versions, with their garbage collection. |
| Pre-materialisation | 6 | A command that renders the release set of each embargoed edition before its release. It reads embargoed editions through statcatlib's `EmbargoReader`. |
| Preview wiring | 6 | The service that serves the `EmbargoReader` preview through sdmxlib-rest. The operator deploys it with its own identity and authentication. |
| `deploy/` | 8, 9 | Reference Kubernetes manifests, and the rollout and restore drills. |

## Place in the suite

statcat-serve depends on three suite projects, and none of them imports it:

- [sdmxlib](https://statcat-suite.github.io/sdmxlib/) owns the edition format,
  the Inventory documents and their reader.
- [statcatlib](https://statcat-suite.github.io/statcatlib/) owns the catalog
  model, the Inventory writer and `EmbargoReader`.
- [sdmxlib-rest](https://statcat-suite.github.io/sdmxlib-rest/) is the generic
  SDMX-REST service. Phase 6 adds four seams to it for statcat-serve: a
  per-request catalog resolver, the ETag set by the route, routing refusals
  mapped to 404 and 503, and a published `RENDER_VERSION`.

The hub's [architecture page](https://statcat-suite.github.io/architecture/)
describes products, editions and the Inventory.

## Installation

statcat-serve has no release yet. After the first release:

```bash
uv add statcat-serve
# or: pip install statcat-serve
```

It requires Python 3.14 or later.

"""statcat-serve: the StatCat Suite's serving program.

The package is a skeleton. Phase 6 of the sharded catalog plan builds it:

- the router over one `EditionEngine`, which attaches a product's live edition
  on first request and evicts by LRU;
- Inventory polling and tier pulls;
- pools and the `/ready` and `/live` probes;
- the result store, its keys and its garbage collection;
- pre-materialisation, which reads embargoed editions through statcatlib's
  `EmbargoReader`;
- the wiring that serves the `EmbargoReader` preview through sdmxlib-rest.

statcat-serve depends on sdmxlib, sdmxlib-rest and statcatlib. None of them
imports it.
"""

import importlib.metadata

#: The installed distribution's version, read from its metadata, as
#: statcatlib's store reads its own. `pyproject.toml` is the one place it is set.
__version__ = importlib.metadata.version("statcat-serve")

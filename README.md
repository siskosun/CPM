# CPM — Cube Method Research

Research code for exploring low-memory, high-speed 3×3 solving methods.

Current module: `cpm.eo`, a geometric edge-cubie model for the standard ZZ-style EO convention. The model is independent of third-party Roux solver coordinate encodings.

Run tests:

```bash
python -m unittest discover -s tests -v
```

This is not yet a full 3×3 solver, complete cubie model, EO searcher, partial-EO optimizer, or human-speed model. See `docs/RESEARCH_LOG.md` for implementation decisions, corrections, validation and limitations.

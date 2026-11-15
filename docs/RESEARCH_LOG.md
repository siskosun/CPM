# Research Log

## 2026-11-15 — EO model bootstrap

- Added a geometric edge-cubie model using sticker normals and slot-dependent EO classification.
- Defined the standard ZZ EO-preserving face-turn generators: `R`, `L`, `U`, `D`, `F2`, `B2` and inverses.
- Added a geometric `M` slice operation to demonstrate that a quarter-turn of the middle slice does not preserve this EO convention.
- Added tests for move inverses, four-quarter-turn identity, EO-preserving generators, F/B quarter-turn effects, and even EO parity.

### Validation

`python -m unittest discover -s tests -v`

Result: 11 tests passed.

### Important implementation correction

The first draft incorrectly classified edge orientation using only the cubie's U/D sticker axis. This made R/L quarter-turns appear to flip edges, contradicting the ZZ EO subgroup. The definition was corrected to use the cubie's primary sticker (U/D sticker when present, otherwise F/B sticker) against the reference axis of the *current slot* (U/D axis for U/D-layer slots, F/B axis for middle-layer slots). A further test caught a non-canonical sticker tuple ordering issue; solved-state construction now sorts sticker entries so inverse and four-turn identity tests compare stable states.

### Scope limits

This is an edge-only geometric model. It does not yet model corners, centers, full cube legality, EO search, partial EO variants, or human execution time. The EO convention and all later algorithms must be cross-checked against an independent cubie implementation before use in comparative experiments.

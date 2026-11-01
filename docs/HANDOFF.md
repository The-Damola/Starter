# Handoff log (newest first)

## Run 1 — 2026-11-01
**Done**
- Research sweep (fan-revival story, 2K14/2K20/2K26 trade-offs, IFF format, dev-blog mechanics catalogue) → `docs/research/`.
- `tools/iff/iff_ls.py`: lists entries of a 2K16–2K20 `.iff`, repairs 2K's near-JSON, extracts the skeleton joint tree. 4 unit tests + 1 real-file smoke test (gated on `IFF_SAMPLE`), all passing on a 2K17 face file (196 joints).

**Next**
- Get a real 2K26 `.iff` (needs the game, via Looyh's 2K26 File Explorer on the user's PC) and check whether the ZIP-inside layout still holds.
- Python possession sim (ratings + tendencies → outcomes), validated against simmed 2K box scores.
- Measurement harness skeleton (virtual pad + frame capture) — Windows only, needs Remote Control.

**Uncertain**
- Whether 2K26's `.iff` entries are still plain ZIP/deflate or wrapped (Looyh's tool exports ZIP-encoded files; untested here).
- `.model` and `.mathnodes` binary layouts are unparsed.

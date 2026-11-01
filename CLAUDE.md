# NBA 2K clean-room rebuild — project rules

Goal: rebuild the *feel* of NBA 2K basketball (dribbling, shooting, defense, possession sim) in our own engine, from data, measurement and 2K's own public dev blogs. Never from the game's executable.

## Hard lines
- No DRM or anti-cheat circumvention. No decompiling the game binary.
- Game assets (models, animations, textures) are studied, never shipped. Nothing from `/tmp/ext` or a game install gets committed.
- Work on offline copies of the game only.

## Layout
- `tools/iff/` — Python inspectors for 2K's `.iff` containers. Tests live next to code (`test_*.py`), run with `python3 -m pytest tools/iff`.
- `docs/research/` — sourced research notes. Every claim carries a URL.
- `docs/HANDOFF.md` — dated Run entries (done / next / uncertain). Read the top entry first.

## Conventions
- Python 3.13, standard library first. Add a dependency only when a test needs it.
- Code-pair rules: simplest thing that works, one responsibility per unit, tests alongside, say how it was checked.
- Run one of anything is bare-bones; polish later.

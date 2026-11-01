# Handoff log (newest first)

## Run 1 — 2026-11-01
**Done**
- Research sweep → `docs/research/`: `revival-story.md` (2K17 Revival shutdown, sourced), `versions.md` (2K14/2K20/2K25/2K26/2K27 as reference material), `iff-format.md` (gen-1 and ZIP-era container layouts, parsers, sample URLs), `data-layer.md` (what of 2K is readable as data), `2k26-data-dictionary.md` (1,812 player fields + 169 AI tuning constants, names only), `executor-tooling.md` (Remote Control, Agent SDK, MCP facts), `mechanics-raw.md` (401 mechanics mined from 2K dev blogs 2K11–2K27, sourced). (No synthesised catalogue: the synthesis agent was stopped to cap spend; `mechanics-raw.md` is complete.)
- `tools/iff/iff_ls.py`: lists ZIP-era (2K15+) `.iff` entries, repairs 2K near-JSON, extracts the skeleton (196 joints on a 2K17 face file); detects gen-1 (2K9–2K14) headers and says so instead of crashing. 6 tests.
- `tools/schema/dump_2k_schema.py`: renders the DB2K Editor offset JSON into the data dictionary. 1 test.
- Scratch sources used (not committed, in /tmp/ext on the session box): gregkwaste/NBA2K17_Explorer, discobisco/2k26-Editor, bep713/2k-tools, wyhuai/SkillMimic (BallPlay-M subset: 101 clips, Apache-2.0).

**Next (in order)**
1. On the user's Windows PC, offline copy: run DB2K Editor against 2K26 or 2K27 and export the AI tuning values and one full team's attributes/tendencies to JSON. That turns the data dictionary into numbers.
2. Python possession sim built on 2K's own vocabulary (attributes, tendencies, tuning constants), fixed timestep, deterministic. Validate against 82 simmed games from the real game.
3. Measurement harness (vgamepad + capture) to reproduce one NBA2KLab green-window test.
4. Engine decision (Unity + JLPM22 motion matching vs Godot) and a half-court dribbling prototype using the 54-slot move taxonomy from the data dictionary.

**Uncertain**
- Whether 2K26 `.iff` exports are still plain ZIP/deflate (untested here; needs a real 2K26 file).
- `.model` and `.mathnodes` binary layouts are unparsed. nothanley/NBA2K_Scene-Model on GitHub may cover `.model`.
- AI tuning *values* are unknown until read from a running game.
- Budget: the research workflow consumed ~1.8M output tokens, ~20M cache-write tokens and ~109M cache-read tokens across 13 agents. At Fable 5.1 API list prices that is roughly $370–620 depending on cache-write rate. Future runs: no multi-agent workflows; one agent at a time, Sonnet or Haiku for web mining.

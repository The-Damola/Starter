# The data layer: what of 2K's "soul" is already readable (2026-11-01)

Verified in this session, in the sandbox, without owning the game.

## 1. The container is a ZIP
A 2K17 `.iff` face file opened with Python's `zipfile`: 14 entries, deflate, no custom header. Entries: `.SCNE` (near-JSON scene graph with the full 196-joint skeleton, LOD chain hihead_1..5), `.model` (binary mesh, magic `0x453C46B2`), `.mathnodes` (binary), `appearance_info.RDAT` (16-byte prefix + JSON). Tool: `tools/iff/iff_ls.py`. Looyh's 2K26 File Explorer exports are also "ZIP-encoded internally" per NLSC coverage, so the same approach likely holds for 2K26 (UNTESTED on a 2K26 file).

## 2. The player model is 1,812 named fields
From the open-source DB2K Editor schema (github.com/discobisco/2k26-Editor), which reads a running 2K22–2K27 process. Full list in `2k26-data-dictionary.md`. The shape that matters for a rebuild:
- **Attributes** (53 gameplay + 18 durability): 3pt, Mid-Range, Close Shot, Layup, Driving Dunk, Standing Dunk, Post Hook/Fade/Control, Ball Handle, Speed With Ball, Pass Accuracy/IQ/Vision, Interior/Perimeter D, Steal, Block, Lateral Quickness, Speed, Acceleration, Agility, Strength, Vertical, Stamina, Hustle, plus hidden ones: Reaction Time, Contest Shot, Pick-and-Roll, Intangibles, Potential.
- **Tendencies** (138 in 9 groups): 32 jump-shot tendencies split by zone and situation (spot-up, off-screen, step-back, transition, contested), 16 driving, 8 drive setup (triple threat variants), 19 post, 10 freelance (iso vs elite/good/average/poor defender, roll vs pop, touches), 7 defense (contest, block, steal, foul, take charge), 31 hot zones. This is the AI's decision table.
- **Signature animation slots** (117): 54 ball-handling slots (IsoCrossover, IsoHesitation, IsoBehindBack, IsoStepback, Moving Crossover/Spin/Stepback, Signature Size-Up, Dribble Style, Triple Threat Style, Escape Moves…), 12+6 jump-shot slots (Jumpshot Base, Upper Release 1/2, Release Timing, Shot Timing Impact Modifier, Go-To Shot), 18 dunk/layup packages, 7 post. **This is the Pro Stick move taxonomy.** Every dribble move the stick can trigger has a slot here, and each slot picks one canned animation family per player.
- **Badges**: ~190 across 2K22–2K27 including the 2K27 set.

## 3. The AI tuning singleton is 169 named constants (2K27)
Also in the DB2K schema: `BodyupDefenderDisengageAngleInDegrees`, `BodyupEntryDefenderSelectionMaxDistanceForTakingChargeInFeet`, `BodyupStealProbabilityMultiplier`, `AnchorDistFromHoopNoHelp`, `JumpToBallCushionDistance`, `StartTurboDistance`, `TerminationTimer`, `BoostJumpersBasic.ShotChanceMultiplier`, `LargerPerfectWindowsBoosted.PerfectShotWindowMultiplier`, `ShotChanceMultiplierMin/Max`, plus Takeover meter multiplier arrays. These are Visual Concepts' own variable names for body-up defense, help-defense positioning and shot-boost maths. Sandbox2K's commercial "2K27 Studio" claims "thousands of gameplay values, each explained in plain English", so the full tuning set is larger than 169 and someone has already decoded it.

Reading the *values* needs the game running on a Windows PC with DB2K Editor attached (offline mode). That is the single highest-value thing the user's PC can do for this project.

## 4. Historic precedent: tunedata.iff
NBA 2K14 shipped gameplay tuning as `tunedata.iff`; modders edited it with Hex on Steroids profiles mapping offsets to names (84 slider-like entries plus more). NLSC: https://forums.nba-live.com/viewtopic.php?t=96395 and https://forums.nba-live.com/viewtopic.php?t=100961.

## What this changes in the plan
The possession-level sim can be built against 2K's own vocabulary (attributes + tendencies + tuning constants) rather than invented ratings, and validated by reading the real numbers off a running offline copy. Animation remains the part that has to be rebuilt, but the *taxonomy* of moves is now known.

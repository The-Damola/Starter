# The NBA 2K17 "Revival" fan server: what actually happened (checked 2026-11-01)

Why this matters for us: it is the clearest recent case of what Take-Two tolerates and what it kills, and it is the only public account of how 2K's online netcode works.

## Timeline (sources inline)

- **28 Jul 2025** — `@revivalclient` X account created, bio "#SaveTheGame / Not affiliated with NBA 2K". ([NBA2KPROAM timeline](https://nba2kproam.com/news/savethegame-nba-2k17-revival-timeline/))
- **24–25 Jul 2026** — Revival Client beta goes live: a Windows launcher plus community-run servers that re-enable NBA 2K17 PC online modes (MyCareer first). Built by "$jay". ([Welcome post](https://revivalclient.net/news/welcome-to-revival-client), [v0.1.7 release](https://revivalclient.net/news/revival-launcher-release))
- **Model** — you bring your own Steam copy; Revival sells server access. Free tier plus a paid tier: "Revival Pass" from $9 one-time (30 days) and "Revival+" $9/month, with Revival Currency welcome packages (+180K / +320K), early-access whitelist, cloud save, badge redeems, Discord role. A $40 one-time unban and a $10 stat reset are listed "coming soon". Payments via Stripe. ([Store page](https://revivalclient.net/revival-plus), [Terms](https://revivalclient.net/terms))
- **25–28 Sep 2026** — YouTube/TikTok blow-up ("NBA 2K17 IS OFFICIALLY BACK"). Reddit thread notes "They charged people 9 dollars to get early access" and that the money is what killed it. ([r/NBA2k](https://www.reddit.com/r/NBA2k/comments/1wtz9li/the_2k17_revival))
- **29 Sep 2026** — creators report copyright claims and strikes on YouTube, TikTok and X. Revival removes purchase gates, then posts it will "temporarily pause all active online revival services and downloads". Site notice: "Download & Services currently unavailable due to restrictions placed upon Revival on behalf of Take-Two." ([NBA2KPROAM](https://nba2kproam.com/news/savethegame-nba-2k17-revival-timeline/))
- **30 Sep – 1 Oct** — #SaveTheGame rally led by creators (Choc, JackedBill, HankDaTank, AllCity). JackedBill reports the paid "Revival Plus" tier publicly; community treats monetised legacy access as the likely trigger. Mike Wang's X account deactivated and reactivated. ([NBA2KPROAM](https://nba2kproam.com/news/savethegame-nba-2k17-revival-timeline/), [2KHQ](https://2khq.com/news/modes/savethegame-nba-2k17-revival-timeline))
- **7 Oct 2026** — Revival publishes a netcode explainer defending itself. ([Input delay post](https://revivalclient.net/news/why-online-2k-has-input-delay))
- **Late Oct 2026** — TikToks say "2k17 servers are back in 2026 … Revival plus available too", and a rival "Reborn Client" appears. As of today the revivalclient.net store and download pages are live again. Whether the servers are actually up is NOT IN SOURCE. ([TikTok tag](https://www.tiktok.com/discover/revival-client-2k17), [homepage](https://revivalclient.net/))

- **NLSC coverage** — the NLSC Podcast (#650) covers the DMCA and reports Revival "dropping the approach of it being a paid service". The same wave also revived 2K15 and 2K16 online. ([NLSC](https://www.nba-live.com/))
- **Counter-example, same month** — a fan revival of WWE 2K19 servers (same publisher, no charging at all) was pulled by its creator around 21 Oct 2026 after a 2K copyright claim on his video. Money made Revival a bigger target; its absence did not make the WWE project safe. ([r/WWEGames](https://www.reddit.com/r/WWEGames/))

**No official statement.** 2K and Take-Two have never named Revival, revivalclient or #SaveTheGame publicly. "DMCA strike" and "cease and desist" wording comes from creators, not from the company. ([NBA2KPROAM](https://nba2kproam.com/news/savethegame-nba-2k17-revival-timeline/))

## What it tells us

1. **The trigger was the server emulation, with money as an accelerant, not the modding.** The WWE 2K19 case shows unpaid server revivals get hit too. 2K lets a decade of NLSC modders ship IFF mods, roster editors and file explorers untouched. The thing that got hit within days was a paid service that reconnects 2K's own client to someone else's server, with its own currency. Our project is the opposite shape: own code, own assets, nothing shipped, no money.
2. **Clean room beats clever emulation.** Revival's whole product depends on 2K's binary and 2K's protocol. One letter ends it. A rebuild that only borrows measured behaviour cannot be ended the same way.
3. **Netcode fact we can use.** Per Revival's engineers, every 2K from 2K14 to 2K27 runs online as deterministic lockstep at 60 fps: only controller inputs cross the wire, each input is stamped six frames ahead (~100 ms fixed delay), no prediction, and one late packet stalls every player. If we ever add online play, deterministic lockstep is the proven design for this genre and a fixed 6-frame delay is the number to start from. ([Input delay post](https://revivalclient.net/news/why-online-2k-has-input-delay))
4. **Determinism is a design constraint early.** Lockstep only works if the sim is bit-identical across machines. That argues for a fixed-timestep sim with integer or deterministic-float math from day one, even if online is years away.

# Handoff — smythp.com / blog repo

Successor brief from the May 9-10 2026 sessions. Read this before starting work.

State at handoff: master is **19 commits ahead of `origin/master`**, none pushed. Dev server is not running.

## What landed this round (May 10)

- **Title fix on live (when pushed)**: Staff → Principal Developer Relations Engineer in `about.md` and `_projects/chainguard.md`. Also fixed a stale `link: https://iotaschool.com/` → `https://www.chainguard.dev/` on the chainguard project entry. Commit `892e5c0`.
- **5 new drafts** wired up with frontmatter, resources, and (where available) embeds + native LI feature images:
  - `2025-05-18-cheese-must-stand-pycon.md`
  - `2024-09-19-beyond-zero-pytorch.md`
  - `2025-03-18-assemble-2025-old-new-strange.md` — Patrick prose committed
  - `2025-12-29-vibelympics-2025.md` — Patrick prose committed
  - `2026-04-27-mythos-zero-days.md` — Patrick added an opening quote; body needs more prose
- **Promotion draft dropped** at Patrick's call ("let's skip this one no promotion post"); the LI post itself stays in `~/li/my_posts/` if anyone reconsiders.
- **`assets/images/posts/*` is now gitignored**. Force-add per-post (`git add -f assets/images/posts/<file>`) when wiring an image into a draft. Already-tracked images stay tracked.
- **Vibelympics header image** scraped from the Chainguard Unchained post and committed at `assets/images/posts/vibelympics-2025.png` (used as feature on that draft).
- **Vibelympics finals YouTube** wired into the embed: field of the vibelympics draft.

## Posts pipeline — 8 of ~19 drafted

Total target was 20; promotion was dropped, so ~19 to go through.

**Drafted in `_drafts/`**:

- `2024-09-19-beyond-zero-pytorch.md` — PyTorch 2024 (no prose yet)
- `2025-03-18-assemble-2025-old-new-strange.md` — Assemble 2025 breakout (prose ✓)
- `2025-05-18-cheese-must-stand-pycon.md` — PyCon US 2025 (no prose yet)
- `2025-12-29-vibelympics-2025.md` — Vibelympics recap (prose ✓)
- `2026-03-23-advisory-feeds-with-konstantinos.md` — Assemble 2026 (no prose yet)
- `2026-03-27-rsac-ml-pipelines.md` — RSAC 2026 (no prose yet)
- `2026-04-27-mythos-zero-days.md` — Mythos blog (opening quote ✓, more prose welcome)
- `2026-05-05-supply-chain-attack-takeaways-webinar.md` — Chainguard webinar (no prose yet)

**Tier A still to draft**:

- Chainguard Assemble 2026 NYC — Manfred Moser talk on Chainguard Libraries (separate from the Konstantinos one already drafted; the 2026-03-16 preview post mentioned both)

**Tier B**:

- AI/ML Supply Chain Security course launch (Jul-Aug 2024)
- FrankenPipe — secure ML pipelines (Oct 2025 + Dec 2025 recording)
- EKS Auto Mode with Sai Vennam (Aug 2025)
- Chainguard Libraries for Python launch (Oct 2025 - Jan 2026)
- AI Native Dev Conference appearance (Dec 2025)
- Hard Truths series episode 1 (Feb 2026) — note: posted from `chainguard-dev` LI account but featuring Patrick; frame as "appeared in" not "I posted"
- Chainguard Unchained: ML pipeline maturity gap blog (2026-01-26)
- Zero CVEs / no-DSA Debian deep dive (2026-02-27) — Chainguard Research piece Patrick co-wrote

**Tier C**:

- Pandas + NumFOCUS + Iota nonvisual data science workshop series (Jan-Mar 2024)
- Austin Kubernetes meetup talk (May 2024)
- 2026: the year of AI-assisted attacks blog / Rakuten teens (2026-04-14)

**Curation rule learned the hard way**: filter LI URL by author. `linkedin.com/posts/smythp_*` and `linkedin.com/posts/iotaschool_*` = Patrick's own posts. Everything else (e.g. `linkedin.com/posts/adrianmouat_*`, `linkedin.com/posts/imjasonh_*`, `linkedin.com/posts/manfredmoser_*`) is a repost — drop. Three picks were dropped earlier (Rejekts, Shai-Hulud, Linux Foundation throwaway) for this reason.

**Pairing pattern that's working**:

1. Agent reads source LI post body, fetches event page / GitHub / recording URL with WebSearch + WebFetch
2. Agent stages `_drafts/<date>-<slug>.md` with frontmatter wired (title, subtitle, image, embed, resources) and a SHORT factual placeholder body
3. Patrick writes the actual prose (or refines what the agent wrote)
4. **NO LLM-written summaries, no editorialized prose, no winks**. Patrick was emphatic: "i dont' want the fucking wink stuff." Boring, factual, lifted from upstream sources is the brief.

## Push to live — cadence

Per the previous handoff: "after Principal title fix lands and 3-5 substantive posts are out of drafts." Title fix has landed (commit `892e5c0`); drafts have not yet been moved into `_posts/`. Currently 2 of 8 drafts have Patrick prose; the rest are scaffolded only.

A push of master right now would make the title fix go live but no new posts (drafts are excluded from build by default). That's safe but partial. Patrick's call when to ship.

## CV is stale

`cv.md` (rendered at `/cv/`) ends with Patrick's pre-2022 academic / Iota positions. Zero Chainguard. Needs:

- **Principal Developer Relations Engineer**, Chainguard, October 2025 — present
- **Staff Developer Relations Engineer**, Chainguard, [start date — Patrick to confirm, somewhere in 2023 or 2024] — October 2025
- New publications / talks since 2022 — PyCon US 2025 (Cheese Must Stand), RSAC 2026 (Securing ML Pipelines), PyTorch Conference 2024 (Beyond Zero), AI Native Dev Conference, Chainguard Assemble 2025 + 2026, plus Chainguard Unchained blog posts (Mythos, ML pipeline maturity gap, AI-assisted attacks, etc.)
- The full list of LI-pointer events is in `~/li/my_posts/*.md` — see the curated 19 in this brief's "Posts pipeline" section

The CV is a real piece of work, not a one-liner. Patrick will need to pair on the actual content; agent's job is to surface candidate material and propose structure. Working source files are in `_cv/` (cv.md, cv.tex, cv.org, cv.pdf, etc. — derivative outputs); the live source the site renders from is the root `cv.md`.

## Site work — broader directions signaled, never finished

- **Project list refresh**: current `_projects/` is all 2018 DH-era (chainguard, dh_box, dri_curriculum, eloud, foundations, iota, neh, stsci, negotiated_access). The whole AI-infra body of work is invisible — tine, spiritengine, skein, spindle, mill, horizon, shuttle, claudio, slub, prism, fathom, etc. Patrick wants framing as "DevRel with academic DNA, does a lot of good shit and stuff with AI." Tagline ("Teacher / Coder / Writer") he said he'd think about. Two tangled questions: which AI projects make the cut, and what happens to DH-era ones (drop / demote to "earlier work" tail / keep mixed).
- **/posts/ index** shows 2015-2017 DH posts mixed with 2025+ stuff. May want to demote, year-section, or hide-by-default. Cosmetic.

## dccccc.cc — never started, parked

Patrick's scrappy/jank personal site. Source is `~/projects/server-www/www/`. Live `index.html` is one line: "This is a website on the internet."

What he signaled he wanted (March-May 2026 conversation):

- Keep the jank energy. "I kinda like the jank. this is corpo Patrick" — referring to smythp. dccccc is the personal-but-public dump.
- Add an index page in the same shitty inline-style HTML that lists all the existing weird stuff — already there: `lily_birthday.html`, `gifts.html`, `officehours.html`, `boris.html`, `lily_two.html`, `baby_it_dances_yo.gif`, `edit_bios.gif`, `ass.ics`, `balls_of_it.txt`, `grammo.txt`, `peeking.png`, `swing.png`, `yoga.png`, `lily_wants_you.png`, `nonsense/` (snuff order page + CSV), `org/` (tarotconnection.net stuff), `archive/`.
- Dump new weird shit from his recent fun-coded projects. Candidates from his ecosystem: `slub` (foreign-text chunk dropper), `tome` (audio kv store), `ko` (clipboard TTS), `cards` (tarot scraper, fits the existing `org/` tarot vibe), `pitch` (daily seed scanner), `snuffs-buy` (snuff catalog, fits `nonsense/`), `timevault` (Wayback resurrector), `anki` (poetry memorization deck generator), `shelf` (fiction reading DB), `pantry` (household ordering CLI), plus old gifs / scratch HTML / random text dumps.

Hosting/deploy target needs confirming — presumed `~/projects/server-www/www/` deploys to dccccc.cc but verify before changes go live.

## Image gaps

`scripts/fetch_post_media.py` pulls native LI image attachments (Unipile API). Of the 15 audited tier A/B candidates, only 4 had native images (slopsquatting, RSAC, AI Native Dev, PyTorch presentation). The rest need pictures from Patrick or another source. He said: "we need images i think. maybe do some best effort, dont' stretch, and i'll help with misses (on images)."

When Patrick provides a pic from `~/Pictures/`, copy to `assets/images/posts/<slug>.png` (or .jpg) and `git add -f` it. Wire into draft frontmatter as `image: { feature: posts/<slug>.png }`. The `cover-img` class on cards (15rem height, `object-fit: cover`) handles the crop.

For Chainguard blog posts (Mythos, etc.), header images can be scraped from the Unchained article — that pattern worked for Vibelympics this round. Look for `images.ctfassets.net/.../*.png` URLs in the page source.

## Loose ends

- `SPEC-feed.md` (root) — design doc for what got built. Currently untracked. Either commit as repo history, move to a notes location, or delete since the implementation is in the templates now.
- `topost` (root) — Patrick's pre-existing untracked single-line ASCII file. **Do not touch.**
- `_drafts/` is not gitignored. Drafts committed in `329c85c`, `6baad4e`, `45dcc77`, `892e5c0`, `441b929`, `431fea6`, `d070f16`, `44f4653`. They're excluded from build by default (rebuild with `--drafts` to preview). Move to `_posts/<date>-<slug>.md` to publish.
- **Mythos draft has an opening quote, not a full body**. Patrick may add more later, or may consider that the whole post.
- **PyCon Cheese Must Stand draft has the booth-day photo as feature**; an on-stage shot would probably be better if Patrick has one.
- **PyTorch Beyond Zero draft uses Chainguard Academy as the recording host** (it's not on standalone YouTube). If Patrick finds a direct YouTube link, swap it into the `embed:` field for inline playback.

## Pipeline aspiration — also parked

Patrick mentioned a "scan LI and put stuff in a pipeline for me" need — frustration that updates are janky and don't go out, wanting one source of truth for activity across surfaces. Deferred consciously this round. Worth picking up after smythp is in better shape.

## Process notes for the next session

- **Roles**: codex on Jekyll templating / structural code, Patrick writes the prose, agent (you) preps links + research + frontmatter scaffolding. Crossing those streams creates friction.
- **No AskUserQuestion form tool**: Patrick prefers questions in plain text in the message body.
- **Plain text for structured data**: Patrick uses a screen reader some of the time. No tables, no markdown columns. One item per line.
- **Don't editorialize**: Fill placeholders, surface material, don't write his voice.
- **Spin, don't DIY** for non-trivial code. Patrick called this out repeatedly: "implementation is for young bucks." Spec the work, spin codex (or CC), fell-r1, fix, fell-r2, merge. The fell discipline is real — "we take our fell seriously in this house."
- **When stuck on a visual issue, USE THE BROWSER**. Patrick has Chrome MCP perms granted on `127.0.0.1:4000`. The pattern that worked: `bundle exec jekyll serve --port 4000 --host 127.0.0.1 --drafts --watch &` then navigate via `mcp__claude-in-chrome__navigate` and inspect with `javascript_tool`. Screenshots can hang on heavy pages — `javascript_tool` for state inspection is more reliable.
- **Patrick's logic exists; use it before inventing**: `_includes/projects.html` has count-mod-2 grid logic for the orphan-card problem. `_sass/main.scss` has `.contain-img img` (logos, object-fit: contain) and `.cover-img img` (photos, object-fit: cover) at 15rem height. Don't add inline `aspect-ratio` / `object-fit` styles; use the existing classes.
- **The blog repo isn't fully SKEIN-initialized**: only `.skein/shards.db` exists. SKEIN folio commands (`brief`, `tender`, etc.) won't work without an initialized site. Use this `HANDOFF.md` file as the persistent successor doc until that's set up.
- **Trust Patrick's aliases**: `clip` is `xsel --clipboard` (input-side via pipe). When he says "pipe to clip," do it; don't second-guess.

## Adjacent work that landed this session (not blog-related, but context for the next agent)

- **strongbox** at `~/projects/strongbox` — drop-in cache wrapper for `op inject`/`op read`. Public on github.com/smythp. v1 merged on master. v2 manifest layer was kicked off this session (a codex spool; check `spool` for status if still incomplete).
- **kagi-wrapper** at `~/projects/kagi-wrapper` — CLI for the Kagi APIs. Private on github.com/smythp. v1 merged on master.
- **op CLI installed**, 1Password desktop app integration enabled. The `kagi.com` 1Password entry now has an `api_key` concealed field; reference is `op://Private/kagi.com/api_key`.
- The full chain works silently: `strongbox read op://Private/kagi.com/api_key` → cached in tmpfs → `kagi search "..."` returns JSON. No prompts after first cold cache.

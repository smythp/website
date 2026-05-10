# Handoff — smythp.com / blog repo

Successor brief from the session that wired up the post feed (commits `0a9fc8d` through `329c85c` on master, May 8-9 2026). Read this before starting work.

## Critical: title is wrong everywhere

Patrick was promoted to **Principal Developer Relations Engineer** in October 2025. The site still says "Staff DevRel Engineer." Three places to fix:

- `about.md` line 7 — "Staff Developer Relations Engineer" in the bio paragraph
- `_projects/chainguard.md` line 5 — `name: Staff DevRel Engineer at Chainguard`
- `_projects/chainguard.md` line 7 — `role: Staff Developer Relations Engineer`
- `_projects/chainguard.md` line 17 — body prose "Patrick is Staff Developer Relations Engineer"

These are one-character / one-line edits. Do them in a single commit before anything else; the wrong title is the most embarrassing thing on the live site.

## CV is stale

`cv.md` (rendered at `/cv/`) ends with Patrick's pre-2022 academic / Iota positions. Zero Chainguard. Needs:

- **Principal Developer Relations Engineer**, Chainguard, October 2025 — present
- **Staff Developer Relations Engineer**, Chainguard, [start date — Patrick to confirm, somewhere in 2023 or 2024] — October 2025
- New publications / talks since 2022 — PyCon US 2025 (Cheese Must Stand), RSAC 2026 (Securing ML Pipelines), PyTorch Conference 2024 (Beyond Zero), AI Native Dev Conference, Chainguard Assemble 2025 + 2026, plus Chainguard Unchained blog posts (Mythos, ML pipeline maturity gap, AI-assisted attacks, etc.)
- The full list of LI-pointer events is in `~/li/my_posts/*.md` — see the curated 20 in this brief's "Posts pipeline" section

The CV is a real piece of work, not a one-liner. Patrick will need to pair on the actual content; agent's job is to surface candidate material from his LI feed and propose structure. Working source files are in `_cv/` (cv.md, cv.tex, cv.org, cv.pdf, etc. — derivative outputs); the live source the site renders from is the root `cv.md`.

## Other stale lines on the site

- `about.md` last paragraph: "hanging out with his six-month-old baby." Lily appears throughout the family pages on `~/projects/server-www/www/` (dccccc.cc) and is clearly older now. Patrick to update.

## dccccc.cc — never started, parked from earlier session

Patrick's scrappy/jank personal site. Source is `~/projects/server-www/www/`. Live `index.html` is one line: "This is a website on the internet."

What he signaled he wanted (March-May 2026 conversation):

- Keep the jank energy. "I kinda like the jank. this is corpo Patrick" — referring to smythp. dccccc is the personal-but-public dump.
- Add an index page in the same shitty inline-style HTML that lists all the existing weird stuff — already there: `lily_birthday.html`, `gifts.html`, `officehours.html`, `boris.html`, `lily_two.html`, `baby_it_dances_yo.gif`, `edit_bios.gif`, `ass.ics`, `balls_of_it.txt`, `grammo.txt`, `peeking.png`, `swing.png`, `yoga.png`, `lily_wants_you.png`, `nonsense/` (snuff order page + CSV), `org/` (tarotconnection.net stuff), `archive/`.
- Dump new weird shit from his recent fun-coded projects. Candidates from his ecosystem: `slub` (foreign-text chunk dropper), `tome` (audio kv store), `ko` (clipboard TTS), `cards` (tarot scraper, fits the existing `org/` tarot vibe), `pitch` (daily seed scanner), `snuffs-buy` (snuff catalog, fits `nonsense/`), `timevault` (Wayback resurrector), `anki` (poetry memorization deck generator), `shelf` (fiction reading DB), `pantry` (household ordering CLI), plus old gifs / scratch HTML / random text dumps.

Hosting/deploy target needs confirming — presumed `~/projects/server-www/www/` deploys to dccccc.cc but verify before changes go live.

## Posts pipeline — 3 of 20 drafted, 17 to go

**Drafted in `_drafts/`** (committed `329c85c`, ready for Patrick to write the body prose):

- `2026-03-23-advisory-feeds-with-konstantinos.md` — Myths of Advisory Feeds (Assemble 2026)
- `2026-03-27-rsac-ml-pipelines.md` — Securing ML Pipelines (RSAC 2026 workshop)
- `2026-05-05-supply-chain-attack-takeaways-webinar.md` — Takeaways from Major Software Supply Chain Attacks (Chainguard webinar)

**Tier A still to draft** — career-defining / high-engagement:

- Promoted to Principal Developer Relations Engineer (2025-10-01, 162 reactions) — short personal post; LI text already says it cleanly
- Anthropic's Mythos blog post (2026-04-27, 45 reactions) — Chainguard Unchained piece; steal summary from the blog
- Chainguard Vibelympics (Oct-Dec 2025) — Patrick organized, wrote a Dec 30 recap; that recap IS the source
- PyCon US 2025: Cheese Must Stand (May-Jun 2025) — Python library ecosystem talk; abstract from PyCon program
- Chainguard Assemble 2025 inaugural breakout (Feb-Apr 2025) — multiple LI posts trace the arc, talk recording dropped April
- Chainguard Assemble 2026 NYC — Manfred Moser talk on Chainguard Libraries (separate from the Konstantinos one already drafted; the 2026-03-16 preview post mentioned both)
- PyTorch Conference 2024: Beyond Zero (Jun-Sep-Oct 2024) — submission, presentation, recap arc; recording probably exists

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

**Curation rule learned the hard way**: filter LI URL by author. `linkedin.com/posts/smythp_*` and `linkedin.com/posts/iotaschool_*` = Patrick's own posts. Everything else (e.g. `linkedin.com/posts/adrianmouat_*`, `linkedin.com/posts/imjasonh_*`, `linkedin.com/posts/manfredmoser_*`) is a repost — drop. Three picks were dropped this round (Rejekts, Shai-Hulud, Linux Foundation throwaway) for this reason.

**Pairing pattern that worked this round**:

1. Agent reads source LI post body, fetches event page / GitHub / recording URL
2. Agent stages `_drafts/<date>-<slug>.md` with frontmatter wired (title, subtitle, image, embed, resources) and a SHORT placeholder body
3. Patrick writes the actual prose
4. **NO LLM-written summaries, no editorialized prose**. Codex auto-generated summaries on the existing 2025 posts; that was a misstep. "Way More Than You Wanted to Know" got "a wink at the runtime" from me — Patrick's reaction: "i dont' want the fucking wink stuff." When Patrick leaves a `TITLE: SUBTITLE` placeholder, fill the actual title. Don't add commentary.

## Site work — broader directions signaled, never finished

- **Project list refresh**: current `_projects/` is all 2018 DH-era (chainguard, dh_box, dri_curriculum, eloud, foundations, iota, neh, stsci, negotiated_access). The whole AI-infra body of work is invisible — tine, spiritengine, skein, spindle, mill, horizon, shuttle, claudio, slub, prism, fathom, etc. Patrick wants framing as "DevRel with academic DNA, does a lot of good shit and stuff with AI." Tagline ("Teacher / Coder / Writer") he said he'd think about. Two tangled questions: which AI projects make the cut, and what happens to DH-era ones (drop / demote to "earlier work" tail / keep mixed).
- **Push to live cadence**: master is 10 commits ahead of `origin/master` after this session. Nothing pushed. We never agreed when to ship publicly. Suggested: after Principal title fix lands and 3-5 substantive posts are out of drafts.
- **/posts/ index** shows 2015-2017 DH posts mixed with 2025+ stuff. May want to demote, year-section, or hide-by-default. Cosmetic.

## Image gaps

`scripts/fetch_post_media.py` pulls native LI image attachments (Unipile API). Of the 15 audited tier A/B candidates, only 4 had native images (slopsquatting, RSAC, AI Native Dev, PyTorch presentation). The rest need pictures from Patrick or another source. He said: "we need images i think. maybe do some best effort, dont' stretch, and i'll help with misses (on images)."

When Patrick provides a pic from `~/Pictures/`, copy to `assets/images/posts/<slug>.png` (or .jpg). Wire into draft frontmatter as `image: { feature: posts/<slug>.png }`. The `cover-img` class on cards (15rem height, `object-fit: cover`) handles the crop.

## Loose ends from this session

- `SPEC-feed.md` (root) — design doc for what got built. Currently untracked. Either commit as repo history, move to a notes location, or delete since the implementation is in the templates now.
- ~70 unused LI post images sitting untracked in `assets/images/posts/`. Patrick's call: `.gitignore` the dir to keep working tree clean, or git-add only as posts go live (current pattern).
- `topost` (root) — Patrick's pre-existing untracked single-line ASCII file. **Do not touch.**
- `_drafts/` is not gitignored. Three drafts committed in `329c85c`. Future drafts go here too; they're excluded from build by default (rebuild with `--drafts` to preview). Move to `_posts/<date>-<slug>.md` to publish.

## Pipeline aspiration — also parked

Patrick mentioned a "scan LI and put stuff in a pipeline for me" need — frustration that updates are janky and don't go out, wanting one source of truth for activity across surfaces. Deferred consciously this round. Worth picking up after smythp is in better shape, but it's a real DX problem he flagged.

## Process notes for the next session

- **Roles**: codex on Jekyll templating / structural code, Patrick writes the prose, agent (you) preps links + research + frontmatter scaffolding. Crossing those streams creates friction.
- **No AskUserQuestion form tool**: Patrick prefers questions in plain text in the message body.
- **Plain text for structured data**: Patrick uses a screen reader some of the time. No tables, no markdown columns. One item per line.
- **Don't editorialize**: Fill placeholders, surface material, don't write his voice.
- **When stuck on a visual issue, USE THE BROWSER**. Patrick has Chrome MCP perms granted on `127.0.0.1:4000`. The pattern that worked: `bundle exec jekyll serve --port 4000 --host 127.0.0.1 --drafts --watch &` then navigate via `mcp__claude-in-chrome__navigate` and inspect with `javascript_tool`. Screenshots can hang on heavy pages — `javascript_tool` for state inspection is more reliable.
- **Patrick's logic exists; use it before inventing**: `_includes/projects.html` has count-mod-2 grid logic for the orphan-card problem. `_sass/main.scss` has `.contain-img img` (logos, object-fit: contain) and `.cover-img img` (photos, object-fit: cover) at 15rem height. Don't add inline `aspect-ratio` / `object-fit` styles; use the existing classes.
- **The blog repo isn't fully SKEIN-initialized**: only `.skein/shards.db` exists. SKEIN folio commands (`brief`, `tender`, etc.) won't work without an initialized site. Use this `HANDOFF.md` file as the persistent successor doc until that's set up.

Server may still be running on PID 1674681 (`bundle exec jekyll serve --port 4000 --host 127.0.0.1 --drafts --watch`). Kill it before starting if you don't need it.

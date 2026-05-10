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

**HEADS UP — push doesn't auto-deploy.** During the May 10 session we pushed master to `origin` (`github.com/smythp/website`), but **`smythp.com` did not update**. The live site is fronted by Netlify (server header confirms), and the Netlify → repo hookup is not obvious from inside this repo — there's no `netlify.toml`, no `_redirects`, and no GitHub action wired up. Possibilities to investigate next session:

- Netlify is connected to a different repo or branch entirely (check the Netlify dashboard)
- A build hook exists but is broken / unauthenticated
- There's a manual deploy step we're missing (e.g. `netlify deploy --prod`)

GitHub Pages is also configured on the repo (serves at `https://smythp.github.io/website/`, builds from `master`, last build succeeded), but that's NOT the production `smythp.com`. Pushing the repo updates the GitHub Pages copy but not Netlify-fronted smythp.com.

For the next agent: figure out the Netlify deploy path, document it here, and ideally wire up an auto-deploy from `master` if it isn't already.

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
- **The blog repo IS skein-init'd** (project `blog`, site `blog-feed`). Folio commands work. The original handoff note saying it wasn't init'd was stale by the time the May 10 session ran. This `HANDOFF.md` file is still the persistent successor doc since multi-section briefs are awkward to fit in folio form, but you can also file `friction`/`brief`/`finding` folios on the `blog-feed` site.
- **Trust Patrick's aliases**: `clip` is `xsel --clipboard` (input-side via pipe). When he says "pipe to clip," do it; don't second-guess.

## Adjacent work that landed this session (not blog-related, but context for the next agent)

- **strongbox** at `~/projects/strongbox` — drop-in cache wrapper for `op inject`/`op read`. Public on github.com/smythp/strongbox. v1 + v2 manifest layer + expanded README all merged and pushed.
- **kagi-wrapper** at `~/projects/kagi-wrapper` — CLI for the Kagi APIs. Private on github.com/smythp/kagi-wrapper. v1 merged + pushed.
- **op CLI installed**, 1Password desktop app integration enabled. The `kagi.com` 1Password entry now has an `api_key` concealed field; reference is `op://Private/kagi.com/api_key`.
- The full chain works silently: `strongbox read op://Private/kagi.com/api_key` → cached in tmpfs → `kagi search "..."` returns JSON. No prompts after first cold cache.
- **`kagi-load` shell function** is in `~/.zshrc`. It's redundant with the v2 manifest path (`eval $(strongbox load kagi)`) but the manifest file isn't created yet, so the function is the working path. Cleanup pending: write `~/.config/strongbox/manifest.toml`, replace the function with the eval form.

## Hinky items / frictions noted this session

- **Codex shard-review permission profile blocks `python -m unittest`** consistently. Every fell-r* review came back with static-analysis-only verdicts because the harness couldn't get bash approval to run tests. Workaround: run the test suite from the main session before merge. Worth filing as a Spindle friction — the read-review profile probably needs `python -m unittest` whitelisted.
- **Skein-not-init'd projects break `skein shard tender`**. Both kagi-wrapper and strongbox were created via spindle's shard mode, which deposits a `.skein/shards.db` but doesn't register the project in `~/.skein/projects.json`. This makes `tender` fail with "No project specified." Workaround used: stash `.skein/shards.db` aside, run `skein init --project NAME`, restore the shards.db. Worth fixing in spindle so shard creation auto-inits the project, or documenting the manual workaround in CLAUDE.md.
- **`BRIEF.md` and `reference/sheet.py` are in strongbox's repo root**, visible in the public GitHub repo. They were build-time artifacts (the brief, the reference code from the auth section of speakbot's `sheet.py`). Could be moved to a `notes/` or `docs/internal/` dir, or deleted entirely. Cosmetic but worth a pass.
- **Codex's intermediate process traces are very large** when unspooled — repeatedly hit the response-size cap and had to be tail-grepped from disk. Not a bug, just a workflow note: codex spools should be unspooled with `tail -c` if you only want the final summary.
- **Strongbox's `STRONGBOX_OP_TIMEOUT=0` semantics**: 0 means "no timeout" (matches `STRONGBOX_TTL=0` disabling expiry). Documented in README, tested. Patrick may or may not want to standardize this convention across other env-var-driven settings.

## Big-idea notes

- **Strongbox is the template for every future API-key-handling tool.** The pattern: tool reads `$ENV_VAR` at runtime; documentation includes the `op://...` reference and a `[keys.NAME]` manifest snippet. Tools never know about op, 1Password, vault paths. Backend can change without touching any tool.
- **The fell discipline justified itself this session.** Three full fell cycles (kagi-wrapper, strongbox v1, strongbox v2). Each fell-r1 caught real polish items the implementation pass missed. The "ready to merge" verdicts came after 1-2 round-trips, not the first review.
- **Codex builds + CC reviews is a productive pairing.** Cross-perspective; mix-and-match harnesses.
- **End-to-end smoke testing is high-leverage.** "Type a command, watch it work silently" >> "all unit tests pass" for confidence in infra. The op-install → 1Password-integration → manifest → smoke chain transformed strongbox from "tested" to "trusted."
- **Mode-shifting between codebases works.** Blog DIY (research+prose), strongbox/kagi spin-driven (code+tests). The work modes were distinct enough that switching didn't cost much.

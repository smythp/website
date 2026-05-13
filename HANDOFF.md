# Handoff — smythp.com / blog repo

Successor brief at the end of the May 11 2026 session (blip-0511). This session continued from the May 10-11 CV-refresh session (handoff was `brief-20260511-o0x3`). Read this before starting work.

## State at handoff

- **smythp.com is live and current.** Netlify-hosted, fed from `origin/master` via auto-deploy. `git push origin master` triggers Netlify build and prod deploy in ~1 min.
- **`master` matches `origin/master` at `e1a5536`** (the `/talks/` index page). One additional commit sits locally at `58f4521` (dead-link audit script + report) — not pushed yet; awaits Patrick's call.
- **Working tree clean** apart from the local-only commit above. `topost` is gitignored.
- **Jekyll exclude list now also covers `reports/`** so any future audit artifacts stay out of the rendered site.

## What landed this session

Live on smythp.com:

- **`/talks/` index page**. Filters `site.posts` by `type ∈ {talk, workshop, webinar}` and renders as the existing `.card-grid`. 17 posts got a new `type:` frontmatter field (talk × 5, workshop × 1, webinar × 1, event × 1, blog × 9). Nav order is now About → Talks → CV → Contact. Vibelympics is tagged `event` (off /talks/, it's a hosting recap not a speaking gig). Boston CSA wasn't in the original brief's tagging list but was tagged `talk` based on its title ("Spoke at Cloud Security Alliance Boston Chapter").
- **Nothing else** — the rest of this session was tooling and triage.

Local-only (not pushed):

- **`scripts/check_dead_links.py`** — rerunnable site-wide external link audit. Handles LinkedIn (200 + deletion banner detection) and YouTube (oembed) as special cases since both return 200 for unavailable content. 16 workers; ~30s for the current 188 URLs.
- **`reports/dead-links-2026-05-11.md`** — baseline audit. 20 DEAD / 34 REDIRECTED / 25 UNCERTAIN / 109 ALIVE.

In SKEIN:

- **`finding-20260511-g2lv`** — dead-link audit triage notes. Six items worth attention; the rest is old DH-era cruft.
- **`brief-20260511-uf2m`** — pair-handoff brief for the dead-link triage resume state. Read before resuming the link work.
- **New site `angelus`** with six kickoff briefs (see below). Net-new initiative; doesn't depend on anything in blog-feed.

## Open briefs (`blog-feed` site)

Unchanged from prior handoff except:

- **`brief-20260511-fvv9`** (`/talks/` index page) — **DONE** this session, close on next torch.
- **`brief-20260511-u7gc`** (dead-link audit) — **partially done**. Script and baseline shipped; **triage is mid-flight** (see pair-handoff brief for resume state). Don't close until link dispositions are decided.

Remaining open:

- `brief-20260511-8xvi` — CV refresh (mostly done last session; some sub-briefs filed)
- `brief-20260511-m0yh` — Refresh `_projects/` (pair-required)
- `brief-20260511-7n78` — Auto-stage LI posts into `_drafts/`
- `brief-20260511-o254` — Archive external pages and videos (now usefully unblocked by the dead-link report — the DEAD list is the input)
- `brief-20260511-1hwc` — City College data science classes for CV
- `brief-20260511-14l6` — Workshops Taught expansion for CV

## New initiative: `angelus`

Net-new SKEIN site for an autonomous-agent reliability layer. Patrick activated on this because iotaschool.com going down was caught only by a manual run of the dead-link script — exactly the kind of thing a scheduled job should have caught.

Vocabulary: **Angelus** (system) → **peal** (consolidated daily digest of routine output) → **strike** (single immediate emergency push). Working terms: **round** (a single scheduled job), **ringer** (the trigger mechanism — cron, email, state change).

Six kickoff briefs in the `angelus` site:

- `brief-20260511-unaw` — Architecture and vocabulary spec (north star)
- `brief-20260511-bkxr` — Trigger system (cron + email-to-patbot + state)
- `brief-20260511-3tb3` — Peal pipeline (digest consolidation + delivery)
- `brief-20260511-7nrm` — Strike pipeline (emergency dispatch, dedup, rate-limit)
- `brief-20260511-e701` — Reliability (three-layer watchdog: per-round expected-fire tracking, external healthchecks.io heartbeat, raw-cron fallback)
- `brief-20260511-9gk5` — Kickoff rounds (six concrete jobs, including a 3-URL liveness watch as first-milestone)

Angelus lives in SKEIN only right now — no `~/projects/angelus/` exists yet. Patrick is pairing on next steps.

## Where to start next session

If Patrick is pairing on links: read `finding-20260511-g2lv` + the dead-link pair-handoff brief, resume triage. The Gemini spool `gemini-2cb230a0` (Chainguard Assemble URL research) may have results pending — check with `unspool gemini-2cb230a0`.

If Patrick is starting Angelus implementation: read `brief-20260511-unaw` first (architecture / vocabulary), then the trigger and reliability briefs. The first concrete milestone is the 3-URL liveness round, which proves trigger → check → finding → peal/strike → delivered.

Other open briefs (projects refresh, auto-stage LI, archive external, CV class/workshop gaps) are unchanged from prior handoff.

## Deploy / Netlify (quick reference)

- Site `smythp`, ID `48e9737e-86d0-4a1d-936f-0d52f050f0ea`, account "Patrick Smyth's team", login `patricksmyth01@gmail.com`.
- Repo `github.com/smythp/website`, branch `master`. Push triggers build.
- DNS legacy: apex `104.198.14.52` (legacy Netlify GCP), `www` CNAME `smythp.netlify.com`. Resolves fine.
- For draft preview without affecting prod: `source ~/.nvm/nvm.sh && nvm use 20 && netlify deploy --dir=_site --no-build`.
- Netlify CLI v26 auth quirk: if `netlify status` says "Not logged in" after a successful `netlify login`, delete `~/.config/netlify/config.json` and re-run `netlify login`.

## Process notes

- **Don't run `deploy.sh` with untracked files dirty in the blog repo** — `git add -A` will scoop them up under "Automatic push." `.claude/`, `topost`, and now `reports/` are protected (gitignored or Jekyll-excluded).
- **CV: `_cv/cv.org` is canonical.** Don't hand-edit `blog/cv.md` directly. The pipeline (`_cv/update.sh` → `deploy.sh`) regenerates it. See the "CV update flow" section of `playbook-20260510-bsbt`.
- **Two-page CV is deleted.** All `_cv/two_page.*` files and `_cv/two-page.docx` were removed this session (Patrick's call). The compact-CV variant is no longer maintained.
- **Patrick uses a screen reader** some of the time. Plain text for structured output; no tables or markdown columns in agent communications.
- **Don't use emojis** unless asked.

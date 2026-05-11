# Handoff — smythp.com / blog repo

Successor brief at the end of the May 10-11 2026 session (mismatched-socks-collective-0510). Read this before starting work.

## State at handoff

- **smythp.com is live and current.** Netlify-hosted, fed from `origin/master` via auto-deploy. `git push origin master` triggers Netlify build and prod deploy in ~1 min — no manual `netlify deploy --prod` needed for normal changes.
- **Git is clean.** `master` matches `origin/master` at `7978c63` (`.claude/` gitignore commit). Only untracked file is `topost` (Patrick's scratch — do NOT touch).
- **Ruby is pinned** via `.ruby-version` to `3.0.2`. Auto-build succeeds against the existing Jekyll 4.2.1 + bundler 2.3.7 stack.
- **`worktrees/` directory is gone** (cleaned up). `SPEC-feed.md` is gone. `.claude/` is gitignored.

## Open briefs (all in `blog-feed` site)

These are the units of work the next agent (or several agents) could pick up. Each is fully spec'd; no preamble needed.

- `brief-20260511-8xvi` — **CV refresh** for 2022 → present. Big job. Points at `~/projects/automate-linkedin` as the data source. Patrick pairs on prose; agent surfaces candidate material + proposes structure. **An agent is already working on this one** per Patrick's "kicked off the new guy" message; coordinate before overlapping.
- `brief-20260511-m0yh` — **Refresh `_projects/`** — surface the AI infra body of work (tine et al). Demote DH-era to "Past Projects." Pair-required (selection is subjective).
- `brief-20260511-fvv9` — **`/talks/` index page**. Tag posts by type (`talk` / `workshop` / `webinar` / `event` / `blog`), build a talks-only listing, add to nav.
- `brief-20260511-7n78` — **Auto-stage new LI posts into `_drafts/`** from automate-linkedin's SQLite. Reduces per-post boilerplate to near-zero; Patrick still gates publication.
- `brief-20260511-u7gc` — **Dead link audit** across smythp.com. LI and YouTube need special-case detection (200-but-deleted is a thing on both).
- `brief-20260511-o254` — **Archive external pages and videos** linked from smythp.com. Wayback + archive.ph + local yt-dlp for videos. Keeps the blog useful as the web rots.

## Reference folios (also in `blog-feed`)

- `playbook-20260510-bsbt` — Blog post workflow playbook. **Read this first** before doing any post work. Covers resource link rule, image preferences, Unsplash gotchas, embed wiring, deploy workflow, browser-driven verification, code change discipline, archeology principle, dev server setup.
- `finding-20260510-3jdl` — Original a11y audit (11 items; most fixed and merged).
- `finding-20260511-m4tr` — r1 review of the a11y fix shard (fell-clean verdict).
- `tender-20260511-17hw` — A11y shard tender summary (merged at commit `6d85feb`).

## What landed this session (May 10-11)

Live on smythp.com:

- **Content**: Mythos post got a real (free-Unsplash) header image, replaced lnkd.in shortlink with goldcast URL on supply-chain webinar, dropped third-party/non-Patrick links from Mythos resources per the cleaner rule, the title fix Staff → Principal is finally visible (was stuck behind broken Netlify auto-build for weeks), `about.md` markdown links render correctly (preexisting `<p>`-wrap bug that suppressed Kramdown was fixed by dropping the wrappers).
- **A11y batch** (codex shard, fell-clean reviewed): skip link + `<main>` + `<footer>` landmarks, nav `aria-current="page"` conditional, project page + project card alt text using `project.name`, iframe titles on YouTube embeds, post-card dual-link collapse to single stretched-link, visually-hidden context spans on Read More / Project Link, `</h5>` → `</h3>` mismatched closer fix in projects, contact email moved from misused `<blockquote>` to `<address>`. Eight commits, all merged at `6d85feb`.
- **Card-grid layout rewrite**: Bootstrap row-cols + count-mod-2 hack replaced with a `.card-grid` flex container. `< 1280px` viewport: 1 col. `>= 1280px`: 3 col with last-row stretch (no widow gap). No 2-col band. Threshold 1280 picked so iPad landscape (1024) stays 1-col, only real-laptop widths get 3-col with cards at ~330px+ wide. Applied across home (Recent posts, Current/Past projects) and /posts and /projects.
- **Project card body reordered**: image → title → description → buttons (was image → buttons → title → description, which sat Read More tight against the heading).
- **Front-page CTA**: "More posts →" plain link became full-width `btn btn-outline-primary` below the recent-posts grid.
- **`/posts/` header spacing**: `mb-5` on the h1.
- **Blockquote CSS**: site-wide `blockquote` rule in `_sass/main.scss` (left rule, indent, italic, muted color) so Kramdown's bare `<blockquote>` renders properly.

Deploy infrastructure:

- **`.ruby-version` pinned**, auto-builds work end-to-end after 18+ months of broken Netlify builds.
- **Internal docs excluded from Jekyll build** via `_config.yml` (HANDOFF, README, SPEC-feed, scripts/, deploy.sh, Gemfile, Gemfile.lock). Before, they were rendered as public pages.

Process / docs:

- **Playbook polished** through three iterations — removed shopping-list flavor, added end-to-end "drafting a new post" recipe, viewport sizes reference, why-flex-not-CSS-Grid-auto-fit reasoning, dev server one-liner, "archeology before reimplementing" section, "spool output too large" handling.
- **Three new briefs filed today** (talks index, auto-stage LI, dead link audit, archive external content, projects refresh). The CV brief was filed earlier in the session and is already being worked.

## Where to start next session

1. **Read `playbook-20260510-bsbt`** in `blog-feed`. It's the workflow doc.
2. **Check what the CV agent did** — see `skein shard triage` for in-flight shards; check `brief-20260511-8xvi` for any updates.
3. **Pick a brief** based on what Patrick wants prioritized. Roughly in difficulty / pairing-intensity order:
   - Talks index (`fvv9`) — mostly mechanical, needs Patrick confirms on tagging and nav position
   - Auto-stage LI (`7n78`) — scripting work, needs Patrick to pair on title heuristics
   - Dead link audit (`u7gc`) — one-shot script + Patrick triages results
   - Archive external content (`o254`) — depends on dead-link enumeration, otherwise independent
   - Projects refresh (`m0yh`) — selection is subjective, real pairing required
   - CV refresh (`8xvi`) — biggest, ongoing

## Deploy / Netlify (quick reference)

- Site `smythp`, ID `48e9737e-86d0-4a1d-936f-0d52f050f0ea`, account "Patrick Smyth's team", login `patricksmyth01@gmail.com`.
- Repo `github.com/smythp/website`, branch `master`. Push triggers build.
- DNS legacy: apex `104.198.14.52` (legacy Netlify GCP), `www` CNAME `smythp.netlify.com`. Resolves fine.
- For draft preview without affecting prod: `source ~/.nvm/nvm.sh && nvm use 20 && netlify deploy --dir=_site --no-build`.
- Netlify CLI v26 auth quirk: if `netlify status` says "Not logged in" after a successful `netlify login`, delete `~/.config/netlify/config.json` and re-run `netlify login`.

## Other notes

- **dccccc.cc** — Patrick will tinker on this directly in emacs, no brief. Loose / personal site, separate codebase (`~/projects/server-www/www/`).
- **Posts pipeline** — 8 posts published, ~11 candidates still to draft (list lives in `~/li/my_posts/`). Auto-stage brief (`7n78`) would mechanize most of the per-post setup.
- **Patrick uses a screen reader** some of the time. Real-stakes accessibility — see playbook.
- **Patrick writes prose**, agents stage frontmatter + factual scaffolding. No LLM-written summaries, no editorialized voice. "No wink stuff."

# Handoff — smythp.com / blog repo

Successor brief at the end of the May 10-11 2026 session (mismatched-socks-collective-0510). Read this before starting work.

## State at handoff

- **smythp.com is live and current.** Netlify-hosted, fed from `origin/master`. Patrick verified visually.
- **Git**: clean. `master` matches `origin/master`. Most recent commits: `cbf9fe1` (.ruby-version pin), `9768bb3` (card-grid layout), `d1ac09f` (a11y + UX), `e496d82` (mythos image + resource cleanup).
- **Untracked (intentional)**: `SPEC-feed.md` (loose end), `topost` (Patrick's scratch — do NOT touch), `.claude/` (CC local).
- **A11y fix batch** is in flight on a codex shard (spool `codex-7e7ef944`) at end of session; fell cycle started but not necessarily completed by next session. Check `skein shard triage` first thing.

## What landed this session (May 10-11)

Live now:

- **Mythos post image** — free-Unsplash photo (NLSXFjl_nhc) at `assets/images/posts/mythos-zero-days.jpg`. Picked over Chainguard's title card to avoid recycling CG's branded design.
- **Resource link rule applied** — Mythos resources cleaned (dropped Anthropic Mythos Preview, Help Net Security, The Hacker News — all third-party content not Patrick's own work and not actively promoting). See playbook for the rule.
- **Supply chain webinar URL fix** — replaced LI `lnkd.in/eJGvCTJJ` shortlink with real goldcast registration URL.
- **Blockquote CSS** — Kramdown emits bare `<blockquote>` (no class), Bootstrap's `.blockquote` styling never applied. Added a global `blockquote` rule in `_sass/main.scss` (left rule, indent, italic, muted color). Markdown `> ...` now renders correctly.
- **`about.md` markdown fix** — removed raw `<p>` wrappers that were preventing Kramdown from rendering `[link](url)` syntax. Was rendering as literal text on `/about` for a long time (preexisting bug across both GH Pages and Netlify).
- **A11y alt-text fixes** — `_layouts/post.html` and `index.html` had `alt="Bootstrap Themes"` (Bootstrap example placeholder). Real screen-reader regression. Replaced with descriptive alt. NOTE: a third instance was caught later by the a11y audit at `_layouts/project.html:10` — fix in flight on the codex shard.
- **Front-page `/posts` CTA** — converted "More posts →" plain link into a full-width `btn btn-outline-primary` below the recent-posts grid.
- **`/posts` header spacing** — added `mb-5` to the h1 for breathing room above the cards.
- **Card-grid layout rewrite** — the May 9 work copied a row-cols + count-mod-2 pattern from a 4-year-old projects.html. Pattern was single-breakpoint, never responsive, and crammed 3 cards per row on phones. Replaced across all three grids (home recent posts, home current/past projects, /posts, /projects) with a single `.card-grid` flex container. `< 1280px` → 1 col, `>= 1280px` → 3 col with last-row stretch (no widow gap). No 2-col band. Threshold 1280 = Bootstrap `xl`, keeps iPad landscape (1024) at 1 col, gives 3-col cards 330px+ to breathe on real-laptop widths.
- **`.ruby-version` pinned to 3.0.2** — Netlify auto-builds had been failing since June 2024 because no Ruby was pinned and Netlify's default Ruby moved past what the Jekyll 4.2.1 + bundler 2.3.7 lockfile combo can handle. Pin matches Patrick's local. **As of end-of-session: auto-build of `cbf9fe1` was in `building` state on Netlify; outcome not yet verified.** First check next session: did it succeed?

## Where to start next session

1. **Triage the codex a11y shard** (`skein shard triage`). If tendered, do a fell review of it (see "Fell cycle" below). If not tendered, check the spool: `unspool codex-7e7ef944`.
2. **Check the Netlify auto-build outcome**: `netlify api listSiteDeploys --data '{"site_id":"48e9737e-86d0-4a1d-936f-0d52f050f0ea"}' | head`. Looking for `cbf9fe1`'s state. If `ready` → auto-build is fixed, future git push deploys cleanly. If `error` → bump `.ruby-version` to 3.1.x or 3.2.x and re-test.
3. **CV refresh**: brief `brief-20260511-8xvi` in `blog-feed` site. Big job. Points at `~/projects/automate-linkedin` as the data source. Patrick needs to pair on prose; agent's job is to surface candidate material + propose structure.

## Open work (briefs and folios in `blog-feed` site)

- **`brief-20260511-8xvi`** — Refresh cv.md for 2022 → present (Chainguard era). Detailed: Principal/Staff dates, ~15 talks/articles to add, data source pointers, conventions for what NOT to do.
- **`finding-20260510-3jdl`** — Full a11y audit report. Some items already fixed; rest are in the codex shard.
- **`playbook-20260510-bsbt`** — Workflow doc for posts (resource link rule, image preferences, Unsplash gotchas, embed wiring, deploy workflow, browser-driven verification). Read this before doing post work.

## Still-unstarted work (not yet briefed, mentioned but not scheduled)

- **`_projects/` refresh** — current entries are all 2018-era DH stuff (chainguard, dh_box, dri_curriculum, eloud, foundations, iota, neh, stsci, negotiated_access). The AI infra body of work is invisible — tine, spiritengine, skein, spindle, mill, horizon, shuttle, claudio, slub, prism, fathom. Patrick wants framing: "DevRel with academic DNA, does a lot of good shit and stuff with AI." Tagline ("Teacher / Coder / Writer") he was going to think about. Two tangled questions: which AI projects make the cut, and what happens to DH-era ones (drop / demote to "earlier work" / keep mixed).
- **Posts pipeline — ~11 still to draft** (of the ~19 candidates curated from `~/li/my_posts/*.md`):
  - Tier A: Manfred Moser Chainguard Libraries talk — Assemble 2026 NYC (separate from the Advisory Feeds session already drafted)
  - Tier B: AI/ML Supply Chain Security course launch (Jul-Aug 2024), FrankenPipe — secure ML pipelines (Oct + Dec 2025), EKS Auto Mode with Sai Vennam (Aug 2025), Chainguard Libraries for Python launch (Oct 2025 – Jan 2026), AI Native Dev Conference (Dec 2025), Hard Truths series episode 1 (Feb 2026), ML pipeline maturity gap blog (2026-01-26), Zero CVEs / no-DSA Debian deep dive (2026-02-27)
  - Tier C: Pandas + NumFOCUS + Iota nonvisual data science workshop series (Jan-Mar 2024), Austin Kubernetes meetup talk (May 2024), AI-assisted attacks blog / Rakuten teens (2026-04-14)
- **Drafted posts that need Patrick prose** (factual placeholder text only):
  - Beyond Zero (PyTorch 2024) — short placeholder
  - Cheese Must Stand (PyCon 2025) — short placeholder
  - Advisory Feeds (Assemble 2026) — short placeholder
  - RSAC ML pipelines — short placeholder
  - Supply Chain webinar — Patrick has the opener but more would help
  - Mythos zero-days — opening quote + a paragraph; Patrick may consider this complete or may add more
- **Borderline resources to audit** in existing posts (per the cleaner "Patrick's stuff OR things Patrick promotes" rule):
  - Beyond Zero: "PyTorch Conference 2024 schedule" (conference site, not his)
  - Cheese Must Stand: "PyCon US 2025 program" (conference site, not his)
  - Old/New/Strange: "What to Expect at Assemble 2025" and "Key Takeaways from Assemble 2025" (CG marketing recaps, probably not Patrick's writing — confirm); "Assemble 2025 session playlist" (broader playlist, not his single talk)
  - Drop per Patrick's call, OR keep if he confirms otherwise.

## Smaller cleanup items (low priority)

- **Emacs backup files tracked**: `_layouts/post.html~`, `projects.md~`, `index.html~`, `.gitignore~`. Just delete + add `*~` to `.gitignore`.
- **`_drafts/#2025-10-01-principal-promotion.md#`** — stale emacs autosave (the promotion draft was dropped). Delete.
- **`/posts/` index DH-era mixing** — 2015-2017 DH posts show alongside 2025+ chronologically. Cosmetic. Consider year-sectioning or hide-by-default for older DH content.
- **`SPEC-feed.md`** at repo root — design doc from earlier session, untracked. Decide: commit / move to a notes location / delete.
- **Card images missing width/height** — flagged LOW by the a11y agent. Minor CLS-adjacent improvement, not urgent.

## Deploy / Netlify state

- **smythp.com is hosted on Netlify**, site ID `48e9737e-86d0-4a1d-936f-0d52f050f0ea`, name `smythp`, account "Patrick Smyth's team", login `patricksmyth01@gmail.com`.
- **DNS** is legacy: apex `104.198.14.52` (legacy Netlify GCP), `www` CNAME `smythp.netlify.com` (legacy Netlify subdomain). Still resolve fine. Modern alternative if ever needed: `apex-loadbalancer.netlify.com` for A records.
- **Netlify CLI** (`netlify-cli/26.0.1`) is installed globally via nvm. Needs node >= 20.12.2 — `source ~/.nvm/nvm.sh && nvm use 20` first if commands fail with `TypeError: Cannot redefine property: __internal__deprecationWarning`.
- **Auth quirk** in CLI v26: doesn't read `~/.config/netlify/config.json` for `netlify status` / `sites:list` even when login worked. If you see "Not logged in" after a successful login, delete the config and re-run `netlify login` for a clean OAuth flow.
- **Manual deploy workflow** (current state, auto-build verification pending):

```
source ~/.nvm/nvm.sh && nvm use 20
bundle exec jekyll build
netlify deploy --dir=_site --no-build --message "draft: <change>"  # draft URL for verify
netlify deploy --prod --dir=_site --no-build                       # promote
```

- If the auto-build of `cbf9fe1` succeeded on Netlify, you can skip the manual deploy and just `git push origin master` for future changes. Verify with `netlify api listSiteDeploys --data ...` first.

## Process patterns from this session

- **Browser-driven verification > guessing on layout/a11y.** Chrome MCP has `tabs_create_mcp`, `navigate`, `javascript_tool`, `resize_window`. Patrick can resize the window manually too — same browser instance is shared. Pattern that worked: navigate to draft URL, javascript_tool to query `window.innerWidth`, `matchMedia(...)`, `getBoundingClientRect()` on cards. Don't trust theoretical CSS analysis — test the actual computed style.
- **The fell discipline catches real things.** This session's a11y agent caught a third `Bootstrap Themes` placeholder I'd missed, the `aria-current` unconditional emission in nav, the `<h3>…</h5>` mismatched closer, and the dual-link cards problem — all things I'd have shipped without it. Worth spinning a review agent even on small batches.
- **Push back on agent claims that don't match reality.** The a11y agent flagged social icon labels as HIGH ("title attribute is unreliable"). Patrick's phone screen-reader announced them correctly. The audit's quote was misleading; reality on device matters more than theoretical worst-case.
- **Spindle shard for code changes** — isolated worktree, doesn't stomp on main. Use `skein shard triage` first to see what's outstanding, `skein shard merge <worktree>` when fell-clean.
- **Codex builds, CC reviews.** Patrick's preferred pairing. Codex's `5.5` model (gpt-5.5) for implementation; Claude `sonnet`/`opus` for review (especially with `tags="review"`, `permission="readonly"` or `"careful"`).
- **Kagi for web search fallback.** Default to WebSearch/WebFetch (free). `kagi search` when WebSearch falls down — most notably video search. Load with `export KAGI_KEY="$(strongbox read 'op://Private/kagi.com/api_key')"`. Costs money — don't reach reflexively.
- **No editorialized content from agents.** Agents stage frontmatter + factual scaffolding. Patrick writes prose. No "wink" voice. He was explicit.
- **No AI-generated images** on this personal blog, even for AI-topic posts.
- **No CG-branded title cards** recycled for his posts about Chainguard work — it retags their visual design as his.

## Useful skein folio references

- `playbook-20260510-bsbt` — Blog post workflow playbook
- `brief-20260511-8xvi` — CV refresh brief
- `finding-20260510-3jdl` — A11y audit findings
- (Spool) `codex-7e7ef944` — In-flight a11y fix batch

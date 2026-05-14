#!/usr/bin/env python3
"""Stage recent LinkedIn posts from ~/li/my_posts/ as Jekyll _drafts/.

Each LinkedIn post (markdown file with frontmatter) is converted into a
Jekyll draft scaffold. The script is idempotent: it skips LI posts already
represented in _posts/ (matched on LI activity ID) or _drafts/ (matched on
the li_id frontmatter field added by this script).

The generated draft is a starting point — title is a heuristic guess from the
first sentence, body is copied verbatim. Patrick reviews/edits in _drafts/
and manually promotes to _posts/ when ready.

Usage:
    python3 scripts/stage_li_drafts.py              # stage up to 10 newest
    python3 scripts/stage_li_drafts.py --limit 5
    python3 scripts/stage_li_drafts.py --dry-run    # preview without writing
"""

import argparse
import re
import sys
from pathlib import Path

BLOG_ROOT = Path(__file__).resolve().parent.parent
LI_DIR = Path.home() / "li" / "my_posts"
DRAFTS_DIR = BLOG_ROOT / "_drafts"
POSTS_DIR = BLOG_ROOT / "_posts"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)", re.DOTALL)
ACTIVITY_ID_RE = re.compile(r"urn:li:activity:(\d+)")
IMAGE_ID_RE = re.compile(r"posts/(\d+)\.(?:jpg|jpeg|png|webp)")


def parse_frontmatter(text):
    """Return (frontmatter_dict, body). Naive YAML — flat scalars only."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def _iter_md(directory):
    """Yield .md files, skipping hidden files like emacs lockfiles (.#name)."""
    if not directory.exists():
        return
    for f in directory.glob("*.md"):
        if f.name.startswith("."):
            continue
        yield f


def existing_li_ids():
    """LI activity IDs already represented in _posts/ or _drafts/."""
    ids = set()
    for f in _iter_md(POSTS_DIR):
        text = f.read_text()
        ids.update(ACTIVITY_ID_RE.findall(text))
        ids.update(IMAGE_ID_RE.findall(text))
    for f in _iter_md(DRAFTS_DIR):
        text = f.read_text()
        fm, _ = parse_frontmatter(text)
        if "li_id" in fm:
            ids.add(str(fm["li_id"]))
        ids.update(ACTIVITY_ID_RE.findall(text))
    return ids


def slugify(text, maxlen=50):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    if len(text) <= maxlen:
        return text
    truncated = text[:maxlen]
    last_dash = truncated.rfind("-")
    if last_dash > maxlen // 2:
        truncated = truncated[:last_dash]
    return truncated


def derive_title(body, maxlen=80):
    body = body.strip()
    first_line = body.split("\n", 1)[0].strip()
    # Prefer first line if it's a substantive header-style line under maxlen
    if 5 <= len(first_line) <= maxlen:
        return first_line.rstrip(".!?")
    # Otherwise pull first sentence
    m = re.search(r"(.+?[.!?])(\s|$)", body)
    sentence = m.group(1).strip() if m else first_line
    sentence = sentence.rstrip(".!?")
    if len(sentence) > maxlen:
        sentence = sentence[:maxlen].rsplit(" ", 1)[0]
    return sentence


def load_li_posts():
    """LI posts sorted newest first. Skips files without an id or with empty body."""
    posts = []
    if not LI_DIR.exists():
        return posts
    for f in sorted(LI_DIR.glob("*.md"), reverse=True):
        if f.name.startswith("."):
            continue
        text = f.read_text()
        fm, body = parse_frontmatter(text)
        if not fm.get("id"):
            continue
        if not body.strip():
            continue
        posts.append((f, fm, body))
    return posts


def render_draft(fm, body):
    title = derive_title(body)
    slug = slugify(title) or f"li-{fm['id']}"
    date = fm["date"]
    li_id = fm["id"]
    safe_title = title.replace('"', "'")
    lines = [
        "---",
        "layout: post",
        "type: blog",
        f'title: "{safe_title}"',
        f"date: {date}",
        f"permalink: /{slug}/",
        f'li_id: "{li_id}"',
        "resources:",
        '  - text: "LinkedIn"',
        f'    link: "https://www.linkedin.com/feed/update/urn:li:activity:{li_id}/"',
        "---",
        "",
        body.strip(),
        "",
    ]
    return "\n".join(lines), slug, date


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limit", type=int, default=10,
                    help="Maximum number of drafts to stage (default: 10)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would be staged without writing files")
    args = ap.parse_args()

    if not LI_DIR.exists():
        print(f"LI source dir not found: {LI_DIR}", file=sys.stderr)
        sys.exit(1)

    DRAFTS_DIR.mkdir(exist_ok=True)

    seen = existing_li_ids()
    print(f"Already staged: {len(seen)} LI activity IDs found in _posts/ + _drafts/")

    candidates = load_li_posts()
    print(f"LI source: {len(candidates)} posts in {LI_DIR}")

    # Window: the N newest LI posts overall, then filter to unstaged.
    # This is intentional — backlog is out of scope. Reruns on the same day
    # naturally stage 0 because the window hasn't moved.
    window = candidates[: args.limit]
    new_candidates = [c for c in window if str(c[1]["id"]) not in seen]
    print(f"Window: newest {len(window)} LI posts; {len(new_candidates)} unstaged in window")
    print()

    staged = 0
    for src, fm, body in new_candidates:
        content, slug, date = render_draft(fm, body)
        out_path = DRAFTS_DIR / f"{date}-{slug}.md"
        if out_path.exists():
            print(f"  SKIP {out_path.name} (filename already in _drafts/)")
            continue
        if args.dry_run:
            print(f"  WOULD STAGE  {out_path.name}")
        else:
            out_path.write_text(content)
            print(f"  STAGED       {out_path.name}")
        staged += 1

    print()
    print(f"{'Would stage' if args.dry_run else 'Staged'}: {staged}")


if __name__ == "__main__":
    main()

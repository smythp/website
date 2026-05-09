#!/usr/bin/env python3
"""
Download image attachments from Patrick's LinkedIn posts via Unipile.

Pulls posts from the Unipile API, downloads the first image attachment of each
into assets/images/posts/<social-id>.<ext>. Idempotent — already-downloaded
images are skipped.

Usage:
    python scripts/fetch_post_media.py            # full sweep
    python scripts/fetch_post_media.py --limit 50 # cap
    python scripts/fetch_post_media.py --since 2024-01-01

Designed to fail soft: a post without an image, an unavailable attachment, or a
404 just gets skipped with a one-line warning. Best effort by design.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path.home() / "projects" / "automate-linkedin"))
from keys import UNIPILE_KEY  # noqa: E402

BASE_URL = "https://api16.unipile.com:14697/api/v1"
ACCOUNT_ID = "-Wl3mhu0QXGDpbhSMGV8cQ"
MY_URN = "ACoAAA5qQKQBqhey1pJKeaLqNKZ6XzJnredlhqU"

BLOG_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BLOG_ROOT / "assets" / "images" / "posts"


def headers():
    return {"X-API-KEY": UNIPILE_KEY, "Accept": "application/json"}


def fetch_posts(limit: int | None):
    cursor = None
    out = []
    while True:
        params = {"account_id": ACCOUNT_ID, "limit": 50}
        if cursor:
            params["cursor"] = cursor
        resp = requests.get(
            f"{BASE_URL}/users/{MY_URN}/posts",
            headers=headers(),
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])
        if not items:
            break
        out.extend(items)
        if limit and len(out) >= limit:
            return out[:limit]
        cursor = data.get("cursor") or data.get("next_cursor")
        if not cursor:
            break
    return out


def parse_date(post):
    raw = post.get("date") or post.get("parsed_datetime")
    if not raw:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw[: len(raw)] if "T" not in raw else raw, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except (ValueError, AttributeError):
        return None


def first_image_attachment(post):
    for att in post.get("attachments") or []:
        if att.get("type") == "img" and not att.get("unavailable") and not att.get("sticker"):
            return att
    return None


def download(url: str, out_path: Path) -> bool:
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  warn: download failed for {out_path.name}: {e}", file=sys.stderr)
        return False
    out_path.write_bytes(resp.content)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--since", help="YYYY-MM-DD")
    args = ap.parse_args()

    since = datetime.strptime(args.since, "%Y-%m-%d").date() if args.since else None

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("fetching posts from Unipile…")
    posts = fetch_posts(args.limit)
    print(f"  got {len(posts)} posts")

    downloaded = 0
    skipped_existing = 0
    no_image = 0
    out_of_range = 0

    for post in posts:
        d = parse_date(post)
        if since and d and d < since:
            out_of_range += 1
            continue

        post_id = post.get("social_id") or post.get("id") or ""
        # Strip the urn:li:<type>: prefix so the filename is just the numeric id
        # (clean URLs, matches the `id:` field in ~/li/my_posts/*.md frontmatter).
        numeric_id = post_id.split(":")[-1] if post_id else ""
        if not numeric_id:
            continue

        att = first_image_attachment(post)
        if not att:
            no_image += 1
            continue

        out_path = OUTPUT_DIR / f"{numeric_id}.jpg"
        if out_path.exists():
            skipped_existing += 1
            continue

        if download(att["url"], out_path):
            downloaded += 1
            print(f"  saved {out_path.name} ({d})")

    print(
        f"\ndone: {downloaded} downloaded, {skipped_existing} already existed, "
        f"{no_image} posts with no image, {out_of_range} outside --since range"
    )
    print(f"output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

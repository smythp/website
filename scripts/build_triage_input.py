#!/usr/bin/env python3
"""Build _data/archives_triage_input.yml — one entry per pending URL with
the inputs an LLM needs to judge whether the URL still serves the content
it was originally referenced for.

For each pending URL in _data/archives.yml (excluding auth-required and
video-deferred hosts):

  - source_excerpts: the first source file's referencing line + 2 lines
    before/after, plus the link's anchor text where extractable
  - current_title: cheap fetch of current <title> tag
  - current_h1: first <h1> if available
  - http_status: the response status from the fetch
  - dead_link_status: prior verdict from the dead-link audit if any

Output drives a triage pass via spindle/sonnet to classify each URL as
legit / squatted / rotted / unsure.
"""

import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "_data" / "archives.yml"
OUT = REPO / "_data" / "archives_triage_input.yml"

AUTH_REQUIRED_HOSTS = {
    "www.linkedin.com", "linkedin.com", "lnkd.in", "x.com", "twitter.com",
}
VIDEO_DEFERRED_HOSTS = {
    "www.youtube.com", "youtube.com", "youtu.be",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}
TIMEOUT = 12
WORKERS = 8


def is_skipped_host(url):
    h = urlparse(url).netloc.lower()
    return h in AUTH_REQUIRED_HOSTS or h in VIDEO_DEFERRED_HOSTS


def fetch_title(url):
    try:
        r = requests.get(url, timeout=TIMEOUT, headers=HEADERS, allow_redirects=True)
    except Exception as e:
        return {"http_status": f"error: {type(e).__name__}", "title": None, "h1": None}
    title = None
    h1 = None
    if r.status_code == 200 and "html" in r.headers.get("Content-Type", "").lower():
        m = re.search(r"<title[^>]*>([^<]+)</title>", r.text[:50000], re.IGNORECASE)
        if m:
            title = m.group(1).strip()[:200]
        m = re.search(r"<h1[^>]*>([^<]+)</h1>", r.text[:50000], re.IGNORECASE)
        if m:
            h1 = m.group(1).strip()[:200]
    return {
        "http_status": str(r.status_code),
        "final_url": r.url if r.url != url else None,
        "title": title,
        "h1": h1,
    }


def extract_excerpt(file_path, line_no):
    p = REPO / file_path
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None
    start = max(0, line_no - 3)
    end = min(len(lines), line_no + 2)
    return "\n".join(lines[start:end])


def main():
    entries = yaml.safe_load(CATALOG.read_text()) or []
    todo = [e for e in entries if not is_skipped_host(e["url"])]
    print(f"building triage input for {len(todo)} URLs")

    # Fetch titles in parallel
    title_results = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(fetch_title, e["url"]): e["url"] for e in todo}
        done = 0
        for fut in as_completed(futs):
            url = futs[fut]
            title_results[url] = fut.result()
            done += 1
            if done % 25 == 0:
                print(f"  fetched {done}/{len(todo)}")

    # Build triage records
    triage = []
    for e in todo:
        first_ref = e["found_in"][0] if e["found_in"] else None
        excerpt = None
        if first_ref:
            excerpt = extract_excerpt(first_ref["file"], first_ref["line"])
        rec = {
            "url": e["url"],
            "found_in": e["found_in"],
            "source_excerpt": excerpt,
            "fetch": title_results.get(e["url"], {}),
        }
        triage.append(rec)

    OUT.write_text(yaml.safe_dump(triage, sort_keys=False, allow_unicode=True))
    print(f"wrote {OUT.relative_to(REPO)} ({len(triage)} entries)")


if __name__ == "__main__":
    sys.exit(main() or 0)

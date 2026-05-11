#!/usr/bin/env python3
"""Audit external links across smythp.com source content.

Output: a markdown report at reports/dead-links-<date>.md listing every
external URL that's not a clean 200, with the source file(s) it appears in.

Special cases: LinkedIn (200 + deletion banner) and YouTube (200 + private/
deleted video) need content-level checks, not just status codes.
"""

import json
import re
import sys
import urllib.parse as up
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

REPO = Path(__file__).resolve().parent.parent
SOURCE_GLOBS = [
    "_posts/*.md",
    "_drafts/*.md",
    "*.md",
    "*.html",
    "_projects/*.md",
    "_data/*.yml",
    "_data/*.yaml",
    "_includes/*.html",
    "_layouts/*.html",
]

URL_RE = re.compile(r'https?://[^\s\'"<>)\]]+')
TIMEOUT = 12
MAX_WORKERS = 16

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36 "
        "(smythp.com dead-link audit)"
    )
}


def make_session():
    s = requests.Session()
    retry = Retry(
        total=2,
        backoff_factor=0.5,
        status_forcelist=[502, 503, 504],
        allowed_methods=["HEAD", "GET"],
    )
    s.mount("http://", HTTPAdapter(max_retries=retry))
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update(HEADERS)
    return s


def find_sources():
    """Walk source files, collect (url, source_file, line_no, context) tuples."""
    occurrences = defaultdict(list)
    for pattern in SOURCE_GLOBS:
        for path in REPO.glob(pattern):
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                for m in URL_RE.finditer(line):
                    url = m.group(0).rstrip(".,;:!?")
                    rel = path.relative_to(REPO)
                    occurrences[url].append((str(rel), i, line.strip()[:120]))
    return occurrences


def is_internal(url):
    """Skip our own domain — checking those is what Jekyll is for."""
    host = up.urlparse(url).netloc.lower()
    return host in ("smythp.com", "www.smythp.com")


def check_youtube(session, url):
    """oembed endpoint returns 401/404 for private/unlisted/deleted videos."""
    parsed = up.urlparse(url)
    vid = None
    if "youtube.com" in parsed.netloc and "watch" in parsed.path:
        qs = up.parse_qs(parsed.query)
        vid = (qs.get("v") or [None])[0]
    elif "youtu.be" in parsed.netloc:
        vid = parsed.path.lstrip("/").split("/")[0]
    elif "youtube.com" in parsed.netloc and "/playlist" in parsed.path:
        return None
    elif "youtube.com" in parsed.netloc and "/embed/" in parsed.path:
        vid = parsed.path.split("/embed/")[1].split("/")[0]
    if not vid:
        return None
    oembed = f"https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3D{vid}&format=json"
    try:
        r = session.get(oembed, timeout=TIMEOUT)
    except Exception as e:
        return ("UNCERTAIN", f"oembed error: {e}")
    if r.status_code == 200:
        try:
            data = r.json()
            return ("ALIVE", f"oembed ok: {data.get('title', '?')[:60]}")
        except Exception:
            return ("ALIVE", "oembed ok")
    if r.status_code in (401, 404):
        return ("DEAD", f"oembed {r.status_code} — video private/unlisted/deleted")
    return ("UNCERTAIN", f"oembed {r.status_code}")


def check_linkedin(session, url, html):
    """LI returns 200 even for unpublished posts.  Look for deletion markers."""
    markers = [
        "this post is no longer available",
        "page not found",
        "page doesn't exist",
        "couldn't find the page",
    ]
    low = html.lower()
    for m in markers:
        if m in low:
            return ("DEAD", f"LI marker: {m!r}")
    return ("ALIVE", "LI 200, no deletion marker")


def check_url(url):
    """Return (status_class, detail, final_url_if_redirected)."""
    session = make_session()
    parsed = up.urlparse(url)
    host = parsed.netloc.lower()

    if "youtube.com" in host or "youtu.be" in host:
        result = check_youtube(session, url)
        if result is not None:
            cls, detail = result
            return (cls, detail, None)

    try:
        r = session.head(url, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code == 405 or r.status_code >= 400:
            r = session.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
            content = r.text if r.status_code == 200 else ""
        elif "linkedin.com" in host:
            r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
            content = r.text
        else:
            content = ""
    except requests.exceptions.SSLError as e:
        return ("DEAD", f"SSL error: {str(e)[:120]}", None)
    except requests.exceptions.ConnectionError as e:
        return ("DEAD", f"connection error: {str(e)[:120]}", None)
    except requests.exceptions.Timeout:
        return ("UNCERTAIN", f"timeout after {TIMEOUT}s", None)
    except requests.exceptions.RequestException as e:
        return ("UNCERTAIN", f"req error: {str(e)[:120]}", None)

    final = r.url if r.url != url else None
    sc = r.status_code

    if "linkedin.com" in host and sc == 200:
        cls, detail = check_linkedin(session, url, content)
        return (cls, detail + f" [{sc}]", final)

    if sc == 200:
        if final:
            return ("REDIRECTED", f"200 via redirect", final)
        return ("ALIVE", "200", None)
    if sc in (301, 302, 308) and final:
        return ("REDIRECTED", f"{sc}", final)
    if sc in (403,):
        # Some servers block bots — treat as uncertain rather than dead.
        return ("UNCERTAIN", f"{sc} (possible bot block)", None)
    if 400 <= sc < 500:
        return ("DEAD", f"HTTP {sc}", None)
    if 500 <= sc < 600:
        return ("UNCERTAIN", f"HTTP {sc} (server)", None)
    return ("UNCERTAIN", f"HTTP {sc}", None)


def main():
    print("Finding sources...", file=sys.stderr)
    occurrences = find_sources()
    urls = [u for u in occurrences if not is_internal(u)]
    urls.sort()
    print(f"Checking {len(urls)} unique external URLs with {MAX_WORKERS} workers...", file=sys.stderr)

    results = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(check_url, u): u for u in urls}
        for i, fut in enumerate(as_completed(futures), 1):
            u = futures[fut]
            try:
                results[u] = fut.result()
            except Exception as e:
                results[u] = ("UNCERTAIN", f"checker error: {e}", None)
            if i % 25 == 0 or i == len(urls):
                print(f"  {i}/{len(urls)}", file=sys.stderr)

    today = date.today().isoformat()
    out_dir = REPO / "reports"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"dead-links-{today}.md"

    by_class = defaultdict(list)
    for url, (cls, detail, final) in results.items():
        by_class[cls].append((url, detail, final))

    counts = {k: len(v) for k, v in by_class.items()}
    counts["TOTAL"] = len(results)

    with out.open("w") as f:
        f.write(f"# Dead link audit — {today}\n\n")
        f.write(f"Audited {len(urls)} unique external URLs from smythp.com source.\n\n")
        f.write("## Counts\n\n")
        for k in ("ALIVE", "REDIRECTED", "DEAD", "UNCERTAIN", "TOTAL"):
            f.write(f"- {k}: {counts.get(k, 0)}\n")
        f.write("\n")

        for cls in ("DEAD", "REDIRECTED", "UNCERTAIN"):
            items = sorted(by_class.get(cls, []))
            if not items:
                continue
            f.write(f"## {cls} ({len(items)})\n\n")
            for url, detail, final in items:
                f.write(f"### `{url}`\n\n")
                f.write(f"- **Status:** {detail}\n")
                if final:
                    f.write(f"- **Redirects to:** {final}\n")
                appearances = occurrences[url]
                f.write(f"- **Found in:**\n")
                for src, line, ctx in appearances:
                    f.write(f"  - `{src}:{line}`\n")
                f.write("\n")

    print(f"\nReport: {out}", file=sys.stderr)
    print(json.dumps(counts), file=sys.stderr)


if __name__ == "__main__":
    main()

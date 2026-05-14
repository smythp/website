#!/usr/bin/env python3
"""Enumerate external links and seed _data/archives.yml.

Pure enumeration, no network calls. Walks the same source globs as
check_dead_links.py, dedupes URLs, merges with any pre-existing
catalog entries (preserving archive.wayback / archive.archive_ph /
archive.local fields if already populated), and writes the catalog
back. Re-runnable safely.

Output format (_data/archives.yml):

    - url: https://example.com/page
      found_in:
        - {file: _posts/X.md, line: 42}
      archive:
        wayback: null
        archive_ph: null
        local: null
      archived_at: null
      status: pending

`status` values: pending | archived | failed | skipped.
"""

import re
import sys
import urllib.parse as up
from collections import defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "_data" / "archives.yml"

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
INTERNAL_HOSTS = {"smythp.com", "www.smythp.com"}


def find_sources():
    occurrences = defaultdict(list)
    for pattern in SOURCE_GLOBS:
        for path in REPO.glob(pattern):
            if path.name.startswith("."):
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                for m in URL_RE.finditer(line):
                    url = m.group(0).rstrip(".,;:!?")
                    rel = str(path.relative_to(REPO))
                    occurrences[url].append({"file": rel, "line": i})
    return occurrences


def is_internal(url):
    host = up.urlparse(url).netloc.lower()
    return host in INTERNAL_HOSTS


def load_existing():
    if not CATALOG.exists():
        return {}
    raw = yaml.safe_load(CATALOG.read_text()) or []
    return {e["url"]: e for e in raw}


def merge(existing, fresh_url, fresh_found):
    prior = existing.get(fresh_url)
    if prior is None:
        return {
            "url": fresh_url,
            "found_in": fresh_found,
            "archive": {"wayback": None, "archive_ph": None, "local": None},
            "archived_at": None,
            "status": "pending",
        }
    prior["found_in"] = fresh_found
    prior.setdefault("archive", {"wayback": None, "archive_ph": None, "local": None})
    for k in ("wayback", "archive_ph", "local"):
        prior["archive"].setdefault(k, None)
    prior.setdefault("archived_at", None)
    prior.setdefault("status", "pending")
    return prior


def main():
    existing = load_existing()
    occurrences = find_sources()
    external = {u: f for u, f in occurrences.items() if not is_internal(u)}

    merged = []
    for url in sorted(external):
        merged.append(merge(existing, url, external[url]))

    dropped = sorted(set(existing) - set(external))

    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(yaml.safe_dump(merged, sort_keys=False, allow_unicode=True))

    pending = sum(1 for e in merged if e["status"] == "pending")
    archived = sum(1 for e in merged if e["status"] == "archived")
    failed = sum(1 for e in merged if e["status"] == "failed")
    print(f"catalog: {CATALOG.relative_to(REPO)}")
    print(f"total URLs: {len(merged)}")
    print(f"  pending:  {pending}")
    print(f"  archived: {archived}")
    print(f"  failed:   {failed}")
    if dropped:
        print(f"dropped (no longer in source): {len(dropped)}")
        for u in dropped:
            print(f"  - {u}")


if __name__ == "__main__":
    sys.exit(main() or 0)

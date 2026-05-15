#!/usr/bin/env python3
"""Capture pending URLs as self-contained SingleFile .html bundles.

Reads _data/archives.yml. For each entry whose archive.singlefile is null
and whose host is not on the AUTH_REQUIRED list (LinkedIn / X / lnkd.in)
or the VIDEO_DEFERRED list (YouTube), runs `single-file` to produce a
self-contained HTML file at ~/projects/hoard/smythp/singlefile/<hash>.html.
Records the path, size, and capture time back into the catalog. Idempotent.

Usage:
  python3 scripts/archive_singlefile.py            # all eligible pending
  python3 scripts/archive_singlefile.py --limit 5  # smoke-test pass
  python3 scripts/archive_singlefile.py --only-host github.com  # one host
"""

import argparse
import hashlib
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "_data" / "archives.yml"
HOARD = Path.home() / "projects" / "hoard" / "smythp" / "singlefile"

AUTH_REQUIRED_HOSTS = {
    "www.linkedin.com",
    "linkedin.com",
    "lnkd.in",
    "x.com",
    "twitter.com",
}
VIDEO_DEFERRED_HOSTS = {
    "www.youtube.com",
    "youtube.com",
    "youtu.be",
}

SINGLE_FILE_BIN = "single-file"
TIMEOUT_SECS = 90
PER_CALL_SLEEP = 0.5


def url_id(url):
    return hashlib.sha1(url.encode()).hexdigest()[:16]


def is_auth_required(url):
    return urlparse(url).netloc.lower() in AUTH_REQUIRED_HOSTS


def is_video_deferred(url):
    return urlparse(url).netloc.lower() in VIDEO_DEFERRED_HOSTS


CAPTURE_VERDICTS = {"legit", "redirected_legit"}


def needs_capture(entry):
    if entry.get("archive", {}).get("singlefile"):
        return False
    verdict = entry.get("triage", {}).get("verdict")
    if verdict not in CAPTURE_VERDICTS:
        return False
    return True


def capture(url, dest):
    cmd = [
        SINGLE_FILE_BIN,
        "--browser-wait-until", "networkIdle",
        "--browser-load-max-time", "30000",
        "--browser-capture-max-time", "30000",
        url,
        str(dest),
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TIMEOUT_SECS
        )
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if result.returncode != 0:
        return False, f"exit {result.returncode}: {result.stderr.strip()[:200]}"
    if not dest.exists() or dest.stat().st_size == 0:
        return False, "no output file"
    return True, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="cap captures this run")
    ap.add_argument("--only-host", help="restrict to one hostname")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not CATALOG.exists():
        print("no catalog — run build_archive_catalog.py first", file=sys.stderr)
        return 1

    HOARD.mkdir(parents=True, exist_ok=True)
    entries = yaml.safe_load(CATALOG.read_text()) or []

    todo = []
    skipped_auth = 0
    skipped_video = 0
    for e in entries:
        if not needs_capture(e):
            continue
        url = e["url"]
        if is_auth_required(url):
            skipped_auth += 1
            e.setdefault("notes", {})
            e["notes"]["singlefile"] = "skipped: auth-required host"
            continue
        if is_video_deferred(url):
            skipped_video += 1
            e.setdefault("notes", {})
            e["notes"]["singlefile"] = "skipped: video, see video brief"
            continue
        if args.only_host and urlparse(url).netloc.lower() != args.only_host.lower():
            continue
        todo.append(e)
        if args.limit and len(todo) >= args.limit:
            break

    print(f"eligible captures: {len(todo)}")
    print(f"skipped auth-required: {skipped_auth}")
    print(f"skipped video: {skipped_video}")

    if args.dry_run:
        for e in todo:
            print(f"  would capture: {e['url']}")
        CATALOG.write_text(yaml.safe_dump(entries, sort_keys=False, allow_unicode=True))
        return 0

    captured = 0
    failed = 0

    for i, entry in enumerate(todo, 1):
        url = entry["url"]
        uid = url_id(url)
        dest = HOARD / f"{uid}.html"
        print(f"[{i}/{len(todo)}] {url}")
        ok, err = capture(url, dest)
        if ok:
            entry["archive"]["singlefile"] = {
                "path": str(dest),
                "url_hash": uid,
                "size_bytes": dest.stat().st_size,
                "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            entry["status"] = "archived"
            if "notes" in entry and "singlefile" in entry.get("notes", {}):
                del entry["notes"]["singlefile"]
                if not entry["notes"]:
                    del entry["notes"]
            captured += 1
            print(f"  ok  {dest.stat().st_size//1024} KB")
        else:
            entry.setdefault("notes", {})
            entry["notes"]["singlefile"] = f"error: {err}"
            failed += 1
            print(f"  FAIL  {err}")
        CATALOG.write_text(yaml.safe_dump(entries, sort_keys=False, allow_unicode=True))
        time.sleep(PER_CALL_SLEEP)

    print()
    print(f"captured: {captured}")
    print(f"failed:   {failed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

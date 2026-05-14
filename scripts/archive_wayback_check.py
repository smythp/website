#!/usr/bin/env python3
"""Phase 2a: query Wayback Machine for existing snapshots.

Reads _data/archives.yml, for every URL whose archive.wayback is null,
asks https://archive.org/wayback/available?url=<URL> whether a snapshot
already exists. If so, records the snapshot URL + timestamp into the
catalog and marks status=archived. If not, leaves archive.wayback=null
and writes a "needs_save" marker so phase 2b can target just the gap.

Read-only with respect to the IA save endpoint — this script does not
trigger new captures. Idempotent: re-running only checks entries still
flagged needs_save or untouched.
"""

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "_data" / "archives.yml"
AVAILABLE = "https://archive.org/wayback/available"
MAX_WORKERS = 1
TIMEOUT = 15
SLEEP_BETWEEN = 1.5
MAX_RETRIES_429 = 4

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36 "
        "(smythp.com archive catalog builder)"
    )
}


def query_available(session, url):
    for attempt in range(MAX_RETRIES_429 + 1):
        try:
            r = session.get(AVAILABLE, params={"url": url}, timeout=TIMEOUT)
        except Exception as e:
            return ("error", str(e), None, None)
        if r.status_code == 429:
            wait = min(60, 5 * (2 ** attempt))
            time.sleep(wait)
            continue
        break
    if r.status_code != 200:
        return ("error", f"HTTP {r.status_code}", None, None)
    try:
        data = r.json()
    except Exception as e:
        return ("error", f"json: {e}", None, None)
    snap = (data.get("archived_snapshots") or {}).get("closest")
    if not snap or not snap.get("available"):
        return ("none", None, None, None)
    return ("ok", None, snap.get("url"), snap.get("timestamp"))


def needs_check(entry):
    if entry.get("archive", {}).get("wayback"):
        return False
    if entry.get("status") == "archived":
        return False
    return True


def main():
    if not CATALOG.exists():
        print("no catalog — run build_archive_catalog.py first", file=sys.stderr)
        return 1
    entries = yaml.safe_load(CATALOG.read_text()) or []

    todo = [e for e in entries if needs_check(e)]
    print(f"checking {len(todo)} pending URLs (of {len(entries)} total)")

    session = requests.Session()
    session.headers.update(HEADERS)

    found = 0
    none_count = 0
    errors = 0

    for i, entry in enumerate(todo, 1):
        kind, msg, snap_url, ts = query_available(session, entry["url"])
        if kind == "ok":
            entry["archive"]["wayback"] = {"url": snap_url, "timestamp": ts}
            entry["status"] = "archived"
            entry["archived_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if "notes" in entry and "wayback_check" in entry.get("notes", {}):
                del entry["notes"]["wayback_check"]
                if not entry["notes"]:
                    del entry["notes"]
            found += 1
        elif kind == "none":
            entry["archive"]["wayback"] = None
            entry.setdefault("notes", {})
            entry["notes"]["wayback_check"] = "no snapshot"
            none_count += 1
        else:
            entry.setdefault("notes", {})
            entry["notes"]["wayback_check"] = f"error: {msg}"
            errors += 1
        if i % 20 == 0:
            print(f"  {i}/{len(todo)} (found {found}, gap {none_count}, errors {errors})")
            CATALOG.write_text(yaml.safe_dump(entries, sort_keys=False, allow_unicode=True))
        time.sleep(SLEEP_BETWEEN)

    CATALOG.write_text(yaml.safe_dump(entries, sort_keys=False, allow_unicode=True))
    print()
    print(f"existing wayback snapshots: {found}")
    print(f"no snapshot yet:            {none_count}")
    print(f"check errors:               {errors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

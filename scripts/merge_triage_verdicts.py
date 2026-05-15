#!/usr/bin/env python3
"""Merge triage verdicts from /tmp/triage_verdicts_{1..N}.yml into
_data/archives.yml. Adds a `triage` field to each matching entry:

    triage:
      verdict: legit | squatted | ...
      reason: <text>

Then applies known agent miscalls as overrides:
  - htmlpreview.github.io URLs marked `rotted`  -> `unsure`
    (the agent saw the service's landing page, not the rendered presentation)
  - CUNY *.commons.gc.cuny.edu and gc.cuny.edu URLs marked `dead`  -> `unsure`
    (these almost certainly bot-block; the dead-link audit also marked them
    UNCERTAIN — not actually dead)
"""

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CATALOG = REPO / "_data" / "archives.yml"

CUNY_BOT_BLOCK_HOSTS = {
    "digitalfellows.commons.gc.cuny.edu",
    "gcdi.commons.gc.cuny.edu",
    "gcdri.commons.gc.cuny.edu",
    "gc.cuny.edu",
    "m.gc.cuny.edu",
    "www.gc.cuny.edu",
}


def load_verdicts():
    verdicts = {}
    for i in range(1, 6):
        p = Path(f"/tmp/triage_verdicts_{i}.yml")
        if not p.exists():
            print(f"missing {p}", file=sys.stderr)
            return None
        for v in yaml.safe_load(p.read_text()):
            verdicts[v["url"]] = {"verdict": v["verdict"], "reason": v["reason"]}
    return verdicts


def apply_overrides(url, triage):
    """Patch known agent miscalls before saving."""
    from urllib.parse import urlparse
    host = urlparse(url).netloc.lower()

    if "htmlpreview.github.io" in host and triage["verdict"] == "rotted":
        triage = dict(triage)
        triage["verdict"] = "unsure"
        triage["reason"] = (
            "Agent saw htmlpreview.github.io landing page; the actual "
            "linked presentation does render in a browser. Manual review."
        )
    elif host in CUNY_BOT_BLOCK_HOSTS and triage["verdict"] == "dead":
        triage = dict(triage)
        triage["verdict"] = "unsure"
        triage["reason"] = (
            "HTTP 403 — CUNY commons bot-blocks; page likely alive. "
            "Manual verification needed."
        )
    return triage


def main():
    verdicts = load_verdicts()
    if verdicts is None:
        return 1

    entries = yaml.safe_load(CATALOG.read_text()) or []
    merged = 0
    for e in entries:
        if e["url"] in verdicts:
            e["triage"] = apply_overrides(e["url"], verdicts[e["url"]])
            merged += 1

    CATALOG.write_text(yaml.safe_dump(entries, sort_keys=False, allow_unicode=True))
    print(f"merged {merged} verdicts into {CATALOG.relative_to(REPO)}")

    # Tally final state
    from collections import Counter
    counts = Counter(e.get("triage", {}).get("verdict") for e in entries)
    print()
    print("Final triage tally:")
    for k in ("legit","redirected_legit","redirected_unrelated","squatted","rotted","dead","unsure", None):
        if k in counts:
            label = k or "(no verdict — auth-required or video)"
            print(f"  {label:32s} {counts[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

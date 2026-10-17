#!/usr/bin/env python3
"""Validate the conference directory and its project-level verifications.

Usage:
  python3 check_directory.py --directory conferences/directory.json
  python3 check_directory.py --directory ... --overlay paper_state/conference-verifications.json --require-verified

Exit codes: 0 pass, 1 failure, 2 IO/config.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

AREAS = {"general", "ml", "nlp", "vision", "data", "hci", "robotics", "theory", "education"}
TYPES = {"conference", "journal"}
CYCLES = {"annual", "rolling"}
STATUS = {"unknown", "in_review", "open", "upcoming", "rolling"}
STALE_DAYS = 180


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", default="conferences/directory.json")
    ap.add_argument("--overlay", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--require-verified", action="store_true")
    args = ap.parse_args()

    dp = Path(args.directory)
    if not dp.exists():
        print(f"IO ERROR: missing {dp}", file=sys.stderr)
        return 2
    try:
        data = json.loads(dp.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"CONFIG ERROR: {e}", file=sys.stderr)
        return 2

    venues = data.get("venues", [])
    if not venues:
        print("FAIL: no venues", file=sys.stderr)
        return 1

    hard, warn = [], []
    ids = set()
    for i, v in enumerate(venues, 1):
        for k in ("id", "name", "type", "areas", "cycle", "official_url", "has_profile"):
            if k not in v:
                hard.append(f"row {i}: missing {k}")
        vid = v.get("id", "")
        if vid in ids:
            hard.append(f"duplicate id: {vid}")
        ids.add(vid)
        if v.get("type") not in TYPES:
            hard.append(f"{vid}: bad type {v.get('type')!r}")
        if v.get("cycle") not in CYCLES:
            hard.append(f"{vid}: bad cycle {v.get('cycle')!r}")
        areas = set(v.get("areas", []))
        if not areas or not areas <= AREAS:
            hard.append(f"{vid}: bad areas {sorted(areas - AREAS)}")
        if not str(v.get("official_url", "")).startswith("https://"):
            hard.append(f"{vid}: official_url must be https")

    overlay = {}
    if args.overlay:
        op = Path(args.overlay)
        if op.exists():
            try:
                overlay = json.loads(op.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                print(f"CONFIG ERROR: overlay {e}", file=sys.stderr)
                return 2
        for vid, o in overlay.items():
            if vid not in ids:
                hard.append(f"overlay: unknown venue {vid}")
            if o.get("status") not in STATUS:
                hard.append(f"{vid}: bad status {o.get('status')!r}")
            if o.get("status") != "unknown" and not str(o.get("source_url", "")).startswith("https://"):
                hard.append(f"{vid}: source_url must be https")
            vo = o.get("verified_on")
            if vo:
                try:
                    d = dt.date.fromisoformat(vo)
                    if (dt.date.today() - d).days > STALE_DAYS:
                        (hard if args.strict else warn).append(f"{vid}: verification stale ({vo})")
                except ValueError:
                    hard.append(f"{vid}: verified_on not YYYY-MM-DD")
            elif o.get("status") not in (None, "unknown"):
                hard.append(f"{vid}: verified_on missing")
            if args.require_verified and not vo:
                hard.append(f"{vid}: not verified")

    if args.require_verified:
        for vid in sorted(ids):
            if not overlay.get(vid, {}).get("verified_on"):
                hard.append(f"{vid}: no project-level verification")

    for x in hard:
        print("FAIL " + x)
    for x in warn:
        print("WARN " + x)
    print(f"RESULT: {'PASS' if not hard else 'FAIL'} (venues={len(venues)}, verified={sum(1 for o in overlay.values() if o.get('verified_on'))})")
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

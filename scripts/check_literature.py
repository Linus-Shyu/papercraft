#!/usr/bin/env python3
"""Validate the literature matrix used for the survey / related-work pass.

Usage:
  python3 check_literature.py --csv paper_state/literature-matrix.csv
  python3 check_literature.py --csv ... --strict --min-rows 10

Exit codes: 0 pass, 1 failure, 2 IO/config.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

REQUIRED = ["key", "title", "year", "venue", "role", "closest", "verified", "claim_supported", "gap", "notes"]
STATUS = {"VERIFIED", "PARTIAL", "UNVERIFIED", "SUSPECT"}
ROLES = {"foundation", "baseline", "closest", "adjacent", "survey"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--min-rows", type=int, default=5)
    ap.add_argument("--min-closest", type=int, default=3)
    args = ap.parse_args()

    p = Path(args.csv)
    if not p.exists():
        print(f"IO ERROR: missing {p}", file=sys.stderr)
        return 2

    rows = list(csv.DictReader(p.open(encoding="utf-8", newline="")))
    if not rows:
        print("FAIL: empty matrix", file=sys.stderr)
        return 1

    missing_cols = [c for c in REQUIRED if c not in rows[0]]
    hard, warn = [], []
    if missing_cols:
        hard.append(f"missing columns: {', '.join(missing_cols)}")

    keys = Counter()
    for i, r in enumerate(rows, 2):
        keys[r.get("key", "")] += 1
        for c in ("key", "title", "year", "venue"):
            if not r.get(c, "").strip():
                hard.append(f"row {i}: empty {c}")
        st = r.get("verified", "").strip().upper()
        if st not in STATUS:
            hard.append(f"row {i}: invalid verified '{st}'")
        elif st in ("UNVERIFIED", "SUSPECT"):
            (hard if (args.strict or st == "SUSPECT") else warn).append(
                f"row {i}: {r.get('key')} is {st}"
            )
        role = r.get("role", "").strip().lower()
        if role and role not in ROLES:
            warn.append(f"row {i}: unknown role '{role}'")
        if r.get("closest", "").strip().lower() == "yes" and not r.get("gap", "").strip():
            hard.append(f"row {i}: closest work needs a specific gap")
        if not r.get("claim_supported", "").strip():
            warn.append(f"row {i}: no claim_supported")

    for k, n in keys.items():
        if k and n > 1:
            hard.append(f"duplicate key: {k}")

    n = len(rows)
    closest = sum(1 for r in rows if r.get("closest", "").strip().lower() == "yes")
    if n < args.min_rows:
        warn.append(f"only {n} rows (min {args.min_rows})")
    if closest < args.min_closest:
        hard.append(f"only {closest} closest works (min {args.min_closest})")

    years = [r["year"] for r in rows if r.get("year", "").strip().isdigit()]
    for m in hard:
        print("FAIL " + m)
    for m in warn:
        print("WARN " + m)
    print(
        f"SUMMARY: rows={n}, closest={closest}, verified={sum(1 for r in rows if r['verified'].upper() == 'VERIFIED')}, "
        f"years={min(years) if years else '?'}-{max(years) if years else '?'}"
    )
    print(f"RESULT: {'PASS' if not hard else 'FAIL'} (hard={len(hard)}, warn={len(warn)})")
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate a conference profile's verification block.

Usage:
  python3 check_conference.py conferences/aaai.md
  python3 check_conference.py conferences/*.md --strict

Exit codes: 0 pass, 1 failure (strict), 2 IO error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

REQUIRED = [
    "id", "name", "year", "source_url", "verified_on", "status",
    "template", "review_model", "anonymity", "page_limit_main",
    "page_limit_refs", "appendix", "supplementary", "reproducibility",
    "llm_policy", "dual_submission", "rebuttal", "camera_ready",
]
STALE_DAYS = 180


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    out = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    failed = 0
    today = dt.date.today()
    for f in args.files:
        p = Path(f)
        if not p.exists():
            print(f"IO ERROR: missing {p}", file=sys.stderr)
            failed += 1
            continue
        if p.stem == "_schema":
            print(f"SKIP {p} (schema, not a profile)")
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        hard, warn = [], []
        for k in REQUIRED:
            if k not in fm or not fm[k]:
                hard.append(f"missing field: {k}")
        if fm.get("id") and p.stem not in ("_default", "_schema") and fm["id"] != p.stem:
            hard.append(f"id '{fm['id']}' != filename '{p.stem}'")

        unverified = [k for k, v in fm.items() if str(v).upper() == "VERIFY"]
        status = fm.get("status", "").upper()
        if status != "VERIFIED":
            warn.append(f"status is {status or 'missing'} (needs VERIFIED before use)")
        if unverified:
            warn.append(f"{len(unverified)} fields still VERIFY: {', '.join(unverified[:6])}")

        src = fm.get("source_url", "")
        if not src.startswith("http"):
            (warn if p.stem == "_default" else hard).append("source_url is not a URL")
        vo = fm.get("verified_on", "")
        if vo in ("", "null", "None"):
            warn.append("verified_on is empty")
        else:
            try:
                d = dt.date.fromisoformat(vo)
                if (today - d).days > STALE_DAYS:
                    warn.append(f"profile stale: verified {(today - d).days} days ago")
            except ValueError:
                hard.append("verified_on is not YYYY-MM-DD")

        for x in hard:
            print(f"FAIL {p}: {x}")
        for x in warn:
            print(f"WARN {p}: {x}")
        if not hard and not warn:
            print(f"PASS {p}")
        failed += len(hard) + (len(warn) if args.strict else 0)

    print(f"RESULT: {'PASS' if not failed else 'FAIL'} ({len(args.files)} profiles, {failed} failed)")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate a structured review and check score/text consistency.

Input: templates/review-score.json (see REVIEWING.md).
Usage:
  python3 score_review.py --review review.json
  python3 score_review.py --review review.json --markdown --strict

Exit codes: 0 pass, 1 failure, 2 IO/config.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DIMS = ["soundness", "novelty", "significance", "clarity", "reproducibility"]
SEV = {"BLOCKER", "MAJOR", "MINOR", "NIT"}
STATUS = {"SUPPORTED", "WEAK", "UNSUPPORTED", "UNCLEAR"}
RECS = {"strong_reject", "reject", "weak_reject", "borderline", "weak_accept", "accept", "strong_accept"}


def band(overall: int) -> set[str]:
    if overall >= 8:
        return {"accept", "strong_accept"}
    if overall >= 6:
        return {"weak_accept", "accept", "borderline"}
    if overall == 5:
        return {"borderline", "weak_accept", "weak_reject"}
    if overall >= 3:
        return {"weak_reject", "reject", "borderline"}
    return {"strong_reject", "reject"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--review", required=True)
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    p = Path(args.review)
    if not p.exists():
        print(f"IO ERROR: missing {p}", file=sys.stderr)
        return 2
    try:
        r = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"CONFIG ERROR: {e}", file=sys.stderr)
        return 2

    hard, warn = [], []

    for k in ("paper_id", "reviewer", "summary", "claims", "strengths", "weaknesses", "scores", "overall", "confidence", "recommendation"):
        if k not in r:
            hard.append(f"missing field: {k}")
    if hard:
        for x in hard:
            print("FAIL " + x)
        return 1

    if len(r["summary"].split(".")) < 3:
        warn.append("summary is shorter than 3 sentences")
    if len(r["strengths"]) < 2:
        hard.append("need at least 2 specific strengths")
    if not r["weaknesses"]:
        hard.append("need at least 1 weakness (or state 'none' with evidence)")

    for i, c in enumerate(r["claims"], 1):
        if c.get("status") not in STATUS:
            hard.append(f"claim {i}: invalid status {c.get('status')!r}")
        if not c.get("evidence"):
            hard.append(f"claim {i}: missing evidence")
    for i, w in enumerate(r["weaknesses"], 1):
        if w.get("severity") not in SEV:
            hard.append(f"weakness {i}: invalid severity {w.get('severity')!r}")
        for f in ("location", "issue", "evidence"):
            if not str(w.get(f, "")).strip():
                hard.append(f"weakness {i}: missing {f}")

    scores = r["scores"]
    for d in DIMS:
        v = scores.get(d)
        if not isinstance(v, int) or not 1 <= v <= 4:
            hard.append(f"score {d}: must be int 1-4, got {v!r}")
    if not isinstance(r["overall"], int) or not 1 <= r["overall"] <= 10:
        hard.append(f"overall must be int 1-10, got {r['overall']!r}")
    if not isinstance(r["confidence"], int) or not 1 <= r["confidence"] <= 5:
        hard.append(f"confidence must be int 1-5, got {r['confidence']!r}")
    if r["recommendation"] not in RECS:
        hard.append(f"invalid recommendation {r['recommendation']!r}")

    if isinstance(r["overall"], int) and r["recommendation"] in RECS:
        if r["recommendation"] not in band(r["overall"]):
            hard.append(f"score/text mismatch: overall {r['overall']} -> {sorted(band(r['overall']))}, got {r['recommendation']}")

    for w in r["weaknesses"]:
        if w.get("severity") == "BLOCKER" and isinstance(r["overall"], int) and r["overall"] > 4:
            hard.append(f"BLOCKER weakness but overall {r['overall']} (>4)")
        if w.get("severity") == "MINOR" and w.get("evidence") in ("", "n/a", "-"):
            warn.append("minor weakness without evidence (acceptable but check)")

    if args.strict:
        hard.extend(warn)
        warn = []

    if args.markdown:
        print(f"# Review: {r['paper_id']} ({r['reviewer']})\n")
        print("## Summary\n")
        print(r["summary"] + "\n")
        print("## Strengths\n")
        for s in r["strengths"]:
            print(f"- {s}")
        print("\n## Weaknesses\n")
        for w in r["weaknesses"]:
            print(f"- **[{w['severity']}]** {w['issue']}  \n  Location: {w['location']}  \n  Evidence: {w['evidence']}")
        print("\n## Scores\n")
        print("| Dimension | Score |")
        print("|---|---|")
        for d in DIMS:
            print(f"| {d} | {scores[d]} |")
        print(f"\n- Overall: {r['overall']}/10")
        print(f"- Confidence: {r['confidence']}/5")
        print(f"- Recommendation: {r['recommendation']}")

    for x in hard:
        print("FAIL " + x)
    for x in warn:
        print("WARN " + x)
    print(f"RESULT: {'PASS' if not hard else 'FAIL'} (hard={len(hard)}, warn={len(warn)})")
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Acceptance risk memo from a structured assessment (not a probability).

Input: templates/acceptance.json.
Usage:
  python3 score_acceptance.py --assessment acceptance.json
  python3 score_acceptance.py --assessment ... --strict

Exit codes: 0 pass, 1 failure (e.g., submit with a BLOCKER), 2 IO/config.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DIMS = ["claim_evidence", "novelty", "rigor", "clarity", "reproducibility"]
SEV = {"BLOCKER", "MAJOR", "MINOR"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assessment", required=True)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    p = Path(args.assessment)
    if not p.exists():
        print(f"IO ERROR: missing {p}", file=sys.stderr)
        return 2
    try:
        a = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"CONFIG ERROR: {e}", file=sys.stderr)
        return 2

    hard, warn = [], []
    for k in ("venue", "readiness", "fit", "risks", "decision"):
        if k not in a:
            hard.append(f"missing field: {k}")
    if hard:
        for x in hard:
            print("FAIL " + x)
        return 1

    rd = a["readiness"]
    for d in DIMS:
        v = rd.get(d)
        if not isinstance(v, int) or not 1 <= v <= 4:
            hard.append(f"readiness.{d}: int 1-4 expected, got {v!r}")
    fit = a["fit"]
    if not isinstance(fit, int) or not 1 <= fit <= 4:
        hard.append(f"fit: int 1-4 expected, got {fit!r}")

    for i, r in enumerate(a["risks"], 1):
        if r.get("severity") not in SEV:
            hard.append(f"risk {i}: invalid severity {r.get('severity')!r}")
        for f in ("risk", "mitigation"):
            if not str(r.get(f, "")).strip():
                hard.append(f"risk {i}: missing {f}")

    mean = sum(rd[d] for d in DIMS) / len(DIMS) if all(isinstance(rd.get(d), int) for d in DIMS) else 0
    majors = sum(1 for r in a["risks"] if r.get("severity") == "MAJOR")
    blockers = [r for r in a["risks"] if r.get("severity") == "BLOCKER"]

    if blockers:
        band = "weak (unresolved BLOCKER)"
    elif mean >= 3.0 and fit >= 3 and majors <= 2:
        band = "competitive"
    elif mean >= 2.4 and fit >= 2:
        band = "borderline"
    else:
        band = "weak"

    decision = str(a["decision"]).lower()
    if decision not in {"submit", "revise", "change_venue"}:
        hard.append(f"decision must be submit/revise/change_venue, got {a['decision']!r}")
    if decision == "submit" and (blockers or band.startswith("weak")):
        hard.append(f"decision=submit but band={band}; resolve blockers or revise")
    if decision == "submit" and band == "borderline" and not a.get("rebuttal_plan"):
        warn.append("borderline + submit without rebuttal_plan")
    if args.strict:
        hard.extend(warn)
        warn = []

    print(f"# Acceptance memo — {a.get('venue')} {a.get('year', '')}".rstrip())
    print(f"\nReadiness mean: {mean:.2f}/4")
    for d in DIMS:
        print(f"- {d}: {rd.get(d)}")
    print(f"- venue fit: {fit}/4")
    print(f"- risks: {len(a['risks'])} (BLOCKER={len(blockers)}, MAJOR={majors})")
    print(f"\nBand: {band}")
    print(f"Decision: {decision}")
    if a["risks"]:
        print("\nTop risks:")
        for r in a["risks"]:
            print(f"- [{r['severity']}] {r['risk']}  \n  Mitigation: {r['mitigation']}")
    print("\nNote: this is a risk assessment, not a probability of acceptance.")

    for x in hard:
        print("FAIL " + x)
    for x in warn:
        print("WARN " + x)
    print(f"RESULT: {'PASS' if not hard else 'FAIL'} (hard={len(hard)}, warn={len(warn)})")
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

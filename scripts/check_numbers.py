#!/usr/bin/env python3
"""Verify that canonical numbers appear in the paper and stale values do not.

Config (JSON):
{
  "tolerance": 0.005,
  "entries": [
    {"id": "E1.product.ear", "value": 0.5623, "format": "0.00",
     "source": "data/results/e1.json#...", "files": ["main.tex"],
     "bad_values": ["0.57"]}
  ]
}

Usage:
  python3 check_numbers.py --config paper_state/numbers.json --tex main.tex
  python3 check_numbers.py --config ... --tex main.tex --check-source --root .

Exit codes: 0 pass, 1 mismatch, 2 config/IO error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def fmt(value: float, spec: str | None) -> str:
    """Accept printf-like (0.00) and Python-like (.2f) specs."""
    spec = spec or "0.00"
    m = re.fullmatch(r"0?\.(\d+)f?", spec)
    try:
        if m:
            g = m.group(1)
            prec = len(g) if g.startswith("0") else int(g)
            return f"{float(value):.{prec}f}"
        return format(float(value), spec)
    except (ValueError, TypeError):
        return str(value)


def pattern_for(text: str) -> re.Pattern:
    # Avoid matching 0.56 inside 0.5623 or 10.56
    return re.compile(r"(?<![\d.])" + re.escape(text) + r"(?![\d])")


INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")


def expand(path: Path, root: Path, depth: int = 0, seen: set[Path] | None = None) -> list[Path]:
    """Return the file plus recursively \\input/\\include'd .tex files."""
    seen = seen or set()
    path = path if path.is_absolute() else root / path
    if depth > 5 or path in seen or not path.exists():
        return []
    seen.add(path)
    out = [path]
    text = path.read_text(encoding="utf-8", errors="ignore")
    for m in INPUT_RE.finditer(text):
        inc = m.group(1).strip()
        if not inc.endswith(".tex"):
            inc += ".tex"
        out.extend(expand(Path(inc), path.parent, depth + 1, seen))
    return out


def find_lines(path: Path, pat: re.Pattern, ctx: re.Pattern | None = None) -> list[int]:
    hits = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if pat.search(line) and (ctx is None or ctx.search(line)):
            hits.append(i)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--tex", nargs="*", default=["main.tex"])
    ap.add_argument("--root", default=".")
    ap.add_argument("--check-source", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    try:
        cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"CONFIG ERROR: {e}", file=sys.stderr)
        return 2

    entries = cfg.get("entries", [])
    if not entries:
        print("CONFIG ERROR: no entries", file=sys.stderr)
        return 2

    tolerances = float(cfg.get("tolerance", 0.005))
    targets = [Path(t) if Path(t).is_absolute() else root / t for t in args.tex]
    for t in targets:
        if not t.exists():
            print(f"IO ERROR: missing tex file {t}", file=sys.stderr)
            return 2

    results = []
    failed = 0

    for e in entries:
        eid = e.get("id", "<unnamed>")
        expected = fmt(e.get("value"), e.get("format"))
        files = e.get("files") or [str(t) for t in targets]
        pat = pattern_for(expected)
        ctx = re.compile(e["context"]) if e.get("context") else None
        hits = {}
        expanded: list[Path] = []
        for f in files:
            expanded.extend(expand(Path(f), root))
        for p in dict.fromkeys(expanded):
            ln = find_lines(p, pat, ctx)
            if ln:
                hits[str(p)] = ln

        bad_hits = []
        for bad in e.get("bad_values", []) or []:
            bpat = pattern_for(str(bad))
            for p in dict.fromkeys(expanded):
                if p.exists():
                    for ln in find_lines(p, bpat):
                        bad_hits.append((str(p), ln, str(bad)))

        source = e.get("source")
        source_ok = True
        if args.check_source and source:
            src = source.split("#", 1)[0]
            sp = Path(src) if Path(src).is_absolute() else root / src
            source_ok = sp.exists()

        ok = bool(hits) and not bad_hits and source_ok
        if not ok:
            failed += 1
        results.append(
            {
                "id": eid,
                "expected": expected,
                "value": e.get("value"),
                "hits": hits,
                "bad_hits": bad_hits,
                "source": source,
                "source_ok": source_ok,
                "ok": ok,
            }
        )

    if args.json:
        print(json.dumps({"ok": failed == 0, "failed": failed, "results": results}, indent=2))
    else:
        print(f"check_numbers: {len(entries)} entries, tolerance={tolerances}")
        for r in results:
            if r["ok"]:
                where = ", ".join(f"{k}:{v[0]}" for k, v in list(r["hits"].items())[:3])
                print(f"  PASS {r['id']}: {r['expected']} ({where})")
            else:
                print(f"  FAIL {r['id']}: expected {r['expected']}")
                if not r["hits"]:
                    print("       - not found in target files")
                if not r["source_ok"]:
                    print(f"       - source missing: {r['source']}")
                for p, ln, bad in r["bad_hits"]:
                    print(f"       - stale value {bad} at {p}:{ln}")
        print(f"RESULT: {'PASS' if failed == 0 else 'FAIL'} ({failed} failed)")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Anonymity / identity / secret scan for a paper source tree.

Usage:
  python3 check_anonymity.py --root . --names "Alice,Bob" --institutions "MIT"
  python3 check_anonymity.py --root . --config paper_state/anonymity.json --strict

Config JSON (optional):
{"names": [...], "institutions": [...], "allow": ["regex", ...],
 "strict_urls": false}

Exit codes: 0 pass, 1 hard hit, 2 IO error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
CODE_HOST_RE = re.compile(r"(?:github|gitlab|bitbucket)\.com/[\w./-]+", re.I)
URL_RE = re.compile(r"https?://[^\s}\)]+", re.I)
PHRASES = [
    r"our (?:previous|prior|earlier) work",
    r"we (?:previously|earlier) (?:showed|proposed|introduced)",
    r"in our (?:earlier|prior) (?:paper|study)",
    r"acknowledg",
    r"grant (?:no|number|#)",
    r"funded by",
]
AUTHOR_RE = re.compile(r"\\author\{([^}]*)\}", re.S)


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        cut = None
        for i, ch in enumerate(line):
            if ch == "%" and (i == 0 or line[i - 1] != "\\"):
                cut = i
                break
        out.append(line if cut is None else line[:cut])
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--tex", nargs="*", default=None,
                    help="files to scan; default: all *.tex under root (excluding paper_state)")
    ap.add_argument("--names", default="")
    ap.add_argument("--institutions", default="")
    ap.add_argument("--extra", nargs="*", default=[],
                    help="extra files/dirs to scan (e.g. code/, scripts/)")
    ap.add_argument("--config", default=None)
    ap.add_argument("--strict", action="store_true", help="URLs become failures")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"IO ERROR: missing root {root}", file=sys.stderr)
        return 2

    names = [x.strip() for x in args.names.split(",") if x.strip()]
    insts = [x.strip() for x in args.institutions.split(",") if x.strip()]
    allow: list[str] = []
    strict_urls = args.strict
    if args.config:
        try:
            cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
            names += cfg.get("names", [])
            insts += cfg.get("institutions", [])
            allow += cfg.get("allow", [])
            strict_urls = strict_urls or bool(cfg.get("strict_urls", False))
        except Exception as e:  # noqa: BLE001
            print(f"CONFIG ERROR: {e}", file=sys.stderr)
            return 2

    files = []
    if args.tex:
        files = []
        for x in args.tex:
            q = Path(x)
            if not q.is_absolute():
                cand = Path.cwd() / q
                q = cand if cand.exists() else (root / q)
            files.append(q)
    else:
        # Prefer the manuscript; scanning templates/tmp produces false positives.
        preferred = [root / "main.tex", root / "supplement.tex"]
        files = [p for p in preferred if p.exists()]
        if not files:
            files = [p for p in root.rglob("*.tex") if "paper_state" not in p.parts]
    TEXT_EXT = {".py", ".sh", ".md", ".txt", ".json", ".yaml", ".yml", ".bib", ".tex", ".cfg", ".ini"}
    for x in args.extra:
        q = Path(x)
        if not q.is_absolute():
            cand = Path.cwd() / q
            q = cand if cand.exists() else (root / q)
        if q.is_dir():
            files.extend(p for p in q.rglob("*") if p.is_file() and p.suffix in TEXT_EXT)
        elif q.is_file():
            files.append(q)
    files = list(dict.fromkeys(p for p in files if p.exists()))
    if not files:
        print("IO ERROR: no .tex files", file=sys.stderr)
        return 2

    name_res = [re.compile(r"\b" + re.escape(n) + r"\b", re.I) for n in names]
    inst_res = [re.compile(r"\b" + re.escape(i) + r"\b", re.I) for i in insts]
    allow_res = [re.compile(a, re.I) for a in allow]

    hard, warn = [], []
    for p in files:
        text = strip_comments(p.read_text(encoding="utf-8", errors="ignore"))
        for i, line in enumerate(text.splitlines(), 1):
            if any(r.search(line) for r in allow_res):
                continue
            loc = f"{p}:{i}"
            if EMAIL_RE.search(line):
                hard.append(f"{loc}: email address")
            if CODE_HOST_RE.search(line):
                hard.append(f"{loc}: code-host URL")
            for phrase in PHRASES:
                if re.search(phrase, line, re.I):
                    hard.append(f"{loc}: identity phrase /{phrase}/")
            for r in name_res:
                if r.search(line):
                    hard.append(f"{loc}: author name /{r.pattern}/")
            for r in inst_res:
                if r.search(line):
                    hard.append(f"{loc}: institution /{r.pattern}/")
            if URL_RE.search(line):
                (hard if strict_urls else warn).append(f"{loc}: URL (check allow-list)")

    # \author{} must be anonymous/empty
    joined = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
    for m in AUTHOR_RE.finditer(joined):
        content = re.sub(r"\s+", " ", m.group(1)).strip()
        if content and "anonymous" not in content.lower():
            hard.append(f"\\author{{...}} is not anonymous: {content[:80]}")

    for x in hard:
        print("FAIL " + x)
    for x in warn:
        print("WARN " + x)
    print(f"RESULT: {'PASS' if not hard else 'FAIL'} (files={len(files)}, hard={len(hard)}, warn={len(warn)})")
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

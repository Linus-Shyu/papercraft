#!/usr/bin/env python3
"""Structural citation audit: cited keys, duplicates, required fields, ID formats.

Usage:
  python3 check_citations.py --tex main.tex --bib references.bib
  python3 check_citations.py --tex main.tex --bib references.bib --strict

Exit codes: 0 pass, 1 hard failure, 2 IO error.
Note: this does NOT verify metadata online. Open the DOI/arXiv yourself and
record it in paper_state/citation-audit.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CITE_RE = re.compile(r"\\cite[a-zA-Z]*\*?\s*\{([^}]*)\}")
ENTRY_START = re.compile(r"@([a-zA-Z]+)\s*\{\s*([^,\s]+)\s*,")
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(v\d+)?", re.I)
ARXIV_URL_RE = re.compile(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", re.I)
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s}\"']+")
REQUIRED = {
    "article": ("author", "title", "journal", "year"),
    "inproceedings": ("author", "title", "booktitle", "year"),
    "conference": ("author", "title", "booktitle", "year"),
    "book": ("author", "title", "publisher", "year"),
    "misc": ("author", "title", "year"),
    "online": ("author", "title", "year", "url"),
}


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


def read_braced(text: str, start: int) -> tuple[str, int]:
    """text[start] == '{'; return (inner, index_after_close)."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
    return text[start + 1 :], len(text)


def parse_bib(text: str) -> list[dict]:
    entries = []
    i = 0
    while True:
        m = ENTRY_START.search(text, i)
        if not m:
            break
        etype, key = m.group(1).lower(), m.group(2)
        # the entry opens at the first "{" after "@type"
        entry_brace = text.find("{", m.start())
        if entry_brace < 0:
            break
        body, end = read_braced(text, entry_brace)
        # body = "key, field={...}, ..."; drop the key
        comma = body.find(",")
        body = body[comma + 1:] if comma >= 0 else ""
        fields = {}
        pos = 0
        field_re = re.compile(r"([a-zA-Z]+)\s*=\s*")
        while True:
            fm = field_re.search(body, pos)
            if not fm:
                break
            name = fm.group(1).lower()
            j = fm.end()
            while j < len(body) and body[j] in " \t\r\n":
                j += 1
            if j >= len(body):
                break
            if body[j] == "{":
                val, j = read_braced(body, j)
            elif body[j] == '"':
                k = body.find('"', j + 1)
                val = body[j + 1 : k if k >= 0 else len(body)]
                j = (k + 1) if k >= 0 else len(body)
            else:
                k = body.find(",", j)
                val = body[j : k if k >= 0 else len(body)].strip()
                j = (k + 1) if k >= 0 else len(body)
            fields[name] = re.sub(r"\s+", " ", val).strip()
            pos = j
        entries.append({"type": etype, "key": key, "fields": fields})
        i = end
    return entries


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", nargs="+", default=["main.tex"])
    ap.add_argument("--bib", default="references.bib")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet-uncited", action="store_true")
    args = ap.parse_args()

    tex_paths = [Path(t) for t in args.tex]
    bib_path = Path(args.bib)
    for p in tex_paths + [bib_path]:
        if not p.exists():
            print(f"IO ERROR: missing {p}", file=sys.stderr)
            return 2

    cited: dict[str, list[str]] = {}
    for p in tex_paths:
        text = strip_comments(p.read_text(encoding="utf-8", errors="ignore"))
        for m in CITE_RE.finditer(text):
            for key in m.group(1).split(","):
                key = key.strip()
                if key and not key.startswith("*"):
                    cited.setdefault(key, []).append(str(p))

    entries = parse_bib(bib_path.read_text(encoding="utf-8", errors="ignore"))
    by_key: dict[str, list[dict]] = {}
    for e in entries:
        by_key.setdefault(e["key"], []).append(e)

    hard: list[str] = []
    warn: list[str] = []
    info: list[str] = []

    for key in sorted(cited):
        if key not in by_key:
            hard.append(f"cited but missing from bib: {key} (in {', '.join(sorted(set(cited[key])))})")

    for key, es in by_key.items():
        if len(es) > 1:
            hard.append(f"duplicate bib key: {key} ({len(es)} entries)")

    for e in entries:
        key, etype, f = e["key"], e["type"], e["fields"]
        req = REQUIRED.get(etype, ("author", "title", "year"))
        missing = [r for r in req if r not in f or not f[r]]
        if missing:
            msg = f"{key}: missing required field(s): {', '.join(missing)} ({etype})"
            (hard if args.strict else warn).append(msg)

        blob = " ".join(f.values())
        ids = ARXIV_RE.findall(blob) + ARXIV_URL_RE.findall(blob)
        for ident in ids:
            val = ident[0] if isinstance(ident, tuple) else ident
            if not re.fullmatch(r"\d{4}\.\d{4,5}", val):
                warn.append(f"{key}: suspicious arXiv id: {val}")
        if "arxiv" in blob.lower() and not ids and "arxiv" in f.get("journal", "").lower():
            warn.append(f"{key}: arXiv mentioned but no parsable id")

        doi = f.get("doi", "")
        if doi and not DOI_RE.search(doi):
            warn.append(f"{key}: suspicious DOI: {doi}")
        if args.strict and ("booktitle" in f or "journal" in f) and not (doi or ids):
            info.append(f"{key}: no DOI/arXiv recorded (optional)")

    uncited = [k for k in by_key if k not in cited]
    if not args.quiet_uncited:
        for k in sorted(uncited):
            info.append(f"uncited bib entry (OK if intentional): {k}")

    for m in hard:
        print(f"FAIL {m}")
    for m in warn:
        print(f"WARN {m}")
    for m in info:
        print(f"INFO {m}")
    print(
        f"RESULT: {'PASS' if not hard else 'FAIL'} "
        f"(cited={len(cited)}, bib={len(entries)}, hard={len(hard)}, warn={len(warn)})"
    )
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

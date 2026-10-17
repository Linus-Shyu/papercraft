#!/usr/bin/env python3
"""Float hygiene: labels, refs, captions, graphics, and orphan floats.

Usage:
  python3 check_floats.py --tex main.tex [--root .] [--ignore-prefix eq:]

Parses \\input/\\include recursively; resolves \\graphicspath.
Exit codes: 0 pass, 1 hard failure, 2 IO error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]*)\}")
FIG_RE = re.compile(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", re.S)
TAB_RE = re.compile(r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}", re.S)
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
GRAPHICSPATH_RE = re.compile(r"\\graphicspath\{((?:\{[^}]*\})+)\}")
EXTS = (".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg")


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


def expand(path: Path, root: Path, depth: int = 0, seen: set[Path] | None = None) -> str:
    seen = seen or set()
    path = path if path.is_absolute() else root / path
    if depth > 5 or path in seen or not path.exists():
        return ""
    seen.add(path)
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    for m in INPUT_RE.finditer(text):
        inc = m.group(1).strip()
        if not inc.endswith(".tex"):
            inc += ".tex"
        text += "\n" + expand(Path(inc), path.parent, depth + 1, seen)
    return text


def resolve_graphic(name: str, tex_dir: Path, gpaths: list[Path]) -> Path | None:
    candidates = []
    p = Path(name)
    if p.is_absolute():
        candidates.append(p)
    else:
        candidates.extend(tex_dir / name for _ in [0])
        candidates.extend(g / name for g in gpaths)
        candidates.append(tex_dir / name)
    for c in candidates:
        if c.exists():
            return c
        if not c.suffix:
            for ext in EXTS:
                if c.with_suffix(ext).exists():
                    return c.with_suffix(ext)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default="main.tex")
    ap.add_argument("--root", default=".")
    ap.add_argument("--ignore-prefix", nargs="*", default=["eq:"])
    args = ap.parse_args()

    root = Path(args.root).resolve()
    tex = Path(args.tex)
    if not tex.is_absolute():
        cand = (Path.cwd() / tex)
        tex = cand if cand.exists() else (root / tex)
    if not tex.exists():
        print(f"IO ERROR: missing {tex}", file=sys.stderr)
        return 2

    text = expand(tex, root)
    tex_dir = tex.parent
    gpaths = []
    for m in GRAPHICSPATH_RE.finditer(text):
        for g in re.findall(r"\{([^}]*)\}", m.group(1)):
            gpaths.append((tex_dir / g).resolve())
    if not gpaths:
        gpaths = [tex_dir]

    labels = set(LABEL_RE.findall(text))
    refs: dict[str, int] = {}
    for m in REF_RE.finditer(text):
        for r in m.group(1).split(","):
            r = r.strip()
            if r:
                refs[r] = refs.get(r, 0) + 1

    hard, warn = [], []

    # floats
    for kind, rx in (("figure", FIG_RE), ("table", TAB_RE)):
        for m in rx.finditer(text):
            body = m.group(1)
            lab = LABEL_RE.search(body)
            cap = "\\caption" in body
            if kind == "figure" and not lab:
                hard.append("figure without \\label" + (" (also no caption)" if not cap else ""))
            if kind == "figure" and not cap:
                hard.append(f"figure {lab.group(1) if lab else '<no-label>'} without \\caption")
            if kind == "table" and not cap:
                warn.append(f"table {lab.group(1) if lab else '<no-label>'} without \\caption")

    # orphan labels (figure/table only)
    for lab in sorted(labels):
        if any(lab.startswith(p) for p in args.ignore_prefix):
            continue
        if lab.startswith(("fig:", "tab:")) and lab not in refs:
            hard.append(f"label never referenced: {lab}")

    # refs without labels
    for r, n in sorted(refs.items()):
        if any(r.startswith(p) for p in args.ignore_prefix):
            continue
        if r not in labels:
            hard.append(f"\\ref to undefined label: {r} ({n}×)")

    # graphics
    for m in GRAPHICS_RE.finditer(text):
        name = m.group(1).strip()
        if resolve_graphic(name, tex_dir, gpaths) is None:
            hard.append(f"missing graphics file: {name}")

    for x in hard:
        print("FAIL " + x)
    for x in warn:
        print("WARN " + x)
    print(
        f"RESULT: {'PASS' if not hard else 'FAIL'} "
        f"(labels={len(labels)}, refs={sum(refs.values())}, hard={len(hard)}, warn={len(warn)})"
    )
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

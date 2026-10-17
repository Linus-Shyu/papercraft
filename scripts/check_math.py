#!/usr/bin/env python3
"""Math audit: labels/refs, delimiter balance, symbol coverage, numeric checks.

This does NOT prove a derivation. It catches undefined symbols, duplicate/
unreferenced equation labels, unbalanced delimiters, and arithmetic slips listed
in math.json.

Usage:
  python3 check_math.py --tex main.tex --config paper_state/math.json
  python3 check_math.py --tex main.tex --config ... --strict --list

Exit codes: 0 pass, 1 failure, 2 IO/config.
"""
from __future__ import annotations

import argparse
import ast
import json
import operator
import re
import sys
from pathlib import Path

ENV_RE = re.compile(
    r"\\begin\{(equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|eqnarray\*?)\}(.*?)\\end\{\1\}",
    re.S,
)
BRACKET_RE = re.compile(r"\\\[(.*?)\\\]", re.S)
DOLLAR_RE = re.compile(r"\$\$(.*?)\$\$", re.S)
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
CMD_RE = re.compile(r"\\([A-Za-z]+)")

BUILTIN = {
    "begin", "end", "frac", "dfrac", "tfrac", "sqrt", "sum", "prod", "int", "lim",
    "left", "right", "big", "Big", "bigg", "Bigg", "cdot", "cdots", "ldots", "dots",
    "times", "div", "pm", "mp", "le", "leq", "ge", "geq", "neq", "approx", "sim",
    "in", "notin", "subset", "subseteq", "cup", "cap", "emptyset", "varnothing",
    "forall", "exists", "mid", "top", "bot", "to", "rightarrow", "leftarrow",
    "mathbb", "mathcal", "mathrm", "operatorname", "text", "textbf", "textit",
    "hat", "bar", "tilde", "overline", "underline", "partial", "nabla", "infty",
    "alpha", "beta", "gamma", "delta", "epsilon", "theta", "lambda", "mu", "pi",
    "rho", "sigma", "tau", "phi", "psi", "omega", "Delta", "Sigma", "Omega",
    "quad", "qquad", "label", "tag", "nonumber", "notag", "hspace", "vspace",
    "color", "textcolor", "boxed", "displaystyle", "scriptstyle", "mathstrut",
    "uparrow", "downarrow", "top", "bot", "langle", "rangle", "lceil", "rceil",
    "lfloor", "rfloor", "vert", "Vert", "star", "ast", "circ", "bullet",
}

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
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


def expand(path: Path, depth: int = 0, seen: set[Path] | None = None) -> str:
    seen = seen or set()
    path = path.resolve()
    if depth > 5 or path in seen or not path.exists():
        return ""
    seen.add(path)
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    for m in INPUT_RE.finditer(text):
        inc = m.group(1).strip()
        if not inc.endswith(".tex"):
            inc += ".tex"
        child = path.parent / inc
        text += "\n" + expand(child, depth + 1, seen)
    return text


def eval_expr(expr: str) -> float:
    node = ast.parse(expr, mode="eval").body

    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return float(n.value)
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.operand))
        raise ValueError(f"unsupported expression: {ast.dump(n)}")

    return ev(node)


def find_blocks(text: str) -> list[tuple[str, str, int]]:
    blocks = []
    for m in ENV_RE.finditer(text):
        line = text[: m.start()].count("\n") + 1
        blocks.append((m.group(1), m.group(2), line))
    for rx in (BRACKET_RE, DOLLAR_RE):
        for m in rx.finditer(text):
            line = text[: m.start()].count("\n") + 1
            blocks.append(("display", m.group(1), line))
    return sorted(blocks, key=lambda x: x[2])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", default="main.tex")
    ap.add_argument("--config", default=None)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    tex = Path(args.tex)
    if not tex.is_absolute():
        cand = Path.cwd() / tex
        tex = cand if cand.exists() else root / tex
    if not tex.exists():
        print(f"IO ERROR: missing {tex}", file=sys.stderr)
        return 2

    cfg = {}
    if args.config:
        try:
            cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"CONFIG ERROR: {e}", file=sys.stderr)
            return 2

    text = expand(tex)
    blocks = find_blocks(text)
    labels = LABEL_RE.findall(text)
    refs = set()
    for m in REF_RE.finditer(text):
        for r in m.group(1).split(","):
            refs.add(r.strip())

    hard, warn = [], []

    dup = {x for x in labels if labels.count(x) > 1}
    for d in dup:
        hard.append(f"duplicate label: {d}")

    eq_labels = [x for x in labels if x.startswith("eq:")]
    for lab in eq_labels:
        if lab not in refs:
            (hard if args.strict else warn).append(f"equation label never referenced: {lab}")

    for env, body, line in blocks:
        if body.count(r"\left") != body.count(r"\right"):
            hard.append(f"line {line}: unbalanced \\left/\\right in {env}")
        if body.count("{") != body.count("}"):
            hard.append(f"line {line}: unbalanced braces in {env}")
        begins = re.findall(r"\\begin\{([^}]*)\}", body)
        ends = re.findall(r"\\end\{([^}]*)\}", body)
        if sorted(begins) != sorted(ends):
            hard.append(f"line {line}: \\begin/\\end mismatch in {env}")
        if args.list:
            first = " ".join(body.split())[:120]
            print(f"  [{line}] {env}: {first}")

    for chk in cfg.get("numeric", []):
        try:
            got = eval_expr(chk["expr"])
            exp = float(chk["expected"])
            tol = float(chk.get("tolerance", 1e-9))
            if abs(got - exp) > tol:
                hard.append(f"numeric {chk.get('id', chk['expr'])}: {chk['expr']} = {got}, expected {exp}")
        except Exception as e:  # noqa: BLE001
            hard.append(f"numeric {chk.get('id', '?')}: cannot evaluate ({e})")

    symbols = set(cfg.get("symbols", {}).keys())
    allow = set(cfg.get("allow", [])) | BUILTIN
    unknown = set()
    for env, body, line in blocks:
        cleaned = re.sub(r"\\(?:text|mathrm|operatorname)\{[^}]*\}", " ", body)
        cleaned = re.sub(r"\\(?:label|tag)\{[^}]*\}", " ", cleaned)
        for cmd in CMD_RE.findall(cleaned):
            if cmd not in allow and cmd not in symbols:
                unknown.add("\\" + cmd)
        for base in re.findall(r"([A-Za-z])_\{?[A-Za-z0-9]+\}?", cleaned):
            if base not in symbols and base not in allow:
                unknown.add(base)
        for tok in re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", cleaned):
            if tok not in symbols and tok not in allow:
                unknown.add(tok)

    for u in sorted(unknown):
        (hard if args.strict else warn).append(f"symbol not in math.json: {u}")
    for s in sorted(symbols):
        if s and s not in text:
            warn.append(f"declared symbol never appears: {s}")

    for m in hard:
        print("FAIL " + m)
    for m in warn:
        print("WARN " + m)
    print(f"SUMMARY: equations={len(blocks)}, labels={len(labels)}, eq_labels={len(eq_labels)}, unknown_symbols={len(unknown)}")
    print(f"RESULT: {'PASS' if not hard else 'FAIL'} (hard={len(hard)}, warn={len(warn)})")
    return 0 if not hard else 1


if __name__ == "__main__":
    raise SystemExit(main())

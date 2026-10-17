#!/usr/bin/env python3
"""Papercraft CLI — scaffold and drive the autopilot pipeline.

Usage:
  ./papercraft new --topic "..." --venue aaai --dir ./my-paper
  ./papercraft status [--dir .]
  ./papercraft next [--dir .]
  ./papercraft mark survey done --note "12 rows" [--dir .]
  ./papercraft check [--dir .] [--with-repro] [--no-build]
  ./papercraft package [--dir .] [--artifact]
  ./papercraft list-venues
  ./papercraft doctor

Exit codes: 0 ok, 1 failure, 2 usage/IO.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import signal
import tempfile
import zipfile
from pathlib import Path

try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

SRC = Path(__file__).resolve().parents[1]
TEMPLATES = SRC / "templates"

STAGES = [
    ("topic", "Topic → falsifiable RQ", "G0"),
    ("survey", "Literature survey + matrix", "G3b"),
    ("feasibility", "MPU + go/no-go", "G0"),
    ("design", "Experiment cards + controls", "G2/G8"),
    ("execute", "Run experiments, record hashes", "G8"),
    ("template", "Fetch/verify official template", "G6"),
    ("write", "Draft LaTeX from ledger", "G1-G4"),
    ("audit", "Run all gates, fix blockers", "G2-G8"),
    ("review", "3 reviewer personas + scores", "G9"),
    ("acceptance", "Risk memo + band", "G10"),
    ("package", "PDF + source/artifact zip", "G11"),
]

PROMPTS = {
    "topic": "Propose 3 falsifiable RQs; pick one or ask H1; write paper_state/rq.md.",
    "survey": "Search/screen/verify; fill literature-matrix.csv; closest-3 + delta; run check_literature.",
    "feasibility": "Write MPU, resources, go/no-go; stop if impossible; H2 if risky.",
    "design": "Write experiment cards; fix baselines/controls/seeds/decision rules.",
    "execute": "Implement + run; record command/output/sha256; run check_repro --run.",
    "template": "papercraft template --venue <id> --url <official-kit> (or --archive); verify TEMPLATE.md.",
    "write": "Draft main.tex from claims + numbers; generate tables/figures.",
    "audit": "bash scripts/audit.sh <dir> <dir>/paper_state --with-repro; fix blockers.",
    "review": "3 personas; fill review-score.json; run score_review.",
    "acceptance": "Fill acceptance.json; run score_acceptance; pre-mortem; H3.",
    "package": "Build in /tmp; check anonymity; create submission/.",
}


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def load_plan(root: Path) -> dict:
    p = root / "paper_state/plan.json"
    if not p.exists():
        raise SystemExit(f"not a papercraft project (missing {p})")
    return json.loads(p.read_text(encoding="utf-8"))


def save_plan(root: Path, plan: dict) -> None:
    p = root / "paper_state/plan.json"
    p.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def default_plan(topic: str, venue: str, assumptions: list[str]) -> dict:
    return {
        "topic": topic,
        "venue": venue,
        "created": now(),
        "assumptions": assumptions,
        "current": "topic",
        "log": [],
        "stages": [
            {"id": sid, "title": title, "gate": gate, "status": "pending", "note": ""}
            for sid, title, gate in STAGES
        ],
    }


def template_text(name: str) -> str:
    p = TEMPLATES / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


def main_tex(topic: str, venue: str) -> str:
    return rf"""% TODO: replace this generic skeleton with the official {venue} template
% (see conferences/{venue}.md; verify the CFP before writing).
\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{booktabs}}
\usepackage{{amsmath,amssymb}}
\usepackage{{graphicx}}
\usepackage{{hyperref}}
\title{{{topic}}}
\author{{Anonymous}}
\date{{}}
\begin{{document}}
\maketitle
\begin{{abstract}}
TODO: 5 sentences — problem, gap, object, evidence, boundary. No number without a source.
\end{{abstract}}

\section{{Introduction}}
TODO: concrete failure, gap, object, evidence preview, non-claims.
\label{{sec:intro}}

\section{{Related Work}}
TODO: closest-3 table; one-sentence delta.
\label{{sec:related}}

\section{{Method}}
TODO: notation table, definitions, assumptions, aggregation level.
\label{{sec:method}}

\section{{Experiments}}
TODO: baselines, controls, splits, n, seeds, metrics, decision rules.
\label{{sec:experiments}}

\section{{Results}}
TODO: claim → evidence → alternative → control → boundary.
\label{{sec:results}}

\section{{Limitations}}
TODO: specific (n, domain, construct validity, external validity).
\label{{sec:limitations}}

\section{{Conclusion}}
TODO: object + strongest evidence + boundary. No new claims.
\label{{sec:conclusion}}

\bibliographystyle{{plain}}
\bibliography{{refs}}
\end{{document}}
"""


def write_empty_state(root: Path, venue: str) -> None:
    ps = root / "paper_state"
    ps.mkdir(parents=True, exist_ok=True)
    (ps / "numbers.json").write_text(json.dumps({"tolerance": 0.005, "entries": []}, indent=2) + "\n", encoding="utf-8")
    (ps / "math.json").write_text(json.dumps({"symbols": {}, "allow": [], "numeric": []}, indent=2) + "\n", encoding="utf-8")
    (ps / "repro-manifest.json").write_text(json.dumps({"timeout": 300, "entries": []}, indent=2) + "\n", encoding="utf-8")
    (ps / "acceptance.json").write_text(
        json.dumps({"venue": venue, "year": None, "readiness": {}, "fit": None, "risks": [], "decision": "revise"}, indent=2) + "\n",
        encoding="utf-8",
    )
    (ps / "review-score.json").write_text(
        json.dumps({"paper_id": "<id>", "reviewer": "R1", "summary": "", "claims": [], "strengths": [], "weaknesses": [], "scores": {}, "overall": 0, "confidence": 0, "recommendation": "borderline"}, indent=2) + "\n",
        encoding="utf-8",
    )
    lit = template_text("literature-matrix.csv")
    header = lit.splitlines()[0] if lit else "key,title,year,venue,role,closest,verified,claim_supported,gap,notes"
    (ps / "literature-matrix.csv").write_text(header + "\n", encoding="utf-8")
    for name in ("claim-ledger.csv", "experiment-registry.csv", "figure-registry.csv"):
        src = TEMPLATES / name
        if src.exists():
            header = src.read_text(encoding="utf-8").splitlines()[0]
            (ps / name).write_text(header + "\n", encoding="utf-8")
        else:
            (ps / name).write_text("", encoding="utf-8")
    (ps / "conference.yaml").write_text(
        f"id: {venue}\nyear: null\nsource_url: VERIFY\nverified_on: null\nstatus: UNVERIFIED\n",
        encoding="utf-8",
    )
    (ps / "rq.md").write_text("# Research question\n\nTODO: claim, falsifier, closest 2, risk.\n", encoding="utf-8")


def cmd_new(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    if root.exists() and any(root.iterdir()) and not args.force:
        print(f"ERROR: {root} exists and is not empty (use --force)", file=sys.stderr)
        return 1
    root.mkdir(parents=True, exist_ok=True)
    (root / "data/results").mkdir(parents=True, exist_ok=True)
    (root / "figures").mkdir(parents=True, exist_ok=True)
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "main.tex").write_text(main_tex(args.topic, args.venue), encoding="utf-8")
    (root / "refs.bib").write_text("", encoding="utf-8")
    (root / ".gitignore").write_text("*.aux\n*.log\n*.out\n*.bbl\n*.blg\n*.synctex.gz\n.env\nsubmission/\n", encoding="utf-8")
    (root / "README.md").write_text(
        f"# {args.topic}\n\nCreated by Papercraft on {now()}.\n\n"
        "Next: read `AUTOPILOT.md`, then run `papercraft status` / `papercraft next`.\n",
        encoding="utf-8",
    )
    write_empty_state(root, args.venue)
    assumptions = [f"venue={args.venue}", "compute=CPU-only", "data=public"]
    save_plan(root, default_plan(args.topic, args.venue, assumptions))
    if getattr(args, "fetch_template", False):
        rc = subprocess.call([
            "python3", str(SRC / "scripts/fetch_template.py"),
            "--venue", args.venue, "--dir", str(root),
        ])
        if rc != 0:
            print("template pending: run `papercraft template --venue ... --url <official-kit>`")
    print(f"created {root}")
    print(f"  main.tex  refs.bib  paper_state/  data/results/  figures/")
    print(f"  venue={args.venue} (profile UNVERIFIED; verify the CFP)")
    print("\nNext:")
    print(f"  cd {root}")
    print(f"  python3 {SRC}/scripts/papercraft.py status")
    print(f"  python3 {SRC}/scripts/papercraft.py next")
    return 0


def cmd_status(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    plan = load_plan(root)
    print(f"Project: {plan.get('topic')}")
    print(f"Venue:   {plan.get('venue')} (verify CFP)")
    print(f"Created: {plan.get('created')}")
    if plan.get("assumptions"):
        print("Assumptions: " + "; ".join(plan["assumptions"]))
    print("\n| Stage | Status | Gate | Note |")
    print("|---|---|---|---|")
    for s in plan["stages"]:
        print(f"| {s['id']} | {s['status']} | {s['gate']} | {s['note'][:60]} |")
    cur = next((s for s in plan["stages"] if s["status"] in ("pending", "in_progress", "blocked")), None)
    print("\nNext: " + (f"{cur['id']} — {cur['title']}" if cur else "all stages done"))
    return 0


def cmd_next(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    plan = load_plan(root)
    cur = next((s for s in plan["stages"] if s["status"] in ("pending", "in_progress", "blocked")), None)
    if not cur:
        print("ALL STAGES DONE. Run `papercraft package` and H3 approval.")
        return 0
    print(f"STAGE: {cur['id']} — {cur['title']} (gate {cur['gate']})")
    print(f"STATUS: {cur['status']}")
    print(f"ACTION: {PROMPTS[cur['id']]}")
    print(f"\nUpdate when done:\n  python3 {SRC}/scripts/papercraft.py mark {cur['id']} done --note \"...\"")
    return 0


def cmd_mark(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    plan = load_plan(root)
    stage = next((s for s in plan["stages"] if s["id"] == args.stage), None)
    if not stage:
        print(f"ERROR: unknown stage {args.stage}", file=sys.stderr)
        return 2
    stage["status"] = args.status
    if args.note:
        stage["note"] = args.note
    plan.setdefault("log", []).append({"ts": now(), "stage": args.stage, "status": args.status, "note": args.note or ""})
    if args.status == "done":
        plan["current"] = next((s["id"] for s in plan["stages"] if s["status"] in ("pending", "in_progress", "blocked")), "done")
    save_plan(root, plan)
    print(f"{args.stage} -> {args.status}")
    return 0


def cmd_check(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    if not (root / "main.tex").exists():
        print("ERROR: main.tex missing", file=sys.stderr)
        return 2
    cmd = ["bash", str(SRC / "scripts/audit.sh"), str(root), str(root / "paper_state")]
    if args.with_repro:
        cmd.append("--with-repro")
    if args.no_build:
        cmd.append("--no-build")
    print(" ".join(cmd))
    return subprocess.call(cmd)


def build_in_place(root: Path) -> int:
    """Compile in root (a temp copy), leaving main.pdf there."""
    log = root / "build.log"
    with log.open("w", encoding="utf-8") as f:
        for cmd in (
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            ["bibtex", "main"],
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
            ["pdflatex", "-interaction=nonstopmode", "main.tex"],
        ):
            subprocess.run(cmd, cwd=root, stdout=f, stderr=subprocess.STDOUT, timeout=300)
    text = log.read_text(encoding="utf-8", errors="ignore")
    bad = re.search(
        r"LaTeX Error|Undefined control sequence|Citation .* undefined|There were undefined references",
        text,
    ) is not None
    return 0 if (root / "main.pdf").exists() and not bad else 1


def cmd_package(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    if not (root / "main.tex").exists():
        print("ERROR: main.tex missing", file=sys.stderr)
        return 2
    if not args.skip_check:
        rc = subprocess.call([
            "bash", str(SRC / "scripts/audit.sh"), str(root),
            str(root / "paper_state"), "--with-repro",
        ])
        if rc != 0:
            print("gates failed; refusing to package (use --skip-check only for drafts)", file=sys.stderr)
            return 1
    anon = subprocess.call([
        "python3", str(SRC / "scripts/check_anonymity.py"),
        "--root", str(root), "--tex", str(root / "main.tex"),
    ])
    if anon != 0:
        print("anonymity check failed; fix before packaging", file=sys.stderr)
        return 1
    out = root / "submission"
    out.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="papercraft-pack-"))
    try:
        shutil.copytree(root, tmp / "repo", ignore=shutil.ignore_patterns(".git", "paper_state", "submission", "tmp", "*.pdf"))
        if build_in_place(tmp / "repo") != 0:
            print("build failed; not packaging (see build.log in the temp copy)", file=sys.stderr)
            return 1
        pdf = tmp / "repo/main.pdf"
        shutil.copy2(pdf, out / "main.pdf")
        # source zip
        with zipfile.ZipFile(out / "source.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for p in (tmp / "repo").rglob("*"):
                if p.is_file() and p.suffix in {".tex", ".bib", ".sty", ".bst", ".cls"}:
                    z.write(p, p.relative_to(tmp / "repo"))
            for d in ("figures", "data"):
                for p in (tmp / "repo" / d).rglob("*"):
                    if p.is_file():
                        z.write(p, p.relative_to(tmp / "repo"))
        if args.artifact:
            with zipfile.ZipFile(out / "artifact.zip", "w", zipfile.ZIP_DEFLATED) as z:
                for d in ("scripts", "code", "data", "figures"):
                    base = tmp / "repo" / d
                    if base.exists():
                        for p in base.rglob("*"):
                            if p.is_file() and p.suffix not in {".aux", ".log", ".pdf"}:
                                z.write(p, p.relative_to(tmp / "repo"))
                for name in ("README.md", "LICENSE"):
                    p = tmp / "repo" / name
                    if p.exists():
                        z.write(p, name)
        # hashes
        with (out / "SHA256SUMS").open("w", encoding="utf-8") as f:
            import hashlib
            for p in sorted(out.iterdir()):
                if p.is_file() and p.name != "SHA256SUMS":
                    f.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n")
        for name in ("review",):
            d = root / name
            if d.is_dir():
                shutil.copytree(d, out / name, dirs_exist_ok=True)
        for name in ("acceptance.md", "paper_state/acceptance.md"):
            p = root / name
            if p.exists():
                shutil.copy2(p, out / "acceptance.md")
        print(f"packaged -> {out}")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cmd_template(args) -> int:
    cmd = ["python3", str(SRC / "scripts/fetch_template.py")]
    if args.list:
        cmd.append("--list")
    else:
        if not args.venue:
            print("ERROR: --venue required (or use --list)", file=sys.stderr)
            return 2
        cmd += ["--venue", args.venue, "--dir", args.dir]
    if getattr(args, "url", None):
        cmd += ["--url", args.url]
    if getattr(args, "archive", None):
        cmd += ["--archive", args.archive]
    if getattr(args, "force", False):
        cmd.append("--force")
    if getattr(args, "allow_http_local", False):
        cmd.append("--allow-http-local")
    print(" ".join(cmd))
    return subprocess.call(cmd)


FIT = SRC / "conferences/fit.json"
REASON_KEYS = {
    "novelty": ("novel", "incremental", "related work", "prior work", "position"),
    "evidence": ("small n", "n=", "baseline", "ablation", "evidence", "significan", "variance", "seed"),
    "scope": ("scope", "fit", "venue", "audience", "out of"),
    "clarity": ("clarity", "writing", "unclear", "confus", "organization"),
    "repro": ("repro", "artifact", "code", "data", "script"),
    "theory": ("math", "proof", "theorem", "derivation", "symbol"),
    "ethics": ("ethic", "consent", "irb", "privacy"),
}


def load_fit() -> dict:
    return json.loads(FIT.read_text(encoding="utf-8"))


def infer_reasons(paths: list[str]) -> set[str]:
    reasons: set[str] = set()
    for path in paths or []:
        p = Path(path)
        if not p.exists() or p.suffix.lower() != ".json":
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for w in data.get("weaknesses", []) or []:
            text = " ".join(str(w.get(k, "")) for k in ("issue", "location", "evidence")).lower()
            for key, words in REASON_KEYS.items():
                if any(x in text for x in words):
                    reasons.add(key)
    return reasons


def cmd_recommend(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    plan = load_plan(root)
    fit = load_fit()
    old = plan.get("venue")
    topic = (plan.get("topic") or "").lower()
    reasons = {r.strip() for r in (args.reasons or "").split(",") if r.strip()}
    reasons |= infer_reasons(args.reviews or [])

    rows = []
    for vid, e in fit.items():
        if vid.startswith("_") or vid == old:
            continue
        score, why = 0, []
        topic_hit = False
        for t in e.get("topics", []):
            if t and t in topic:
                score += 2
                topic_hit = True
                why.append(f"topic:{t}")
        type_hit = args.type in e.get("types", [])
        if type_hit:
            score += 3
            why.append(f"type:{args.type}")
        if not topic_hit and not type_hit and vid != "tmlr":
            continue
        if args.scale in e.get("scale", []):
            score += 1
            why.append(f"scale:{args.scale}")
        for r in sorted(reasons):
            if r in e.get("focus", []):
                score += 2
                why.append(f"review:{r}")
        rows.append((score, vid, why, e.get("notes", "")))
    rows.sort(key=lambda x: (-x[0], x[1]))

    print(f"topic: {plan.get('topic')}")
    print(f"current venue: {old} (excluded)")
    print(f"type={args.type} scale={args.scale} reasons={','.join(sorted(reasons)) or '-'}")
    print("\nShortlist (heuristic; verify every CFP; not an acceptance prediction):")
    for i, (score, vid, why, notes) in enumerate(rows[: args.top], 1):
        print(f"{i}. {vid:8} score={score:2}  why={', '.join(why) or '-'}")
        print(f"   template: papercraft template --venue {vid} --url <official-kit>")
        print(f"   notes: {notes}")
    if args.json:
        print(json.dumps([{"venue": r[1], "score": r[0], "why": r[2], "notes": r[3]} for r in rows[: args.top]], indent=2))
    return 0


def cmd_resubmit(args) -> int:
    root = Path(args.dir).expanduser().resolve()
    plan = load_plan(root)
    old = plan.get("venue")
    new = args.to
    if not new:
        print("ERROR: --to <venue> required", file=sys.stderr)
        return 2
    if new == old:
        print("ERROR: target venue equals current venue", file=sys.stderr)
        return 2
    reasons = {r.strip() for r in (args.reasons or "").split(",") if r.strip()}
    reasons |= infer_reasons(args.reviews or [])

    if args.dry_run:
        print("DRY RUN — no files changed")
        print(f"old: {old} -> new: {new}")
        print(f"reasons: {', '.join(sorted(reasons)) or '-'}")
        print("would archive: root *.sty/*.bst/*.cls + TEMPLATE.md")
        print(f"would fetch: papercraft template --venue {new} [--url/--archive]")
        print("would update: paper_state/conference.yaml, plan.json, RESUBMISSION.md")
        return 0

    tmp = Path(tempfile.mkdtemp(prefix="papercraft-resubmit-"))
    try:
        stage = tmp / "proj"
        (stage / "paper_state").mkdir(parents=True)
        root_cache = root / "paper_state/template-source.json"
        if root_cache.exists():
            shutil.copy2(root_cache, stage / "paper_state/template-source.json")
        cmd = ["python3", str(SRC / "scripts/fetch_template.py"), "--venue", new, "--dir", str(stage)]
        if args.url:
            cmd += ["--url", args.url]
        if args.archive:
            cmd += ["--archive", args.archive]
        if subprocess.call(cmd) != 0:
            print("template fetch failed; old template left untouched", file=sys.stderr)
            return 1

        ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        arch = root / "template" / f"previous-{old}-{ts}"
        arch.mkdir(parents=True, exist_ok=True)
        for suffix in (".sty", ".bst", ".cls"):
            for p in root.glob(f"*{suffix}"):
                shutil.move(str(p), str(arch / p.name))
        if (root / "TEMPLATE.md").exists():
            shutil.move(str(root / "TEMPLATE.md"), str(arch / "TEMPLATE.md"))

        copied = []
        for suffix in (".sty", ".bst", ".cls"):
            for p in stage.glob(f"*{suffix}"):
                shutil.copy2(p, root / p.name)
                copied.append(p.name)
        if (stage / "TEMPLATE.md").exists():
            shutil.copy2(stage / "TEMPLATE.md", root / "TEMPLATE.md")
        if (stage / "template").exists():
            shutil.copytree(stage / "template", root / "template" / new, dirs_exist_ok=True)
        cache_src = stage / "paper_state/template-source.json"
        if cache_src.exists():
            cache_dst = root / "paper_state/template-source.json"
            try:
                old_cache = json.loads(cache_dst.read_text(encoding="utf-8")) if cache_dst.exists() else {}
            except Exception:  # noqa: BLE001
                old_cache = {}
            try:
                new_cache = json.loads(cache_src.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                new_cache = {}
            old_cache.update(new_cache)
            cache_dst.write_text(json.dumps(old_cache, indent=2) + "\n", encoding="utf-8")

        (root / "paper_state/conference.yaml").write_text(
            f"id: {new}\nyear: null\nsource_url: VERIFY\nverified_on: null\n"
            f"status: UNVERIFIED\nprevious: {old}\nswitched_at: {now()}\n",
            encoding="utf-8",
        )
        plan["venue"] = new
        for st in plan.get("stages", []):
            if st["id"] in ("review", "acceptance", "package"):
                st["status"] = "pending"
                st["note"] = f"resubmitted from {old}"
        plan.setdefault("log", []).append(
            {"ts": now(), "stage": "resubmit", "status": "done", "note": f"{old} -> {new}"}
        )
        plan["current"] = next(
            (st["id"] for st in plan.get("stages", []) if st["status"] in ("pending", "in_progress", "blocked")),
            "done",
        )
        save_plan(root, plan)

        fix = "\n".join(f"- {r}: address in abstract/intro/results, or scope it explicitly" for r in sorted(reasons)) or "- no structured reasons supplied"
        (root / "RESUBMISSION.md").write_text(
            f"# Resubmission: {old} -> {new}\n\n"
            f"- switched: {now()}\n"
            f"- reasons: {', '.join(sorted(reasons)) or 'not specified'}\n"
            f"- old template archived: `template/previous-{old}-{ts}/`\n"
            f"- new style files: {', '.join(copied) or 'see TEMPLATE.md'}\n"
            f"- new source: see `TEMPLATE.md` (verify the CFP)\n\n"
            f"## What to fix\n\n{fix}\n\n"
            "## Checklist\n\n"
            "- [ ] Verify the new CFP/page limit/anonymity/checklist\n"
            "- [ ] Update abstract + related work framing\n"
            "- [ ] Rerun experiments or scope the claim\n"
            "- [ ] `papercraft check --with-repro` green\n"
            "- [ ] New `TEMPLATE.md` source_verified=true or manually verified\n",
            encoding="utf-8",
        )
        print(f"resubmitted: {old} -> {new}")
        print(f"template archived: {arch}")
        print(f"new style files: {', '.join(copied) or '(none copied)'}")
        print(f"memo: {root / 'RESUBMISSION.md'}")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cmd_venues(_args) -> int:
    for p in sorted((SRC / "conferences").glob("*.md")):
        if p.name.startswith("_"):
            continue
        print(p.stem)
    return 0


def cmd_doctor(_args) -> int:
    ok = True
    for name, cmd in (("python3", ["python3", "--version"]), ("pdflatex", ["pdflatex", "--version"]), ("bibtex", ["bibtex", "--version"])):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print(f"{name}: ok ({out.stdout.splitlines()[0] if out.stdout else ''})")
        except FileNotFoundError:
            print(f"{name}: MISSING")
            ok = False
    print("skill:", SRC)
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="papercraft")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new")
    p.add_argument("--topic", required=True)
    p.add_argument("--venue", default="aaai")
    p.add_argument("--dir", required=True)
    p.add_argument("--force", action="store_true")
    p.add_argument("--fetch-template", action="store_true",
                   help="fetch the official template if a source is configured")
    p.set_defaults(fn=cmd_new)

    for name, fn in (("status", cmd_status), ("next", cmd_next)):
        p = sub.add_parser(name)
        p.add_argument("--dir", default=".")
        p.set_defaults(fn=fn)

    p = sub.add_parser("mark")
    p.add_argument("stage")
    p.add_argument("status", choices=["pending", "in_progress", "done", "blocked", "skipped"])
    p.add_argument("--note", default="")
    p.add_argument("--dir", default=".")
    p.set_defaults(fn=cmd_mark)

    p = sub.add_parser("check")
    p.add_argument("--dir", default=".")
    p.add_argument("--with-repro", action="store_true")
    p.add_argument("--no-build", action="store_true")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("package")
    p.add_argument("--dir", default=".")
    p.add_argument("--artifact", action="store_true")
    p.add_argument("--skip-check", action="store_true", help="draft only; do not run gates")
    p.set_defaults(fn=cmd_package)

    p = sub.add_parser("recommend")
    p.add_argument("--dir", default=".")
    p.add_argument("--type", default="evaluation")
    p.add_argument("--scale", default="small")
    p.add_argument("--reasons", default="")
    p.add_argument("--reviews", nargs="*", default=[])
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_recommend)

    p = sub.add_parser("resubmit")
    p.add_argument("--dir", default=".")
    p.add_argument("--to", required=True)
    p.add_argument("--url", default=None)
    p.add_argument("--archive", default=None)
    p.add_argument("--reasons", default="")
    p.add_argument("--reviews", nargs="*", default=[])
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_resubmit)

    p = sub.add_parser("template")
    p.add_argument("--venue", default=None)
    p.add_argument("--dir", default=".")
    p.add_argument("--url", default=None)
    p.add_argument("--archive", default=None)
    p.add_argument("--force", action="store_true")
    p.add_argument("--allow-http-local", action="store_true")
    p.add_argument("--list", action="store_true")
    p.set_defaults(fn=cmd_template)

    p = sub.add_parser("list-venues")
    p.set_defaults(fn=cmd_venues)

    p = sub.add_parser("doctor")
    p.set_defaults(fn=cmd_doctor)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())

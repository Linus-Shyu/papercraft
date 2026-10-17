#!/usr/bin/env python3
"""Verify (and optionally run) the experiments behind the paper's numbers.

Manifest: paper_state/repro-manifest.json
{
  "timeout": 300,
  "entries": [
    {"id": "E1", "command": "python3 scripts/exp1.py",
     "output": "data/results/e1.json", "sha256": null,
     "expect": {"conditions.0.ear": 0.5623}}
  ]
}

Usage:
  python3 check_repro.py --manifest paper_state/repro-manifest.json --root .
  python3 check_repro.py --manifest ... --root . --run --timeout 600
  python3 check_repro.py --manifest ... --root . --run --only E1

Exit codes: 0 pass, 1 failure, 2 IO/config.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

IGNORE = shutil.ignore_patterns(
    ".git", "__pycache__", "*.pyc", "paper_state", "tmp", "output",
    "*.zip", "*.mp4", "*.mov", "*.aux", "*.log", "*.bbl", "*.blg",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get_path(obj, dotted: str):
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


def close(a, b, tol: float) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) <= tol
    return a == b


def verify_output(path: Path, entry: dict, tol: float) -> list[str]:
    errs = []
    if not path.exists():
        return [f"missing output: {path}"]
    if entry.get("sha256"):
        got = sha256(path)
        if got != entry["sha256"]:
            errs.append(f"sha256 mismatch: got {got[:16]}..., expected {entry['sha256'][:16]}...")
    if entry.get("expect"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            return errs + [f"cannot parse JSON: {e}"]
        for dotted, expected in entry["expect"].items():
            try:
                got = get_path(data, dotted)
            except Exception as e:  # noqa: BLE001
                errs.append(f"{dotted}: path error ({e})")
                continue
            if not close(got, expected, tol):
                errs.append(f"{dotted}: got {got!r}, expected {expected!r}")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--run", action="store_true", help="execute commands in a temp copy")
    ap.add_argument("--only", default=None)
    ap.add_argument("--timeout", type=int, default=None)
    ap.add_argument("--tolerance", type=float, default=1e-6)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--log", default=None)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    mpath = Path(args.manifest)
    if not mpath.is_absolute():
        mpath = root / mpath
    if not mpath.exists():
        print(f"IO ERROR: missing manifest {mpath}", file=sys.stderr)
        return 2
    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"CONFIG ERROR: {e}", file=sys.stderr)
        return 2

    entries = manifest.get("entries", [])
    if args.only:
        entries = [e for e in entries if e.get("id") == args.only]
    if not entries:
        print("CONFIG ERROR: no entries (or --only matched none)", file=sys.stderr)
        return 2

    timeout = args.timeout or int(manifest.get("timeout", 300))
    work = root
    tmp = None
    if args.run:
        tmp = Path(tempfile.mkdtemp(prefix="papercraft-repro-"))
        work = tmp / "repo"
        shutil.copytree(root, work, ignore=IGNORE)

    results = []
    failed = 0
    for e in entries:
        eid = e.get("id", "?")
        out_rel = e.get("output", "")
        if not out_rel or ".." in Path(out_rel).parts:
            results.append({"id": eid, "ok": False, "errors": ["invalid output path"]})
            failed += 1
            continue
        errs = []
        run_info = {}
        if args.run:
            cmd = e.get("command", "")
            try:
                proc = subprocess.run(
                    cmd, shell=True, cwd=work, timeout=timeout,
                    capture_output=True, text=True,
                )
                run_info = {"exit": proc.returncode, "stdout": proc.stdout[-2000:], "stderr": proc.stderr[-2000:]}
                if proc.returncode != 0:
                    errs.append(f"command exit {proc.returncode}")
            except subprocess.TimeoutExpired:
                errs.append(f"timeout after {timeout}s")
            except Exception as ex:  # noqa: BLE001
                errs.append(f"command error: {ex}")
        out_path = (work / out_rel) if args.run else (root / out_rel)
        if not errs:
            errs.extend(verify_output(out_path, e, args.tolerance))
        ok = not errs
        if not ok:
            failed += 1
        results.append({"id": eid, "ok": ok, "errors": errs, "run": run_info, "output": str(out_path)})

    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)

    if args.json:
        payload = {"ok": failed == 0, "failed": failed, "results": results}
        print(json.dumps(payload, indent=2))
        if args.log:
            Path(args.log).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        for r in results:
            if r["ok"]:
                print(f"  PASS {r['id']}")
            else:
                print(f"  FAIL {r['id']}")
                for x in r["errors"]:
                    print(f"       - {x}")
                if r["run"].get("stderr"):
                    print("       stderr: " + r["run"]["stderr"].strip().splitlines()[-1][:160])
        print(f"RESULT: {'PASS' if failed == 0 else 'FAIL'} ({len(entries)} entries, {failed} failed)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

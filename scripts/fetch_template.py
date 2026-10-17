#!/usr/bin/env python3
"""Fetch and safely extract an official conference LaTeX template.

Never guesses a URL. A source must come from:
  1. --url on the command line (official kit), or
  2. --archive (a kit you downloaded manually), or
  3. paper_state/template-source.json (cached from a previous --url), or
  4. conferences/templates.json with a non-null verified url.

Usage:
  python3 fetch_template.py --venue aaai --dir ./paper --url https://.../aaai2027.zip
  python3 fetch_template.py --venue aaai --dir ./paper --archive ~/Downloads/aaai2027.zip
  python3 fetch_template.py --list
Exit codes: 0 ok, 1 extract/verify failure, 2 usage/source missing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import stat
import sys
import signal
import tarfile
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

SRC = Path(__file__).resolve().parents[1]
REGISTRY = SRC / "conferences/templates.json"
MAX_ARCHIVE = 50 * 1024 * 1024
MAX_EXTRACT = 200 * 1024 * 1024
MAX_FILE = 50 * 1024 * 1024
ALLOWED = {".sty", ".bst", ".cls", ".tex", ".pdf", ".md", ".txt", ".bib",
           ".png", ".jpg", ".jpeg", ".eps", ".svg"}


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def load_cache(project: Path) -> dict:
    p = project / "paper_state/template-source.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return {}
    return {}


def save_cache(project: Path, venue: str, url: str, year: int | None) -> None:
    p = project / "paper_state/template-source.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    data = load_cache(project)
    data[venue] = {"url": url, "year": year, "saved_at": now()}
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def validate_url(url: str, allow_local_http: bool) -> None:
    u = urlparse(url)
    if u.scheme == "https" and u.hostname:
        return
    if allow_local_http and u.scheme == "http" and u.hostname in ("127.0.0.1", "localhost"):
        return
    raise SystemExit("ERROR: only https URLs are allowed (http is allowed only for localhost tests)")


def download(url: str, dest: Path, allow_local_http: bool) -> str:
    validate_url(url, allow_local_http)
    req = Request(url, headers={"User-Agent": "papercraft/3.1 (+template-fetch)"})
    with urlopen(req, timeout=30) as r:  # noqa: S310
        final = r.geturl()
        validate_url(final, allow_local_http)
        length = int(r.headers.get("Content-Length") or 0)
        if length and length > MAX_ARCHIVE:
            raise SystemExit(f"ERROR: archive too large ({length} bytes)")
        total = 0
        with dest.open("wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_ARCHIVE:
                    raise SystemExit("ERROR: archive exceeds 50 MB")
                f.write(chunk)
    return final


def check_member(name: str, size: int, total: int) -> None:
    p = Path(name)
    if not name or p.is_absolute() or ".." in p.parts:
        raise SystemExit(f"ERROR: unsafe path in archive: {name}")
    if size > MAX_FILE or total + size > MAX_EXTRACT:
        raise SystemExit(f"ERROR: archive member too large: {name}")
    if p.suffix.lower() not in ALLOWED:
        return


def extract_zip(archive: Path, dest: Path) -> list[str]:
    out = []
    total = 0
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            check_member(info.filename, info.file_size, total)
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise SystemExit(f"ERROR: symlink in archive: {info.filename}")
            total += info.file_size
            p = Path(info.filename)
            if p.suffix.lower() not in ALLOWED:
                continue
            target = dest / info.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(info))
            out.append(info.filename)
    return out


def extract_tar(archive: Path, dest: Path) -> list[str]:
    out = []
    total = 0
    with tarfile.open(archive) as t:
        members = t.getmembers()
        for m in members:
            check_member(m.name, m.size, total)
            if m.issym() or m.islnk() or m.isdev():
                raise SystemExit(f"ERROR: link/device in archive: {m.name}")
        for m in members:
            if not m.isfile():
                continue
            total += m.size
            p = Path(m.name)
            if p.suffix.lower() not in ALLOWED:
                continue
            target = dest / m.name
            target.parent.mkdir(parents=True, exist_ok=True)
            data = t.extractfile(m)
            if data is None:
                continue
            target.write_bytes(data.read())
            out.append(m.name)
    return out


def extract(archive: Path, dest: Path) -> list[str]:
    dest.mkdir(parents=True, exist_ok=True)
    if zipfile.is_zipfile(archive):
        return extract_zip(archive, dest)
    if tarfile.is_tarfile(archive):
        return extract_tar(archive, dest)
    raise SystemExit("ERROR: archive is neither zip nor tar")


def copy_files(extracted: Path, project: Path, force: bool) -> tuple[list[str], list[str]]:
    copied, skipped = [], []
    template_dir = project / "template"
    template_dir.mkdir(exist_ok=True)
    for p in extracted.rglob("*"):
        if not p.is_file():
            continue
        suffix = p.suffix.lower()
        if suffix in {".sty", ".bst", ".cls"}:
            target = project / p.name
            if target.exists() and not force:
                skipped.append(str(target))
                continue
            shutil.copy2(p, target)
            copied.append(str(target))
        elif suffix in {".tex", ".md", ".pdf", ".bib", ".txt"}:
            rel = p.relative_to(extracted)
            target = template_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and not force:
                skipped.append(str(target))
                continue
            shutil.copy2(p, target)
            copied.append(str(target))
    return copied, skipped


def write_provenance(project: Path, venue: str, year: int | None, source: str,
                     archive: Path, archive_hash: str, copied: list[str],
                     entry: dict, source_verified: bool) -> None:
    lines = [
        "# Template provenance",
        "",
        f"- venue: `{venue}`",
        f"- year: `{year or 'unknown'}`",
        f"- source: `{source}`",
        f"- fetched_at: `{now()}`",
        f"- archive_sha256: `{archive_hash}`",
        f"- source_verified: `{str(source_verified).lower()}`",
        f"- license: `{entry.get('license') or 'VERIFY'}`",
        f"- notes: {entry.get('notes') or 'VERIFY'}",
        "",
        "## Files copied",
        "",
    ]
    for f in copied:
        p = Path(f)
        lines.append(f"- `{p}`  sha256 `{sha256(p)[:16]}…`")
    lines += [
        "",
        "## Next",
        "",
        "1. Confirm the style version matches the current CFP (open the source URL).",
        "2. If `source_verified` is false, update `conferences/templates.json` with the",
        "   verified URL and `verified_on`, or keep this note and verify manually.",
        "3. Copy the relevant `\\documentclass`/`\\usepackage` lines from",
        "   `template/` into `main.tex` (do not overwrite your content blindly).",
    ]
    (project / "TEMPLATE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_list() -> int:
    reg = load_registry()
    for venue, e in sorted(reg.items()):
        if venue.startswith("_"):
            continue
        status = "VERIFIED-URL" if e.get("url") else "UNSET"
        print(f"{venue:8} {status:12} files={','.join(e.get('files') or []) or '-'}  notes={e.get('notes','')[:70]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue", default=None)
    ap.add_argument("--year", type=int, default=None)
    ap.add_argument("--dir", default=".")
    ap.add_argument("--url", default=None)
    ap.add_argument("--archive", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--allow-http-local", action="store_true")
    ap.add_argument("--no-save-source", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list:
        return cmd_list()
    if not args.venue:
        print("usage: fetch_template.py --venue <id> --dir <project> [--url|--archive]", file=sys.stderr)
        return 2

    project = Path(args.dir).expanduser().resolve()
    if not project.exists():
        print(f"ERROR: project dir missing: {project}", file=sys.stderr)
        return 2

    reg = load_registry()
    entry = reg.get(args.venue, reg.get("_default", {}))

    source_url = args.url
    archive = Path(args.archive).expanduser().resolve() if args.archive else None
    if not source_url and not archive:
        cache = load_cache(project).get(args.venue, {})
        if cache.get("url"):
            source_url = cache["url"]
    if not source_url and not archive and entry.get("url") not in (None, "", "VERIFY"):
        source_url = entry["url"]
    if not source_url and not archive:
        print(
            f"ERROR: no template source for '{args.venue}'.\n"
            "Open the current CFP/author kit, then run one of:\n"
            f"  papercraft template --venue {args.venue} --url <official-kit-url>\n"
            f"  papercraft template --venue {args.venue} --archive <downloaded-kit.zip>\n"
            "Do not reuse last year's style.",
            file=sys.stderr,
        )
        return 2

    tmp = Path(tempfile.mkdtemp(prefix="papercraft-template-"))
    try:
        if source_url:
            if args.url and not args.no_save_source:
                save_cache(project, args.venue, source_url, args.year)
            archive = tmp / "kit"
            final = download(source_url, archive, args.allow_http_local)
            source_label = final
            source_verified = bool(entry.get("url") == source_url and entry.get("verified_on"))
        else:
            source_label = str(archive)
            source_verified = False

        if archive is None or not archive.exists():
            print("ERROR: archive not found", file=sys.stderr)
            return 2
        if archive.stat().st_size > MAX_ARCHIVE:
            print("ERROR: archive exceeds 50 MB", file=sys.stderr)
            return 2

        h = sha256(archive)
        extracted = tmp / "extract"
        members = extract(archive, extracted)
        if not members:
            print("ERROR: no allowed files extracted", file=sys.stderr)
            return 1

        copied, skipped = copy_files(extracted, project, args.force)
        missing = [f for f in (entry.get("files") or []) if not (project / f).exists()]
        write_provenance(project, args.venue, args.year, source_label, archive, h, copied, entry, source_verified)

        print(f"template: {args.venue}")
        print(f"source:   {source_label}")
        print(f"sha256:   {h}")
        print(f"files:    {len(members)} extracted, {len(copied)} copied, {len(skipped)} skipped")
        if missing:
            print(f"WARN: expected files not found (check the kit version): {', '.join(missing)}")
        print(f"provenance: {project / 'TEMPLATE.md'}")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())

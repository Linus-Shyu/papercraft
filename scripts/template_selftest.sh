#!/usr/bin/env bash
# Template fetch: safe archive, malicious archive, missing source.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-tmpl.XXXXXX")"
trap 'rm -rf "${TMP}"' EXIT

mkdir -p "${TMP}/kit" "${TMP}/paper/paper_state"
printf '\\ProvidesPackage{aaai2027}\n' > "${TMP}/kit/aaai2027.sty"
printf '\\documentclass{article}\\begin{document}x\\end{document}\n' > "${TMP}/kit/sample.tex"
( cd "${TMP}/kit" && zip -qr "${TMP}/safe.zip" . )

"${ROOT}/papercraft" template --venue aaai --dir "${TMP}/paper" --archive "${TMP}/safe.zip" >/dev/null
[[ -f "${TMP}/paper/aaai2027.sty" ]] || { echo "sty not copied" >&2; exit 1; }
grep -q "archive_sha256" "${TMP}/paper/TEMPLATE.md" || { echo "no provenance" >&2; exit 1; }

python3 - <<PY
import zipfile
with zipfile.ZipFile("${TMP}/evil.zip", "w") as z:
    z.writestr("../evil.sty", "x")
PY
set +e
"${ROOT}/papercraft" template --venue aaai --dir "${TMP}/paper" --archive "${TMP}/evil.zip" >/dev/null 2>&1
rc=$?
set -e
[[ "${rc}" -ne 0 ]] || { echo "malicious archive accepted" >&2; exit 1; }
[[ ! -e "${TMP}/evil.sty" ]] || { echo "path traversal escaped" >&2; exit 1; }

mkdir -p "${TMP}/empty/paper_state"
set +e
"${ROOT}/papercraft" template --venue kdd --dir "${TMP}/empty" >/dev/null 2>&1
rc=$?
set -e
[[ "${rc}" -eq 2 ]] || { echo "missing source should exit 2, got ${rc}" >&2; exit 1; }

"${ROOT}/papercraft" template --list > "${TMP}/list.txt"
grep -q "aaai" "${TMP}/list.txt"

echo "TEMPLATE SELFTEST: PASS"

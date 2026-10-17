#!/usr/bin/env bash
# Rejection/resubmission: recommend -> dry-run -> switch template -> failure safety.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-resub.XXXXXX")"
trap 'rm -rf "${TMP}"' EXIT
P="${TMP}/paper"

"${ROOT}/papercraft" new --topic "How should we evaluate LLM tutoring?" --venue aaai --dir "${P}" >/dev/null

mkdir -p "${TMP}/aaai" "${TMP}/acl"
printf '\\ProvidesPackage{aaai2027}\n' > "${TMP}/aaai/aaai2027.sty"
printf '\\documentclass{article}\\begin{document}x\\end{document}\n' > "${TMP}/aaai/sample.tex"
( cd "${TMP}/aaai" && zip -qr "${TMP}/aaai.zip" . )
printf '\\ProvidesPackage{acl}\n' > "${TMP}/acl/acl.sty"
printf '\\documentclass{article}\\begin{document}x\\end{document}\n' > "${TMP}/acl/sample.tex"
( cd "${TMP}/acl" && zip -qr "${TMP}/acl.zip" . )

"${ROOT}/papercraft" template --venue aaai --dir "${P}" --archive "${TMP}/aaai.zip" >/dev/null

"${ROOT}/papercraft" recommend --dir "${P}" --reasons novelty,evidence --type evaluation --scale small --top 3 > "${TMP}/rec.txt"
grep -q "acl" "${TMP}/rec.txt"
grep -q "emnlp" "${TMP}/rec.txt"

"${ROOT}/papercraft" resubmit --dir "${P}" --to acl --archive "${TMP}/acl.zip" --reasons novelty,evidence --dry-run >/dev/null
[[ -f "${P}/aaai2027.sty" ]] || { echo "dry-run changed files" >&2; exit 1; }

"${ROOT}/papercraft" resubmit --dir "${P}" --to acl --archive "${TMP}/acl.zip" --reasons novelty,evidence >/dev/null
[[ -f "${P}/acl.sty" ]] || { echo "new style missing" >&2; exit 1; }
[[ ! -f "${P}/aaai2027.sty" ]] || { echo "old style not archived" >&2; exit 1; }
grep -q "id: acl" "${P}/paper_state/conference.yaml"
[[ -f "${P}/RESUBMISSION.md" ]] || { echo "memo missing" >&2; exit 1; }
ls "${P}/template"/previous-aaai-* >/dev/null 2>&1 || { echo "archive dir missing" >&2; exit 1; }

set +e
"${ROOT}/papercraft" resubmit --dir "${P}" --to kdd >/dev/null 2>&1
rc=$?
set -e
[[ "${rc}" -ne 0 ]] || { echo "missing source should fail" >&2; exit 1; }
[[ -f "${P}/acl.sty" ]] || { echo "failure destroyed current template" >&2; exit 1; }

echo "RESUBMIT SELFTEST: PASS"

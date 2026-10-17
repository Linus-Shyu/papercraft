#!/usr/bin/env bash
# End-to-end CLI test: new -> next -> mark -> check -> package --skip-check.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-auto.XXXXXX")"
trap 'rm -rf "${TMP}"' EXIT
P="${TMP}/paper"

"${ROOT}/papercraft" new --topic "Test topic" --venue aaai --dir "${P}" >/dev/null
[[ -f "${P}/main.tex" && -f "${P}/paper_state/plan.json" ]] || { echo "scaffold missing" >&2; exit 1; }
"${ROOT}/papercraft" status --dir "${P}" | grep -q "| topic |"
"${ROOT}/papercraft" next --dir "${P}" | grep -q "STAGE: topic"
"${ROOT}/papercraft" mark topic done --note "rq" --dir "${P}" >/dev/null
"${ROOT}/papercraft" next --dir "${P}" | grep -q "STAGE: survey"

set +e
"${ROOT}/papercraft" check --dir "${P}" --no-build >/dev/null 2>&1
rc=$?
set -e
[[ "${rc}" -ne 0 ]] || { echo "check should fail on empty state" >&2; exit 1; }

"${ROOT}/papercraft" package --dir "${P}" --skip-check >/dev/null
[[ -f "${P}/submission/main.pdf" && -f "${P}/submission/source.zip" ]] || { echo "package missing" >&2; exit 1; }

echo "AUTOPILOT SELFTEST: PASS"

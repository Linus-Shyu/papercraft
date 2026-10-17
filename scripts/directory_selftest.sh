#!/usr/bin/env bash
# Conference directory: filters, JSON, marking, validator.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-dir.XXXXXX")"
trap 'rm -rf "${TMP}"' EXIT
mkdir -p "${TMP}/paper/paper_state"

"${ROOT}/papercraft" venues --area nlp > "${TMP}/nlp.txt"
grep -q "acl" "${TMP}/nlp.txt"
grep -q "naacl" "${TMP}/nlp.txt"

"${ROOT}/papercraft" venues --json > "${TMP}/all.json"
python3 - "${TMP}/all.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
assert len(d) >= 30, len(d)
assert all("status" in x and "verified" in x for x in d)
PY

"${ROOT}/papercraft" venues-mark --id acl --status in_review --source-url https://aclweb.org/ --dir "${TMP}/paper" >/dev/null
"${ROOT}/papercraft" venues --dir "${TMP}/paper" --verified-only | grep -q "VERIFIED:in_review"

set +e
"${ROOT}/papercraft" venues-mark --id not_a_venue --status open --source-url https://example.org --dir "${TMP}/paper" >/dev/null 2>&1
rc=$?
set -e
[[ "${rc}" -ne 0 ]] || { echo "unknown venue accepted" >&2; exit 1; }

python3 "${HERE}/check_directory.py" --directory "${ROOT}/conferences/directory.json" >/dev/null
python3 "${HERE}/check_directory.py" --directory "${ROOT}/conferences/directory.json" \
  --overlay "${TMP}/paper/paper_state/conference-verifications.json" >/dev/null

set +e
python3 "${HERE}/check_directory.py" --directory "${ROOT}/conferences/directory.json" \
  --overlay "${TMP}/paper/paper_state/conference-verifications.json" --require-verified >/dev/null 2>&1
rc=$?
set -e
[[ "${rc}" -ne 0 ]] || { echo "require-verified should fail" >&2; exit 1; }

echo "DIRECTORY SELFTEST: PASS"

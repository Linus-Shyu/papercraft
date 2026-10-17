#!/usr/bin/env bash
# Self-tests for the research-lifecycle checkers.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-ext.XXXXXX")"
trap 'rm -rf "${TMP}"' EXIT

expect() {
  local want="$1"; shift
  set +e
  "$@" >/dev/null 2>&1
  local got=$?
  set -e
  if [[ "${got}" -ne "${want}" ]]; then
    echo "FAIL: want exit ${want}, got ${got}: $*" >&2
    exit 1
  fi
}

mkdir -p "${TMP}/lit" "${TMP}/math" "${TMP}/repro"

# literature: missing required columns
printf 'key,title\nA,T\n' > "${TMP}/lit/bad.csv"
expect 1 python3 "${HERE}/check_literature.py" --csv "${TMP}/lit/bad.csv"

# literature: valid template
expect 0 python3 "${HERE}/check_literature.py" --csv "${ROOT}/templates/literature-matrix.csv"

# math: duplicate label + wrong arithmetic
cat > "${TMP}/math/bad.tex" <<'TEX'
\documentclass{article}\begin{document}
\begin{equation}\label{eq:a} x = 1 \end{equation}
\begin{equation}\label{eq:a} y = 2 \end{equation}
See Eq.~\ref{eq:a}.
\end{document}
TEX
cat > "${TMP}/math/math.json" <<'JSON'
{"symbols": {"x": "x", "y": "y"}, "numeric": [{"id": "bad", "expr": "1+1", "expected": 3}]}
JSON
expect 1 python3 "${HERE}/check_math.py" --tex "${TMP}/math/bad.tex" --root "${TMP}/math" --config "${TMP}/math/math.json"

# math: clean
cat > "${TMP}/math/ok.tex" <<'TEX'
\documentclass{article}\begin{document}
\begin{equation}\label{eq:a} x = 1 \end{equation}
See Eq.~\ref{eq:a}.
\end{document}
TEX
cat > "${TMP}/math/ok.json" <<'JSON'
{"symbols": {"x": "x"}, "numeric": [{"id": "ok", "expr": "1+1", "expected": 2}]}
JSON
expect 0 python3 "${HERE}/check_math.py" --tex "${TMP}/math/ok.tex" --root "${TMP}/math" --config "${TMP}/math/ok.json"

# repro: expectation mismatch
mkdir -p "${TMP}/repro/data"
echo '{"x": 0.4}' > "${TMP}/repro/data/out.json"
cat > "${TMP}/repro/bad.json" <<'JSON'
{"entries": [{"id": "bad", "command": "true", "output": "data/out.json", "expect": {"x": 0.5}}]}
JSON
expect 1 python3 "${HERE}/check_repro.py" --manifest "${TMP}/repro/bad.json" --root "${TMP}/repro"

# repro: command runs and matches
cat > "${TMP}/repro/ok.json" <<'JSON'
{"entries": [{"id": "ok", "command": "python3 -c \"import json;json.dump({'x':0.5},open('data/out.json','w'))\"", "output": "data/out.json", "expect": {"x": 0.5}}]}
JSON
expect 0 python3 "${HERE}/check_repro.py" --manifest "${TMP}/repro/ok.json" --root "${TMP}/repro" --run

# review: score/text mismatch
python3 - <<'PY'
import json
r=json.load(open("/Users/linusshyu/Desktop/document/papercraft/templates/review-score.json"))
r["overall"]=3; r["recommendation"]="accept"
json.dump(r,open("/tmp/pc_bad_review.json","w"))
PY
expect 1 python3 "${HERE}/score_review.py" --review /tmp/pc_bad_review.json
expect 0 python3 "${HERE}/score_review.py" --review "${ROOT}/templates/review-score.json"

# acceptance: submit with a BLOCKER
python3 - <<'PY'
import json
a=json.load(open("/Users/linusshyu/Desktop/document/papercraft/templates/acceptance.json"))
a["risks"].append({"id":"R3","severity":"BLOCKER","risk":"artifact fails","mitigation":"fix"})
json.dump(a,open("/tmp/pc_bad_accept.json","w"))
PY
expect 1 python3 "${HERE}/score_acceptance.py" --assessment /tmp/pc_bad_accept.json
expect 0 python3 "${HERE}/score_acceptance.py" --assessment "${ROOT}/templates/acceptance.json"

rm -f /tmp/pc_bad_review.json /tmp/pc_bad_accept.json
echo "EXTENDED SELFTEST: PASS"

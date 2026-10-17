#!/usr/bin/env bash
# Negative + positive self-tests for every checker (no LaTeX required).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-selftest.XXXXXX")"
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

mkdir -p "${TMP}/num" "${TMP}/cite" "${TMP}/anon" "${TMP}/float" "${TMP}/conf"

# numbers: stale value and wrong context must fail
cat > "${TMP}/num/main.tex" <<'TEX'
\documentclass{article}\begin{document}We report 0.57 on the pilot.\end{document}
TEX
cat > "${TMP}/num/numbers.json" <<'JSON'
{"entries":[{"id":"x","value":0.5623,"format":"0.00","files":["main.tex"],"context":"report","bad_values":["0.57"]}]}
JSON
expect 1 python3 "${HERE}/check_numbers.py" --config "${TMP}/num/numbers.json" --root "${TMP}/num"

# numbers: missing context must fail even if the value exists elsewhere
cat > "${TMP}/num/main.tex" <<'TEX'
\documentclass{article}\begin{document}We report 0.56 on the pilot. Background 0.56.\end{document}
TEX
cat > "${TMP}/num/numbers.json" <<'JSON'
{"entries":[{"id":"x","value":0.5623,"format":"0.00","files":["main.tex"],"context":"THIS_CONTEXT_DOES_NOT_EXIST"}]}
JSON
expect 1 python3 "${HERE}/check_numbers.py" --config "${TMP}/num/numbers.json" --root "${TMP}/num"

# citations: missing key
cat > "${TMP}/cite/main.tex" <<'TEX'
\documentclass{article}\begin{document}See \cite{missing_key}.\end{document}
TEX
printf '@inproceedings{ok, title={T}, author={A}, booktitle={B}, year={2020}}\n' > "${TMP}/cite/refs.bib"
expect 1 python3 "${HERE}/check_citations.py" --tex "${TMP}/cite/main.tex" --bib "${TMP}/cite/refs.bib"

# anonymity: email + non-anonymous author
cat > "${TMP}/anon/main.tex" <<'TEX'
\documentclass{article}\author{Alice}\begin{document}Contact a@b.com.\end{document}
TEX
expect 1 python3 "${HERE}/check_anonymity.py" --root "${TMP}/anon" --tex "${TMP}/anon/main.tex"

# floats: orphan label + undefined ref
cat > "${TMP}/float/main.tex" <<'TEX'
\documentclass{article}\begin{document}See \ref{fig:nope}.
\begin{figure}\caption{x}\label{fig:orphan}\end{figure}\end{document}
TEX
expect 1 python3 "${HERE}/check_floats.py" --tex "${TMP}/float/main.tex" --root "${TMP}/float"

# conference: unverified profile must fail strict; fully filled must pass
cat > "${TMP}/conf/p.md" <<'MD'
---
id: p
name: P
year: 2027
source_url: https://example.org/cfp
verified_on: 2026-10-17
status: UNVERIFIED
template: VERIFY
review_model: VERIFY
anonymity: VERIFY
page_limit_main: VERIFY
page_limit_refs: VERIFY
appendix: VERIFY
supplementary: VERIFY
reproducibility: VERIFY
llm_policy: VERIFY
dual_submission: VERIFY
rebuttal: VERIFY
camera_ready: VERIFY
---
# P
MD
expect 1 python3 "${HERE}/check_conference.py" "${TMP}/conf/p.md" --strict
sed 's/^id: p/id: ok/; s/UNVERIFIED/VERIFIED/; s/VERIFY/known/g' "${TMP}/conf/p.md" > "${TMP}/conf/ok.md"
expect 0 python3 "${HERE}/check_conference.py" "${TMP}/conf/ok.md" --strict

echo "SELFTEST: PASS"

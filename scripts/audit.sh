#!/usr/bin/env bash
# Run all papercraft gates on a paper repo.
#
# Usage: audit.sh <paper_dir> [state_dir] [--strict] [--no-build]
# Exit:  0 all pass, 1 any fail, 2 usage/IO.

set -uo pipefail

PAPER="${1:-}"
if [[ -z "${PAPER}" || ! -d "${PAPER}" ]]; then
  echo "usage: audit.sh <paper_dir> [state_dir] [--strict] [--no-build]" >&2
  exit 2
fi
shift || true

STATE=""
STRICT=""
BUILD="1"
for arg in "$@"; do
  case "${arg}" in
    --strict) STRICT="--strict" ;;
    --no-build) BUILD="0" ;;
    *) STATE="${arg}" ;;
  esac
done
[[ -z "${STATE}" ]] && STATE="${PAPER}/paper_state"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER="$(cd "${PAPER}" && pwd)"

FAILD=0
run() {
  local name="$1"; shift
  echo "== ${name}"
  if "$@"; then
    echo "-- ${name}: PASS"
  else
    echo "-- ${name}: FAIL"
    FAILD=1
  fi
}

if [[ -f "${STATE}/numbers.json" ]]; then
  run "G2 numbers" python3 "${HERE}/check_numbers.py" --config "${STATE}/numbers.json" --tex "${PAPER}/main.tex" --root "${PAPER}"
else
  echo "== G2 numbers: SKIP (no ${STATE}/numbers.json)"
fi

if [[ -f "${PAPER}/references.bib" ]]; then
  run "G3 citations" python3 "${HERE}/check_citations.py" --tex "${PAPER}/main.tex" --bib "${PAPER}/references.bib" ${STRICT} --quiet-uncited
else
  echo "== G3 citations: SKIP (no references.bib)"
fi

run "G4 floats" python3 "${HERE}/check_floats.py" --tex "${PAPER}/main.tex" --root "${PAPER}"

run "G5 anonymity" python3 "${HERE}/check_anonymity.py" --root "${PAPER}" --tex "${PAPER}/main.tex" "${PAPER}/supplement.tex"

if [[ "${BUILD}" == "1" ]]; then
  run "G6 build" bash "${HERE}/build.sh" "${PAPER}" main.tex
else
  echo "== G6 build: SKIP (--no-build)"
fi

if [[ "${FAILD}" -eq 0 ]]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL"
exit 1

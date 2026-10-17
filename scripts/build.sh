#!/usr/bin/env bash
# Clean build in /tmp; never writes to the source tree.
#
# Usage: build.sh <paper_dir> [main.tex]
# Exit:  0 clean, 1 errors/undefined refs, 2 usage/IO.

set -uo pipefail

SRC="${1:-}"
MAIN="${2:-main.tex}"

if [[ -z "${SRC}" || ! -d "${SRC}" ]]; then
  echo "usage: build.sh <paper_dir> [main.tex]" >&2
  exit 2
fi

SRC="$(cd "${SRC}" && pwd)"
BUILD="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-build.XXXXXX")"
trap 'rm -rf "${BUILD}"' EXIT

if command -v rsync >/dev/null 2>&1; then
  rsync -a \
    --exclude '.git' --exclude 'paper_state' --exclude 'tmp' \
    --exclude 'output' --exclude '*.zip' --exclude '*.mp4' --exclude '*.mov' \
    "${SRC}/" "${BUILD}/"
else
  cp -R "${SRC}/." "${BUILD}/"
fi

cd "${BUILD}"

echo "== build dir: ${BUILD}"
echo "== pass 1"
pdflatex -interaction=nonstopmode -halt-on-error "${MAIN}" > pass1.log 2>&1 || true

if [[ -f references.bib ]]; then
  echo "== bibtex"
  bibtex "${MAIN%.tex}" > bibtex.log 2>&1 || true
fi

echo "== pass 2/3"
pdflatex -interaction=nonstopmode "${MAIN}" > pass2.log 2>&1 || true
pdflatex -interaction=nonstopmode "${MAIN}" > pass3.log 2>&1 || true

LOG="${MAIN%.tex}.log"
[[ -f "${LOG}" ]] || LOG=pass3.log

ERRORS=0
if grep -nE '^!|LaTeX Error|Undefined control sequence|File .* not found' "${LOG}" >/tmp/pc_errors.$$ 2>/dev/null; then
  echo "== errors"
  cat /tmp/pc_errors.$$
  ERRORS=1
fi

if grep -nE 'There were undefined references|Citation .* undefined|Reference .* undefined' "${LOG}" >/tmp/pc_undef.$$ 2>/dev/null; then
  echo "== undefined refs/citations"
  cat /tmp/pc_undef.$$
  ERRORS=1
fi
rm -f /tmp/pc_errors.$$ /tmp/pc_undef.$$

PDF="${MAIN%.tex}.pdf"
if [[ -f "${PDF}" ]]; then
  PAGES=""
  if command -v pdfinfo >/dev/null 2>&1; then
    PAGES="$(pdfinfo "${PDF}" 2>/dev/null | awk '/^Pages:/ {print $2}')"
  elif python3 -c 'import fitz' >/dev/null 2>&1; then
    PAGES="$(python3 -c "import fitz,sys; print(fitz.open(sys.argv[1]).page_count)" "${PDF}" 2>/dev/null)"
  fi
  echo "== pdf: ${PDF} pages=${PAGES:-unknown}"
else
  echo "== pdf missing"
  ERRORS=1
fi

if [[ "${ERRORS}" -eq 0 ]]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL"
exit 1

#!/usr/bin/env bash
# End-to-end smoke test on examples/mini-paper. Should exit 0.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
python3 -m py_compile "${ROOT}"/scripts/*.py
bash "${HERE}/audit.sh" "${ROOT}/examples/mini-paper" "${ROOT}/examples/mini-paper/paper_state"
echo "SMOKE TEST: PASS"

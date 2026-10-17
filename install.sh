#!/usr/bin/env bash
# Backward-compatible wrapper around install.py.
# See ./install.py --help (or ./install.py --list) for the full matrix.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${HERE}/install.py" "$@"

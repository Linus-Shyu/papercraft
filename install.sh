#!/usr/bin/env bash
# Install papercraft as a DSH skill.
#
# Usage:
#   ./install.sh                 # symlink to ~/.dsh/skills/papercraft
#   ./install.sh --copy          # copy instead of symlink
#   ./install.sh --project DIR   # install into DIR/.dsh/skills/papercraft
#   ./install.sh --target DIR    # custom skill directory

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="link"
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) MODE="copy"; shift ;;
    --project)
      [[ -n "${2:-}" ]] || { echo "--project needs a directory" >&2; exit 2; }
      TARGET="$2/.dsh/skills/papercraft"; shift 2 ;;
    --target)
      [[ -n "${2:-}" ]] || { echo "--target needs a directory" >&2; exit 2; }
      TARGET="$2"; shift 2 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "${TARGET}" ]]; then
  TARGET="${HOME}/.dsh/skills/papercraft"
fi

[[ -f "${HERE}/SKILL.md" ]] || { echo "SKILL.md missing in ${HERE}" >&2; exit 2; }

mkdir -p "$(dirname "${TARGET}")"
if [[ -e "${TARGET}" || -L "${TARGET}" ]]; then
  echo "target exists: ${TARGET}" >&2
  echo "remove it first, or use --target with a new path" >&2
  exit 1
fi

if [[ "${MODE}" == "copy" ]]; then
  mkdir -p "${TARGET}"
  cp -R "${HERE}/." "${TARGET}/"
  rm -rf "${TARGET}/.git"
  echo "copied papercraft -> ${TARGET}"
else
  ln -s "${HERE}" "${TARGET}"
  echo "linked ${TARGET} -> ${HERE}"
fi

cat <<MSG

Installed. Next:
  1. Restart DSH or start a new session (skills are loaded at session start).
  2. Ask: "Use papercraft to audit <paper dir>".
  3. Optional: cp examples/config.example.yaml <paper>/paper_state/config.yaml

Verify:
  python3 "${TARGET}/scripts/check_conference.py" "${TARGET}/conferences/aaai.md"
MSG

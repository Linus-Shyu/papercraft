#!/usr/bin/env bash
# Self-test for the multi-agent installer. No network, no home writes.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/papercraft-install.XXXXXX")"
trap 'rm -rf "${TMP}"' EXIT

PROJ="${TMP}/paper"
mkdir -p "${PROJ}"
echo "# User project" > "${PROJ}/AGENTS.md"

python3 "${ROOT}/install.py" --list | grep -q "DSH" 
python3 "${ROOT}/install.py" --list | grep -q "Claude Code"
python3 "${ROOT}/install.py" --list | grep -q "Codex"

python3 "${ROOT}/install.py" --project "${PROJ}" >/dev/null

for p in .dsh .agents .claude .cursor .codex; do
  [[ -L "${PROJ}/${p}/skills/papercraft" ]] || { echo "missing native ${p}" >&2; exit 1; }
done
for f in AGENTS.md CLAUDE.md GEMINI.md CONVENTIONS.md .rules \
         .cursor/rules/papercraft.mdc .clinerules/papercraft.md \
         .windsurf/rules/papercraft.md .continue/rules/papercraft.md \
         .github/copilot-instructions.md; do
  [[ -e "${PROJ}/${f}" ]] || { echo "missing pointer ${f}" >&2; exit 1; }
done

# idempotent: exactly one marker block
python3 "${ROOT}/install.py" --project "${PROJ}" >/dev/null
n="$(grep -c "papercraft:begin" "${PROJ}/AGENTS.md")"
[[ "${n}" -eq 1 ]] || { echo "marker count ${n} != 1" >&2; exit 1; }

python3 "${ROOT}/install.py" --uninstall --project "${PROJ}" >/dev/null
grep -q "papercraft:begin" "${PROJ}/AGENTS.md" && { echo "marker not removed" >&2; exit 1; }
grep -q "User project" "${PROJ}/AGENTS.md" || { echo "user content lost" >&2; exit 1; }
[[ ! -L "${PROJ}/.dsh/skills/papercraft" ]] || { echo "native link not removed" >&2; exit 1; }
[[ ! -e "${PROJ}/CLAUDE.md" ]] || { echo "generated CLAUDE.md not removed" >&2; exit 1; }

echo "INSTALL SELFTEST: PASS"

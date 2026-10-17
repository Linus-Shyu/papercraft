# Changelog

## 1.1.0 — 2026-10-17

- Multi-agent installer `install.py` (wrapper: `install.sh`):
  - native skill dirs for DSH (`~/.dsh/skills`), shared `~/.agents/skills`,
    Claude Code (`~/.claude/skills`), Cursor (`~/.cursor/skills`), Codex
    (`~/.codex/skills`);
  - project pointers for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
    `.cursor/rules/*.mdc`, `.clinerules/`, `.windsurf/rules/`, `.continue/rules/`,
    `.github/copilot-instructions.md`, `CONVENTIONS.md`, `.rules`;
  - idempotent marker blocks, backups only for user-owned files, `--uninstall`,
    `--dry-run`, `--copy`, `--force`, `--list`.
- `scripts/install_selftest.sh` verifies install/idempotency/uninstall in a temp
  project; `make test` runs it.

## 1.0.1 — 2026-10-17

- Fix relative-path resolution in `check_floats.py` and `check_anonymity.py`
  (`--tex` now resolves from cwd first, then `--root`).
- Add `scripts/selftest.sh`: negative tests for every checker (numbers,
  citations, anonymity, floats, conference strict) plus a positive profile.
- `make test` now runs the smoke test and the self-tests.
- No external behavior or rule changes.

## 1.0.0 — 2026-10-17

Initial release.

- `SKILL.md`: modes, prime directive, gates G0–G8, Harness rules.
- `WRITING.md`: section-by-section writing playbook, claim/number/citation/
  float discipline, LLM failure modes, pre-submission checklist.
- `REVIEWING.md`: claim–evidence matrix, numbers/method/citation/artifact
  audits, rubric, report template, anti-hallucination rules.
- `conferences/`: AAAI, NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, KDD, CHI, TMLR,
  a generic default, a schema, and an alias index. Volatile fields are `VERIFY`
  by design.
- `guides/`: evidence, citations, harness, failure modes, rebuttal.
- `templates/`: claim ledger, experiment registry, figure registry, numbers,
  review report, camera-ready checklist.
- `scripts/`: `check_numbers.py`, `check_citations.py`, `check_floats.py`,
  `check_anonymity.py`, `check_conference.py`, `build.sh`, `audit.sh`.
- `install.sh`: symlink/copy into `~/.dsh/skills` or a project.
- `examples/mini-paper`: a tiny paper that passes all gates; `make test` runs it
  end-to-end (build + G2–G6).

### Known limitations

- Online citation verification is not automated; the scripts are structural.
- Conference profiles must be verified against the current CFP.
- `check_numbers.py` matches a formatted value in a context; it cannot prove
  that the number is semantically correct.

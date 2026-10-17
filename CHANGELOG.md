# Changelog

## 3.0.0 — 2026-10-17

One-topic autopilot:

- `AUTOPILOT.md`: end-to-end runbook (topic → RQ → survey → feasibility →
  design → execute → write → audit → review → acceptance → package), with
  stage prompts, 3 questions, 3 human checkpoints, and explicit stop conditions.
- `START_HERE.md`: user-facing 3-step quickstart.
- `papercraft` CLI (stdlib only):
  - `new` scaffolds `main.tex`, `refs.bib`, `paper_state/`, `data/results/`;
  - `status`, `next`, `mark` drive `paper_state/plan.json`;
  - `check` runs the audit gates; `package` builds PDF + source/artifact zip
    and refuses to package when gates fail (unless `--skip-check`);
  - `list-venues`, `doctor`.
- `SKILL.md` gains an `autopilot` mode: only the topic is required; at most 3
  questions; no fabricated experiments/citations; stop with a plan if infeasible.
- `scripts/autopilot_selftest.sh` tests scaffold → next → mark → package.

## 2.0.1 — 2026-10-17

Fixes found by a controlled A/B audit of a planted-error paper:

- `audit.sh` now runs `check_math.py --strict` for G7. Undefined symbols and
  unreferenced equation labels are **failures**, not warnings. (Previously G7
  could PASS with undefined symbols.)
- `check_anonymity.py` gained `--extra FILE_OR_DIR`; `audit.sh` scans `code/`
  (or `scripts/`) in addition to `main.tex`/`supplement.tex`, so an email or
  code-host URL hidden in the artifact is caught.
- Documented that math.json must be complete before G7 can pass.

## 2.0.0 — 2026-10-17

Full research lifecycle:

- New guides: `literature`, `feasibility`, `experiments`, `math`, `repro`,
  `acceptance`.
- New scripts:
  - `check_literature.py` (matrix schema, closest-work coverage, verification);
  - `check_math.py` (labels/refs, delimiter balance, symbol coverage, numeric
    expressions);
  - `check_repro.py` (run or verify commands, output hashes, expected values);
  - `score_review.py` (review schema, evidence requirements, score/text
    consistency);
  - `score_acceptance.py` (readiness/fit/risk band, submit safety check).
- New templates: literature matrix, feasibility memo, experiment plan, math
  config, repro manifest, review score, acceptance assessment.
- New gates: G3b literature, G7 math, G8 repro, G9 review, G10 acceptance,
  G11 camera-ready.
- `audit.sh` runs literature/math/repro when the state files exist;
  `--with-repro` executes commands in a temp copy.
- Extended self-tests: `scripts/selftest_extended.sh`.

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

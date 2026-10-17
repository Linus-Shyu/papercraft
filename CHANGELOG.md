# Changelog

## 3.6.0 — 2026-10-17

Conference directory:

- `conferences/directory.json`: 37 active AI venues with area, type, cycle,
  official URL, and a `has_profile` flag. **No deadlines or statuses are stored**
  until verified.
- `papercraft venues` (alias `list-venues`): filter by area/type/status,
  `--verified-only`, `--json`.
- `papercraft venues-mark`: writes `paper_state/conference-verifications.json`
  with status, source URL, `verified_on`, optional deadline/notes.
- `scripts/check_directory.py`: schema, URLs, duplicates, overlay, staleness.
- `guides/conferences.md`; `scripts/directory_selftest.sh`.

## 3.5.0 — 2026-10-17

Minimal invocation:

- One sentence is enough: `写一篇关于 <题目> 的论文，投 <会议>.`
- Defaults: `./papercraft-paper`, venue AAAI, 3 questions, H1/H2/H3.
- `papercraft new` now defaults `--dir` to `./papercraft-paper`.
- `SKILL.md`, `AUTOPILOT.md`, `CHAT.md`, `START_HERE.md`, README lead with the
  one-sentence form; the long prompts are fallback only.

## 3.4.0 — 2026-10-17

Chat-only UX:

- `CHAT.md`: open a folder, mention the skill, paste one message; no terminal.
- `AUTOPILOT.md` §0b: the agent bootstraps the project itself (`papercraft new`
  or templates); never asks the user to run commands.
- `SKILL.md` autopilot contract updated; no-terminal mode must mark G2/G6/G8 as
  `SKIPPED (no terminal)` instead of claiming they passed.
- `START_HERE.md` and `EDITORS.md` point to the chat-only path.

## 3.3.0 — 2026-10-17

GitHub release packaging:

- OpenAI-style `README.md` with logo, badges, quickstart, pipeline, gates,
  editor matrix, safety limits, and citation.
- `assets/logo.svg`, `assets/social-preview.png`.
- `CITATION.cff`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `ROADMAP.md`,
  `.editorconfig`, `.gitattributes`.
- GitHub issue forms, PR template, and a CI workflow (`fast` + `full`).
- `docs/` GitHub Pages landing page.
- `VERIFICATION.md`: what was actually run, the A/B result, and what remains
  unverified.
- `make test-fast` for the subset that does not need LaTeX.

## 3.2.0 — 2026-10-17

Rejection → resubmission:

- `conferences/fit.json`: heuristic venue-fit signals (topics, contribution
  types, scale, review focus). No deadlines, no acceptance predictions.
- `papercraft recommend`: shortlist from the paper topic + review categories.
- `papercraft resubmit --to <venue>`: stages the new template first, archives the
  old style files/TEMPLATE.md, copies the new ones, updates
  `conference.yaml`/`plan.json`, writes `RESUBMISSION.md`. Old template is left
  untouched if the fetch fails; `--dry-run` changes nothing.
- `guides/resubmission.md`: triage, fix-vs-switch, shortlist, template switch,
  policies, memo.
- `scripts/resubmit_selftest.sh` covers dry-run, switch, archive, and failure
  safety.

## 3.1.0 — 2026-10-17

Official template fetching:

- `conferences/templates.json`: per-venue template sources, deliberately
  `url: null` (never guess; verify the current CFP).
- `scripts/fetch_template.py`: HTTPS download or local `--archive`; size caps;
  path-traversal/symlink rejection; copies `.sty/.bst/.cls` to the project,
  samples to `template/`; writes `TEMPLATE.md` with source, date, archive
  sha256, and file hashes; caches the URL in `paper_state/template-source.json`.
- `papercraft template --venue ... [--url|--archive] [--list]`.
- `papercraft new --fetch-template`.
- New autopilot stage `template` (G6) between execute and write.
- `guides/templates.md`; `scripts/template_selftest.sh` (safe archive,
  malicious archive, missing source).

## 3.0.1 — 2026-10-17

- `EDITORS.md`: per-editor activation matrix (DSH, Claude Code, Cursor, Codex,
  Gemini, Copilot, Cline, Windsurf, Continue, Aider, Zed), smoke test,
  troubleshooting, and "installation is not activation".
- Cursor project rule now uses `alwaysApply: true` (project install only), so
  the skill is in context without an explicit `@` mention.

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

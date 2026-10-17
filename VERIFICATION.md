# Verification log

> What was actually run, what passed, what failed, and what remains unverified.
> This file is deliberately boring: commands, outputs, limits.

- Date: 2026-10-17
- Environment: macOS, Python 3.14.6, TeX Live 2025 (`pdfTeX 3.141592653-2.6-1.40.27`), `gh` authenticated as `Linus-Shyu`
- Scope: the local repository before the public GitHub release

## Commands that were run

| Command | Result |
|---|---|
| `python3 -m py_compile scripts/*.py` | pass |
| `bash -n install.sh scripts/*.sh` | pass |
| `make lint` | pass (10 venue profiles, 0 hard failures) |
| `make test` | pass: smoke + `selftest` + `selftest_extended` + `install_selftest` + `autopilot_selftest` + `template_selftest` + `resubmit_selftest` |
| `make test-fast` | pass (the subset that does not need LaTeX) |
| Fresh unzip of the release zip → `make test` | pass |
| `papercraft new` → `status` → `next` → `mark` | pass |
| `papercraft template --archive <safe.zip>` | pass; `.sty` copied, `TEMPLATE.md` written |
| `papercraft template --archive <../evil.sty>` | fail as expected; no path escape |
| `papercraft template` with no source | exit 2 with instructions |
| `papercraft resubmit --dry-run` | no files changed |
| `papercraft resubmit --to acl --archive <acl.zip>` | pass; old style archived, new style copied, `RESUBMISSION.md` written |
| `papercraft resubmit` with no source | fail as expected; current template untouched |
| `papercraft recommend --reasons novelty,evidence` | shortlist printed |
| `install.sh --all` | 5 native symlinks created (`~/.dsh`, `~/.agents`, `~/.claude`, `~/.cursor`, `~/.codex`) |
| `install.sh --project` → `--uninstall --project` | pointers created, user `AGENTS.md` restored |
| `skill` load in DSH | catalog lists `papercraft`; content returned |

## Real-paper audit

On a real AAAI-style paper (outside this repository), `audit.sh` reported:

```
FAIL figure without \label
FAIL label never referenced: fig:atep
FAIL label never referenced: tab:e3e4
FAIL label never referenced: tab:gold
```

These were confirmed by hand. The run also exercised `check_numbers`,
`check_citations`, `check_anonymity`, and `build.sh` on that paper.

## Controlled A/B audit (small)

A 19-line fixture with five planted errors was audited by two subagents:

| | Baseline (no skill) | Skill-guided |
|---|---|---|
| Planted errors found | 5/5 | 5/5 |
| Findings | 8 | 10 |
| Evidence | file:line + comparisons | file:line + checker commands + gate table |
| Major false positives | 0 | 0 (some severity inflation) |
| Process gaps found | partial | better (no `paper_state`, no repro, no seed) |

The skill did **not** improve raw detection on this tiny fixture. It improved
traceability, evidence format, and process discipline. n=1, one model, 19 lines:
this is not a controlled study.

The A/B also exposed two real bugs in Papercraft:

1. G7 could PASS while symbols were undefined (`check_math` was not strict in
   `audit.sh`);
2. the anonymity scan did not cover `code/` or `scripts/`.

Both were fixed in v2.0.1 and are covered by tests.

## What is not verified

- No proof that any paper written with Papercraft will be accepted.
- `check_math` checks labels, delimiters, symbol coverage, and listed arithmetic;
  it does **not** prove a derivation.
- `check_citations` is structural; DOI/arXiv/ACL metadata is verified by a human
  or agent opening the page.
- `check_repro --run` trusts the commands in the manifest; private data/APIs may
  make a run fail.
- Anonymity scanning does not read PDF metadata or binary assets.
- No Windows test; the scripts are POSIX-oriented (Python is cross-platform).
- The A/B is n=1 and not a peer-reviewed evaluation.
- GitHub Actions ran on the first push: `fast` (Python 3.11 and 3.12) and
  `full (LaTeX)` both passed
  ([run 39031016182](https://github.com/Linus-Shyu/papercraft/actions/runs/39031016182)).
- GitHub Pages built: <https://linusshyu.dev/papercraft/> returns 200.
- Release: <https://github.com/Linus-Shyu/papercraft/releases/tag/v3.3.0>.

## AI assistance

This repository was developed with an AI coding assistant and reviewed through
the checks above. The assistant can make mistakes; the scripts, tests, and this
log exist to make those mistakes visible. If you find one, please open an issue
with the command and output.

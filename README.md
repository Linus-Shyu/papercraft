<p align="center">
  <img src="assets/logo.svg" width="96" alt="Papercraft logo">
</p>

<h1 align="center">Papercraft</h1>

<p align="center"><strong>Evidence-first paper writing and review for AI agents.</strong></p>

<p align="center">
  <a href="https://github.com/Linus-Shyu/papercraft/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/Linus-Shyu/papercraft/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg">
  <a href="https://github.com/Linus-Shyu/papercraft/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Linus-Shyu/papercraft?style=social"></a>
</p>

Papercraft is a portable skill and CLI for the full research lifecycle. Give it a
topic; it runs **survey → feasibility → experiment design → execution → writing →
audit → review → acceptance → packaging**, with explicit checkpoints and
fail-closed gates.

It works inside DSH, Claude Code, Cursor, Codex, and any editor that can read a
Markdown instruction file. It is not a ghostwriter: every number, citation,
claim, and float must trace to an artifact.

> **No zero-error guarantee.** No prompt or tool can guarantee that an AI never
> makes a mistake. Papercraft makes mistakes **detectable, localized, and
> blocking**: a number without a source, a citation without verification, or a
> figure without a reference stops the pipeline.

---

## Why Papercraft

LLM-written papers fail in predictable ways:

- fabricated or mis-attributed citations;
- numbers that drift from the code after a re-run;
- figures hand-tuned to look right, then contradicting the text;
- “ablations” that are text substitutions, not module removals;
- floats that no sentence references;
- conference rules (page limits, templates, anonymity, checklists) recalled from
  memory instead of read from the CFP;
- reviews that demand impossible experiments or cite papers that do not exist.

Papercraft turns each failure into a gate with a checker, a ledger, or a written
stop condition.

---

## Quickstart

**Chat-only (recommended).** Install once, then just talk to your editor:

```bash
git clone https://github.com/Linus-Shyu/papercraft.git
cd papercraft
./install.sh --all
```

Open an empty folder (or an existing paper repo) in your editor, mention
`@papercraft` (or `@SKILL.md`), and paste the message from [CHAT.md](CHAT.md).
The agent bootstraps the project; you only answer H1/H2/H3.

**Terminal (optional).**

```bash
./papercraft new --topic "How should we evaluate step-by-step LLM tutoring?" \
  --venue aaai --dir ~/papers/my-paper
./install.sh --project ~/papers/my-paper
```

Open `~/papers/my-paper` in your editor, start a new chat, and paste:

```text
Run Papercraft Autopilot for this repo (the topic is in paper_state/plan.json).
Read /absolute/path/to/papercraft/AUTOPILOT.md and follow it.
I only care about the topic; ask me at most 3 questions.
Do not fabricate results or citations. Stop at H1, H2, H3.
```

You answer at most three questions (venue, constraints, must-use data/code) and
approve three checkpoints:

| Checkpoint | You see | You choose |
|---|---|---|
| **H1** | 3 falsifiable research questions + venue | one, or “you decide” |
| **H2** | minimum publishable unit, resources, go/no-go | go / change scope / stop |
| **H3** | PDF, simulated reviews, acceptance risk | submit / revise |

Everything else is automated. If the work is not feasible with your resources,
you get a **plan and a negative result**, not a fabricated paper.

---

## What it does

```mermaid
flowchart LR
  A[Topic] --> B[Survey]
  B --> C[Feasibility]
  C --> D[Experiment design]
  D --> E[Execute]
  E --> F[Template]
  F --> G[Write]
  G --> H[Audit]
  H --> I[Review]
  I --> J[Acceptance]
  J --> K[Package]
```

| Stage | Output | Gate |
|---|---|---|
| Survey / novelty | literature matrix, closest-3, delta | G3b |
| Feasibility | MPU, resources, go/no-go | G0 |
| Experiment design | cards, controls, seeds, decision rules | G2/G8 |
| Execute | commands, outputs, hashes | G8 |
| Template | official style files + provenance | G6 |
| Write | LaTeX draft from claims and numbers | G1–G4 |
| Audit | all gates, blockers fixed | G2–G8 |
| Review | 3 reviewer personas + scores | G9 |
| Acceptance | risk memo + band | G10 |
| Package | PDF, source zip, artifact zip | G11 |

### Gates

| Gate | Question | Checker |
|---|---|---|
| G2 | Every number traces to a source | `check_numbers.py` |
| G3 | Every citation verifies | `check_citations.py` |
| G3b | Survey covers the closest work | `check_literature.py` |
| G4 | Every float is labelled and referenced | `check_floats.py` |
| G5 | No identity/secret leak | `check_anonymity.py` |
| G6 | Compiles, page limit respected | `build.sh` |
| G7 | Symbols defined, delimiters balanced, arithmetic checks | `check_math.py` |
| G8 | Code actually ran; outputs match | `check_repro.py --run` |
| G9 | Reviews are evidence-based and consistent | `score_review.py` |
| G10 | No unresolved blocker before submit | `score_acceptance.py` |

---

## Works with

| Editor / agent | How it loads |
|---|---|
| DSH | `~/.dsh/skills/papercraft` (native) |
| Claude Code | `~/.claude/skills/papercraft` + `CLAUDE.md` |
| Cursor | `~/.cursor/skills/papercraft` + `.cursor/rules/papercraft.mdc` |
| Codex | `~/.codex/skills/papercraft` + `AGENTS.md` |
| Copilot / Cline / Windsurf / Continue | project rules (`--project`) |
| Aider / Zed / Gemini CLI | `CONVENTIONS.md` / `.rules` / `GEMINI.md` |
| Anything else | paste the absolute path to `SKILL.md` |

See [EDITORS.md](EDITORS.md) for activation and a 5-minute smoke test.

---

## Install

```bash
./install.sh --all                  # native dirs for DSH, ~/.agents, Claude, Cursor, Codex
./install.sh --project DIR          # project dirs + pointers inside one paper repo
./install.sh --list                 # show the matrix
./install.sh --uninstall --project DIR
```

`--project` is required for editors that do not support native skills. Pointers
are marker blocks; existing user content is backed up once, and `--uninstall`
removes only Papercraft’s block.

---

## Use it manually

The autopilot is optional. Every stage is also a command:

```bash
papercraft status --dir ~/papers/my-paper
papercraft next   --dir ~/papers/my-paper
papercraft mark survey done --note "12 rows, 3 closest"
papercraft template --venue aaai --url https://.../aaai2027-kit.zip
papercraft check --dir ~/papers/my-paper --with-repro
papercraft recommend --dir ~/papers/my-paper --reviews review/*.json
papercraft resubmit --dir ~/papers/my-paper --to acl --url https://.../acl-style.zip
papercraft package --dir ~/papers/my-paper
```

If the paper is rejected, `recommend` produces a venue shortlist from the review
categories, and `resubmit` archives the old style files, fetches the new
template, updates the project state, and writes `RESUBMISSION.md`.

---

## Documentation

| File | What it covers |
|---|---|
| [START_HERE.md](START_HERE.md) | 3-step quickstart |
| [CHAT.md](CHAT.md) | chat-only UX: open a folder, mention the skill, paste one message |
| [AUTOPILOT.md](AUTOPILOT.md) | full pipeline, prompts, checkpoints, stop conditions |
| [EDITORS.md](EDITORS.md) | per-editor activation and troubleshooting |
| [WRITING.md](WRITING.md) | section-by-section writing playbook |
| [REVIEWING.md](REVIEWING.md) | adversarial review and scoring |
| [guides/resubmission.md](guides/resubmission.md) | rejection triage, venue shortlist, template switch |
| [conferences/](conferences/) | 10 venue profiles + template/fit metadata |
| [VERIFICATION.md](VERIFICATION.md) | what was actually run, and what remains unverified |

---

## Repository layout

```text
SKILL.md              skill contract: modes, prime directive, gates
START_HERE.md         user quickstart
CHAT.md               chat-only UX (no terminal)
AUTOPILOT.md          end-to-end runbook
EDITORS.md            per-editor activation
WRITING.md            writing playbook
REVIEWING.md          reviewing playbook
conferences/          venue profiles, template sources, fit signals
guides/               evidence, citations, math, repro, acceptance, resubmission
templates/            ledgers, registries, review/acceptance sheets
scripts/              checkers, CLI, build/audit
examples/             a mini paper that passes every gate
assets/               logo + social preview
```

---

## Safety and limits

- **No fabricated experiments.** If the minimum publishable unit cannot be run,
  Papercraft stops at feasibility and delivers a plan.
- **No fabricated citations.** A DOI/arXiv/ACL page must be opened; otherwise
  the key is `UNVERIFIED` and does not go into the PDF.
- **No template guessing.** `conferences/templates.json` ships with `url: null`;
  you provide the official URL once, and Papercraft records provenance.
- **No acceptance guarantee.** The acceptance step is a risk memo, not a
  prediction.
- **Not a replacement for peer review.** Simulated reviewers are a check, not a
  decision.
- **The checkers have limits.** `check_math` does not prove derivations;
  `check_citations` is structural (metadata requires a human/agent to open the
  page); `check_repro` trusts the manifest commands it is given.

---

## Development

No third-party Python dependencies. LaTeX is required for the build tests.

```bash
make lint        # profiles + Python compile
make test        # smoke, unit, install, autopilot, template, resubmit
make test-fast   # the subset that does not need LaTeX
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Good contributions: verified conference
profiles, new checkers with tests, failure-mode case studies, clearer rules.
Please do not add rules that encourage hiding limitations or fabricating results.

---

## License

MIT. See [LICENSE](LICENSE).

## Citation

```bibtex
@software{papercraft2026,
  title  = {Papercraft: Evidence-first paper writing and review for AI agents},
  author = {{Papercraft contributors}},
  year   = {2026},
  url    = {https://github.com/Linus-Shyu/papercraft}
}
```

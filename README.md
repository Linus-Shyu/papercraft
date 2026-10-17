# Papercraft

**Evidence-first paper production and review for AI agents.**

Papercraft is a portable skill for the DeepSeek Harness (and any agent that can
read Markdown and run Python). It turns "write me a paper" into a pipeline with
**claims, canonical numbers, verified citations, generated floats, and blocking
gates** — so the failure modes that plague LLM-written papers become visible
before submission.

> **No zero-error guarantee.** No prompt or skill can guarantee that an AI never
> makes a mistake. Papercraft guarantees something more useful: mistakes become
> **detectable, localized, and blocking**. If a number has no source, a citation
> has no verification, or a figure has no reference, the gate fails and the paper
> stops.

---

## Why

LLM-assisted papers fail in predictable ways:

- fabricated or mis-attributed citations;
- numbers that drift from the code/JSON after a re-run;
- figures hand-tuned to look right, then contradicting the text;
- "ablations" that are text substitutions, not module removals;
- orphan floats that no sentence references;
- conference rules (page limits, anonymity, checklists) recalled from memory;
- reviews that demand impossible experiments or cite papers that do not exist.

Papercraft is a set of **contracts and checkers** for exactly these failures.

---

## Full research lifecycle

| Stage | Mode | Playbook | Gate |
|---|---|---|---|
| Survey / novelty | `survey` | `guides/literature.md` | G3b |
| Feasibility / go-no-go | `feasibility` | `guides/feasibility.md` | G0 |
| Experiment design | `design` | `guides/experiments.md` | G2, G8 |
| Writing | `write` | `WRITING.md` | G1–G4 |
| Math audit | `math` | `guides/math.md` | G7 |
| Did the code run? | `repro` | `guides/repro.md` | G8 |
| Paper check | `audit` | `scripts/audit.sh` | G2–G8 |
| Review / scoring | `review` | `REVIEWING.md` | G9 |
| Acceptance risk | `acceptance` | `guides/acceptance.md` | G10 |
| Rebuttal | `rebut` | `guides/rebuttal.md` | — |
| Camera-ready | `camera-ready` | `templates/camera-ready-checklist.md` | G11 |

`audit.sh` is the mechanical pass; the modes are the thinking passes. Run the
mechanical gates first, then the human/agent judgments.

---

## Install (all agents / IDEs)

```bash
git clone <this-repo> papercraft && cd papercraft
./install.sh                 # DSH only (old default)
./install.sh --all           # native dirs for DSH, ~/.agents, Claude Code, Cursor, Codex
./install.sh --project DIR   # project native dirs + pointer files (recommended per paper repo)
./install.sh --list          # show the full matrix
./install.sh --uninstall --project DIR
```

| Agent / IDE | Native skill dir (`SKILL.md`) | Project pointer |
|---|---|---|
| DSH | `~/.dsh/skills/papercraft` | — |
| Shared Agent Skills | `~/.agents/skills/papercraft` | — |
| Claude Code | `~/.claude/skills/papercraft` | `CLAUDE.md` |
| Cursor | `~/.cursor/skills/papercraft` | `.cursor/rules/papercraft.mdc` |
| Codex | `~/.codex/skills/papercraft` | `AGENTS.md` |
| Gemini CLI | — | `GEMINI.md` |
| Cline | — | `.clinerules/papercraft.md` |
| Windsurf | — | `.windsurf/rules/papercraft.md` |
| Continue | — | `.continue/rules/papercraft.md` |
| GitHub Copilot | — | `.github/copilot-instructions.md` |
| Aider | — | `CONVENTIONS.md` |
| Zed | — | `.rules` |

How it works:

- **Native dirs** get a symlink to this repo (or `--copy`). The `SKILL.md`
  frontmatter is the common Agent Skills format used by DSH/Claude/Cursor/Codex.
- **Pointers** are short marker blocks that tell the agent to read the absolute
  path of `SKILL.md`. They are idempotent; shared files are backed up only if
  you already had content; `--uninstall` removes only Papercraft's block.
- `AGENTS.md` is the universal fallback for tools without a skill loader.
- Pointers embed an **absolute path**; re-run the installer if you move the
  repo. Tools differ: a pointer is an instruction, not a guarantee that the
  tool auto-loads it — check the tool's docs/UI.

Restart DSH (or start a new session) so the skill catalog reloads.

Verify:

```bash
python3 scripts/check_conference.py conferences/aaai.md
./install.sh --list
```

---

## Quickstart

### Audit an existing paper

```bash
paper=/path/to/paper
mkdir -p "$paper/paper_state"
cp examples/numbers.example.json "$paper/paper_state/numbers.json"  # edit for your numbers
bash scripts/audit.sh "$paper" "$paper/paper_state"
# add --with-repro to actually execute the repro manifest
```

Output: one line per gate (`G2` numbers, `G3` citations, `G4` floats,
`G5` anonymity, `G6` build). Exit code 1 if any gate fails.

### Write a paper

Ask the agent:

```
Use papercraft in write mode for <paper dir>. Target: AAAI 2027.
Start with intake: read conferences/aaai.md, verify the CFP, fill
paper_state/conference.yaml, and write a 5-line scope memo with non-claims.
Do not draft prose until the claim ledger has at least 3 supported rows.
```

### Review a paper

```
Use papercraft in review mode on <pdf/tex>. Follow REVIEWING.md.
Every weakness needs a location and evidence; mark UNVERIFIED if you cannot
check a citation or artifact; score with the rubric and give confidence.
```

### Select a conference

```
Use papercraft in conference mode for NeurIPS. Open the current CFP,
fill the VERIFY fields in conferences/neurips.md, and record verified_on.
Do not apply any page limit from memory.
```

---

## What is inside

| Path | Purpose |
|---|---|
| `SKILL.md` | Router: modes, gates, prime directive, Harness rules |
| `WRITING.md` | Section-by-section writing playbook |
| `REVIEWING.md` | Adversarial review + scoring rubric |
| `conferences/` | 10 venue profiles + schema + index |
| `guides/literature.md` | Survey protocol, screening, closest-work delta |
| `guides/feasibility.md` | Go/no-go, resources, MPU, novelty risk |
| `guides/experiments.md` | Hypotheses, controls, power, leakage, registry |
| `guides/evidence.md` | Claim ledger, numbers, statuses |
| `guides/citations.md` | Citation verification and BibTeX hygiene |
| `guides/math.md` | Notation, derivation checklist, numeric checks |
| `guides/repro.md` | Run registry, cache vs run, artifact |
| `guides/acceptance.md` | Readiness, venue fit, reviewer risk, decision |
| `guides/harness.md` | Tool-by-tool operating rules |
| `guides/failure-modes.md` | Failure taxonomy with detectors |
| `guides/rebuttal.md` | Rebuttal and camera-ready corrections |
| `templates/` | Ledgers, registries, numbers, review report, checklist |
| `scripts/` | `check_numbers`, `check_citations`, `check_literature`, `check_floats`, `check_math`, `check_repro`, `check_anonymity`, `check_conference`, `score_review`, `score_acceptance`, `build`, `audit` |
| `examples/` | Minimal config and numbers file |
| `install.sh` / `install.py` | Multi-agent installer (native dirs + pointer files) |
| `scripts/install_selftest.sh` | Installer round-trip test (temp project only) |

---

## Design principles

1. **Evidence before prose.** A sentence without a ledger row is a draft TODO.
2. **One number, one source.** Numbers live in `numbers.json`; tables/figures
   are generated; stale values are `bad_values` that fail the checker.
3. **Citations are `UNVERIFIED` by default.** A DOI/arXiv/ACL page must be
   opened; "could not verify" is a valid status, "fabricated" requires a
   contradictory source.
4. **Floats are generated, labelled, referenced.** No hand-tuned bars; no orphan
   figures; captions carry the message.
5. **Conference rules are cached with an expiry.** Volatile fields are `VERIFY`;
   a profile older than 180 days is `STALE`.
6. **Fail closed.** A red gate stops the pipeline; it is never "fixed" by
   wording.
7. **Adversarial review.** The reviewer pass is separate from the author pass;
   it must give locations and evidence, and may not invent citations.

---

## Conference profiles

Included: **AAAI, NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, KDD, CHI, TMLR**, plus
a generic default. Every profile separates:

- **Volatile layer** (page limits, template, anonymity, checklist, LLM policy,
  supplementary, rebuttal) — YAML, marked `VERIFY`, with `verified_on`.
- **Stable layer** (review emphasis, structure, common pitfalls).

The skill will **not** apply a volatile rule until the profile is verified
against the current CFP. This is deliberate: venue rules are the most common
hallucination in AI-written papers.

Add a venue: copy `conferences/_default.md`, fill YAML, add an alias to
`conferences/index.yaml`, run `check_conference.py`.

---

## Scripts

```bash
python3 scripts/check_numbers.py --config paper_state/numbers.json --tex main.tex --check-source
python3 scripts/check_citations.py --tex main.tex --bib references.bib --strict
python3 scripts/check_floats.py --tex main.tex
python3 scripts/check_anonymity.py --root . --tex main.tex supplement.tex
python3 scripts/check_conference.py conferences/aaai.md --strict
bash scripts/build.sh /path/to/paper main.tex
bash scripts/audit.sh /path/to/paper /path/to/paper/paper_state
```

All scripts are dependency-free Python 3 (plus a POSIX shell and a LaTeX
toolchain for `build.sh`). They never write to the paper source.

Smoke test (a tiny paper that should pass every gate):

```bash
make test            # or: bash scripts/smoke_test.sh
```

It compiles `examples/mini-paper`, checks numbers/citations/floats/anonymity,
and exits 0 only if all gates pass.

---

## Limits (read this)

- Papercraft cannot verify that your experiments are correct; it can only check
  that the paper matches the artifact you give it.
- It cannot make a weak idea strong.
- It cannot guarantee acceptance.
- Online citation verification is a human/agent step; the scripts are
  structural only.
- A profile is a cache, not a CFP. If `verified_on` is missing, the rule is
  unknown, not "probably the same as last year".

---

## Contributing

See `CONTRIBUTING.md`. Good contributions: new venue profiles with verified
CFPs, new checkers with tests, failure-mode case studies, clearer rules.
Please do not add rules that encourage hiding limitations or fabricating
results.

---

## License

MIT. See `LICENSE`.

## Citation

```bibtex
@misc{papercraft2026,
  title  = {Papercraft: Evidence-First Paper Production and Review for AI Agents},
  author = {Papercraft contributors},
  year   = {2026},
  url    = {https://github.com/<your-org>/papercraft}
}
```

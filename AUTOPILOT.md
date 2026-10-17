# AUTOPILOT — topic in, paper pipeline out

> The user supplies **one thing**: a topic or question they care about.
> The agent runs the full Papercraft pipeline, asks at most **3 questions**, and
> stops at **3 human checkpoints**. It never invents results, citations, or
> experiments.

---

## 0. The contract

| Item | Rule |
|---|---|
| Input | A topic/question in natural language, optionally a venue |
| Questions | At most 3, all in one message: venue, constraints (time/compute/data), must-use code/data |
| Defaults | If the user says "you decide", pick and **record the assumption** in `paper_state/plan.json` |
| Human checkpoints | H1 research question + venue; H2 feasibility go/no-go; H3 final submission |
| Fabrication | Forbidden. No number without a source; no citation without verification; no experiment that was not run |
| Stop | If the MPU cannot be run with available resources, stop at feasibility and deliver a plan, not a fake paper |
| Output | A submission pack (`submission/`), a risk memo, and a reviewer report |

**The user is not expected to know LaTeX, statistics, or the literature.** The
agent is expected to explain, not to guess silently.

---

## 1. First message (the only one the user needs)

The agent sends:

```
I can run this end-to-end. I need at most 3 answers (defaults in brackets):
1. Venue? [AAAI 2027]
2. Constraints: deadline, compute, data/code you must use? [4 weeks, CPU-only, public data]
3. Anything you already know must be cited or avoided? [none]

If you don't care, say "you decide" and I'll record my assumptions.
```

Then it proceeds without waiting for a perfect answer.

---

## 2. Stages

| # | Stage | Agent does | Output | Gate |
|---|---|---|---|---|
| 0 | `topic` | Refine the topic into 3 falsifiable RQs; pick one (or ask H1) | `paper_state/rq.md` | G0 |
| 1 | `survey` | Search, screen, fill matrix, closest-3, novelty delta | `literature-matrix.csv`, `survey.md` | G3b |
| 2 | `feasibility` | MPU, resources, go/no-go; **H2** if risky | `feasibility.md` | G0 |
| 3 | `design` | Experiment cards, baselines, controls, seeds, decision rules | `experiment-plan.md` | G2/G8 plan |
| 4 | `execute` | Write code, run it, record command/output/hash | `data/results/*`, `repro-manifest.json` | G8 |
| 4b | `template` | Fetch/verify the official template; record provenance | `TEMPLATE.md`, `.sty/.bst/.cls` | G6 |
| 5 | `write` | Draft LaTeX from ledger + numbers; generate tables/figures | `main.tex`, tables, figures | G1–G4 |
| 6 | `audit` | Run all gates, fix, rebuild | gate report | G2–G8 |
| 7 | `review` | 3 reviewer personas (methods, stats, novelty), score | `review/` | G9 |
| 8 | `acceptance` | Risk memo + band; **H3** before submit | `acceptance.md` | G10 |
| 9 | `package` | Build PDF, anonymize, zip source/artifact | `submission/` | G11 |

Update `paper_state/plan.json` after every stage:

```bash
python3 scripts/papercraft.py mark survey done --note "12 rows, 3 closest"
python3 scripts/papercraft.py status
```

---

## 3. Stage prompts (agent copies these)

### 3.1 Topic → RQ

```
Read AUTOPILOT.md §2 stage 0. Given the user's topic, propose 3 falsifiable
research questions. For each: claim, evidence needed, closest 2 papers, risk.
Pick one if the user said "you decide"; otherwise ask H1 with the 3 options.
Write paper_state/rq.md and update plan.json.
Do not start the survey until the RQ has a falsifier.
```

### 3.2 Survey

```
Run stage 1. Search Semantic Scholar/ACL/arXiv, screen, fill
paper_state/literature-matrix.csv. Verify every key (DOI/arXiv/ACL page).
Write survey.md: closest-3 table + one-sentence delta + what is NOT claimed.
Run check_literature.py. Stop if <3 closest or any SUSPECT.
```

### 3.3 Feasibility

```
Run stage 2. Write the MPU, resource matrix, novelty risk, and a go/no-go.
If any critical resource is 0, STOP and deliver a plan (no fake results).
If conditional, scope the claim around the missing resource and say so.
Human checkpoint H2 if the decision is conditional/no-go.
```

### 3.4 Design

```
Run stage 3. One experiment card per question (guides/experiments.md).
Fix baselines, controls, splits, seeds, metrics, decision rule.
Write paper_state/experiment-plan.md and the registry rows.
Every experiment must have a falsifier.
```

### 3.5 Execute

```
Run stage 4. Implement the smallest scripts that produce the numbers.
Run them; record command, exit code, output path, sha256 in
paper_state/repro-manifest.json. Run check_repro.py --run.
If a command needs an API/private data you do not have, mark it cached and say so.
```

### 3.5b Template

```
Run stage 4b. Find the current author kit URL in the CFP. Run
`papercraft template --venue <id> --url <url>` (or --archive if the kit is
behind a login). Check TEMPLATE.md: source, sha256, version. If the kit's
version differs from the CFP, stop. Then copy the documentclass/usepackage
lines into main.tex.
```

### 3.6 Write

```
Run stage 5. Draft main.tex from the claim ledger and canonical numbers
(WRITING.md). Generate tables/figures from JSON; no hand-typed numbers.
Use the venue template from the profile; verify the CFP first.
```

### 3.7 Audit

```
Run stage 6. bash scripts/audit.sh <project> <project>/paper_state --with-repro.
Fix every BLOCKER. Re-run after each change. Do not "fix" by wording.
```

### 3.8 Review

```
Run stage 7. Simulate 3 reviewers: methods, statistics/evidence, novelty/related
work. Use REVIEWING.md and templates/review-score.json. Each weakness needs a
location and evidence. Run score_review.py. Summarize consensus and blockers.
```

### 3.9 Acceptance

```
Run stage 8. Fill templates/acceptance.json; run score_acceptance.py.
Write the memo + pre-mortem + rebuttal plan. H3: ask the user to approve submit.
```

### 3.10 Package

```
Run stage 9. Build in /tmp; run check_anonymity; create submission/
(main.pdf, source.zip, artifact.zip). Record hashes. Do not include paper_state.
```

---

## 4. Defaults (record them as assumptions)

| Choice | Default | When to change |
|---|---|---|
| Venue | AAAI main track | User names one; or the topic fits ACL/CHI/CVPR better |
| Paper type | evaluation/protocol or empirical study | Topic is theoretical → analysis paper |
| Compute | CPU-only, ≤ 4 h total | User grants GPU/API budget |
| Data | public/synthetic | User provides private data (check license) |
| Human study | none (explicitly not claimed) | User has IRB + recruitment |
| Scope | one clear claim + 3 contributions | Topic too broad; split |

Every default goes into `paper_state/plan.json` under `assumptions`.

---

## 5. Stop conditions (the important part)

Stop and report instead of writing:

- no verifiable closest work → the novelty claim is unknown;
- no data/code and no feasible public alternative → MPU impossible;
- experiment fails or is inconclusive → report the negative result;
- a citation cannot be verified → remove it or mark `UNVERIFIED`;
- a number has no source → `TODO(source)`, not a guess;
- reviewer/acceptance band = weak with a BLOCKER → revise, do not submit.

A plan + negative result is a valid deliverable. A fabricated paper is not.

---

## 5b. If the paper is rejected

1. Triage the reviews (`guides/resubmission.md` §1): novelty / evidence / scope /
   clarity / repro / theory / ethics.
2. `papercraft recommend --dir <p> --reviews review/*.json --type <type> --scale <scale>`.
3. Decide: fix and retry the same venue, or switch.
4. `papercraft resubmit --dir <p> --to <venue> --url <official-kit>` (or `--archive`).
5. Update the abstract/related work for the new audience; rerun all gates.
6. Never resubmit the same PDF with a new template.

## 6. Human checkpoints

| Checkpoint | When | What the user sees |
|---|---|---|
| H1 | After RQ options | 3 RQs, one recommended, venue |
| H2 | After feasibility | MPU, resources, go/no-go, what will be cut |
| H3 | Before submit | PDF, reviewer report, acceptance band, risks |

Everything else is automated. The user can say "go" at H1/H2 and only see H3.

---

## 7. Final deliverable

```
submission/
  main.pdf
  source.zip          # tex, bib, figures, data tables (no paper_state)
  artifact.zip        # code, data, README, license (optional)
  review/
    r1.json r2.json r3.json
    consensus.md
  acceptance.md
  audit-log.md
```

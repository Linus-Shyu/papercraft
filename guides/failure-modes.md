# Failure modes — what goes wrong, how to catch it, how to prevent it

> Use this as a checklist during `audit` and as a red-flag scanner while writing.
> Each row has a **detector** (mechanical where possible) and a **severity**.

---

## 1. Numbers

| ID | Failure | Example | Detector | Severity |
|---|---|---|---|---|
| N1 | Hand-typed number drifts from source | paper 0.57, JSON 0.5623 | `check_numbers.py`; grep stale | BLOCKER |
| N2 | Stale number after re-run | table updated, prose not | `bad_values` in `numbers.json` | BLOCKER |
| N3 | Denominator mismatch | macro vs micro; n=16 vs n=86 | read caption + JSON | MAJOR |
| N4 | Percentage vs percentage points | 0.00→0.45 written as +45% | recompute | MAJOR |
| N5 | Missing n / CI / seed | "0.56" with no n | caption check | MINOR–MAJOR |
| N6 | Rounding inconsistency | 0.56 / 0.562 / 0.5623 | grep variants | MINOR |
| N7 | Vacuous metric credit | empty page gets 0.35 because "no code → 1.0" | read scorer | MAJOR |
| N8 | Composite weights not summing | 0.4+0.35+0.25=1.0 | check | MINOR |
| N9 | Best-only reporting | max over seeds | check registry | MAJOR |

---

## 2. Citations

| ID | Failure | Example | Detector | Severity |
|---|---|---|---|---|
| C1 | arXiv ID mismatch | 2410.07820 is another paper | open the ID | BLOCKER |
| C2 | Workshop cited as conference | AI4E → AAAI proceedings | publisher page | MAJOR |
| C3 | Wrong author/year/venue | Das et al. cited as Huang | ACL/DOI page | MAJOR |
| C4 | Invented pages/volume | 107–117 with no source | publisher page | MINOR–MAJOR |
| C5 | Claim–citation mismatch | survey cited for a method | read abstract | MAJOR |
| C6 | Uncited required source | GSM8K used, not cited | grep concepts | MAJOR |
| C7 | Unverified key in PDF | `UNVERIFIED` left in bib | audit file | BLOCKER |
| C8 | Self-citation leak | "our previous work" | anonymity scan | MAJOR |

**Rule:** "unverified" ≠ "fabricated". Only call it fabricated with a
contradictory source.

---

## 3. Claims

| ID | Failure | Example | Detector | Severity |
|---|---|---|---|---|
| H1 | Abstract outruns evidence | "works across domains" from one exam | claim matrix | BLOCKER |
| H2 | Causal wording without control | "X improves Y" from correlation | read design | MAJOR |
| H3 | Generality from one dataset | "LLM tutors are…" | scope check | MAJOR |
| H4 | Contribution inflation | 4 contributions, 2 are the same | contribution list | MINOR |
| H5 | Definition drift | "frame" means two things | terminology grep | MAJOR |
| H6 | Unsupported "first" | "first to…" with no search | literature check | MAJOR |
| H7 | Hype adjectives | "novel, powerful, significant" | style scan | NIT |

---

## 4. Floats

| ID | Failure | Example | Detector | Severity |
|---|---|---|---|---|
| F1 | Orphan float | Figure 1 never referenced | `check_floats.py` | MAJOR |
| F2 | No label | `figure` without `\label` | same | MINOR |
| F3 | Hand-edited data in plot | bars don't match JSON | regenerate from data | BLOCKER |
| F4 | Self-contained caption missing | "Results on Z20." | read caption | MINOR |
| F5 | Unreadable at print size | 5pt labels, color-only | render/zoom | MINOR |
| F6 | Axis truncation not disclosed | y-axis starts at 0.5 | read plot code | MAJOR |
| F7 | Missing error bars/definition | mean only | caption | MINOR–MAJOR |
| F8 | Table overfull | text cut at margin | build log / PDF | MINOR |
| F9 | Inconsistent table/prose | table 0.56, prose 0.57 | `check_numbers.py` | BLOCKER |

---

## 5. Paper ↔ code

| ID | Failure | Example | Detector | Severity |
|---|---|---|---|---|
| P1 | Description ≠ implementation | "empties state" but code truncates text | read code | BLOCKER |
| P2 | Fake ablation | "w/o X" is text replacement | read code | BLOCKER |
| P3 | Baseline fallback | "Python Tutor" uses product frames | read code/data | BLOCKER |
| P4 | Circular metric | state keys derived from scored text | read code | BLOCKER |
| P5 | Coverage understated | 5/16 episodes but "n=16" | count files | MAJOR |
| P6 | Placeholder data | state values "mentioned" | scan JSON | MAJOR |
| P7 | Default-true flags | missing `tests_pass` counts as pass | read code | MAJOR |
| P8 | Non-reproducible experiment | no script/seed | registry | MAJOR |

**Detector:** for each experiment, read the entry script and the output JSON;
write one sentence "what the code actually changes". If it differs from the
paper, it is P1–P8.

---

## 6. Conference / compliance

| ID | Failure | Example | Detector | Severity |
|---|---|---|---|---|
| V1 | Page limit from memory | "AAAI is 8 pages" | CFP check | BLOCKER |
| V2 | Wrong template version | last year's `.sty` | template check | MAJOR |
| V3 | Anonymity leak | GitHub link, acknowledgments | `check_anonymity.py` | BLOCKER |
| V4 | Missing checklist | reproducibility form | CFP check | MAJOR |
| V5 | Dual submission | same paper elsewhere | author confirmation | BLOCKER |
| V6 | Modified style | custom `.sty` | diff vs official | MAJOR |
| V7 | Supplementary deadline | uploaded late | CFP | MAJOR |
| V8 | LLM policy | undisclosed generation | CFP | MAJOR |

---

## 7. Review-specific

| ID | Failure | Example | Detector | Severity |
|---|---|---|---|---|
| R1 | Unverified citation in review | "Smith et al. 2023 ignores…" | open it | BLOCKER |
| R2 | Impossible demand | "add a 10k-hour human study" | scope check | MAJOR |
| R3 | "I don't understand" = "unclear" | no location | reread | MINOR |
| R4 | Score/text mismatch | major issues, score 7 | rubric | MAJOR |
| R5 | Novelty hand-wave | "incremental" with no closest work | position | MAJOR |
| R6 | Artifact claim without run | "code fails" no command | rerun | MAJOR |
| R7 | Identity leak | naming authors | scan | BLOCKER |

---

## 8. LLM-specific (the big ones)

| Failure | Why it happens | Prevention |
|---|---|---|
| Fabricated citation | plausible-sounding title/ID | open every ID; `check_citations.py` |
| Placeholder number | "0.XX" or "~80%" | `numbers.json`; gate G2 |
| Stale number | re-run without propagation | generated tables; `bad_values` |
| Fake ablation | describing an intention, not the code | read code; "stress test" wording |
| Orphan float | writing text after figures move | `check_floats.py` |
| Claim drift | abstract written from memory | claim ledger; abstract last |
| Venue-rule hallucination | "usually 8 pages" | CFP fetch; `verified_on` |
| Fake reviewer objection | inventing a citation/limitation | `REVIEWING.md` rules |
| Over-hedging | fear of being wrong | one hedge + one boundary |
| Silent correction | fixing a number without notice | diff log; response letter |

---

## 9. Case studies (from a real audit)

These are illustrative; the pattern matters, not the specific paper.

1. **"w/o visual state"** — paper says it empties the state; code truncates the
   annotation. Detector: read `apply_baseline(..., "no_viz")`. Severity: P1.
2. **"module ablation"** — `w/o explain` sets the annotation to `""`; `w/o
   simulate` sets it to `"Okay."`. Detector: read the ablation function.
   Severity: P2.
3. **"Python Tutor baseline"** — only 5/16 episodes have traces; the rest use
   product frames. Detector: `tutor_traced_episodes` in the JSON. Severity: P3.
4. **Figure panel vs JSON** — bars are hard-coded and differ from the results
   file. Detector: regenerate the panel from JSON. Severity: F3.
5. **arXiv ID mismatch** — entry says "From Code to Animation", ID resolves to a
   gender-bias paper. Detector: open the ID. Severity: C1.

---

## 10. Red-flag phrases (grep before submission)

- "state-of-the-art" / "SOTA" without a same-setting baseline.
- "significantly" without a test.
- "novel" / "first" without a contrast.
- "as shown in Table X" where X has no such row.
- "we believe" / "it is well known".
- "due to space limitations" hiding a missing control.
- "approximately" before a number that should be exact.
- "n/a" in a column that should have a value.

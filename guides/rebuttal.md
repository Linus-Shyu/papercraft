# Rebuttal & camera-ready

> The goal of a rebuttal is not to "win"; it is to make the correct decision easy
> for the AC. Concede facts, clarify scope, and never introduce a number that is
> not in the artifact.

---

## 1. Before writing

1. Read all reviews; make a table of **every** point (not just the hostile ones).
2. Classify each point:

| Class | Meaning | Response |
|---|---|---|
| `FACT` | We made an error | Concede, correct, say where |
| `SCOPE` | Reviewer wants a different paper | Clarify boundary; cite paper text |
| `EVIDENCE` | Missing control/analysis | Add if cached/cheap; else say what is feasible |
| `CLARITY` | Misread due to writing | Fix wording; thank |
| `MISREAD` | Reviewer missed something | Point to section/table/line |
| `OUT-OF-SCOPE` | Impossible in rebuttal | Say why; offer camera-ready plan |

3. Identify **shared concerns** across reviewers; answer once, point to the
   answer from each.
4. Decide what can be added **within the rebuttal window** (cached analyses,
   re-plots, extra numbers from existing JSON). Do not promise a new study.

---

## 2. Response structure

```
We thank the reviewers. Below we address each point; R1/R2/R3 refer to ...

## Common concerns
C1. <shared concern> — <one paragraph with evidence + what changed>

## R1
R1.1 <short quote of the point>
Response: <concede/clarify/evidence>. <pointer to section/table/line>.
R1.2 ...

## R2
...

## Summary of changes
- <change 1> (section/table)
- <change 2>
```

Rules:

- **Quote the point** so the AC can follow without the review open.
- **One paragraph per point**; no wall of text.
- **Evidence first**, opinion second.
- **No new claims**; if a new analysis is added, label it "additional analysis on
  cached outputs" and give the command.
- **No arguing with a correct criticism**; say "we agree, and we will…".
- **Never** say "the reviewer is wrong" without a pointer.

---

## 3. Conceding without collapsing

Bad: "We thank the reviewer for this insightful comment and will add it to the
limitations." (says nothing)

Good:

> We agree that n=16 cannot support a population-level claim. The paper already
> states this in §7 and reports no significance tests; the pilot is used to test
> whether the contract can score heterogeneous traces, and the verifiable splits
> (720 episodes) test metric behavior. We will make this scope explicit in the
> abstract and add the missing boundary sentence in §5.

---

## 4. Camera-ready correction policy

If the paper is accepted:

1. **Fix errors, not results.** Correct descriptions, citations, figures, and
   numbers that do not match the artifact.
2. **If a headline number changes** because of a bug fix:
   - update every table/figure/abstract;
   - regenerate the artifact;
   - record the correction in a diff log and, if the venue allows, a note to the
     AC/PC;
   - never silently change a number reviewers saw.
3. **Rebuild and re-run all gates** (G2–G6).
4. **Update the artifact** so paper = code = data.
5. **Record hashes** (PDF, zip) in `audit-log.md`.

Camera-ready diff log format:

```
| file | change | reason | evidence | date |
|---|---|---|---|---|
| references.bib | fixed arXiv ID for wei2024 | ID resolved to another paper | arxiv.org/abs/... | 2026-10-17 |
| fig4.tex | regenerate panel D from JSON | hand-coded bars mismatched | data/results/e9... | 2026-10-17 |
| main.tex §6.1 | "empties state" → "truncates rationale" | code does not empty state | metrics.py:174 | 2026-10-17 |
```

---

## 5. What not to do

- Do not add a new experiment in the rebuttal and present it as if it was in the
  paper.
- Do not cite a paper you have not opened.
- Do not promise "we will add a 10k-hour human study" to satisfy a reviewer.
- Do not re-run the whole pipeline the night before the deadline without a
  freeze and a diff log.
- Do not change the template/style to gain space; cut content instead.
- Do not argue about a number; show the source or fix it.

---

## 6. Rebuttal checklist

- [ ] Every reviewer point is in the table, with a class.
- [ ] Shared concerns answered once.
- [ ] Each response has a pointer (`§`, `Table`, `Fig`, `line`).
- [ ] No new claim without a source.
- [ ] No unverified citation.
- [ ] Tone: thanks + evidence + concession where true.
- [ ] Length within the venue limit.
- [ ] A colleague read it for tone and clarity.

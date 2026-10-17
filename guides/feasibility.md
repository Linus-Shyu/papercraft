# Feasibility — should this paper be written at all?

> Answer five questions before committing. A "no" is cheaper now than after the
> experiments.

---

## 1. The five questions

| # | Question | Evidence to write down |
|---|---|---|
| F1 | What is the **claim**? | One sentence, falsifiable (see `WRITING.md` §2) |
| F2 | What is the **minimum publishable unit** (MPU)? | Smallest experiment that supports the claim |
| F3 | Do we have the **resources**? | data access, compute, annotators, IRB, API budget, time |
| F4 | What could **falsify** it? | control / negative result that would kill the claim |
| F5 | What is the **venue fit**? | profile + 3 closest papers from that venue |

If F2 cannot be stated, the project is not ready.

---

## 2. Feasibility matrix

| Dimension | Score 0–2 | Notes |
|---|---|---|
| Data access | 0 none / 1 partial / 2 ready | license, PII, size |
| Compute | 0 none / 1 shared / 2 dedicated | GPU-hours, API budget |
| Human labels | 0 none / 1 proxy / 2 experts | IRB, pay, time |
| Implementation | 0 unknown / 1 prototype / 2 working | repo, tests |
| Evaluation | 0 ad hoc / 1 metrics / 2 controls + CI | baselines |
| Novelty | 0 known / 1 incremental / 2 clear delta | closest 3 |
| Timeline | 0 impossible / 1 tight / 2 comfortable | weeks to deadline |

Rule of thumb: any 0 in Data/Compute/Human/Evaluation is a **no-go** unless the
claim is explicitly scoped around it (and the paper says so).

---

## 3. Novelty risk

- Search the closest 5; if 3 already do the same thing, stop or change the claim.
- If the delta is "better numbers", the paper needs a strong compute/baseline
  story; otherwise it is a workshop paper.
- If the delta is "new evaluation object", the paper needs falsifiers, not SOTA.

---

## 4. Minimum publishable unit (MPU)

Write it as:

```
With <data>, <method>, and <controls>, we can show <claim> at <n>.
If <control> shows <pattern>, the claim fails.
```

The MPU must be runnable **before** the full paper. If the MPU is 6 months away,
the paper is not feasible for this deadline.

---

## 5. Go / no-go

| Decision | Criteria |
|---|---|
| Go | MPU runnable in ≤ 2 weeks; closest 3 known; venue fit; no 0 in critical resources |
| Conditional go | One 0 with a written workaround and a scope boundary |
| No-go | Claim untestable, data unavailable, or closest work already does it |

Record the decision in `templates/feasibility-memo.md`; revisit after the pilot.

---

## 6. Red flags

- "We will figure out the baselines later."
- A claim that requires a human study but no IRB/recruitment plan.
- A benchmark that does not exist yet and is the main contribution.
- Deadline-driven scope that silently drops controls.

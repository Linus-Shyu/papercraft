# Literature survey — search, screen, position, verify

> Goal: know the **closest 3 papers** better than the reviewer does, and be able to
> state the delta in one sentence.

---

## 1. Protocol (write it down before searching)

| Field | Example |
|---|---|
| Question | "How are process-level tutoring traces evaluated?" |
| Keywords | tutor evaluation, process supervision, code explanation, trace grounding |
| Databases | Semantic Scholar, ACL Anthology, arXiv, ACM DL, Google Scholar |
| Date range | 2019–2026 (plus 2 foundational) |
| Inclusion | evaluates tutoring/explanation traces; proposes metrics; benchmarks |
| Exclusion | pure model papers with no evaluation object; no trace/state |
| Snowball | backward/forward from the closest 3 |
| Stop rule | 3 consecutive searches add no new closest work |

Record the protocol in `paper_state/literature-matrix.csv` notes or a memo; a
reviewer may ask "how did you search?".

---

## 2. Screening

1. Title/abstract screen → keep if it evaluates the same **object** (not just the
   same task).
2. Full-text screen for: metric, unit of analysis, data, baselines, limitations.
3. Extract into the matrix (`templates/literature-matrix.csv`):

| Column | Meaning |
|---|---|
| `key` | BibTeX key |
| `title` | exact title |
| `year` | published year |
| `venue` | conference/journal/workshop |
| `role` | foundation / baseline / closest / adjacent / survey |
| `closest` | yes/no (at most 5 yes) |
| `verified` | VERIFIED / PARTIAL / UNVERIFIED / SUSPECT |
| `claim_supported` | C1;C2 (which claims it supports) |
| `gap` | what it does **not** do (specific) |
| `notes` | one-line delta |

`check_literature.py` enforces the schema and flags missing verification.

---

## 3. Closest-work analysis (the part reviewers check)

For each of the closest 3, write:

```
Paper: <key>
Object: <what it evaluates>
Unit: <frame/step/dialogue/answer>
Metrics: <names>
Evidence: <data, n, controls>
What it cannot do: <specific limitation>
Our delta: <one sentence; must be checkable in our paper>
```

If the delta is "we use a new dataset", say why the dataset changes the
conclusion. If the delta is "we combine X and Y", show an ablation that the
combination is necessary.

---

## 4. Novelty statement

Write one paragraph and one table:

> Prior work evaluates <object> as <projection>. None reports <missing binding>;
> therefore <failure> cannot be localized. We add <binding/metric> and show
> <evidence>.

Table: `work × object × unit × missing binding × our addition`.

Avoid "first" unless you searched and state the search. "To our knowledge" is
acceptable only with a dated search protocol.

---

## 5. Verification

Every key in the matrix must be `VERIFIED` or explicitly `PARTIAL` with a reason.
Use `guides/citations.md`; `SUSPECT` keys are blockers. Never write a related-work
sentence from a title alone: read at least the abstract and the relevant section.

---

## 6. Red flags

- Related work is a list of one-sentence summaries with no delta.
- The closest paper is cited but not discussed.
- A survey is used to support a specific technical claim.
- "No prior work" without a search protocol.
- The citation exists but its venue/year is wrong (see `guides/citations.md`).

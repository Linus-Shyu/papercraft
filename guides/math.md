# Math audit — what a script can and cannot catch

> A checker can catch undefined symbols, unbalanced delimiters, and arithmetic
> slips. It **cannot** prove a derivation. The protocol below is the part that
> matters; `check_math.py` is the mechanical net.

---

## 1. Notation table (before any equation)

| Symbol | Meaning | Domain |
|---|---|---|
| $n$ | number of episodes | positive integer |
| $T_e$ | frames in episode $e$ | positive integer |
| $K_t$ | salient state keys | finite set |
| $a_t$ | rationale text | string |

Rules:

- Every symbol used later appears here.
- Subscripts/superscripts are defined (`$t$`, `$e$`, `$i$`).
- Sets vs sequences vs scalars are explicit.
- Units are stated (ms, %, count).

---

## 2. Definitions before use

- Define the object, the metric, and the aggregation level before the first use.
- State whether means are frame-level, episode-level, or corpus-level.
- State the empty-set convention: `EAR=1` when $K_t=\varnothing$ is a choice, not
  a law; justify it or it looks like vacuous credit.
- State what happens when a denominator is 0 (`n/a`, not 0).

---

## 3. Derivation checklist

1. Start from the definition; do not skip a step that a reviewer cannot fill.
2. Check the summation index and limits.
3. Check each denominator: is it the count you think?
4. Check units/dimensions on both sides.
5. Check boundary cases: empty set, n=1, zero denominator, all-equal values.
6. Check monotonicity/direction: does the metric increase when the property
   increases?
7. Check the composition: if a score is a weighted sum, do weights sum to 1?
8. Check the code: does `metrics.py` implement exactly this formula?

---

## 4. Numeric spot checks

For each numeric claim in the paper, recompute with a calculator/script:

- `0.4 + 0.35 + 0.25 = 1.0` (weights).
- `428 + 5350 = 5778` (frames).
- `120 + 600 = 720` (episodes).
- `73.3 - 72.6 = 0.7` (delta).
- `0.00 -> 0.45` is **45 pp**, not 45%.

`check_math.py` evaluates a list of simple expressions from `math.json`.

---

## 5. Code–formula consistency

For every equation, open the implementation and check:

- same variables, same order of operations;
- same aggregation (macro vs micro);
- same handling of missing values;
- same rounding (only for display, not for intermediate values).

If the paper says "empties $s_t$" and the code truncates the annotation, the
formula is not the issue — the description is. Log it as a paper–code mismatch.

---

## 6. Common errors

| Error | Example | Check |
|---|---|---|
| Undefined symbol | $n$ used but only $m,v$ defined | notation table |
| Empty-set credit | $K_t=\varnothing \Rightarrow EAR=1$ | boundary case |
| Wrong denominator | divide by frames when averaging episodes | aggregation |
| Sum limits | $\sum_{t=1}^{T}$ but $T$ is per-episode | notation |
| Percent vs pp | +45% for 0.00→0.45 | recompute |
| Double counting | same frame in two splits | split hash |
| Code drift | formula updated, code not | diff |
| Unit mismatch | ms vs s in a ratio | units |

---

## 7. `check_math.py`

```bash
python3 scripts/check_math.py --tex main.tex --config paper_state/math.json
python3 scripts/check_math.py --tex main.tex --config paper_state/math.json --list
```

It checks:

- duplicate equation labels;
- equation labels never referenced (warn);
- `\left`/`\right` and `\begin`/`\end` balance per block;
- symbols not in `math.json` (warn; fail with `--strict`);
- numeric expressions from `math.json` (fail on mismatch).

It does **not** check semantic correctness, dimensional analysis, or whether the
derivation is valid. Those are human/agent review steps.

---

## 8. Review questions

1. Can I restate the metric in one sentence without looking at the formula?
2. Does the formula match the code path?
3. What happens at the boundary (empty, zero, n=1)?
4. Is the aggregation level stated?
5. Are the weights/units consistent?
6. Is any symbol undefined or overloaded?

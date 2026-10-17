# Experiment design — from claim to evidence

> Every experiment must answer one question and be able to **fail**. If no outcome
> would change your mind, it is a demo, not an experiment.

---

## 1. Experiment card

Write one card per experiment before running it:

```
ID: E3
Question: Does the metric separate trace-aware from answer-only tutors?
Hypothesis: trace-aware EAR > answer-only EAR by >= 0.2
Conditions: reference / direct-answer / w/o state
Unit: episode (n=16); frame-level reported separately
Metric: EAR (macro over episodes), SC, OTP
Control: same frames, same annotations except the manipulated factor
Falsifier: EAR difference < 0.05 or CI includes 0
Seeds: N/A (deterministic); if stochastic, 5 seeds
Output: data/results/e3.json
Decision: if falsified, claim C2 is downgraded to WEAK/UNSUPPORTED
```

If a field is unknown, the experiment is not ready.

---

## 2. Variables

| Type | Examples | Rule |
|---|---|---|
| Independent | state visibility, steering, model family | change one at a time |
| Dependent | EAR/SC/VGR/SCR/OTP, judge score | pre-register direction |
| Controlled | split, prompt, decoding, budget | hold fixed or report variation |
| Nuisance | seed, order, hardware | randomize or block |

Confounds to check: model family vs judge family, prompt vs contract, frame count
vs annotation length, dataset vs difficulty.

---

## 3. Baselines

- **Floor**: answer-only or random; shows the metric is not free.
- **Reference**: product/expert trace; shows the ceiling.
- **Strong**: same-family LLM under the same budget; the one reviewers care about.
- **Ablation**: remove the mechanism, not the text (see `guides/failure-modes.md`).

Every baseline must use the **same split, prompt budget, and evaluation script**.
If not, the comparison is descriptive only.

---

## 4. Controls and falsifiers

- **Projection isolation**: hold one projection fixed, flip another.
- **Negative control**: blank/empty input should score low; if it scores high, the
  metric has a vacuous-credit bug.
- **Placebo**: same-length text with no relevant content.
- **Wrong trace**: executable but wrong transition; tests OTP.
- **Paraphrase**: same meaning, different words; tests lexical vs semantic.

A control that cannot fail is not a control.

---

## 5. Metrics and statistics

- Report **n** (episodes/frames) for every number.
- Report **mean + CI** or per-seed spread; do not report best-of-N only.
- For a difference claim: paired comparison on the same units; bootstrap CI.
- For a correlation: n, rho, p (or CI); do not causalize.
- For a judge: same-family and cross-family; report both.
- Multiple comparisons: say how many; correct or label exploratory.

Power intuition: with n=16, only large effects are distinguishable; do not claim
small differences. If the claim needs a small effect, increase n or downgrade to
"descriptive".

---

## 6. Splits and leakage

- Freeze the test split before tuning; record the hash.
- No test-set prompt selection; no "best checkpoint on test".
- Deduplicate train/test (near-duplicates, templates, same problem family).
- Report the source of each split (product-mined, curated, synthetic).
- Synthetic/constructed splits are valid for **metric behavior**, not for
  population claims; say so.

---

## 7. Pre-registration (lightweight)

Before running, write in `paper_state/experiment-registry.csv`:

```
exp_id, hypothesis, command, seed, output, table, status, owner
```

After running, add the output hash and the observed value. If you change the
hypothesis after seeing results, mark it `exploratory`.

---

## 8. Ablations

- Remove a **mechanism** (module, input channel, state), not the output text.
- If the "ablation" is a text substitution, call it a **stress test**.
- Report the manipulation exactly: what changed, what stayed fixed.
- If removing a module improves the score, explain why (artifact, leakage,
  over-regularization); do not hide it.

---

## 9. Negative results

- Report them; they are evidence about the boundary.
- A negative result that kills a sub-claim is fine; a hidden one is not.
- If the main claim survives only after removing a condition, that is a scope
  change; state it.

---

## 10. Compute and ethics

- Record hardware, runtime, model versions, API dates.
- Estimate cost before running a sweep; stop at the budget.
- Human subjects: IRB/consent; simulated users are not human evidence.
- Data license and PII; do not put raw exam scans in the artifact without rights.

---

## 11. Checklist

- [ ] One question per experiment; falsifier written.
- [ ] Same split/budget for all baselines.
- [ ] Control changes one variable.
- [ ] n, seeds, CI reported.
- [ ] Leakage checked.
- [ ] Command + output + hash in the registry.
- [ ] Negative results reported.
- [ ] Claim status updated in the ledger.

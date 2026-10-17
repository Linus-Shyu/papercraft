# Acceptance assessment — a risk memo, not a prediction

> No one can predict a review outcome. What you can do is estimate **scientific
> readiness**, **venue fit**, and **reviewer risk**, and decide whether to submit,
> revise, or change venue.

---

## 1. Three separate questions

| Question | Evidence | Output |
|---|---|---|
| Is the science ready? | claims ↔ evidence; controls; numbers; artifact | readiness score |
| Is it a fit for this venue? | profile + 3 closest papers from the venue | fit score |
| What will reviewers attack? | pre-mortem; risk register | risk list |

Do not collapse them into one number until the end.

---

## 2. Readiness rubric (1–4)

| Dimension | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Claim–evidence | unsupported | weak | supported, bounded | supported + controls |
| Novelty | known | incremental | clear delta | new object/insight |
| Rigor | ad hoc | single run | baseline + control | controls + CI + ablations |
| Clarity | hard to follow | partial | clear | excellent |
| Reproducibility | none | partial | script + data | clean artifact + hash |

Average ≥ 3.0 with no 1 in Claim/Evidence or Rigor → **competitive**.
Average 2.4–2.9 → **borderline**.
Average < 2.4 or any 1 in Claim/Evidence → **not ready**.

---

## 3. Venue fit

- Read the profile; check the 3 closest papers from the same venue.
- Is the contribution type one the venue rewards (method / benchmark / analysis /
  application / human study)?
- Is the page budget enough to show the evidence? If not, the paper is not ready
  for that venue (or needs a shorter format).
- Is the novelty delta legible to that community's reviewers?

---

## 4. Reviewer risk register

For each likely objection:

```
Risk: "n=16 is too small"
Severity: MAJOR
Evidence in paper: pilot scope; 720 verifiable episodes for metric behavior
Mitigation in rebuttal: scope clarification + falsifier evidence
Residual risk: reviewer still discounts
```

Common risks: small n, no human study, constructed controls, weak baselines,
lexical metrics, judge bias, missing related work, unclear novelty, artifact not
running, overclaiming, anonymity leak.

If a BLOCKER risk has no mitigation, do not submit.

---

## 5. Forecast bands (not probabilities)

| Band | Conditions | Action |
|---|---|---|
| Competitive | readiness ≥ 3.0; fit ≥ 3; no BLOCKER; ≤ 2 MAJOR | submit |
| Borderline | readiness 2.4–2.9 or fit 2; ≤ 1 BLOCKER with mitigation | submit only if rebuttal plan is strong; otherwise revise |
| Weak | readiness < 2.4 or unresolved BLOCKER | revise or change venue |

`score_acceptance.py` computes the band from `paper_state/acceptance.json` and
prints the top risks; it does not output a probability.

---

## 6. Decision memo

`templates/acceptance-memo.md`:

```
Venue / deadline:
Readiness: X/4 (claim, novelty, rigor, clarity, repro)
Fit: X/4
Top 3 reviewer risks + mitigation
What would change the band (one experiment / one clarification)
Decision: submit / revise / resubmit elsewhere
```

---

## 7. Pre-mortem

Assume the paper is rejected. Write the three most likely review sentences.
For each, write:

- the evidence that answers it;
- the experiment that would answer it (if cheap);
- the scope sentence that concedes it.

If you cannot answer a likely rejection reason, the paper is not ready.

---

## 8. After the decision

- Submit: freeze the PDF, record the hash, prepare the rebuttal table.
- Revise: turn the risk register into experiments; re-run gates.
- Change venue: adjust the profile, page budget, and novelty framing; do not
  resubmit the same PDF blindly.

---

## 9. Red flags

- "It will probably be fine."
- A forecast with decimals but no evidence.
- Ignoring a BLOCKER because the deadline is close.
- Submitting to a venue whose reviewers do not share the paper's object.

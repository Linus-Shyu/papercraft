# Rejection → resubmission

> A rejection is data: it tells you which **claim** or **evidence** the venue did
> not accept. Decide whether to fix the paper, change the venue, or both.

---

## 1. Triage the reviews (do this before choosing a venue)

For each review:

| Field | What to extract |
|---|---|
| Decision | reject / weak reject / borderline (and confidence) |
| Main objection | one sentence, in the reviewer's words |
| Category | novelty / evidence / scope / clarity / repro / theory / ethics |
| Actionable? | can it be fixed with existing data/code? |
| Venue-specific? | is it about this venue's audience/format? |

Count categories across reviews:

- **Novelty/related work** → fix positioning, add closest-work delta, consider a
  venue that values the object/benchmark rather than SOTA.
- **Evidence/scale** → add controls/seeds/larger split; if impossible, scope the
  claim and choose a venue that accepts pilot/analysis papers.
- **Scope/fit** → the paper is in the wrong room; change venue.
- **Clarity** → rewrite; do not change venue to avoid it.
- **Repro/artifact** → fix the artifact; this travels with you.
- **Theory/math** → fix or downgrade the claim.
- **Ethics** → fix before any resubmission.

If the same **fatal** objection appears in ≥2 reviews and cannot be fixed with
existing resources, do not resubmit the same paper; change the claim or the
project.

---

## 2. Fix vs switch

| Situation | Action |
|---|---|
| One fixable evidence gap | fix, resubmit to the **same** venue next cycle |
| Novelty objection but clear object/benchmark | reposition; consider ACL/EMNLP/TMLR |
| Scope mismatch | **change venue**; reuse the paper |
| Small-n pilot, strong falsifiers | TMLR / workshop / evaluation-focused venue |
| Human-centered study | CHI / CSCW / AIED (verify) |
| Applied/deployment | KDD / industry track (verify) |
| Vision/multimodal | CVPR / ICCV / ECCV (verify) |
| NLP/dialogue/education | ACL / EMNLP / NAACL (verify) |
| General ML method | NeurIPS / ICML / ICLR |
| Needs fast, rolling review | TMLR |

`papercraft recommend` uses topic/type/scale + review categories to produce a
**shortlist**, not a decision. Deadlines and page limits are always `VERIFY`.

---

## 3. Venue shortlist (verify every CFP)

| Venue | Best for | Watch |
|---|---|---|
| AAAI | general AI, evaluation, applied | checklist; broad audience |
| NeurIPS | ML methods, benchmarks | evidence scale; checklist |
| ICML | ML theory/methods | technical depth |
| ICLR | ML methods/analysis | OpenReview response |
| ACL | NLP/dialogue/education | limitations; ARR |
| EMNLP | empirical NLP | variance/seeds |
| CVPR | vision/multimodal | benchmark gains; visuals |
| KDD | applied/data mining | deployment/scale |
| CHI | HCI/human study | contribution type; ethics |
| TMLR | journal, rolling, correctness | no deadline; certification |

---

## 4. Switch the template

```bash
papercraft resubmit --dir <paper> --to acl \
  --url https://.../acl-style.zip
# or, if the kit is behind a login:
papercraft resubmit --dir <paper> --to acl --archive ~/Downloads/acl-style.zip
```

What it does:

1. fetches the **new** template into a temp project (old files untouched if it
   fails);
2. archives the old `.sty/.bst/.cls` and `TEMPLATE.md` under
   `template/previous-<old>-<timestamp>/`;
3. copies the new style files + `TEMPLATE.md`;
4. updates `paper_state/conference.yaml` and `plan.json` (venue, switch log);
5. resets `review`, `acceptance`, `package` to `pending`;
6. writes `RESUBMISSION.md` with reasons, fixes, template provenance, checklist.

`--dry-run` prints the plan without changing anything. If no verified source is
available, it stops and prints the exact `papercraft template --venue ...`
command; the old template remains intact.

---

## 5. What to change in the paper

- **Abstract**: remove the old venue's framing; state the object and the
  evidence scale honestly.
- **Intro/related**: add the closest work the reviewers named; state the delta.
- **Experiments**: add the control/seed/scale the reviews asked for, or scope
  the claim and say why.
- **Limitations**: make the fatal objection a explicit boundary.
- **Template**: swap the class/style; re-check page limits, anonymity,
  checklist, appendix, references.
- **Artifact**: rerun `check_repro --run`; update the zip.

Do **not** resubmit the same PDF with a new template. That is the fastest way to
get the same rejection.

---

## 6. Policies

- **Dual submission**: do not submit to two venues at once; check each CFP.
- **arXiv**: allowed by many venues, but check the current policy; do not
  violate anonymity.
- **Reviews**: do not publish them; use them privately.
- **Response**: if the venue allows a rebuttal, use `guides/rebuttal.md`; if
  rejected, do not argue with the decision—fix the paper.

---

## 7. Resubmission memo

`RESUBMISSION.md` should contain:

```
Old venue / decision / date
New venue / why (fit signals) / what to verify in the CFP
Review categories + counts
Fixes done (with file:line)
Fixes not done + why (scope)
Template switch: old → new, source, sha256
New page limit / anonymity / checklist
Gates to rerun
```

---

## 8. Red flags

- Choosing a venue only because the deadline is close.
- Changing venue to avoid a correct criticism.
- Reusing the old template "because it compiles".
- Submitting before `papercraft check` is green.
- Claiming the new venue has a page limit you did not verify.

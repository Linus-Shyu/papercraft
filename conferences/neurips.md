---
id: neurips
name: Conference on Neural Information Processing Systems
year: null
source_url: https://neurips.cc/
verified_on: null
status: UNVERIFIED
template: VERIFY
review_model: VERIFY
anonymity: VERIFY
page_limit_main: VERIFY
page_limit_refs: VERIFY
appendix: VERIFY
supplementary: VERIFY
reproducibility: VERIFY
llm_policy: VERIFY
dual_submission: VERIFY
rebuttal: VERIFY
camera_ready: VERIFY
---

# NeurIPS

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~9 pages of content plus references; mandatory paper checklist; two-column NeurIPS style. **Verify the current year.**

## Review emphasis (stable)

Empirical rigor and clarity of claims; broader impact and limitations; checklist consistency; reproducibility. Strong papers make the evaluation question explicit and rule out alternatives.

## Structure notes (stable)

Abstract; intro; related; method; experiments (baselines, ablations, compute); results; limitations/broader impact; checklist. The checklist is part of the review, not an appendix formality.

## Common pitfalls

Checklist answers that promise code/data that are not in the supplement; missing compute details; claims that outrun the checklist; page-limit counting; anonymity leaks in links/acknowledgments.

## Verify before writing

- [ ] page limit and reference policy
- [ ] paper checklist fields and required answers
- [ ] broader impact / limitations requirements
- [ ] supplementary deadline and format
- [ ] LLM-use policy

## CFP lookup

1. Open <https://neurips.cc/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/neurips.md`.

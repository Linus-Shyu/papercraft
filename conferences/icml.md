---
id: icml
name: International Conference on Machine Learning
year: null
source_url: https://icml.cc/
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

# ICML

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~8 pages of content plus references; two-column ICML style; reproducibility statement/checklist. **Verify the current year.**

## Review emphasis (stable)

Technical depth and correctness; well-controlled experiments; theoretical or empirical insight; reproducibility. Reviewers reward a clear statement of what is new relative to the closest method.

## Structure notes (stable)

Abstract; intro; related; problem setup; method; experiments; results; discussion/limitations; references; appendix. A short reproducibility statement is common.

## Common pitfalls

Overlength appendix used to hide missing main-paper evidence; unclear notation; single-seed results presented as robust; missing compute; template version mismatch.

## Verify before writing

- [ ] page limit and appendix policy
- [ ] reproducibility statement requirements
- [ ] anonymity scope
- [ ] supplementary rules
- [ ] rebuttal format

## CFP lookup

1. Open <https://icml.cc/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/icml.md`.

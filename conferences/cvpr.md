---
id: cvpr
name: IEEE/CVF Conference on Computer Vision and Pattern Recognition
year: null
source_url: https://cvpr.thecvf.com/
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

# CVPR

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~8 pages (content) plus references; IEEE two-column format; supplementary; double-blind. **Verify the current year.**

## Review emphasis (stable)

Visual results and quantitative gains on standard benchmarks; novelty of the method; ablations; reproducibility. Figures must be readable at print size.

## Structure notes (stable)

Abstract; intro; related; method; experiments; ablation; qualitative results; limitations; references; supplementary.

## Common pitfalls

Benchmark leakage; unfair compute/baseline comparisons; figure readability; page-limit counting; anonymity in supplementary videos/links.

## Verify before writing

- [ ] page limit and supplementary rules
- [ ] IEEE template version
- [ ] anonymity policy
- [ ] rebuttal format
- [ ] code/data release policy

## CFP lookup

1. Open <https://cvpr.thecvf.com/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/cvpr.md`.

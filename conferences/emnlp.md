---
id: emnlp
name: Conference on Empirical Methods in Natural Language Processing
year: null
source_url: https://sigdat.org/
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

# EMNLP

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~8 pages (content) plus references; two-column ACL style; limitations section; ARR. **Verify the current year.**

## Review emphasis (stable)

Empirical contribution; strong baselines; statistical reliability; data/annotation; responsible NLP. Reviewers expect multiple seeds or clear variance reporting for empirical claims.

## Structure notes (stable)

Similar to ACL: abstract, intro, related, method, experiments, results, limitations, ethics, references, appendix.

## Common pitfalls

Weak baselines; missing variance; limitations as an afterthought; checklist mismatch; page-limit counting.

## Verify before writing

- [ ] page limit
- [ ] ARR/commitment dates
- [ ] limitations and ethics requirements
- [ ] anonymity policy
- [ ] supplementary rules

## CFP lookup

1. Open <https://sigdat.org/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/emnlp.md`.

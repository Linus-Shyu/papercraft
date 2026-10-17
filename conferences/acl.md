---
id: acl
name: Annual Meeting of the Association for Computational Linguistics
year: null
source_url: https://aclweb.org/
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

# ACL

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~8 pages long / ~4 pages short (content), plus references; two-column ACL style; mandatory limitations section; ARR submission. **Verify the current year.**

## Review emphasis (stable)

NLP-specific contribution; responsible NLP checklist; limitations; data/annotation quality; reproducibility. Long and short papers have different expectations.

## Structure notes (stable)

Abstract; intro; related; method; experiments; results; limitations (mandatory); ethics/broader impact as required; references; appendix. Use the official ACL template.

## Common pitfalls

Missing mandatory limitations; responsible NLP checklist inconsistencies; anonymized supplementary leaks; page-limit counting; dataset licensing.

## Verify before writing

- [ ] long/short page limits
- [ ] limitations section requirement
- [ ] responsible NLP checklist
- [ ] ARR vs direct submission
- [ ] anonymity and preprint policy

## CFP lookup

1. Open <https://aclweb.org/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/acl.md`.

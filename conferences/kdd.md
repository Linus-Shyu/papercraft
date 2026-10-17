---
id: kdd
name: ACM SIGKDD Conference on Knowledge Discovery and Data Mining
year: null
source_url: https://kdd.org/
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

# KDD

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~9 pages (content) plus references; ACM format; reproducibility track. **Verify the current year.**

## Review emphasis (stable)

Applied impact and data-driven insight; scalability; real-world validity; reproducibility. Reviewers value deployment details and honest limitations.

## Structure notes (stable)

Abstract; intro; related; problem; method; experiments (offline + online if possible); deployment; limitations; references.

## Common pitfalls

Offline-only claims; unrepresentative data; missing scale/cost; page-limit counting; anonymity of industrial data.

## Verify before writing

- [ ] page limit
- [ ] reproducibility track requirements
- [ ] ACM template version
- [ ] anonymity/industry policy
- [ ] rebuttal format

## CFP lookup

1. Open <https://kdd.org/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/kdd.md`.

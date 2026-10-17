---
id: tmlr
name: Transactions on Machine Learning Research
year: null
source_url: https://jmlr.org/tmlr/
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

# TMLR

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Journal-style, rolling submissions; no fixed page limit; certification-based review; reproducibility statement. **Verify the current policy.**

## Review emphasis (stable)

Correctness, clarity, and reproducibility over novelty alone; action editors and certified reviewers; responses can be iterative.

## Structure notes (stable)

Journal-style: abstract, intro, related, method, experiments, limitations, references, appendix. No page-limit gaming; write for the reviewer who will certify.

## Common pitfalls

Assuming conference-style page limits; missing reproducibility statement; slow iteration; unclear response to reviewers.

## Verify before writing

- [ ] review/certification process
- [ ] page/length policy
- [ ] reproducibility statement
- [ ] anonymity policy
- [ ] appeal process

## CFP lookup

1. Open <https://jmlr.org/tmlr/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/tmlr.md`.

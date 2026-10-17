---
id: iclr
name: International Conference on Learning Representations
year: null
source_url: https://iclr.cc/
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

# ICLR

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~9 pages of content plus references; OpenReview; reciprocal reviewing. **Verify the current year.**

## Review emphasis (stable)

Clarity of the scientific question; analysis and insight; reproducible evidence; discussion of failure modes. OpenReview makes the response public, so tone and evidence matter.

## Structure notes (stable)

Abstract; intro; related; method; experiments; analysis; limitations; references. Reviews and author responses are public; write for a reader who will see the thread.

## Common pitfalls

Public response tone; claims that rely on hidden appendix; missing seeds; anonymity in links; page-limit counting; ignoring the closest prior work.

## Verify before writing

- [ ] page limit
- [ ] supplementary/appendix policy
- [ ] reciprocal review obligations
- [ ] LLM policy
- [ ] discussion/rebuttal window

## CFP lookup

1. Open <https://iclr.cc/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/iclr.md`.

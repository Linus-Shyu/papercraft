---
id: chi
name: ACM CHI Conference on Human Factors in Computing Systems
year: null
source_url: https://chi.acm.org/
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

# CHI

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~10 pages (content) plus references; ACM format; contribution types; anonymous review. **Verify the current year.**

## Review emphasis (stable)

Human-centered contribution; study design and validity; ethics; reflexivity; readability. The contribution type (empirical, artifact, methodological, theoretical) shapes the rubric.

## Structure notes (stable)

Abstract; intro; related; method/study design; findings; discussion; limitations; ethics; references. Figures and participant quotes are evidence.

## Common pitfalls

Under-specified study design; missing ethics/consent; overgeneralizing from a small sample; anonymity in images/quotes; page-limit counting.

## Verify before writing

- [ ] page limit and contribution types
- [ ] ethics/consent requirements
- [ ] anonymity of images and quotes
- [ ] supplementary/video rules
- [ ] rebuttal format

## CFP lookup

1. Open <https://chi.acm.org/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/chi.md`.

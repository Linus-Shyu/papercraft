---
id: aaai
name: AAAI Conference on Artificial Intelligence
year: null
source_url: https://aaai.org/conference/aaai/
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

# AAAI

> **Status: UNVERIFIED.** This is a checklist for the current CFP, not a rule
> sheet. Fill every `VERIFY` field from the official author kit, then set
> `verified_on` and `status: VERIFIED`.

## Typical (do not trust without verification)

Recent editions: ~7 pages of technical content plus references; two-column AAAI style; reproducibility checklist. **Verify the current year.**

## Review emphasis (stable)

Technical novelty and clarity of the contribution; a clean problem formulation; evidence that the method is more than a combination; reproducibility checklist. Reviewers are usually generalists, so the first page must teach the problem.

## Structure notes (stable)

Two-column; abstract; intro with explicit contributions; related work that positions against the closest 3 papers; method with a notation table; experiments with baselines and controls; limitations; references. A reproducibility checklist is typically part of the submission.

## Common pitfalls

Page-limit counting (references/appendix); modified style files; anonymity of appendix/checklist; overclaiming on small pilots; checklist answers that contradict the paper.

## Verify before writing

- [ ] CFP page limit and whether references count
- [ ] author kit version and TemplateVersion string
- [ ] reproducibility checklist requirements
- [ ] anonymity scope (main/appendix/supplement)
- [ ] rebuttal format and length

## CFP lookup

1. Open <https://aaai.org/conference/aaai/> and find the current edition's **Call for Papers** and
   **Author Kit**.
2. Copy exact wording for page limits, template version, anonymity, appendix,
   supplementary, checklist, and LLM policy into the YAML block.
3. Record `source_url` (the exact CFP page, not the homepage) and
   `verified_on: YYYY-MM-DD`.
4. Run `python3 scripts/check_conference.py conferences/aaai.md`.

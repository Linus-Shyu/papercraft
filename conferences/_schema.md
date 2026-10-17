# Conference profile schema

Every **profile** file in `conferences/` (`<id>.md`, not `_schema.md` or
`index.yaml`) **must** start with this YAML block. The skill reads it before
applying any venue rule.

```yaml
---
id: aaai                      # short id, matches index.yaml
name: AAAI Conference on Artificial Intelligence
year: 2027                    # the edition you are submitting to
source_url: https://...       # official CFP / author kit URL
verified_on: null             # YYYY-MM-DD, null = never verified
status: UNVERIFIED            # UNVERIFIED | VERIFIED | STALE
template: VERIFY              # e.g. aaai2027.sty, neurips_2026.sty
review_model: VERIFY          # double-blind | single-blind | open
anonymity: VERIFY             # yes/no + scope (main only? appendix? supplement?)
page_limit_main: VERIFY       # content pages, excluding references? state it
page_limit_refs: VERIFY       # references allowed? unlimited? extra pages?
appendix: VERIFY              # allowed in main PDF? separate? not reviewed?
supplementary: VERIFY         # allowed? deadline? format?
reproducibility: VERIFY       # checklist? code/data? required?
llm_policy: VERIFY            # disclosure? forbidden? allowed for writing?
dual_submission: VERIFY       # policy + arXiv exception
rebuttal: VERIFY              # text-only? length? new results allowed?
camera_ready: VERIFY          # deadline, copyright, extra page?
---
```

## Rules

1. **Volatile fields are `VERIFY` until proven.** Page limits, deadlines, template
   names, anonymity scope, supplementary rules and LLM policies change every
   year. A profile with `verified_on: null` is a checklist, not a rule sheet.
2. **Verification is a gate.** To set `status: VERIFIED` you must:
   - open the official CFP (not a blog, not a Twitter thread);
   - record `source_url` and `verified_on`;
   - fill every `VERIFY` field with the exact wording or `N/A`;
   - note the section/heading where you found it in the body.
3. **Staleness.** After 180 days, `scripts/check_conference.py` marks the profile
   `STALE`; re-verify before using it.
4. **Two-layer profiles.** Keep the *volatile* layer in YAML and the *stable*
   layer (review emphasis, structure, pitfalls) in prose. Never mix them: a
   stable norm ("reviewers reward controls") is not a page limit.
5. **No cross-year copying.** "It was 8 pages last year" is not evidence.
6. **No cross-venue copying.** ACL and EMNLP look similar but have different
   templates and deadlines; AAAI and NeurIPS have different checklists.

## Stable layer (what belongs in prose)

- What the venue's reviewers typically reward (e.g., technical novelty vs
  empirical rigor vs artifact).
- Expected structure (e.g., mandatory limitations section, broader impact,
  reproducibility checklist).
- Common desk-rejection causes (anonymity, dual submission, format, page limit).
- Review form fields and scoring scale, if stable.
- Typical rebuttal shape (text-only vs revision), with `VERIFY`.

## Adding a new venue

1. Copy `_default.md` → `<id>.md`.
2. Fill YAML; leave unknown fields `VERIFY`.
3. Add an alias to `index.yaml`.
4. Write the stable layer from the current CFP + review form.
5. Run `python3 scripts/check_conference.py conferences/<id>.md`.

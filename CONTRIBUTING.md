# Contributing

Thanks for helping. The bar is: **every rule must be checkable or falsifiable.**

## What to contribute

- A new conference profile with a verified CFP (`verified_on`, `source_url`,
  every `VERIFY` replaced or explicitly `N/A`).
- A checker with a clear failure mode and a test case.
- A failure-mode case study with a detector (not just a story).
- Clearer wording for an existing rule.

## What not to contribute

- Rules that encourage hiding limitations, overclaiming, or fabricating data.
- Venue page limits copied from another year without verification.
- "Best practice" claims with no source.
- Checks that fail on normal LaTeX (e.g., flagging every URL in references).

## Adding a conference

1. `cp conferences/_default.md conferences/<id>.md`.
2. Fill the YAML block. Leave unknown fields `VERIFY`.
3. Add aliases to `conferences/index.yaml`.
4. Write the stable layer: review emphasis, structure, pitfalls.
5. Run:
   ```bash
   python3 scripts/check_conference.py conferences/<id>.md
   ```
6. In the PR, include the CFP URL and the exact wording for page limits,
   anonymity, checklist, and LLM policy.

## Adding a checker

- Python 3, standard library only.
- `--help`, exit codes (0 pass, 1 fail, 2 IO/config), no writes to the paper.
- A short docstring with usage and a "what it does not check" line.
- Add it to `scripts/audit.sh`.
- Add a test or a reproducible example to `examples/`.

## Testing

```bash
python3 -m py_compile scripts/*.py
bash scripts/build.sh /path/to/paper main.tex
bash scripts/audit.sh /path/to/paper /path/to/paper/paper_state
```

## Style

- Markdown, short sentences, tables for checklists.
- Use `VERIFY`, `UNVERIFIED`, `SUSPECT` consistently.
- Never claim a citation is fake without a contradictory source.

# Changelog

## 1.0.0 — 2026-10-17

Initial release.

- `SKILL.md`: modes, prime directive, gates G0–G8, Harness rules.
- `WRITING.md`: section-by-section writing playbook, claim/number/citation/
  float discipline, LLM failure modes, pre-submission checklist.
- `REVIEWING.md`: claim–evidence matrix, numbers/method/citation/artifact
  audits, rubric, report template, anti-hallucination rules.
- `conferences/`: AAAI, NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR, KDD, CHI, TMLR,
  a generic default, a schema, and an alias index. Volatile fields are `VERIFY`
  by design.
- `guides/`: evidence, citations, harness, failure modes, rebuttal.
- `templates/`: claim ledger, experiment registry, figure registry, numbers,
  review report, camera-ready checklist.
- `scripts/`: `check_numbers.py`, `check_citations.py`, `check_floats.py`,
  `check_anonymity.py`, `check_conference.py`, `build.sh`, `audit.sh`.
- `install.sh`: symlink/copy into `~/.dsh/skills` or a project.
- `examples/mini-paper`: a tiny paper that passes all gates; `make test` runs it
  end-to-end (build + G2–G6).

### Known limitations

- Online citation verification is not automated; the scripts are structural.
- Conference profiles must be verified against the current CFP.
- `check_numbers.py` matches a formatted value in a context; it cannot prove
  that the number is semantically correct.

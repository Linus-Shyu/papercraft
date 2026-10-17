# Conference directory — what is active, without inventing deadlines

> `conferences/directory.json` is **metadata**, not a deadline tracker. It knows
> the venue, area, type, cycle, and official page. It does **not** know this
> year's deadline until someone verifies it.

---

## 1. What is in the directory

37 venues across general AI/ML, NLP, vision, data/IR, HCI/education, robotics,
and theory/stats. Each row has:

| Field | Meaning |
|---|---|
| `id` | stable id (also used by `papercraft template`) |
| `name` | official name |
| `type` | `conference` or `journal` |
| `areas` | general, ml, nlp, vision, data, hci, robotics, theory, education |
| `cycle` | `annual` or `rolling` |
| `official_url` | official site |
| `has_profile` | whether `conferences/<id>.md` exists |
| `notes` | what the venue is for |

**No deadlines, no status, no page limits.** Those are project-level
verifications.

---

## 2. Commands

```bash
papercraft venues                         # all 37, all UNVERIFIED
papercraft venues --area nlp              # ACL, EMNLP, NAACL, EACL, COLING, TACL, ...
papercraft venues --type journal          # TMLR, JAIR, TACL, TPAMI
papercraft venues --verified-only         # only what you verified
papercraft venues --json                  # machine-readable
```

Mark a venue after opening its official CFP:

```bash
papercraft venues-mark --id acl --status in_review \
  --source-url https://... --verified-on 2026-10-17 --dir <paper>
```

Statuses: `unknown`, `in_review`, `open`, `upcoming`, `rolling`.

`venues-mark` writes `paper_state/conference-verifications.json` in the paper
project; the global directory stays clean.

---

## 3. Workflow

1. Filter by area: `papercraft venues --area nlp`.
2. Open the official URL / CFP; find the current edition, deadline, format.
3. Mark: `papercraft venues-mark --id ... --status ... --source-url ...`.
4. For submission, use `papercraft recommend` (shortlist) and
   `papercraft template --venue ...` (template provenance).
5. Do not treat an `UNVERIFIED` row as a deadline.

---

## 4. Why no dates in the directory

- Deadlines change every year; a stale date is worse than no date.
- Some venues use rolling ARR cycles; a single "deadline" is misleading.
- papercraft's P7: no conference rule from memory.

If you want a deadline calendar, build it per project with `venues-mark`, and
record the exact source URL and `verified_on`.

---

## 5. Adding a venue

1. Add an entry to `conferences/directory.json`.
2. Optionally copy `conferences/_default.md` → `conferences/<id>.md` and fill the
   YAML after verifying the CFP.
3. Add the id to `conferences/index.yaml` if it should be usable by
   `papercraft template`.
4. Run `python3 scripts/check_directory.py --directory conferences/directory.json`.

---

## 6. Limits

- The directory is a starting point, not a ranking.
- `has_profile: no` means template/page-limit rules are not available yet.
- `venues-mark` does not fetch the CFP; a human/agent must open it.
- Acceptance is never predicted by this directory.

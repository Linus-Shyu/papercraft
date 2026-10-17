# Citations — verify, record, and never guess

> **Default state of a citation is `UNVERIFIED`.** It becomes `VERIFIED` only
> after a human or agent has opened a DOI/arXiv/ACL/publisher page and matched
> title, authors, venue, and year.

---

## 1. Verification levels

| Level | How | Allowed in |
|---|---|---|
| `VERIFIED` | DOI/arXiv/ACL page opened; title+authors+venue+year match | PDF, rebuttal, review |
| `PARTIAL` | Some fields verified; e.g. arXiv title matches but venue unknown | draft only |
| `UNVERIFIED` | No check yet, or only from memory | nowhere in the PDF |
| `SUSPECT` | Contradictory evidence (arXiv ID → different title, DOI → different paper) | remove or fix immediately |

**Do not use the word "fabricated" unless you have a contradictory source.**
"Could not verify" is a factual statement; "fabricated" is an accusation.

---

## 2. Verification workflow (per key)

1. **Find the DOI/arXiv/ACL ID** from the bib entry or a search.
2. **Open it.** Check:
   - title (exact, including subtitle);
   - author list (first author + order; "et al." is not enough for BibTeX);
   - venue (conference/journal/workshop, not "arXiv" if published);
   - year (published, not preprint);
   - pages/volume (if the style requires).
3. **Compare with the sentence** that cites it: does the cited work actually
   support the claim?
4. **Record** in `paper_state/citation-audit.md`:
   ```
   key: lekshmi2024line
   status: VERIFIED
   source: https://proceedings.mlr.press/v257/lekshmi-narayanan24a.html
   checked: 2026-10-17
   note: AI4E Workshop 2024 (PMLR 257), not AAAI proceedings
   ```
5. If mismatch: fix the bib or remove the citation; update the sentence if the
   claim was supported only by the wrong paper.

---

## 3. High-risk metadata (check these first)

| Field | Common LLM error | Check |
|---|---|---|
| arXiv ID | ID belongs to another paper | open `arxiv.org/abs/<id>`; title must match |
| Venue | workshop cited as main conference; arXiv cited as conference | publisher/ACL page |
| Year | preprint year vs published year | use published year in `year` |
| Authors | wrong first author / invented co-author | publisher page |
| Pages | invented range | publisher page; if unknown, omit |
| Title | paraphrased or shortened | exact title |
| DOI | invented / wrong suffix | resolves to the paper |

If any field is unknown, leave it out rather than invent it. A missing page
range is a minor formatting issue; a wrong author is an integrity issue.

---

## 4. BibTeX hygiene

- One entry per key; keys are `firstauthorYYYYkeyword` (stable, lowercase).
- Required fields:
  - `@inproceedings`: author, title, booktitle, year, pages (if known).
  - `@article`: author, title, journal, year, volume, pages (if known).
  - `@misc`/`@online`: author (or organization), title, year, url, urldate.
- Use `{}` to protect capitalization in titles (`{LLM}`, `{AI}`, `{Python}`).
- `author = {Last, First and Last, First}`; do not use "et al." in BibTeX.
- Do not put `arXiv` in `journal` for a published paper; use the published venue.
- Prefer `doi = {...}` over a URL when available.
- Keep a `note = {arXiv:XXXX.XXXXX}` only if you need the preprint.

---

## 5. Citation audit file

`paper_state/citation-audit.md`:

```markdown
# Citation audit

| key | status | source | checked | note |
|---|---|---|---|---|
| guo2013pythontutor | VERIFIED | https://dl.acm.org/doi/10.1145/2445196.2445368 | 2026-10-17 | SIGCSE 2013 |
| wei2024code2vec | SUSPECT | https://arxiv.org/abs/2410.07820 | 2026-10-17 | ID resolves to a different paper |
| cao2025tutoreval | UNVERIFIED | — | 2026-10-17 | could not find; remove or replace |
```

Rules:

- Every key cited in the PDF must be `VERIFIED` or explicitly accepted by the
  author as `PARTIAL` with a written reason.
- `SUSPECT` keys are blockers: remove the citation or replace it before build.
- Uncited bib entries are not errors; do not report them as such.

---

## 6. Commands

```bash
# cited vs defined
grep -o '\\cite{[^}]*}' main.tex | sed 's/\\cite{//;s/}//' | tr ',' '\n' | sort -u
grep -o '^@[a-z]*{[^,]*' references.bib | sed 's/.*{//' | sort

# structural checks
python3 scripts/check_citations.py --tex main.tex --bib references.bib --strict
```

`check_citations.py` reports:

- cited but missing from bib (FAIL);
- duplicate keys (FAIL);
- missing required fields (FAIL with `--strict`);
- malformed arXiv/DOI (WARN);
- uncited entries (INFO).

It does **not** verify metadata online by default (network calls are opt-in and
must be recorded). Online verification is a human/agent step with a URL.

---

## 7. Claim–citation fit

A citation can be structurally correct and still wrong for the sentence:

- "LLM judges are biased [X]" — X must study judge bias, not just LLM evaluation.
- "Visualizers expose state [Python Tutor]" — Python Tutor is a visualizer; a
  survey is not.
- "TRAVER's DICT is the closest protocol [TRAVER]" — verify that DICT exists in
  that paper; if you cannot find it, do not attribute it.

Rule: **read at least the abstract and the relevant section** of the closest 3
papers; for the rest, cite only claims you can see in the abstract.

---

## 8. LLM-specific traps

| Trap | Example | Fix |
|---|---|---|
| Plausible but wrong | arXiv ID from memory | open the ID |
| Workshop as conference | AI4E workshop → AAAI proceedings | check publisher |
| Wrong first author | "Huang et al." for a paper by Das et al. | check ACL page |
| Invented pages | `107--117` with no source | omit if unknown |
| Title drift | shortened/paraphrased title | copy exact |
| Citation does not support claim | cite a survey for a specific method | read the section |
| Self-citation leak | "our previous work [us]" | third person in anonymous review |

When in doubt: **remove the citation and rewrite the sentence without it.**
A missing citation is a minor issue; a fabricated one is a serious one.

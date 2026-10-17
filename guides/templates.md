# Conference templates — fetch, verify, record

> Wrong template = desk rejection. This is not a formatting nicety.

---

## 1. Policy

1. **Never guess a template URL.** Open the current CFP / author kit; copy the
   exact URL or download the kit yourself.
2. The registry (`conferences/templates.json`) ships with `url: null` on purpose.
   Fill it only after verifying the current year.
3. Every fetch writes `TEMPLATE.md` with URL, date, archive sha256, and file
   hashes. No provenance, no template.
4. **Do not redistribute** style files in the Papercraft repo; fetch them into
   the user's project at runtime. Respect the license.
5. **Do not reuse last year's .sty.** The version string in the class/style must
   match the CFP.

---

## 2. Find the kit

| Venue | Where to look |
|---|---|
| AAAI | Author kit / formatting page linked from the current CFP |
| NeurIPS | CFP "Paper checklist / style files" |
| ICML | Conference site "Author instructions" |
| ICLR | Conference site "Style files" |
| ACL / EMNLP | ACL rolling review / `acl-org` style repository |
| CVPR | CVPR author kit (IEEE format) |
| KDD / CHI | ACM master template / proceedings template |
| TMLR | Journal site style package |

If the kit is behind a login or a license click-through, download it manually
and use `--archive`.

---

## 3. Commands

```bash
# from a paper project
papercraft template --venue aaai --url https://.../aaai2027-kit.zip
papercraft template --venue aaai --archive ~/Downloads/aaai2027-kit.zip
papercraft template --list
```

What happens:

- HTTPS only (localhost http allowed for tests);
- archive ≤ 50 MB, extracted ≤ 200 MB;
- path traversal, absolute paths, symlinks, devices rejected;
- only document/template extensions extracted;
- `.sty`, `.bst`, `.cls` copied to the project root (LaTeX finds them);
- samples/PDFs/READMEs copied to `template/`;
- `TEMPLATE.md` written with provenance;
- expected files from the registry are checked; missing ones are warned.

The source URL is cached in `paper_state/template-source.json` (so
`papercraft new --fetch-template` works next time); remove the cache to force a
re-check.

---

## 4. After fetching

1. Open `TEMPLATE.md`; confirm `source_verified` and the style version.
2. Copy the `\documentclass`/`\usepackage` lines from `template/sample.tex`
   into `main.tex`; do not overwrite your content blindly.
3. Run `papercraft check`; G6 build must pass with the official class.
4. If the kit's version differs from the CFP, stop and re-download.

---

## 5. Security

- Only fetch from official domains; prefer `https`.
- Treat the archive as untrusted: the extractor rejects traversal/symlinks and
  caps size.
- Do not run scripts from the kit; only read `.sty/.bst/.cls/.tex`.
- Record the sha256; if the file changes later, the provenance no longer matches.

---

## 6. Common failures

| Symptom | Cause | Fix |
|---|---|---|
| `no template source` | registry URL is `null` | pass `--url` or `--archive` |
| class not found | `.sty` not copied / wrong dir | check project root and `TEXINPUTS` |
| page limit changed | old kit | re-download; check CFP |
| missing `.bst` | partial kit | use the full author kit |
| Overleaf compiles, local doesn't | missing fonts/packages | install TeX packages; record environment |
| `source_verified: false` | URL not matched to a verified registry entry | verify and update `conferences/templates.json` |

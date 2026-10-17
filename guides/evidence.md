# Evidence — claim ledger, numbers, and statuses

> The single most effective anti-hallucination device is a **ledger**: if a
> sentence cannot point to a row, it does not go into the paper.

---

## 1. Claim ledger

File: `paper_state/claim-ledger.csv` (template in `templates/claim-ledger.csv`).

| Column | Meaning | Example |
|---|---|---|
| `claim_id` | stable ID | `C1`, `C2a` |
| `claim` | one sentence, falsifiable | "Key-only rationales score high EAR but low VGR" |
| `type` | existence / comparative / causal / generality / mechanistic | `mechanistic` |
| `section` | where it lives | `abstract; results §6.3` |
| `evidence_id` | experiment / table / figure / analysis | `E18; Table 6` |
| `status` | SUPPORTED / WEAK / UNSUPPORTED / UNCLEAR | `SUPPORTED` |
| `strength` | how strongly worded | `shows` |
| `boundary` | where it stops | "V-120 only; constructed control" |
| `owner` | who can change it | `first author` |
| `updated` | date | `2026-10-17` |

### Status rules

- **SUPPORTED** — direct evidence, n and setting clear, control exists if causal.
- **WEAK** — evidence exists but one of: small n, single seed, no CI, no control,
  single domain, constructed benchmark.
- **UNSUPPORTED** — no evidence, or evidence points the other way.
- **UNCLEAR** — evidence and claim cannot be matched; rewrite before drafting.

**Gate G1**: no `UNSUPPORTED` claim in abstract/intro; every `WEAK` claim in the
abstract must carry its boundary in the same sentence or in limitations.

---

## 2. Evidence hierarchy

From strongest to weakest:

1. **Intervention with control** — change one variable, hold others fixed.
2. **Pre-registered / fixed split** — no test-set tuning.
3. **Multiple seeds + CI** — variance reported.
4. **Single run on a fixed split** — descriptive only.
5. **Anecdote / qualitative example** — illustration, never proof.
6. **Citation of someone else's result** — not your evidence.

When you write "shows", you need 1–3. When you write "suggests", 4 is enough.
When you write "we observe", 5 is enough but label it.

---

## 3. Number pipeline

```
experiment command → output JSON/CSV → canonical numbers.json
    → table generator → .tex table
    → figure generator → PDF/PNG
    → prose (only via \input or generated macros)
```

Rules:

1. **Never type a number into prose by hand.** Use `\input{data/numbers.tex}` or
   generated macros (`\newcommand{\eoneear}{0.56}`).
2. `numbers.json` entry:
   ```json
   {
     "id": "E1.product.ear",
     "value": 0.5623,
     "format": "0.00",
     "source": "data/results/e1_atep.json#conditions[0].ear",
     "note": "episode-macro; n=16",
     "bad_values": ["0.57", "0.55"]
   }
   ```
3. **Staleness**: after re-running, old numbers go into `bad_values` so
   `check_numbers.py` fails if they survive anywhere.
4. **Rounding**: pick one rule per metric; document it in the table caption.
5. **Denominator**: record whether the mean is frame-level, episode-level, or
   corpus-level. They are not interchangeable.
6. **Missing values**: use `n/a`/`—`, never `0`, unless 0 is measured.

---

## 4. Evidence map (paper-level)

For each section, list the claims and their evidence:

```
Abstract:  C1 (Table 3), C2 (Table 5), C3 (Table 6)
Intro:     C1 (Table 3), C2 (Fig 4), C3 (Table 6)
Method:    definitions only; no empirical claims
Results:   C1–C5, each with a table/figure/control
Discussion:C1–C3 + boundaries; no new claims
```

If a section has a claim with no row, either add evidence or delete the sentence.

---

## 5. Artifact evidence

Every empirical claim should be reproducible by a command. Record in
`experiment-registry.csv`:

| Column | Example |
|---|---|
| `exp_id` | `E18` |
| `hypothesis` | value-only text separates EAR from VGR |
| `command` | `python3 scripts/experiments/e18.py --seed 20270620` |
| `seed` | `20270620` |
| `output` | `data/results/e18_semantic_grounding.json` |
| `table` | `Table 6` |
| `status` | `cached` / `live` / `failed` |
| `runtime` | `2 min CPU` |
| `owner` | `first author` |

If a command cannot be re-run (missing API key, private data), mark it `cached`
and say so in the paper/README.

---

## 6. Auditing evidence (for the reviewer/auditor)

1. Pick 3 claims from abstract/intro/results.
2. For each, find the table/figure/section; check n, split, metric, control.
3. Recompute one delta and one percentage.
4. Check whether the claim's wording matches the evidence strength.
5. Check whether the artifact command reproduces the number (if provided).

Output:

```
C2: "X outperforms Y" — Table 2, n=16, no CI, single seed → WEAK
   Wording should be "on this pilot, X is higher (0.56 vs 0.45)".
```

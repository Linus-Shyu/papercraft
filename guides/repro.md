# Reproducibility — did the code actually run?

> A cached JSON file is not evidence that the code ran. Evidence is:
> **command + exit code + output hash + expected values**, recorded together.

---

## 1. Run registry

`paper_state/repro-manifest.json`:

```json
{
  "timeout": 300,
  "entries": [
    {
      "id": "E1",
      "command": "python3 scripts/experiments/e1.py",
      "output": "data/results/e1.json",
      "sha256": "<optional>",
      "expect": {"conditions.0.ear": 0.5623}
    }
  ]
}
```

Rules:

- `command` runs in a **temp copy** of the repo, never in the source tree.
- `output` is relative to the repo root; it must exist after the command.
- `sha256` pins the exact output; omit only if the output is non-deterministic.
- `expect` uses dotted paths into JSON; numeric tolerance is `--tolerance`.
- If a command needs an API key, mark it `cached` and do not put the key in the
  manifest; document the cache path.

---

## 2. Modes

```bash
# verify existing outputs only (fast, no execution)
python3 scripts/check_repro.py --manifest paper_state/repro-manifest.json --root .

# actually run every command in a temp copy, then verify
python3 scripts/check_repro.py --manifest ... --root . --run --timeout 600

# run only one entry
python3 scripts/check_repro.py --manifest ... --root . --run --only E1
```

`--run` copies the repo (excluding `.git`, `tmp`, `paper_state`, large media),
executes, records exit code and output hash, and fails on:

- non-zero exit;
- missing output;
- hash mismatch;
- expected value mismatch.

`--verify-only` is the default; it cannot prove the command ran, only that the
output matches the expectation. Use `--run` before submission.

---

## 3. Determinism

- Fix seeds (`random`, `numpy`, framework).
- Record model names + versions + dates (APIs change).
- Disable nondeterministic ops where possible; if not, report variance.
- For LLM calls: cache completions and hash the cache; a re-run without cache is
  a new experiment.
- For hardware: record device, driver, precision.

---

## 4. Cache vs run

| Situation | What to report |
|---|---|
| Cached completion used | "cached; hash X; produced on date Y with model Z" |
| Live call used | model version, date, temperature, max tokens |
| Deterministic script | command + seed + output hash |
| Human annotation | annotator count, instructions, agreement |

Never describe cached results as "we run"; say "cached" or "replayed".

---

## 5. Artifact packaging

- Include: source, scripts, data (or derived caches), figures, README, LICENSE.
- Exclude: `.git`, `paper_state/`, `.env`, logs, secrets, raw restricted data.
- README must contain: environment, install, minimal command, expected output,
  runtime, license, and what is **not** included (and why).
- Test the artifact in a clean directory with no network; record the result.

---

## 6. "Code actually ran" checklist

- [ ] Every main-table number has a command and an output file.
- [ ] The command exits 0 in a clean copy.
- [ ] Output hash matches the recorded hash.
- [ ] Expected values match within tolerance.
- [ ] Seeds/model versions/dates recorded.
- [ ] Cached vs live is labeled.
- [ ] Artifact README reproduces at least one table.
- [ ] No API key or private path in the artifact.

---

## 7. Red flags

- "Results available upon request."
- A table with no script and no JSON.
- A script that reads a hard-coded result file.
- A cache with no provenance (model/date/hash).
- A re-run that silently changes a headline number.

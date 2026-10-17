# Start here — one topic, full pipeline

You only need a topic. The agent runs survey → feasibility → experiments →
writing → audit → review → acceptance. It asks at most 3 questions and stops at
3 checkpoints. It will **not** invent results or citations.

## 1. Create a project

```bash
./papercraft new --topic "How should we evaluate step-by-step LLM tutoring?" \
  --venue aaai --dir ~/papers/my-tutoring-paper
cd ~/papers/my-tutoring-paper
```

This creates the LaTeX skeleton, `paper_state/` ledgers, and `plan.json`.

## 2. Paste one prompt into your agent

```
Run Papercraft Autopilot for the project at ~/papers/my-tutoring-paper.
Read /path/to/papercraft/AUTOPILOT.md and follow it exactly.
I only care about the topic; ask me at most 3 questions
(venue, constraints, must-use data/code). If I say "you decide", pick defaults
and record them. Do not fabricate results or citations. Stop at H1, H2, H3.
```

If you don't have a path, install Papercraft first (see `README.md`).

## 3. Answer only what you care about

| Question | Default if you skip |
|---|---|
| Venue | AAAI 2027 |
| Deadline/compute/data | 4 weeks, CPU-only, public data |
| Must-cite / avoid | none |

Then wait for **H1** (pick a research question), **H2** (go/no-go), **H3**
(approve submission). Everything else is automated.

## What you get

- `main.pdf` and a submission pack
- a literature matrix with verified citations
- an experiment registry with commands and output hashes
- a reviewer report (3 personas) and an acceptance risk memo
- a gate log showing what passed and what was cut

## What it will not do

- invent experiments, numbers, or citations
- promise acceptance
- run a human study without IRB/recruitment
- hide a negative result or a scope cut

If the topic is not feasible with your resources, you get a **plan and a
negative result**, not a fake paper.

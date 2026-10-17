---
layout: default
title: Papercraft
---

# Papercraft

**Evidence-first paper writing and review for AI agents.**

Papercraft runs the full research lifecycle from a topic: survey → feasibility →
experiment design → execution → writing → audit → review → acceptance →
packaging. Every number, citation, claim, and float is checked against an
artifact; gates fail closed.

[GitHub repository](https://github.com/Linus-Shyu/papercraft) ·
[Quickstart](https://github.com/Linus-Shyu/papercraft/blob/main/START_HERE.md) ·
[Autopilot](https://github.com/Linus-Shyu/papercraft/blob/main/AUTOPILOT.md) ·
[Editor setup](https://github.com/Linus-Shyu/papercraft/blob/main/EDITORS.md)

## Quickstart

```bash
git clone https://github.com/Linus-Shyu/papercraft.git
cd papercraft
./install.sh --all

./papercraft new --topic "How should we evaluate step-by-step LLM tutoring?" \
  --venue aaai --dir ~/papers/my-paper
./install.sh --project ~/papers/my-paper
```

Then open the paper repo in your editor and paste the autopilot prompt from
[START_HERE.md](https://github.com/Linus-Shyu/papercraft/blob/main/START_HERE.md).

## What it is not

- Not a ghostwriter: it will stop rather than invent experiments or citations.
- Not a guarantee of acceptance.
- Not a replacement for peer review.

## Works with

DSH · Claude Code · Cursor · Codex · Copilot · Cline · Windsurf · Continue ·
Aider · Zed · any editor that can read `SKILL.md`.

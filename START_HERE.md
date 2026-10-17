# Start here — one topic, one chat

You only need a topic. The agent runs survey → feasibility → experiments →
writing → audit → review → acceptance. It asks at most 3 questions and stops at
3 checkpoints. It will **not** invent results or citations.

## 1. Open a folder

Create an empty folder for the paper (or open an existing paper repo). Open
**that folder** in your editor — not its parent.

## 2. Mention the skill and paste one message

| Editor | Mention |
|---|---|
| DSH | `@papercraft` |
| Claude Code | `Use the papercraft skill` |
| Cursor | `@papercraft` or `@.cursor/rules/papercraft.mdc` |
| Codex | `Use papercraft` or `@AGENTS.md` |
| Copilot / Cline / Windsurf / Continue | `@AGENTS.md` |
| Anything else | `@SKILL.md` or paste the absolute path |

Then paste:

```text
Use the Papercraft skill. I want to write a paper about:

<YOUR TOPIC>

Venue: <AAAI / NeurIPS / ACL / ... or "you decide">.

Work in this folder. Do NOT ask me to run terminal commands — bootstrap the
project yourself (papercraft new, or the templates in papercraft/templates/).
Then follow AUTOPILOT.md end-to-end. Ask me at most 3 questions, and stop at
H1, H2, H3. Do not fabricate results or citations. If the work is not feasible,
stop and give me a plan.
```

## 3. Answer only H1 / H2 / H3

| Checkpoint | What you see | What to say |
|---|---|---|
| H1 | 3 research questions + venue | pick one, or “you decide” |
| H2 | feasibility, resources, go/no-go | go / change scope / stop |
| H3 | PDF, reviews, acceptance risk | submit / revise |

Everything else is automated.

## What you get

- a submission pack (`main.pdf`, `source.zip`, `artifact.zip`)
- a verified literature matrix
- an experiment registry with commands and output hashes
- a reviewer report and an acceptance risk memo
- a gate log showing what passed and what was cut

## What it will not do

- invent experiments, numbers, or citations
- promise acceptance
- run a human study without IRB/recruitment
- hide a negative result or a scope cut

If the topic is not feasible with your resources, you get a **plan and a
negative result**, not a fake paper.

## Optional: terminal CLI

If you prefer the terminal (or your editor has no file tools):

```bash
./install.sh --all
./papercraft new --topic "..." --venue aaai --dir ~/papers/x
./install.sh --project ~/papers/x
./papercraft status --dir ~/papers/x
./papercraft next --dir ~/papers/x
```

See `CHAT.md` for the chat-only path and `EDITORS.md` for activation.

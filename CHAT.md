# Chat-only usage — no terminal

> Open a folder. Mention the skill. Paste one message. That is the whole UX.

## The only sentence you need

```text
写一篇关于 <题目> 的论文，投 <会议>。
```

That is enough. Defaults: folder `./papercraft-paper` in the current workspace,
venue AAAI, at most 3 questions, H1/H2/H3. The agent bootstraps the project.

If the agent does not pick up the skill automatically, put **用 papercraft** in
front:

```text
用 papercraft 写一篇关于 <题目> 的论文，投 <会议>。
```

The rest of this file is only for editors that do not auto-route.

---

## 1. Open the paper folder

- New paper: create an empty folder (e.g. `~/papers/my-paper`) and open **that
  folder** in the editor.
- Existing paper: open its repo root.

## 2. Mention the skill

| Editor | What to type |
|---|---|
| DSH | `@papercraft` |
| Claude Code | `Use the papercraft skill` |
| Cursor | `@papercraft` or `@.cursor/rules/papercraft.mdc` |
| Codex | `Use papercraft` or `@AGENTS.md` |
| Copilot / Cline / Windsurf / Continue | `@AGENTS.md` (or the rule file) |
| Any editor | `@SKILL.md` / paste the absolute path |

## 3. Paste this message

```text
Use the Papercraft skill. I want to write a paper about:

<YOUR TOPIC>

Venue: <AAAI / NeurIPS / ACL / ... or "you decide">.

Work in this folder. Do NOT ask me to run terminal commands — bootstrap the
project yourself (papercraft new, or the templates in papercraft/templates/).
Then follow AUTOPILOT.md end-to-end. Use web search/fetch for the survey and
record URLs. Ask me at most 3 questions, and stop at H1, H2, H3. Do not
fabricate results or citations. If the work is not feasible, stop and give me a
plan.
```

If the agent asks you to run a command, reply:

```text
You have file and terminal tools. Bootstrap it yourself per AUTOPILOT.md §0.
I only want to answer H1/H2/H3.
```

## 4. Answer only these

| Checkpoint | What you see | What to say |
|---|---|---|
| H1 | 3 research questions + venue | pick one, or “you decide” |
| H2 | feasibility, resources, go/no-go | go / change scope / stop |
| H3 | PDF, reviews, acceptance risk | submit / revise |

## 5. If the editor has no terminal

Some web chats cannot run commands or read local files. In that case:

- paste `SKILL.md`, `AUTOPILOT.md`, `WRITING.md`, and `REVIEWING.md` into the
  chat (or attach them);
- the agent can still run the stages **manually**, but `check_*` scripts cannot
  run;
- require it to mark `G2/G6/G8` as `SKIPPED (no terminal)` in the audit log — it
  must not claim those gates passed;
- do the LaTeX build and checks in a local editor afterwards.

## 6. If it forgets the skill

Ask:

```text
List the 10 non-negotiable rules from SKILL.md and your current mode.
```

If it cannot, re-mention the file with an absolute path.

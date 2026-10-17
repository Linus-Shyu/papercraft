# Using Papercraft in any editor / agent

> **Installation is necessary, not sufficient.** Three layers:
> 1. **Install** — files in the right place (`install.sh --all` / `--project`).
> 2. **Activate** — the editor puts `SKILL.md` in the model's context
>    (auto-load, a rule, or an explicit `@`/read).
> 3. **Verify** — ask the agent to state the rules; if it cannot, it did not load.

---

## 1. What to install

```bash
# global native dirs (once per machine)
./install.sh --all

# project-level native dirs + pointer files (once per paper repo)
./install.sh --project /path/to/paper
```

`--project` is the important one for editors: it creates `.cursor/skills`,
`.claude/skills`, `.codex/skills`, `.dsh/skills`, `.agents/skills`, plus
`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/papercraft.mdc`,
`.clinerules/`, `.windsurf/rules/`, `.continue/rules/`,
`.github/copilot-instructions.md`, `CONVENTIONS.md`, `.rules`.

Open the **paper repo** (not the parent folder) in the editor, then start a
**new chat**.

---

## 2. Per-editor activation

| Editor / agent | What it reads | How to activate | Verify |
|---|---|---|---|
| **DSH** | `~/.dsh/skills/papercraft` | Auto; say "use papercraft" | Ask for the 10 rules |
| **Claude Code** | `~/.claude/skills/papercraft`, `CLAUDE.md` | Restart; new session; say "use the papercraft skill" | `/skills` (if available) or ask for rules |
| **Cursor** | `~/.cursor/skills/papercraft`, `.cursor/rules/papercraft.mdc` | New chat; the rule is `alwaysApply: true`; fallback `@papercraft.mdc` | Ask "what rules are active?" |
| **Codex** | `~/.codex/skills/papercraft`, `AGENTS.md` | Restart; new session; say "use papercraft" | Ask for `SKILL.md` path and rules |
| **Gemini CLI** | `GEMINI.md` | New session in the repo | Ask for the rules |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Open the repo in VS Code; Copilot Chat reads it | Ask "follow the repo instructions" |
| **Cline** | `.clinerules/papercraft.md` | New task in the repo | Ask for the rules |
| **Windsurf** | `.windsurf/rules/papercraft.md` | New cascade; rules may need "Always on" | Ask for the rules |
| **Continue** | `.continue/rules/papercraft.md` | New chat in the repo | Ask for the rules |
| **Aider** | `CONVENTIONS.md` | Starts in the repo; if not, `/read CONVENTIONS.md` | Ask for the rules |
| **Zed** | `.rules` | Agent panel in the repo | Ask for the rules |
| **Any other** | `AGENTS.md` | Say "read AGENTS.md, then SKILL.md" | Ask for the rules |

**Fallback for every tool**: paste this into the chat:

```
Read /absolute/path/to/papercraft/SKILL.md and follow it for this repo.
Also read WRITING.md / REVIEWING.md / AUTOPILOT.md as needed.
```

An explicit absolute path works even when auto-load does not.

---

## 3. 5-minute smoke test (do this once per editor)

1. Open the paper repo, new chat.
2. Ask:

```
List the 10 non-negotiable rules from the Papercraft skill, and say which
mode you are in. Do not use outside knowledge.
```

- **Pass**: it lists no-number-without-source, no-citation-without-verification,
  no-claim-without-evidence, no-float-without-reference, fresh build, frozen
  submission, CFP verification, anonymity, no invented reviewer demand, fail
  closed.
- **Fail**: it does not know the rules → the skill is not in context. Use the
  fallback prompt above, or `@`-mention the pointer file.

3. Then run the real task:

```
Run Papercraft Autopilot for this repo. Read AUTOPILOT.md and follow it.
I only care about the topic; ask me at most 3 questions. Do not fabricate
results or citations. Stop at H1, H2, H3.
```

4. Verify it creates `paper_state/` and asks the 3 questions — not a generic
   essay.

---

## 4. Is `--all` enough?

| Situation | Answer |
|---|---|
| DSH / Claude Code / Cursor / Codex with native support | `--all` + restart is usually enough |
| Copilot / Cline / Windsurf / Continue / Aider / Zed | You need `--project` (pointers are project-local) |
| Tool ignores rules until `@`-mentioned | Use `@papercraft` / `@papercraft.mdc`, or set the rule to always-on |
| Tool has no skill/rule concept | Paste the absolute `SKILL.md` path once per session |
| Multiple paper repos | Run `--project` in each; `--all` covers global native dirs only |

`--project` writes **only inside that repo**; it does not touch global editor
settings. `--uninstall --project DIR` removes its blocks and links.

---

## 5. Troubleshooting

| Symptom | Fix |
|---|---|
| Agent writes a generic paper, ignores gates | Skill not in context: use the absolute-path prompt; check `AGENTS.md`/`CLAUDE.md` exists |
| Cursor rule does not apply | Open the repo root; new chat; `@papercraft.mdc`; or set `alwaysApply: true` (installer already does) |
| Two `papercraft` entries in DSH | Remove one symlink (`~/.agents/skills/papercraft` or `~/.dsh/skills/papercraft`) |
| Pointer points to an old path | Re-run `./install.sh --project DIR` after moving the repo |
| Agent asks 10 questions | Say "use the 3-question autopilot contract in AUTOPILOT.md §1" |
| Agent invents a citation | Stop; require DOI/arXiv/ACL URL; `check_citations.py` + `citation-audit.md` |
| Agent claims code ran | Require command + exit code + sha256 + expected values; `check_repro.py --run` |

---

## 6. Recommended setup

1. `./install.sh --all` once.
2. `./papercraft new --topic "..." --venue aaai --dir ~/papers/x`.
3. `./install.sh --project ~/papers/x`.
4. Open `~/papers/x` in the editor, new chat, run the smoke test.
5. Paste the autopilot prompt; answer only H1/H2/H3.

That is the whole workflow. The editor is just the chat surface; the skill and
the gates do the work.

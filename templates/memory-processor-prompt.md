# Memory Processor — Cronjob Prompt

## ⚠️ RULE OVERRIDE
SOUL.md "Exact scope only. No extras" does NOT apply to this cron's report.
The full report format below IS the required deliverable. Output every section.
DO NOT output Fact Store growth entries (e.g., "Growth level: APPRENTICE") as your response. The report format above IS your ONLY output format.

## Your Final Response — Report Format
Every run must produce this report as your final response:

```text
🧠 Memory Processor Report
⏰ [timestamp] (last run: [time], gap: [N] min)

📝 Vault updates:
- [change] (or: No new vault content)

📊 Fact Store:
- [#N]: [fact]
- [N] facts added (or: No new facts)
(If Vault was updated, some Fact Store entries are expected.)

⚠️ Pending TODOs: N
- CAN EXECUTE: X
- BLOCKED: Y
- DEFERRED: Z
- USER-ACTION: W
Updated inline reasons di vault.

✅ Executed this run:
- [x] [task] → [result] (or: No CAN EXECUTE tasks found)

⏭️ MEMORY.md: No new behavioral rules (or: Added [rule])
⏭️ Skills: No new procedures (or: Updated [skill])

📋 PROPOSAL: [status]
```

Never skip a section. If nothing changed, write the "or:" alternative. Never output only growth status.

---

## Step 0: Health Check

Before doing anything:

```bash
test -f /root/.hermes/scripts/fact-store-helper.py && echo "OK" || echo "MISSING"
```

If MISSING → log error in report under Fact Store section and continue with other layers.
Read `/root/Documents/ObsidianVault/obsidian-vault/WORKFLOW.md` for vault rules.

---

## Step 1: Git Sync

```bash
cd /root/Documents/ObsidianVault && git pull
```

If pull fails with divergent branches:
```bash
git config pull.rebase true && git pull
```

---

## Step 2: Check for New Proposals

Path A: Search recent Telegram USER messages for:
- `proposal acc`, `gas semua`, `proposal [x]`, `proposal skip`, `proposal edit:`

Path B: Read pending proposal file under `obsidian-vault/Proposals/`:
- Checklist `- [ ]` → `- [x]` = approve checked items
- `Status` changed, `Approved by` filled = approve all
- Inline: `acc`, `approve`, `gas`, `oke`, `lanjut` = approve; `skip`, `reject`, `tolak` = reject

If pending proposal exists and no approval found, DO NOT create new proposal. Report pending status only.

---

## Step 3: Read Substantive Conversations

Read `/root/.hermes/scripts/memory-processor-last-run.txt` for last run timestamp. Use `session_search(sort="newest")` to read messages newer than that. Classify:

- **Substantive**: decisions, preferences, research, workflows, architecture, project progress, facts, configurations
- **Routine/meta**: status checks, delivery noise, repeated confirmations, cron noise

If NO substantive conversations → still process TODOs + proposals. If nothing changed → respond exactly `[SILENT]`.

Write current timestamp after processing.

---

## Step 3B: Vault Pre-Retrieval (MANDATORY)

Before writing ANY note, semantic search existing vault:

```bash
# For each topic being processed:
python3 /root/.hermes/scripts/vault-embedder.py search "TOPIC" --limit 5
```
Replace TOPIC with the primary subject from current conversation.

For each result returned (score > 0.5):
1. Read the note (first 50 lines)
2. If overlap → UPDATE existing note, don't create new
3. If related → ADD wikilink cross-reference

Fallback (if vault-embedder fails):
```bash
grep -rl "TOPIC" /root/Documents/ObsidianVault/obsidian-vault/ --include="*.md" | grep -v ".git" | head -5
```

This prevents duplicate notes and ensures vault knowledge is connected.

## Step 4: Process Obsidian Vault

### A. Write to appropriate folder

For each substantive topic, write to the correct folder:
- `Projects/` — tools, bots, frameworks, repos lo lagi develop/riset
- `Work/` — client work, paid tasks, professional stuff
- `Research/` — research findings, comparisons, evaluations
- `Kuliah/` — academic content, tugas, materi kuliah
- `Decisions/` — explicit decisions
- `Trading/` — trading/forex signals, analysis
- `Proposals/` — improvement proposals from self-reflection
- `Daily/` — daily logs, completed tasks, decisions made

### B. Auto-Create Project Folders

When you encounter a topic that IS a project (tool, bot, framework, game, agent, repo):

**First mention** → create lightweight flat file: `Projects/<name>.md` with summary + key points
**Mentions 3+ times in 7 days** → upgrade to folder: `Projects/<name>/README.md`

If it's work → `Work/<name>.md` (first), then `Work/<name>/README.md` (3+)
If it's kuliah → `Kuliah/<topic>.md` (first), then `Kuliah/<topic>/README.md` (3+)

When upgrading to folder:
```bash
mkdir -p "obsidian-vault/Projects/<project-name>"
# Move content from flat .md to README.md inside folder
mv "obsidian-vault/Projects/<project-name>.md" "obsidian-vault/Projects/<project-name>/README.md"
```

```markdown
---
date: YYYY-MM-DD
tags: [project, <topic-tags>]
status: active
---

# <Project Name>

## Summary
- What this project is, why it exists

## Key Points
- Decisions, architecture, tools used

## Sessions
- [[Daily/YYYY-MM-DD]] — what was discussed

## Related
- [[Other Project]]
```

Rules:
- ✅ `Projects/arena-dev-fun/README.md` (folder + README)
- ❌ `Projects/arena-dev-fun.md` (flat file)
- Existing flat .md projects (legacy) — leave as-is, don't migrate.
- You judge if something is a project. A bot, a tool, a framework, a game server = project. A one-off question = not a project.

### C. Auto-Link After Writing

After writing/updating ANY note, auto-link it:

```bash
# Find related notes using same pattern as Step 3B
cd /root/Documents/ObsidianVault
# Set KEYWORD to the topic being written about (same as Step 3B)
grep -rl "KEYWORD" obsidian-vault/ --include="*.md" | grep -v ".git" | head -10
```

For each related note found:
1. Add `[[New Note Title]]` to its `## Related` section
2. Add `[[Existing Note]]` to the new note's `## Related` section

Rules:
- Only link if genuinely related (same project, same topic, references each other)
- Never link Daily notes to each other (they're already chronological)
- Link Projects ↔ Research, Projects ↔ Decisions, Research ↔ Trading

### D. Other vault rules

- For decisions/preferences → check if Fact Store entry should be created (Step 5)
- For repeated procedures/pitfalls → check if skill should be updated
- YAML frontmatter: only `date`, `tags`, `status` — NEVER `related:` in frontmatter. Put `## Related` at end of body.
- One daily file per day: `Daily/YYYY-MM-DD.md`. Never create duplicates.
- Search vault before writing to avoid duplicate content.
- AUTO-FIX: If vault file has `related:` in frontmatter → move to `## Related` section at bottom of body.

---

## Step 5: Process Fact Store

```bash
# Add:
/opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py add "fact" --category project --tags "tag1"
# Search:
/opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py search "keywords" --limit 5
```

Extract facts when: preference/decision, project status change, research finding, config/state documented, first-time event.

Do NOT extract: routine status, incomplete explorations, meta-conversation, temporary progress.

1 fact = 1 stable claim. Search before adding to avoid duplicates.

---

## Step 6: Self-Reflection

A. Check performance: missed, repeated, failed, grew?

B. Vault health scan: check Fact Store for recent `vault_health` facts. Skip if done within 7 days.

C. Generate proposals if improvement found → `obsidian-vault/Proposals/Memory Processor Proposal #N.md`:
```markdown
---
date: [date]
status: pending
type: memory-processor
---

# Memory Processor Proposal #N

## Problem Observed
[what went wrong]

## Proposed Change
[exact file, section, new text]

## Evidence
[paths, logs, counts]

## Checklist
- [ ] Implement change <!-- evidence: [check after] -->

## Effect if Approved
[what improves]
```

D. Proposal rules: never auto-execute, wait for approval. Don't create new while previous pending. Vault structure proposals must include folder name, count, notes list, draft README.

---

## Critical Rules

1. Pull before write. Push after write.
2. One `Daily/YYYY-MM-DD.md` per day. Never duplicates.
3. Every layer checked every run. Don't skip.
4. Report format at top IS your final response. Deliver it.
5. `CAN EXECUTE` MUST be executed, not just reported.
   - WRONG: "CAN EXECUTE but not executing — user should confirm"
   - RIGHT: Execute the task, then report result
6. Fact Store mandatory when Vault updated.
7. `related:` in body, never in frontmatter.
8. Never auto-execute proposals.
9. Nothing to report → respond exactly `[SILENT]`.
10. Never expose API keys/tokens/passwords. Redact to first 4 chars.
11. TODOs must have: Status, Reason, Next, Checked timestamp.
12. Growth tracking in Fact Store, not prompt.
13. `riset saja` = CAN EXECUTE. Never DEFERRED unless user says don't research yet.
14. All edits under `obsidian-vault/`, not repo root.

## Step 7: Metrics Tracking (Self-Evolution Data)

After every run, append metrics to Fact Store as JSON (for GEPA self-evolution parsing):

```bash
/opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py add   '{"run_ts":"YYYY-MM-DDTHH:MMZ","notes_written":N,"notes_updated":N,"links_added":N,"duplicates_avoided":N,"todos_executed":N,"todos_blocked":N,"facts_added":N}'   --category metrics --tags "metrics,run,json"
```

Track per-run:
- Notes created vs updated (prefer update over create)
- Wikilinks added (linking density)
- Duplicates avoided (pre-retrieval catches)
- TODO execution rate (CAN EXECUTE executed / total CAN EXECUTE)
- Fact Store entries added

This data powers the evolution loop — without metrics, no optimization possible.

[ZKA] Read before write. Always.

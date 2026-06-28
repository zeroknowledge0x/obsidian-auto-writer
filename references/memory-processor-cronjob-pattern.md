# Memory Processor Cronjob Pattern

## When to Use
Background LLM cronjob that reads conversations since last run, processes to ALL memory layers, reports to Telegram.

## Architecture
```
Cronjob (every 10m)
  → Read timestamp from memory-processor-last-run.txt
  → session_search(sort="newest") conversations AFTER timestamp
  → Process to 5 layers:
      1. Obsidian Vault (substantive topics)
      2. Fact Store (technical facts) — available via `memory` toolset
      3. MEMORY.md (behavioral rules, max 8)
      4. Skills (procedures)
      5. MemPalace (verbatim archive) — NOTE: mcp_mempalace tool unavailable in cron
  → Push to GitHub (git add -A && git commit && git push)
  → Report to Telegram Alert (thread 14) — NOTE: send_message unavailable, report as cron output
  → Update timestamp
```

## Prompt Architecture (June 2026)
The prompt has evolved through multiple iterations. Key architectural decisions:

### Report format at TOP
The report format is the FIRST substantive section after RULE OVERRIDE. This is deliberate — model reads the first section most reliably. If report format is at the bottom (after long instructions), model may not reach it.

### SOUL.md carve-out
SOUL.md "Exact scope only. No extras" conflicts with verbose cron reports. The RULE OVERRIDE section at the very top explicitly exempts this cron's report from that rule.

### GROWTH line removed
Previously, `GROWTH: APPRENTICE...` appeared at the end of the prompt. Model would output just that line instead of the full report. Now removed — growth tracking lives in Fact Store via helper script.

### Auto-Create Project Folders (Step 4B)
When a topic IS a project (tool, bot, framework, game) → CREATE folder immediately. Don't wait, don't count mentions. Projects use FOLDERS (`Projects/<name>/README.md`), not flat files.

### Auto-Write Research Notes (planned)
User wants memory processor to proactively write research/summary notes about topics discussed. Not yet in prompt — next session should implement as Step 4A2.

## Three-way sync
`/root/.hermes/scripts/memory-processor-prompt.md`

## Three-way sync
When editing the prompt, ALWAYS sync all 3 locations:
1. `/root/.hermes/scripts/memory-processor-prompt.md` (working copy)
2. `templates/memory-processor-prompt.md` (skill template, canonical reference)
3. `/root/.hermes/cron/jobs.json` (embedded prompt, what cron actually reads)

Verify sha256 match across all 3. See pitfall "Three-way sync required" in SKILL.md.

## Timestamp File
`/root/.hermes/scripts/memory-processor-last-run.txt`
- Format: ISO 8601 UTC (`2026-06-26T18:03:35Z`)
- Created on first run
- Updated after each successful run

## Cronjob Config
```
name: memory-processor
schedule: every 10m
enabled_toolsets: [terminal, file, skills, session_search, memory]
deliver: telegram:-1003919406547:14 (Alert topic)
```

`memory` toolset is required so the cron session has access to the built-in `memory` tool. However, `fact_store` is NOT available via toolsets — it comes from the holographic memory plugin which requires `_memory_manager` (blocked by `skip_memory=True` in cron). Use the terminal helper script `/root/.hermes/scripts/fact-store-helper.py` with `/opt/hermes-venv/bin/python3` instead.

## Key Rules
1. NEVER ask for permission — just process
2. Be selective — only substantive content
3. Avoid duplicates — check before writing
4. Respect MEMORY.md limit (8 entries)
5. Silent operation — report only at end
6. If TODO.md has unchecked tasks (`- [ ]`), execute the task first, then mark it `- [x]` only after successful completion, commit, and push
7. Do not use a bash/mtime pre-check for "new conversations" — it is unreliable because session DB files can change for reasons other than user chat. Let the LLM perform the timestamp guard with `session_search()` instead

## Report Format
```
🧠 Memory Processor Report
⏰ [timestamp]

📝 Vault updates:
- [list notes written/updated]

📊 Fact Store:
- [fact] → [value/status]
- [N] facts added total

⚠️ Pending TODOs:
- [ ] [task] — [BLOCKED/DEFERRED/CAN EXECUTE: reason]

⏭️ [Layer]: [what was checked, what was found, why no action]
```

## Report Quality Rules (added 2026-06-27)
- **Every skipped layer MUST explain WHY** — what was checked, what was found, why no action needed.
  - Bad: `⏭️ Skills: no new procedures`
  - Good: `⏭️ Skills: checked 3 sessions — topics were Obsidian config, cron tuning, prompt edit. No repeatable multi-step procedures, only one-off fixes.`
- **Every pending TODO MUST explain WHY it's pending** — BLOCKED (what dependency), DEFERRED (user instruction), or CAN EXECUTE (what's needed).
  - Bad: `[ ] Monitor B5D v2 vs-field test — Daily/2026-06-27.md`
  - Good: `[ ] Monitor B5D v2 vs-field test — BLOCKED: tmux s5-runner still running, check next run for final ranking`
- NEVER list a TODO as "pending" without a reason.
- NEVER use bare "no new X" without evidence of what was checked.

## Pitfalls (from first real run 2026-06-26)

### `session_search(around_message_id=0)` FAILS
- **Error:** `"around_message_id 0 not in session_id ..."`
- **Cause:** `around_message_id=0` is not a valid message ID. There is no message with ID 0.
- **Fix:** Use `session_search(session_id="...", around_message_id=<real_id>)` with an actual message ID from a prior discovery call, or use the **browse shape** (`session_search()` with no args) to list recent sessions.

### Correct session_search patterns for memory processor
```python
# 1. BROWSE — get recent sessions (no args)
session_search()

# 2. DISCOVERY — find sessions matching a topic
session_search(query="topic keywords", limit=5, sort="newest")

# 3. SCROLL — read inside a specific session (use real message IDs!)
session_search(session_id="20260626_130108_ca8b06", around_message_id=172598, window=10)
```
- **Never** use `around_message_id=0` — it always fails.
- After a discovery call, use `match_message_id` from results as the anchor for scrolling.

### `session_search(query="*")` returns NO RESULTS
- **Error:** `{"success": true, "results": [], "count": 0, "message": "No matching sessions found."}`
- **Cause:** FTS5 does not support `*` as a wildcard query. `query="*"` is treated as a literal asterisk, which matches nothing.
- **Fix:** Use `session_search()` with NO args (browse shape) to list recent sessions chronologically. Or use specific keywords: `session_search(query="topic keywords", sort="newest")`.

### Filter out cron sessions from results
- Cron sessions (session_id starts with `cron_`) are noise — they're memory processor runs, not user conversations.
- Skip them when scanning for substantive content.
- Look for sessions with `source="telegram"` as the user-facing ones.

### Tools available/unavailable in cron session context
The memory processor prompt references tools with varying availability in a cron session:
- **`fact_store(action='add')`** — **NOT AVAILABLE** in cron sessions. Root cause: cron scheduler passes `skip_memory=True` to AIAgent constructor (cron/scheduler.py line 1686), which sets `_memory_manager = None` (agent/agent_init.py line 1091), preventing holographic plugin tools from being injected. The `memory` in `enabled_toolsets` only enables the built-in `memory` tool, NOT the plugin's `fact_store`/`fact_feedback`.
- **`fact_store` workaround — terminal helper script**: `/root/.hermes/scripts/fact-store-helper.py` provides `add`, `search`, `probe`, `list` commands. MUST use `/opt/hermes-venv/bin/python3` (not bare `python3` — system python lacks `yaml` module). Usage:
  ```bash
  # Add:
  /opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py add "fact content" --category project --tags "tag1,tag2"
  # Search (dedup):
  /opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py search "keywords" --limit 5
  # List:
  /opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py list --limit 10
  ```
- **WAJIB/UNLIMITED prompt pattern** (June 2026): Weak prompt ("For each technical fact found") caused agent to skip fact_store. Fix: replace with explicit "Fact Store — WAJIB, UNLIMITED CAPACITY" section + MANDATORY RULES + helper script instructions. Patch both live jobs.json AND templates/memory-processor-prompt.md.
- **`send_message(action='send', target='telegram:...')`** — NOT available. Report as cron output (auto-delivered).
- **`mcp_mempalace_mempalace_add_drawer()`** — NOT available. Skip MemPalace archiving in cron runs.

When tools are unavailable, document the gap in the report under "⏭️ Skipped" rather than failing.

### Avoid unreliable pre-check scripts
- Do **not** add a bash pre-check based on `sessions.db` mtime to skip LLM runs.
- It is not a reliable signal for "new user chat" because the DB can be touched by scheduler/session internals.
- Keep the guard inside the LLM prompt: read `/root/.hermes/scripts/memory-processor-last-run.txt`, browse/search sessions with `session_search()`, process only messages newer than that timestamp, and exit early with "No new conversations" when none qualify.
- If trying to reduce token use further, split deterministic git sync into no-agent cronjobs, but keep conversation filtering in the LLM run.

### TODO.md processing inside memory processor
- It is okay to merge the old TODO worker into the memory processor to avoid duplicate LLM cronjobs.
- The prompt must explicitly say: if TODO.md has unchecked tasks (`- [ ]`), read each task, execute it, mark `- [x]` only after successful completion, then commit and push.
- If a task fails or is ambiguous, leave it unchecked and report the blocker instead of marking it done.
- Pause/disable the older standalone TODO processor after merging, otherwise the user sees duplicate cron responses.

### TODO source file sync (2026-06-27)
**Critical rule:** When marking a task done, update ALL locations — not just the Daily note.
- Source file (TODO.md, Projects/*.md, etc.) → mark `- [x]` with Done timestamp
- Daily note → record in "✅ Executed this run" section
- If task text appears as `- [ ]` in any non-Daily file after completion → update it
**Detection:** After completing a task, grep vault-wide: `grep -rn "task text" --include="*.md"` to find all locations.
**Incident:** 14:22 UTC run recorded completions in Daily file but left TODO.md unchecked. 16:39 UTC run caught the discrepancy.

### Delivery: one final response only
- Cron runs normally deliver one final response to the configured `deliver` target.
- Do not put `send_message(...)` in the cron prompt unless intentionally sending an extra message; it causes duplicate reports or wrong-thread messages.
- Prefer `deliver: telegram:-1003919406547:14` for the Alert topic and keep the prompt's report step as plain final output.

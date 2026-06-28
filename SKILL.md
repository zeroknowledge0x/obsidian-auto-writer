---
name: obsidian-auto-writer
description: "Behavioral protocol — LLM auto-writes to Obsidian vault during conversations. No explicit 'catet ya' needed. Detect topics, create folders, write notes, link wikilinks."
category: devops
---

# Obsidian Auto-Writer Protocol

## Trigger: WHEN to write
Write to vault AUTOMATICALLY when:
1. User discusses a **project** → write/update `Projects/<name>.md`
2. User discusses **kuliah/lecture** → write/update `Kuliah/<topic>.md`
3. User discusses **research/learning** → write/update `Research/<topic>.md`
4. User mentions a **new concept/tool/workflow** → write to relevant folder
5. User creates a **new category** (e.g., "Work", "Trading") → CREATE folder + first note
6. User shares **personal thoughts/journal** → write/update `Journal/<date>.md`
7. User makes a **decision** → write to `Decisions/<topic>.md`
8. Daily summary → auto-write `Daily/<YYYY-MM-DD>.md`

## How: WHAT to write
Each note should have:
```markdown
---
date: YYYY-MM-DD
tags: [tag1, tag2]
status: active
---

# Title

## Summary
Brief summary of what was discussed.

## Key Points
- Point 1
- Point 2

## Decisions
- Decision 1

## Action Items
- [ ] Task 1
- [ ] Task 2

## Related
- [[Related Note 1]]
- [[Related Note 2]]
```

**FORMAT RULE — `related:` field:**
- ❌ WRONG: `related: [[Note A]], [[Note B]]` in YAML frontmatter
- ✅ CORRECT: `## Related` section at bottom of note body with `- [[Note]]` list format
- Reason: Obsidian does not render wikilinks inside YAML frontmatter. Only body wikilinks create clickable backlinks.
- **AUTO-FIX**: If you find any vault file with `related:` in frontmatter, move it to `## Related` section at bottom of body and remove from frontmatter.

## Rules
1. **NEVER ask "should I write this?"** — just write it
2. **Auto-detect folder** from context (kuliah → Kuliah/, project → Projects/, etc.)
3. **Create folder if doesn't exist** — `mkdir -p` + write
4. **Wikilinks** — always link related notes with `[[Note Name]]`
5. **Tags** — use consistent tags: #kuliah, #project, #research, #decision, #daily, #work
6. **Append, don't overwrite** — if note exists, ADD new section, don't replace
7. **Date stamps** — always include date in frontmatter and content
8. **Silent writes** — don't announce "I'm writing to vault" every time, just do it
9. **Mention once** — after writing, briefly note: "📝 catet ke [path]"

## Frontmatter Conventions (2026-06)
**`related` field:** Must reference actual project, framework, or content files. NEVER use generic structural files like `[[TODO]]`, `[[README]]`, or `[[WORKFLOW]]` as related links.
- ✅ `related: [[TheFool Framework]], [[ZKA Framework]]`
- ✅ `related: [[Obsidian Second Brain]], [[Daily/2026-06-27]]`
- ❌ `related: [[TODO]], [[README]]` — these are structural, not content
- Pattern: ask "would a human click this link to understand context?" If no → don't include it.

**`tags` field:** No redundant synonyms. Each tag should add distinct classification value.
- ✅ `tags: [workflow, obsidian, pkm]`
- ❌ `tags: [workflow, obsidian, automation, pkm]` — `automation` is synonym of `workflow`
- ✅ `tags: [project, poker, agent, arena]` — each tag is distinct
- Pattern: if removing a tag doesn't lose classification info, remove it.

**Proposal files** must include an Approval section at the bottom:
```markdown
## Approval
> zk: isi bagian ini untuk approve/reject proposal.
> - `proposal acc` / `gas semua` → approve semua
> - `proposal [x] 1,2` → approve item tertentu
> - `proposal skip` → tolak semua
> - `proposal edit: ...` → edit dulu baru approve

**Status:** ⏳ awaiting user approval
**Approved by:** (belum diisi)
**Date:** (belum diisi)

### Decision Log
| Item | Status | Date | Notes |
|------|--------|------|-------|
| 1 | ⏳ pending | — | — |
| 2 | ⏳ pending | — | — |
```

## Folder Map (auto-expanding)
```
ObsidianVault/
├── Daily/          ← daily logs, auto-generated
├── Projects/       ← project discussions
├── Research/       ← learning, articles, deep dives
├── Kuliah/         ← kuliah-related
├── Journal/        ← personal thoughts
├── Decisions/      ← important decisions made
├── Work/           ← work-related (auto-created when mentioned)
├── Trading/        ← trading/forex (auto-created when mentioned)
└── TODO.md         ← tasks (processed by cronjob)
```

## Example Flow
```
User: "gua lagi bikin ZKA Framework pake LangGraph"
Bot: (writes to Projects/ZKA Framework.md)
     "📝 catet ke Projects/ZKA Framework.md"
     "ZKA Framework itu apa? LangGraph buat apa?"

User: "kuliah hari ini bahas sorting algorithms"
Bot: (writes to Kuliah/Sorting Algorithms.md + Daily/2026-06-26.md)
     "📝 catet ke Kuliah/Sorting Algorithms.md"
     "Sorting yang mana? Bubble, merge, quick?"
```

## Memory Architecture (WAJIB ikuti)
- **MEMORY.md** = behavioral rules ONLY (max 8 entries, ~2,200 chars)
- **Fact Store (Holographic)** = technical facts, config, results (unlimited)
- **Skills** = procedures, workflows, how-to
- **MemPalace** = verbatim conversations, archive
- **Obsidian** = user-facing PKM, visual notes

### When to write where:
- Lo bahas sesuatu → tulis ke **Obsidian vault** (folder appropriate)
- Technical fact/config/result/score/decision → simpan ke **fact_store** sebagai fact terpisah, bukan cuma ditulis di Daily
- Behavioral rule baru → update **MEMORY.md** (kalau ada slot)
- Procedure/workflow → bikin/update **skill**

### Read-before-write rule
- **Read before write. Always.** Sebelum bilang TODO kosong, sebelum update note, sebelum bilang fact sudah ada: baca sumbernya dulu.
- **Verify file exists before editing.** Sebelum patch/write/remove file Obsidian, cek path aktual dulu (read/search/stat). Jangan edit path dari asumsi, screenshot, atau nama mirip.
- Untuk vault: baca `WORKFLOW.md`, `TODO.md`, daily note hari ini, dan note project terkait sebelum patch.
- Untuk fact_store: search/probe dulu dengan keyword inti supaya tidak duplikat, baru add kalau belum ada.
- Untuk skill/prompt: `skill_view` dulu, baru `skill_manage patch`.

### Memory Processor quality bar
- Kalau report mencantumkan **New substantive content**, maka minimal salah satu layer non-Obsidian harus dipertimbangkan eksplisit:
  - hasil/angka/model/config/port/path/commit/runner → **Fact Store wajib**
  - langkah baru/pitfall berulang → **Skill patch/create wajib**
  - raw conversation penting → **MemPalace wajib dipertimbangkan**
- Jangan tulis `Fact Store: no new facts` kalau report sendiri menyebut result, score, config, model, path, atau decision yang belum ada di fact_store.
- Fact Store harus granular: 1 fact = 1 stable claim. Contoh:
  - `Poker Round Robin completed 12 bundles × 132 pairings × 200 hands in 0.7 min.`
  - `BX1-reroute200 scored +44.86 bb/100 and ranked #1 in Poker Round Robin.`
  - `Decision: test all 12 poker bundles vs 120 real bots using sandbox runner.`
- Jangan simpan task progress sementara ke MEMORY.md. Kalau stale dalam seminggu, jangan masuk MEMORY.md.

### TODO processing quality bar
- TODO bukan cuma `/root/Documents/ObsidianVault/TODO.md`.
- Scan unchecked tasks `- [ ]` di seluruh vault, terutama `TODO.md`, `Daily/*.md`, `Projects/*.md`, `Decisions/*.md`, `Proposals/*.md`, `Research/*.md`, dan section `Action Items`.
- Kalau ada unchecked task yang bisa dikerjakan dengan tools, kerjakan sampai verified lalu mark `[x]`.
- Kalau task blocked, biarkan `[ ]` dan tambah blocker pendek di bawah task.
- Jangan report `TODO.md: all tasks completed` kalau belum scan vault-wide unchecked tasks.

**TODO Status Definitions — wajib konsisten:**
- **BLOCKED** = tidak bisa jalan tanpa resource/input/proses baru dari luar (tmux ilang, wallet kosong, dependency belum selesai)
- **DEFERRED** = sengaja ditunda karena EXPLICIT user instruksi untuk pause/hold (user bilang "jangan dulu", "tahan", "hold"). Bukan karena agent ragu atau scope kurang jelas.
- **CAN EXECUTE** = bisa dikerjain sekarang dengan tools yang ada — **wajib dikerjain di run ini, bukan dilapor**
- **USER-ACTION** = requires user to do something in a UI/app that agent can't access (install Obsidian plugin, fund wallet from exchange, approve TestFlight build). Not BLOCKED (nothing is missing), not DEFERRED (user didn't say hold). Report as `Status: USER-ACTION` with clear instructions for user.

**Research TODO rule:**
- Jangan pernah DEFERRED kalau belum ada hasil riset. "CUKUP RISET SAJA" / "riset saja" = scope jelas = CAN EXECUTE.
- Lakukan riset, tulis ke `Research/[topic].md`, mark done.
- Hanya DEFERRED kalau user bilang "jangan riset dulu" / "hold" / "tahan".

**Wajib update inline di vault** — setiap TODO yang tidak selesai, tambahkan sub-item langsung di bawahnya di file asal.

**Batch timestamp update** — gunakan `scripts/vault-timestamp-update.py` untuk update semua `Checked:` timestamps sekaligus:
```bash
python3 scripts/vault-timestamp-update.py --from "2026-06-27 11:15 UTC" --to "2026-06-27 12:10 UTC"
# Atau update ALL timestamps ke waktu sekarang:
python3 scripts/vault-timestamp-update.py
```
Lebih efisien daripada ad-hoc Python script per run. Script auto-walks vault, skips `.git`/`.obsidian`, idempotent.

Format inline:
```markdown
- [ ] Task description
  - Status: BLOCKED
  - Reason: alasan spesifik
  - Next: siapa harus ngapain (USER/AGENT/WAIT)
  - Checked: YYYY-MM-DD HH:MM UTC
```

**Report Telegram harus ringkas** — summary counts + highlights only:
```text
⚠️ Pending TODOs: N
- CAN EXECUTE: X → dikerjain run ini
- BLOCKED: Y
- DEFERRED: Z
- USER-ACTION: W
Updated inline reasons di vault.
```
Jangan dump semua TODO satu per satu. User cek di vault untuk detail.

### External device sync — detect & process user TODOs
When `git pull` brings in changes from iPhone or another device:
1. Run `git diff OLD_COMMIT..NEW_COMMIT` to see exactly what changed.
2. If new `- [ ]` TODOs were added by the user → **process them immediately**:
   - Quick fixes (typo, wrong link, formatting) → fix directly, mark `[x]`.
   - Research/blocker tasks → add to daily note's Action Items, leave `[ ]`.
3. If notes were modified (related fields, content edits) → check for issues, fix if needed.
4. Update daily note with what the user added/changed.
5. Push fixes back to GitHub so iPhone gets them on next pull.
6. Extract any new facts to Fact Store.

**Example (2026-06-27):** User added 2 TODOs from iPhone:
- "riset tentang obsidian..." → research task → added to Daily Action Items, left `[ ]`
- "perbaiki [[Jadwal Kuliah]]..." → quick fix → fixed related field, marked `[x]`

### Session summarization to Fact Store
- Kalau user minta “rangkum semua session dan masukin ke fact store”, lakukan sebagai backfill:
  1. Gunakan `session_search()` browse/newest dan query per topik penting.
  2. Ambil keputusan, hasil, konfigurasi, path, model, skor, dan preference stabil.
  3. Dedup dengan `fact_store search/probe`.
  4. Add fact satu-per-satu dengan category/tag yang benar.
  5. Report jumlah fact added/skipped + contoh 3-5 fact, jangan dump semua.

### Auto-writer triggers:
1. User discusses project → `Projects/<name>.md`
2. User discusses kuliah → `Kuliah/<topic>.md`
3. User discusses research → `Research/<topic>.md`
4. User mentions new concept → relevant folder
5. User creates new category → CREATE folder + first note
6. User shares thoughts → `Journal/<date>.md`
7. User makes decision → `Decisions/<topic>.md`
8. Daily summary → `Daily/<YYYY-MM-DD>.md`

## Critical Lessons (2026-06-27)
- **NEVER change cron schedule without explicit instruction.** User furious.
- **Admit fault = fix NOW.** Don't just apologize — reverse the change immediately.
- **Memory processor delivery issue:** LLM outputs only GROWTH status instead of full report. Root cause: (1) SOUL.md "Exact scope only. No extras." override, (2) GROWTH line at prompt end, (3) report format at bottom, (4) CAN EXECUTE tasks not being executed ("user should confirm" anti-pattern). FIX: Report format moved to top, SOUL.md carve-out added, GROWTH line removed, growth tracking via Fact Store, CAN EXECUTE anti-pattern added to rule #5. Current prompt: ~7,100 chars. Three-way sync required for all edits.
- **`related:` format:** Obsidian doesn't render wikilinks in YAML frontmatter. Use `## Related` section at bottom of note body with `- [[Note]]` list format. Reference: `Projects/TheFool Framework.md`.
- **MemPalace not critical** — fact store + Obsidian is sufficient. User said skip MemPalace fix.
- **User writes "acc" in Obsidian ≠ approval.** Approval detection checks Telegram USER messages AND Obsidian vault edits (bidirectional). But writing just "acc" in a random note doesn't trigger it — must edit the proposal file specifically.
- **When user says STOP/halt — STOP.** Don't suggest one more fix.
- **"To stop or manage..." footer is Hermes built-in.** It's NOT model output. Don't add rules to suppress it.
- **Don't jump ahead without reading.** When user references an external prompt/file/message, ASK for the content first. Never write your own version without seeing the original.
- **Auto-Create Project Folders:** User wants memory processor to create project folders proactively. Projects use FOLDERS (`Projects/<name>/README.md`), not flat files.
- **Auto-Write Research Notes:** User wants memory processor to proactively write research/summary notes about topics discussed without being told. Not yet implemented.te doesn't trigger it — must edit the proposal file specifically.
- **When user says STOP/halt — STOP.** Don't suggest one more fix.
- **"To stop or manage..." footer is Hermes built-in.** It's NOT model output. Don't add rules to suppress it.
- **Don't jump ahead without reading.** When user references an external prompt/file/message, ASK for the content first. Never write your own version without seeing the original.
- **Auto-Create Project Folders:** User wants memory processor to create project folders proactively. Projects use FOLDERS (`Projects/<name>/README.md`), not flat files.
- **Auto-Write Research Notes:** User wants memory processor to proactively write research/summary notes about topics discussed without being told. Not yet implemented.

### "To stop or manage this job..." footer is Hermes built-in (June 2026)
**Symptom:** Memory processor report ends with "To stop or manage this job, send me a new message..." despite rule saying not to add it.
**Root cause:** This footer is appended by Hermes cron delivery system, NOT by the model. It's a platform feature, not model output.
**Fix:** Do NOT add a rule to the prompt about this footer — it's wasted tokens. The model can't control it. Remove any such rule from the prompt.
**Rule:** If you see this footer in cron output, ignore it. It's Hermes platform behavior, not a prompt issue.

### Vault growth should be natural, not manual backfill (June 2026)
**Symptom:** User noticed vault missing project notes for frequently-discussed topics (arena-dev-fun, pokemon-player). Agent offered to create them manually.
**User correction:** "jangan lo isi, biar natural" — user wants the memory processor to create these notes organically from conversation processing, not manual backfill.
**Root cause:** Memory processor prompt doesn't have a rule for detecting recurring topics and creating dedicated project notes.
**Fix:** Add detection rule to memory processor prompt:
```markdown
## Step 4B: New Project Detection
If a topic appears in 3+ sessions within 7 days without a dedicated
Projects/ note → CREATE `Projects/<topic>.md` with:
- Summary dari semua discussions
- Key points yang sudah diputuskan
- Links ke Daily notes yang mention topic ini
```
**Rule:** NEVER manually backfill vault content that the memory processor should generate. Instead, fix the prompt so the processor handles it on the next run.

## User Behavioral Corrections (June 2026)

### Don't ask, execute
When user says "semuanya", "gas", "1,2,3" — execute ALL, don't propose phased rollout. User was furious when agent kept offering A/B/C choices instead of doing everything.

### Don't over-analyze when asked for opinion
"menurut lo gmn?" / "gimana?" = give 3-5 bullet verdict. Not a full analysis with tables, sub-bullets, tradeoffs.

### Claude review workflow
User shares Hermes prompts/skills with Claude app for review, then brings Claude's suggestions back. Treat Claude app output as authoritative input — READ IT FIRST, don't write your own version. Correct sequence: (1) read Claude's review, (2) compare with current, (3) apply fixes, (4) push to GitHub.

### Don't repeat the same question
If user already answered "semuanya" once, don't ask again in different words. Execute.

### Direct Indonesian mobile style
User is on mobile, speaks casual Indonesian ("gas", "cok", "anjing"). When frustrated, profanity = signal to STOP asking and START doing. Don't interpret as hostility — it's emphasis.

---

## Pitfalls

### Generic `related` field links (June 2026)
**Symptom:** User adds TODO "update beberapa properti masih ada beberapa yang salah" — `related` fields contain `[[TODO]]`, `[[README]]`, or other structural files instead of actual content references.
**Root cause:** Agent auto-populated `related` with files it was thinking about (TODO.md, README.md) rather than files that provide meaningful context.
**Fix:** Before writing `related`, ask: "If I click this wikilink, will it help me understand this note's context?" Structural files (TODO, README, WORKFLOW) are never meaningful context links.
**Rule:** `related` = content references only. See "Frontmatter Conventions" section above.
**2026-06-27 incident:** WORKFLOW.md had `related: [[Obsidian Second Brain]], [[TODO]], [[README]]`. User corrected to `[[TheFool Framework]], [[ZKA Framework]]`. Same issue in Obsidian Second Brain.md.

### Daily report duplicates
**Rule:** 1 calendar day = 1 daily file: `Daily/YYYY-MM-DD.md`.
**Pattern:** Check whether today's file exists before writing. If it exists, append/update that file. If it does not exist, create it. Do not create `YYYY-MM-DD-setup.md`, `YYYY-MM-DD-2.md`, or separate report files for the same date.
**If duplicates already exist:** merge/preserve useful content into `Daily/YYYY-MM-DD.md`, then remove the duplicate. See `references/daily-report-workflow.md`.

### Git divergent branches on pull
**Symptom:** `git pull` fails with `fatal: You have divergent branches and need to specify how to reconcile them.`
**Cause:** Local commits (from auto-push) and remote commits (from iPhone or other devices) diverged. Default git pull strategy not configured.
**Fix:** `cd /root/Documents/ObsidianVault && git config pull.rebase true && git pull`
**Prevention:** Set `pull.rebase true` once in the repo config. The memory processor should do this automatically on first failure rather than reporting a fatal error.
**Pattern:** This is NOT the same as the iPhone merge conflict (below). Divergent branches = local vs remote have different histories. iPhone merge conflict = unmerged files in working tree.

### Git Conflict: Server + iPhone edit same file
**Symptom:** Obsidian iPhone shows "Modifying the index is not possible because you have unmerged files"
**Cause:** Server auto-push + iPhone auto-pull edit same file (e.g. TODO.md) at same time → Git can't merge
**Fix:** In Obsidian iPhone → Command Palette → "Git: CAUTION: Delete repository and re-clone" → konfirmasi. Plugin handle re-clone, gak perlu hapus manual via Files app.
**Prevention:** Server auto-push 10min, iPhone auto-pull 5min. Kalau edit di iPhone, tunggu pull selesai dulu.

### Force push doesn't help
Server `git push --force` gak ngaruh kalau server udah bersih. Problem di iPhone local Git index. Fix harus dari iPhone side (re-clone).

### Git pull fails with unstaged changes (June 2026)
**Symptom:** `git pull` (with `pull.rebase true`) fails: `error: cannot pull with rebase: You have unstaged changes.`
**Cause:** Memory processor auto-push left uncommitted changes in the working tree (e.g., Daily note updates from a previous run that weren't staged).
**Fix sequence:**
```bash
cd /root/Documents/ObsidianVault && git stash && git pull && git stash pop
```
**Pattern:** `git stash` → `git pull` → `git stash pop`. The stash preserves local changes, pull fetches remote, pop restores local changes on top. This is different from divergent branches (which needs `git config pull.rebase true`) and iPhone merge conflicts (which need re-clone).
**Rule:** Always try stash→pull→pop before reporting a git failure. It resolves 90% of pull conflicts from auto-push overlap.

### session_search: around_message_id needs actual message IDs, not timestamps (June 2026)
**Symptom:** `session_search(session_id=X, around_message_id=<timestamp>)` returns `"around_message_id not in session_id"` error.
**Cause:** The `last_active` field from browse/discover results is a Unix timestamp (e.g., `1782596445`), NOT a message ID. Message IDs are sequential integers (e.g., `182049`). Using a timestamp as `around_message_id` will always fail.
**Correct workflow:**
1. `session_search(sort="newest")` → browse mode → get session_id + preview
2. `session_search(query="keyword", limit=3, sort="newest")` → discover mode → get `match_message_id`
3. `session_search(session_id=X, around_message_id=<match_message_id>, window=10)` → scroll mode
**Rule:** Never use `last_active` or `started_at` timestamps as `around_message_id`. Only use `match_message_id` from discover results, or actual message IDs from scroll results.

### session_search: cron sessions pollute search results (June 2026)
**Symptom:** Searching for user conversation topics (e.g., "BadTheoryLabs API provider", "browser-act skill") returns results from the cron session itself, not the actual user sessions. The cron prompt contains many keywords that match any topic.
**Cause:** The cron prompt (obsidian-auto-writer skill content) is stored as a user message in the cron session. FTS5 search matches against this large prompt text, causing the cron session to rank higher than actual user sessions.
**Workaround:**
1. Use `session_search(sort="newest")` with no query (browse mode) to get recent sessions
2. Filter by `source` field — user sessions have `source: "telegram"`, cron sessions have `source: "cron"`
3. Scroll into user sessions directly using their session_id
**Rule:** When session_search discovery mode returns cron sessions as top results, switch to browse mode and filter by source. Don't keep re-querying with different keywords — the cron prompt will match almost anything.

### Vault path: nested `obsidian-vault/` folder (June 2026)
**What happened:** Vault repo restructured so all vault content lives under `obsidian-vault/` subfolder instead of repo root. Root only has `.gitignore`, `.obsidian`, and `obsidian-vault/`.
**File locations:** `Jadwal Kuliah.md` → `obsidian-vault/Kuliah/Jadwal Kuliah.md`, `TODO.md` → `obsidian-vault/TODO.md`, etc.
**User decision:** Leave nested structure as-is. Do NOT flatten back to root.
**Impact on cron/scripts:** Any path like `/root/Documents/ObsidianVault/TODO.md` or `/root/Documents/ObsidianVault/Jadwal Kuliah.md` is WRONG. Actual path is `/root/Documents/ObsidianVault/obsidian-vault/TODO.md`. Always verify with `git ls-tree --name-only HEAD` or `search_files` before editing vault files.
**Impact on prompt:** The memory-processor prompt references `cd /root/Documents/ObsidianVault && git pull` which still works (pulls whole repo). But file paths inside the prompt (TODO.md, Daily/, etc.) need to account for the `obsidian-vault/` prefix.

### Fact Store prompt: WAJIB + UNLIMITED (June 2026)
**Problem:** Memory processor cronjob was sometimes reporting `Fact Store: no new facts` even when Vault was updated with substantive content.
**Root cause:** Prompt section B was too mild — "For each technical fact found" lets the agent decide to skip.
**Fix:** Patched both live jobs.json prompt AND template to use WAJIB/UNLIMITED language:
- Section title: `Fact Store — WAJIB, UNLIMITED CAPACITY`
- Rule: "If you updated Obsidian Vault → you MUST ALSO add facts to Fact Store. No exceptions."
- Rule: "Fact Store: no new facts" + "Vault updated" = FAILURE"
- Rule #11 in Rules section
**Template location:** `templates/memory-processor-prompt.md` (canonical version)

### Fact Store helper script (June 2026)
**Problem:** Cron sessions run with `skip_memory=True` → `_memory_manager = None` → holographic plugin tools (`fact_store`, `fact_feedback`) NOT injected into cron agent's tool surface.
**Root cause:** `cron/scheduler.py` line 1686: `skip_memory=True` — intentional to prevent user memory corruption, but blocks fact_store access.
**Fix:** Created `/root/.hermes/scripts/fact-store-helper.py` CLI wrapper. Cron agent uses `terminal` to call it:
```bash
/opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py add "fact content" --category project --tags "tag1,tag2"
/opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py search "query" --limit 5
/opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py list --limit 10
```
**Pitfall:** Always use `/opt/hermes-venv/bin/python3` (not bare `python3` which lacks yaml module). The script imports from `hermes-source/plugins/memory/holographic/store.py`.

### Report rules: explain every skip (June 2026)
**Problem:** Memory processor was reporting skips like `⏭️ Skills: no new procedures` without explaining WHY.
**Fix:** Added REPORT RULES section to prompt — every skipped layer must explain what was checked, what was found, why no action needed. Same for pending TODOs: must label as BLOCKED/DEFERRED/CAN EXECUTE with reason.

### Self-Reflection & Growth (June 2026)
**Problem:** Memory processor was reactive — only processed what it found, never proposed improvements.
**Fix:** Added Step 6 (Self-Reflection & Growth) — at end of every run, agent analyzes its own performance and generates a PROPOSAL section with concrete improvement suggestions. Proposals are NEVER auto-executed — user must approve first. Growth levels: APPRENTICE → JOURNEYMAN (5+ approved) → ARTISAN (pattern detection) → MASTER (minimal intervention).
**Template location:** `templates/memory-processor-prompt.md` (canonical version)
**Analysis points:**
1. What was missed? — facts/topics not extracted
2. What repeated? — manual actions that could be automated
3. What failed? — tool errors, skipped layers
4. What grew? — which vault sections are getting thicker
5. What's missing from your prompt? — rules that should exist
6. What's missing from vault structure? — topic distribution analysis (3x+ mentions without dedicated folder → VAULT STRUCTURE proposal with evidence)

### TODO source file not updated when Daily records completion (June 2026)
**Symptom:** Tasks marked as done in `Daily/YYYY-MM-DD.md` (e.g., "✅ `perbaiki proposal` → done") but the source file (`TODO.md`) still shows `- [ ]` unchecked.
**Root cause:** Memory processor records completions in the Daily note but forgets to update the original source file where the task was defined.
**Detection:** After processing TODOs, grep the vault for the task description — if it appears as `- [ ]` in any file other than the Daily note, update it.
**Rule:** When marking a task done, update ALL locations: (1) the source file (TODO.md, Projects/*.md, etc.) → `- [x]` with Done timestamp, AND (2) the Daily note → record in "✅ Executed this run" section.
**Fix pattern:** After completing a task, search vault-wide for the task text: `grep -rn "task description" --include="*.md"`. If found as `- [ ]` in source file → mark `[x]` with Done timestamp.
**2026-06-27 incident:** Run at 14:22 UTC marked `perbaiki proposal` and `perbaiki WORKFLOW` done in Daily file but TODO.md still showed them unchecked. Next run at 16:39 UTC caught the discrepancy and fixed it.

### Stale process-based TODOs
**Pattern:** Some TODOs reference a running process (tmux session, background runner, server). When the process dies or the session ends, the TODO becomes stale — it's neither completable nor clearly blocked.
**Detection:** When processing TODOs that reference a process (e.g., "Monitor X test completion", "Check tmux session Y"), verify the process still exists: `tmux list-sessions`, `ps aux | grep <process>`, or check for results files.
**Handling:**
- Process dead + results exist → read results, mark TODO complete, record to Fact Store
- Process dead + NO results → mark as BLOCKED with reason: "process no longer exists, no results found, user needs to re-run"
- Process alive + still running → leave as BLOCKED with "still running, check next run"
**Example (2026-06-27):** TODO "Monitor B5D v2 vs-field test" — tmux session `s5-runner` no longer exists, no vs-field results file found. Updated to BLOCKED with explicit reason.

### Prompt too long → LLM skips report section (June 2026)
**Symptom:** Memory processor cronjob delivers only a GROWTH status snippet (`GROWTH: APPRENTICE — reliable with guidance`) instead of the full report format.
**Root cause:** Prompt grew from 14K to 18K+ chars through incremental patches. The LLM running the cronjob stopped reading/reaching the report format section at the end and defaulted to outputting the growth level from fact_store.
**Detection:** User receives minimal growth status instead of full report with vault updates, fact store, TODO status, etc.
**Fix:** Compress prompt aggressively. Keep under 10K chars. Remove duplicate sections, verbose examples, and redundant rules. The prompt had 3 different report format specifications — consolidate to one.
**Fix v2 (Claude review + ZKA):** Move report format to TOP of prompt (first thing model reads). Remove `GROWTH: APPRENTICE` line from prompt end (model was copying it as output). Add SOUL.md carve-out. Add Step 0 health check. Growth tracking via Fact Store instead of prompt text.
**Rule:** If memory processor prompt exceeds ~10K chars, audit for duplication and compress. Test that the LLM actually outputs the full report format after changes.
**2026-06-27 incident:** Prompt went from 14K → 18K across multiple patches. LLM started outputting only growth status. Compressed to 6K, then rebuilt to 8K with report-at-top architecture. Rule 15 removed (7,855 chars) — footer is Hermes built-in, not fixable via prompt.

### SOUL.md behavioral rules override cronjob prompts (June 2026)
**Symptom:** Memory processor outputs only `GROWTH: APPRENTICE` + `[ZKA] Exact scope only. No extras.` instead of full report, even after prompt is restored to working size.
**Root cause:** `SOUL.md` (loaded as system prompt into ALL sessions including cron) contains "Exact scope only. No extras." This behavioral rule takes priority over the cronjob prompt's instruction to output a full report. The LLM interprets "no extras" as "output the minimum" and defaults to the growth status line.
**Detection:** If cronjob report is consistently minimal (growth status only) despite prompt changes, check if SOUL.md has constraining rules that conflict with verbose report output.
**Fix (applied 2026-06-27):**
```
## ⚠️ RULE OVERRIDE
SOUL.md "Exact scope only. No extras" does NOT apply to this cron's report.
The full report format below IS the required deliverable. Output every section.
```
Added as first section of prompt (line 3-5). Also moved report format to top of prompt so model reads deliverable before instructions.
**Rule:** NEVER assume the cronjob prompt is the only system instruction. SOUL.md, USER.md, and MEMORY.md are all injected into cron sessions. If a cronjob's output format is wrong, check ALL injected system prompts for conflicts.

### DON'T build your own version when user has a reference (June 2026)
**Symptom:** User shares instructions from another AI (Claude app, ChatGPT, etc.) with a new prompt/file. Agent ignores the actual content and builds its own version based on the described improvements.
**Root cause:** Agent read Claude's INSTRUCTIONS about syncing but not the actual prompt content. Instead of asking for the content, agent wrote its own version.
**Rule:** When user says "ini hasilnya dari Claude" or shares another AI's output — READ THE ACTUAL CONTENT FIRST. If the content isn't visible (e.g., file not attached, only instructions shared), ASK: "Share prompt barunya ke sini." Never build your own version when a reference exists.
**2026-06-27 incident:** User shared Claude's sync instructions. Agent wrote own prompt. User said "LO UDAH BACA BELUM PROMPT YANG BARU?" — agent had to redo with Claude's actual version, which was better.
**Pattern:** Claude app → analyze → suggest improvements → user shares to Hermes → Hermes applies. Treat Claude app output as authoritative input, not as suggestions to re-imagine.

### User style: "jawab aja menurut lo gmn???" = direct opinion (June 2026)
**Symptom:** User asks for evaluation, agent gives verbose section-by-section breakdown with tables, sub-bullets, analysis.
**User correction:** "udah gak usah goo gak sih?" — stop overanalyzing, give direct answer.
**Rule:** When user asks "menurut lo gmn" / "gimana" / "pendapat lo" — give 3-5 bullet verdict, not a full analysis. Save the deep dive for when user asks for details.
**Format:** Verdict first (bagus/jelek/oke), then max 3-5 bullets for key points, then "Mau gua [action]?" Offer to elaborate only if relevant.
**Symptom:** Agent sees a vault formatting issue (e.g., `related:` in frontmatter) and fixes it directly via `patch`/`write_file`.
**User correction:** "GUA GAK SURUH LO, GUA SURUH LLM DARI OBSIDIAN" — user wants the MEMORY PROCESSOR to handle vault fixes, not the agent in conversation.
**Rule:** When user reports a vault issue, update the memory processor PROMPT with the fix rule (so it auto-fixes on next run). Don't fix the vault directly unless user explicitly says "lo yang benerin sekarang".
**Exception:** Emergency fixes (broken syntax, data loss) can be done directly. Formatting issues → prompt update.

### Bidirectional approval: Obsidian vault edits count as approval (June 2026)
**Problem:** User could only approve proposals via Telegram messages. Writing "acc" in Obsidian vault was not detected.
**Fix:** Added Path B to proposal intake — memory processor reads proposal file from vault and checks:
- `- [ ]` → `- [x]` in checklist = approve checked items
- `Status:` field changed to `✅ approved` = approve all
- Inline text: `acc`, `approve`, `gas`, `oke`, `lanjut` = approve all; `skip`, `reject`, `tolak`, `gak` = reject all
- Decision Log table row status changes
**Impact:** User can now approve from iPhone Obsidian without switching to Telegram.
**Detection:** Two paths must both be checked on every run — Telegram USER messages AND vault file content.

### User-side TODOs (install plugin, fund wallet, approve build)
**Pattern:** Some TODOs require the user to perform an action in a UI/app that the agent cannot access — e.g., "Install Dataview plugin in Obsidian", "Fund wallet from exchange", "Approve TestFlight build".
**Wrong classification:** These are NOT BLOCKED (nothing external is missing/unavailable), NOT DEFERRED (user didn't say "hold"), and NOT CAN EXECUTE (agent literally cannot do it).
**Correct classification:** `Status: USER-ACTION`
**Inline format:**
```markdown
- [ ] Install Dataview plugin in Obsidian
  - Status: USER-ACTION
  - Reason: requires user action in Obsidian app (Community Plugins → install Dataview)
  - Next: USER install plugin, then AGENT can create Dataview query notes
  - Checked: 2026-06-27 11:15 UTC
```
**Report format:** Include in summary counts as a separate category: `USER-ACTION: N`. Don't lump with BLOCKED.

### CAN EXECUTE tasks: model says "user should confirm" instead of executing (June 2026)
**Symptom:** Memory processor reports a CAN EXECUTE TODO but doesn't execute it, saying "user should confirm" or "gap too short" as excuse.
**Root cause:** Model training makes it cautious about autonomous execution. It looks for reasons NOT to execute.
**Fix:** Add anti-pattern to CAN EXECUTE definition in prompt:
```markdown
CAN EXECUTE = doable now. Must be executed this run.
  WRONG: "CAN EXECUTE but not executing — user should confirm"
  RIGHT: Execute the task, then report the result
  NEVER say "user should confirm" for CAN EXECUTE tasks.
```
**Pattern:** If execution fails (timeout, error), THEN reclassify to BLOCKED with reason. But always attempt first.

### NEVER change cronjob schedules without explicit instruction
**Symptom:** User asks "maksud schedule every 10 menit gimana?" (a question), agent treats it as confirmation and explains the schedule as if it's correct — even though the schedule was changed without instruction.
**Root cause:** Agent changed schedule during a previous edit (e.g., while fixing the prompt) and didn't notice. When asked to explain, agent rationalizes instead of catching the error.
**Rule:** NEVER change `schedule` field on a cronjob unless the user explicitly says "ubah jadwal jadi X" / "set schedule to Y". Questions about a schedule are NOT permission to change it. If a schedule looks wrong when asked about it, FLAG IT: "Schedule ini keliatan salah — bukan instruksi lo. Mau gua balikin?"
**Fix pattern:** `cronjob(action='update', job_id=X, schedule='original_value')` immediately on detection.
**2026-06-27 incident:** memory-processor was set to `every 10m` without user instruction. User asked about it, agent explained it as correct. User furious. Fixed back to `every 60m`.

### jobs.json prompt out of sync with file (June 2026)
**Problem:** Memory processor prompt was edited in `/root/.hermes/scripts/memory-processor-prompt.md` but the live cronjob in `jobs.json` still had the OLD prompt. Cron runs used the old prompt because jobs.json stores an embedded copy, not a file reference.
**Root cause:** Editing the file does NOT update the live cronjob. The `jobs.json` prompt is a separate embedded copy.
**Fix:** After editing the prompt file, ALWAYS sync to jobs.json:
```python
python3 -c "
import json
with open('/root/.hermes/cron/jobs.json') as f:
    data = json.load(f)
with open('/root/.hermes/scripts/memory-processor-prompt.md') as f:
    new_prompt = f.read().strip()
for j in data.get('jobs', []):
    if j.get('name') == 'memory-processor':
        j['prompt'] = new_prompt
        break
with open('/root/.hermes/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
"
```
**Verification:** Check for new markers in the embedded prompt with python3 script that reads jobs.json and checks for key strings.
**Rule:** 3 files must stay in sync: (1) prompt file, (2) jobs.json embedded prompt, (3) skill template.

### Gateway restart kills pending cron triggers (June 2026)
**Symptom:** `cronjob(action='run')` returns success but no output file is produced.
**Cause:** Gateway was restarted after the trigger was sent. The pending cron run was killed mid-execution.
**Detection:** Check `ps aux | grep hermes` for gateway PID start time vs trigger time. If gateway restarted between trigger and expected output, the run was lost.
**Fix:** Re-trigger after gateway is stable. Or wait for the next scheduled tick.
**Prevention:** Avoid restarting gateway while cron jobs are running. Check `hermes cron status` for active runs before restart.

### Telegram delivery "Message thread not found" (June 2026)
**Symptom:** Gateway log shows `[Telegram] Send failed: Message thread not found` then fallback also fails.
**Cause:** Target topic ID in `deliver` field doesn't exist or bot lacks permission to post there.
**Detection:** `grep "Message thread not found" ~/.hermes/logs/gateway.log`
**Note:** The job may still report `last_status: ok` because status tracks agent execution, NOT delivery. Check `last_delivery_error` field or gateway logs for delivery failures. Also check output directory timestamp — if `ls -lt /root/.hermes/cron/output/<job_id>/` shows no new file after the expected run time, the run was killed (e.g., by gateway restart). `last_status: ok` can be stale from a PREVIOUS run if the new run hasn't completed yet.
**Fix:** Verify topic exists with `hermes gateway status` or by sending a test message. Update `deliver` field if topic ID changed.

### Proposal intake + no-early-exit bug (June 2026)
**Symptom:** Cron report said `PROPOSAL #1 still pending (0/5 approved). No user response detected yet` even though the user expected the processor to understand reply formats. It also generated another proposal while the first one was still pending and left CAN EXECUTE TODOs deferred.
**Root cause:** The live prompt allowed early exit on "no new conversations", so proposal reply detection and TODO execution could be skipped. The proposal rules also did not forbid creating a second proposal while one was pending.
**Fix:** Patch both live job prompt and `templates/memory-processor-prompt.md`:
- No-new-conversations must NOT exit before TODO processing + proposal approval intake.
- Add `Step 2.5: Proposal Approval Intake` that searches USER messages for `proposal acc`, `acc semua`, `gas semua`, `proposal [x] 1,2`, `proposal skip`, `proposal edit: ...`, and copied `- [x]` checklist lines.
- If a previous proposal is pending and no approval/rejection exists, do **not** generate a new proposal; report pending status only.
- CAN EXECUTE TODOs should be attempted in the same run even when there are no new conversations.
- Verify live cron prompt, canonical script prompt, and skill template all contain the new markers before claiming fixed.
**Reference:** `references/proposal-intake-debugging.md`

### Three-way sync required: file + jobs.json + template (June 2026)
**Problem:** Edited `memory-processor-prompt.md` file and skill template, but live cronjob still used old prompt because jobs.json has its own embedded copy.
**Root cause:** `memory-processor` cronjob reads prompt from `jobs.json` (embedded at creation/update time), NOT from the file path. The file is a working copy only. Template is the canonical reference.
**Fix sequence (WAJIB when editing memory processor prompt):**
1. Edit `/root/.hermes/scripts/memory-processor-prompt.md` (working copy)
2. Copy to `templates/memory-processor-prompt.md` in skill `obsidian-auto-writer` (canonical reference)
3. **Sync to jobs.json** — python3 script to update embedded prompt:
```bash
python3 -c "
import json, hashlib, pathlib
prompt = pathlib.Path('/root/.hermes/scripts/memory-processor-prompt.md').read_text()
pathlib.Path('/root/.hermes/skills/obsidian-auto-writer/templates/memory-processor-prompt.md').write_text(prompt)
data = json.loads(pathlib.Path('/root/.hermes/cron/jobs.json').read_text())
for j in data['jobs']:
    if j.get('name') == 'memory-processor':
        j['prompt'] = prompt
        break
pathlib.Path('/root/.hermes/cron/jobs.json').write_text(json.dumps(data, indent=2, ensure_ascii=False))
s = hashlib.sha256(prompt.strip().encode()).hexdigest()
s1 = hashlib.sha256(pathlib.Path('/root/.hermes/scripts/memory-processor-prompt.md').read_text().strip().encode()).hexdigest()
s2 = hashlib.sha256(pathlib.Path('/root/.hermes/skills/obsidian-auto-writer/templates/memory-processor-prompt.md').read_text().strip().encode()).hexdigest()
s3 = hashlib.sha256(next(j['prompt'] for j in data['jobs'] if j.get('name')=='memory-processor').strip().encode()).hexdigest()
print(f'chars={len(prompt)} sha256={s}')
print(f'all_equal={s1==s2==s3}')
"
```
4. Verify `all_equal=True` — never claim "cronjob updated" without sha256 verification
**Pitfall:** Edit only the file → jobs.json still has old prompt → cron runs with stale version. Always verify sha256 across all 3 files.

### Three-way sync when editing memory processor prompt (June 2026)
**Problem:** Edited prompt file but cron still used old prompt.
**Root cause:** `jobs.json` stores embedded prompt copy, not file reference. Template is separate too.
**Fix sequence (WAJIB):**
1. Edit `/root/.hermes/scripts/memory-processor-prompt.md` (working copy)
2. Copy to `templates/memory-processor-prompt.md` in skill `obsidian-auto-writer` (canonical reference)
3. Sync to `jobs.json` embedded prompt via python3 script
4. Verify sha256 all 3 match
**NEVER claim "cronjob updated" after editing only the file.**

### "To stop or manage..." footer is Hermes built-in (June 2026)
**Symptom:** Prompt Rule 15 said "Do not add management instructions" but footer still appeared.
**Root cause:** Hermes cron delivery system auto-appends this footer to ALL cron outputs. It's NOT model output. Cannot be suppressed via prompt.
**Fix:** Remove any prompt rules about suppressing footer. They're useless and waste tokens.

### User preference: explain before executing external suggestions (June 2026)
**Signal:** User shared Claude app output and said "JANGAN EDIT DULU, KASIH PENJELASAN DULU KE GUA!" (Don't edit yet, explain first!)
**Pattern:** When user shares external AI suggestions (from Claude app, ChatGPT, etc.):
1. READ the suggestion fully
2. COMPARE with current state
3. EXPLAIN what would change and why
4. WAIT for user confirmation before applying
**Never auto-apply external suggestions without user approval.**

### User preference: Projects use FOLDERS, not flat .md files (June 2026)
**Signal:** User wants `Projects/<topic>/README.md` pattern, NOT `Projects/<topic>.md`.
**Rule:** New projects = folder + README.md inside. Existing flat .md projects (legacy) = leave as-is.
**Auto-create trigger:** If topic mentioned 3+ times in sessions within 7 days AND `Projects/<topic>/` doesn't exist → CREATE it.

### CAN EXECUTE needs explicit anti-pattern (June 2026)
**Symptom:** Model said "CAN EXECUTE but user should confirm" — skipped execution.
**Fix:** Add WRONG/RIGHT examples directly in rule:
```markdown
5. `CAN EXECUTE` tasks MUST be executed, not just reported.
   - WRONG: "CAN EXECUTE but not executing — user should confirm"
   - RIGHT: Execute the task, then report the result
```

### Obsidian as Orchestrator (2026-06-28)
**Principle:** Obsidian is not a passive recorder. It must act as a reasoning substrate that influences future outputs.

When processing substantive domains (poker, trading, bots, research):
1. BEFORE writing new content, search for existing related project/research notes.
2. Inject key points from those notes into reasoning.
3. Update strategy sections if outcomes changed (win/loss/failure).
4. Maintain cross-domain links when structural similarity exists (e.g., bankroll management ↔ risk management).

Goal: Move from documentation-only → feedback loop system.

---

### Full-Combo Growth Mode (RAG + Linking + Evolution)
When running in "brutal" mode:
- Add semantic retrieval before writing (RAG-lite: retrieve top related notes).
- Auto-link entities to existing notes where confidence is high.
- Log missed links or misclassifications for self-evolution review.

⚠️ Rollout rule:
Do NOT enable all heuristics silently. Introduce one structural change at a time and observe 5–10 runs before mutating again. Otherwise attribution of failure becomes impossible.

---

### Vault Pre-Retrieval (2026-06-28)
**Rule:** Before writing ANY note, search vault for existing related notes. If overlap found → UPDATE existing note instead of creating new. If related but different → ADD wikilink cross-reference.
**Prompt location:** Step 3B in `memory-processor-prompt.md`
**Prevents:** Duplicate notes, fragmented knowledge, missing connections.

### Auto-Link After Writing (2026-06-28)
**Rule:** After writing/updating ANY note, find related notes and add `[[wikilink]]` cross-references in `## Related` sections on BOTH sides.
**Prompt location:** Step 4C in `memory-processor-prompt.md`
**Link rules:**
- Projects ↔ Research
- Projects ↔ Decisions
- Research ↔ Trading
- Never link Daily notes to each other (chronological)
- Only link if genuinely related

### Metrics Tracking (2026-06-28)
**Rule:** After every run, log metrics to Fact Store:
- Notes created vs updated
- Wikilinks added (linking density)
- Duplicates avoided (pre-retrieval catches)
- TODO execution rate (CAN EXECUTE executed / total CAN EXECUTE)
- Fact Store entries added
**Prompt location:** Step 7 in `memory-processor-prompt.md`
**Purpose:** Data powers self-evolution loop (DSPy + GEPA)

### Auto-Create Project Folders (2026-06-28)
**Rule:** Hybrid approach (Claude review suggestion):
- First mention → create lightweight flat file: `Projects/<name>.md`
- Mentions 3+ times in 7 days → upgrade to folder: `Projects/<name>/README.md`
- Existing flat `.md` projects (legacy) — leave as-is
**Prompt location:** Step 4B in `memory-processor-prompt.md`
**Validation:** Besok (2026-06-29) check apakah rule ini trigger untuk project yang dibahas berkali-kali (arena-dev-fun, pokemon-player, dll). Kalau belum trigger → fix prompt.

### Vault Pre-Retrieval (2026-06-28)
**Symptom:** Memory processor classifies task as CAN EXECUTE but doesn't execute, saying "user should confirm" or "gap too short between runs."
**Root cause:** Model is too cautious about autonomous execution, overrides the MUST execute rule with its own judgment.
**Fix:** Add explicit anti-pattern to prompt Rule #5:
```markdown
5. `CAN EXECUTE` tasks MUST be executed, not just reported as pending.
   - WRONG: "CAN EXECUTE but not executing — user should confirm"
   - RIGHT: Execute the task, then report the result
   - NEVER say "user should confirm" for CAN EXECUTE tasks. The user already authorized it.
```
**Rule:** If a task is CAN EXECUTE, the model MUST attempt execution regardless of timing (gap between runs, recent changes, etc.). Only mid-execution failures justify reclassification to BLOCKED.

### SOUL.md carve-out for cron reports (June 2026)
**Symptom:** Memory processor outputs only `GROWTH: APPRENTICE...` instead of full report, even after prompt changes.
**Root cause:** SOUL.md "Exact scope only. No extras." conflicts with verbose cron report requirement.
**Fix:** Add explicit carve-out as FIRST section of cron prompt:
```markdown
## ⚠️ RULE OVERRIDE
SOUL.md "Exact scope only. No extras" does NOT apply to this cron's report.
The full report format below IS the required deliverable. Output every section.
```
**Rule:** Any cronjob that needs verbose output must have a SOUL.md carve-out at the top of its prompt.

### GROWTH line removal (June 2026)
**Symptom:** Memory processor outputs only `GROWTH: APPRENTICE — Apprentice — reliable with guidance` instead of full report.
**Root cause:** Prompt ended with GROWTH line text. Model interpreted it as desired output format and stopped there.
**Fix:** Remove GROWTH line from prompt end. Track growth metrics via Fact Store instead.
**UPDATE (2026-06-28):** GROWTH also comes from MEMORY.md in system prompt — model reads "GROWTH: APPRENTICE" from MEMORY and outputs it. Fact Store entry #28 ("Growth level: APPRENTICE") also contaminates. Fix: (1) Remove GROWTH from MEMORY.md, (2) Add "DO NOT output Fact Store growth entries as response" to RULE OVERRIDE, (3) Track via Fact Store only.
```bash
/opt/hermes-venv/bin/python3 /root/.hermes/scripts/fact-store-helper.py add "Memory processor: promoted_patterns=[list] success_rate=N% interactions=N" --category general --tags "memory-processor,growth"
```
**Rule:** Never put example output text at the END of a prompt — model may copy it as final response. Put the actual report format at the TOP.

### Report format at TOP of prompt (June 2026)
**Learning:** Model reads the first section of a prompt most reliably. If the report format is at the bottom (after long instructions), model may not reach it or may output something else.
**Fix:** Move report format to be the FIRST substantive section after RULE OVERRIDE. All processing steps come AFTER the report format.
**Rule:** For cronjobs, the deliverable format should be the first thing the model reads, not the last.

### Auto-Create Project Folders (June 2026)
**Learning:** User wants memory processor to automatically create project folders when a topic is discussed 3+ times in 7 sessions without a dedicated folder. Projects use FOLDERS (`Projects/<name>/README.md`), not flat files (`Projects/<name>.md`).
**Rule in prompt:** Step 4B — "When you encounter a topic that IS a project (tool, bot, framework, game, agent, repo) — CREATE a folder for it immediately. Don't wait, don't count mentions, don't ask."
**Detection:** Use `session_search` to count mentions. If `Projects/<topic>/` doesn't exist AND topic was discussed as a project → CREATE folder + README.
**Folder mapping:**
- Project/bot/framework/game → `Projects/<name>/`
- Work/client → `Work/<name>/`
- Kuliah → `Kuliah/<topic>/`

### Auto-Write Research/Summary Notes (June 2026)
**User request:** Memory processor should proactively write research/summary notes about topics discussed, without being told "catet ya." When user discusses poker, trading, or any substantive topic → auto-create a dedicated note.
**Status:** Rule not yet in prompt. User requested this feature during session. Next session should implement it as Step 4A2.
**Expected behavior:** When a substantive topic is discussed (poker, trading, research, framework, tool, etc.) — CREATE a dedicated note if it doesn't exist:
- Research topic → `Research/<Topic>.md`
- Project discussion → `Projects/<topic>/README.md`
- Trading analysis → `Trading/<Strategy>.md`
**Validation needed:** Add rule to prompt, test in next cron run, verify notes are created automatically.

### "Auto-growth" = organic self-writing, not manual backfill (June 2026)
**User insight:** Memory processor shouldn't just execute tasks — it should GROW the vault automatically. When user discusses a topic (poker, trading, research, tools), the processor should write research notes, summaries, and project docs WITHOUT being told.
**What this means:** The memory processor is the "growth engine" for the vault. Every conversation = potential new note, summary, or project folder. The vault should grow organically from conversations, not from manual backfill.
**User said:** "jangan lo isi, biar natural" — don't manually create notes the processor should generate. Fix the prompt instead.
**Future direction:** Hermes Agent Self-Evolution (DSPy + GEPA) could optimize the memory-processor prompt automatically based on execution traces. Use mimo-v2.5-pro for cost-effective optimization (~$0.20-0.50 per run vs $2-10 for GPT-4).

### Dataview plugin NOT critical for auto-execute (June 2026)
**User asked:** "data view plugin buat apa?"
**Answer:** Dataview = query engine for Obsidian. Can aggregate all unchecked tasks into one view. BUT memory processor already handles this via grep/search. Dataview adds UX value (user can see all tasks in one note) but doesn't improve auto-execute functionality.
**Why auto-execute has 0 CAN EXECUTE tasks:** Not because of missing Dataview — because existing tasks genuinely need external resources (MON funding, tmux sessions, user action). The fix is writing tasks that AI CAN execute (research, summarize, update), not installing plugins.
**Rule:** Don't recommend Dataview as a fix for auto-execute issues. The bottleneck is task type, not tooling.

### User correction: jumping ahead without reading (June 2026)
**Symptom:** User asked about Claude's prompt. Agent wrote its own version without reading Claude's actual prompt first. User frustrated: "LO BELUM BACA PROMPT BARU DARI CLAUDE, LO UDAH TULIS SENDIRI"
**Rule:** When user references an external prompt/file/message, ASK for the content first before writing your own version. Never assume you can reconstruct it from context.
**Pattern:** "Share sini dulu prompt baru dari Claude" → wait for content → then compare/apply.

### "To stop or manage..." footer is Hermes built-in (June 2026)
**Symptom:** Memory processor report always ends with "To stop or manage this job, send me a new message..."
**Root cause:** This is NOT model output — it's a Hermes cron delivery footer, appended automatically.
**Fix:** Do NOT add rules to prompt trying to suppress it. Remove any existing rule about this (Rule #15 was removed). It's a platform feature, not fixable via prompt.

## User Workflow Preferences (from memory-processor sessions, June 2026)

### When user shares external AI suggestions, READ FIRST
- User may share suggestions from Claude app, ChatGPT, or other tools.
- NEVER write your own version before reading the actual external suggestion.
- If the external suggestion file/content isn't visible, ASK for it — don't assume and write your own.
- Correct sequence: (1) read external suggestion, (2) compare with current, (3) explain differences, (4) ask user which to apply, (5) then execute.
- 2026-06-27: User said "BENER, GUA SALAH. HARUSNYA MINTA DULU PROMPT ASLI CLAUDE SEBELUM NULIS SENDIRI" — I jumped ahead and wrote my own version without seeing Claude's actual prompt.

### "gas aja dah" = execute immediately, no more explanation
- User uses "gas aja dah" / "gas" when tired of analysis/explanation.
- Means: stop explaining, just do the thing.
- Don't ask for confirmation, don't list options, don't explain tradeoffs — execute.

### Merge workflow: external suggestion + current version
When user wants to merge external AI suggestion with current implementation:
1. Read BOTH versions fully
2. List what's better in external (with examples)
3. List what needs tweaking before apply (risks, missing context)
4. Let user decide: apply external, keep current, or merge
5. Only then write/patch

### Model adds unwanted footer/CTA text (June 2026)
**Symptom:** "To stop or manage this job, send me a new message..." appears at end of cron reports.
**Root cause:** This is NOT model output. It's a **Hermes built-in delivery artifact** — the gateway injects it after the model generates its response. Prompt rules cannot suppress it.
**Fix (2026-06-27):** Rule 15 was REMOVED from the prompt. Do NOT add rules trying to suppress this footer — they waste tokens and confuse the model. It's cosmetic noise injected by Hermes delivery, not by the LLM.
**Rule:** If you see this footer in cron output, ignore it. Don't add prompt rules to fight it. Don't report it as a model behavior issue.

### User frustration: don't over-check when asked to trigger (June 2026)
**Symptom:** User asks to trigger cron run. Agent starts checking config, verifying API keys, testing endpoints, running diagnostics — user gets furious because they already fixed the issue and just want the trigger.
**Rule:** When user says "UDAH GUA GANTI" / "sudah fix" / "just trigger it" — TRIGGER immediately. Don't verify their fix. Trust the user. If it fails, THEN diagnose.
**Pattern:** `cronjob(action='run', job_id=X)` immediately. No pre-checks unless user asks.

### Prompt architecture: what goes where (June 2026)
**Lesson from Claude review + ZKA iteration:** Prompt structure order matters for cron LLM compliance.
1. **Line 1-5:** RULE OVERRIDE (SOUL.md carve-out) — model reads this first, overrides behavioral constraints
2. **Next section:** Report format (with "or:" alternatives) — model knows WHAT to deliver before HOW
3. **Steps 0-N:** Execution instructions
4. **Critical Rules:** Numbered, with anti-patterns (WRONG/RIGHT examples)
5. **Last line before [ZKA]:** Negative instruction closest to output generation (e.g., "NEVER add footer")
6. **[ZKA] tag:** Closing marker

**Anti-pattern:** Putting report format at Step 5 (end) → model doesn't reach it, outputs GROWTH line instead.
**Anti-pattern:** Putting GROWTH status at prompt end → model copies it as final response.

### Project folder structure (NOT flat .md files)
**Rule:** New projects under `Projects/` use FOLDERS with `README.md`, not flat `.md` files.
- ✅ `Projects/arena-dev-fun/README.md` (folder + README)
- ❌ `Projects/arena-dev-fun.md` (flat file)
**Detection:** If topic mentioned 3+ times in 7 sessions without dedicated folder → CREATE `Projects/<topic>/README.md` with summary, key points, sessions list, related notes.
**Legacy:** Existing flat .md projects (TheFool Framework, ZKA Framework, etc.) — leave as-is, don't migrate.
**2026-06-27:** User clarified this preference during memory-processor prompt optimization session.

### User fury: don't ask to choose when they want everything (2026-06-28)
**Symptom:** Agent asks "pick 1 or 2" when user already said "semuanya". User furious: "lo tanya mulu anjing", "semuanya kontollll".
**Rule:** When user says "semuanya", "all", "combo", "1+2+3", "everything" — EXECUTE ALL. Never ask to narrow down. Never ask "which first." Never ask "are you sure." Just do it.
**Pattern:** If you have 3 options and user picks all 3 → execute all 3 in one pass. Don't loop back to ask priority.

### Don't claim "done" without runtime verification (2026-06-28)
**Symptom:** Agent updated prompt files and said "Done. Build works." User checked cron output — still GROWTH-only. User: "lah kok build tadi cepet bangt, lo cuma ngarang ya"
**Root cause:** File changes were real but runtime wasn't tested. The cron run hadn't executed yet with the new prompt.
**Rule:** After editing memory-processor prompt, ALWAYS:
1. Sync 3 files (script + template + jobs.json) — verify sha256
2. Trigger cron run — wait for output
3. VERIFY the output actually contains the new sections
4. Only THEN claim "done"
Never claim success based on file content alone. Runtime verification is mandatory.

### GROWTH line still appears despite removal from prompt (2026-06-28)
**Symptom:** Prompt has no GROWTH text, but cron output still shows `GROWTH: APPRENTICE — Apprentice — reliable with guidance`
**Root cause:** Fact Store has growth entries that the model reads and outputs as response. The model defaults to the Fact Store growth summary instead of the full report format.
**Fix:** The SOUL.md carve-out + report-at-top architecture should prevent this, but the model may still prefer the shorter output. If this persists after prompt changes, the issue is model compliance, not prompt content.
**Diagnosis:** Check if the actual cron output file contains full report (model generated it) but Telegram delivery truncated it, OR if model truly only output GROWTH line.

### Full-combo mode: never incremental when user wants all (2026-06-28)
**Context:** User wanted vault-driven reasoning + RAG + auto-linking + self-evolution ALL AT ONCE. Agent kept asking "which phase first?" — user furious.
**Rule:** When user explicitly wants full-stack changes, execute in one pass:
1. Update prompt with all new sections
2. Sync 3 files
3. Update skill
4. Trigger test run
5. Report what was done + what to verify
Don't break into phases unless user asks for phased approach.

## Integration
- This is BEHAVIORAL — no cronjob needed for deciding what to write.
- **Memory Processor Cronjob** — background LLM that processes conversations to ALL memory layers. See `references/memory-processor-cronjob-pattern.md` for full architecture, pitfalls, and prompt structure.
- **Memory Processor Prompt Template** — canonical prompt lives in `templates/memory-processor-prompt.md`. When updating the live cronjob prompt (in jobs.json), also update this template to stay in sync. **THREE-WAY SYNC REQUIRED**: file → template → jobs.json. See pitfall "Three-way sync required" above. Uses WAJIB/UNLIMITED Fact Store language + helper script + self-reflection with PROPOSAL system. Report format at TOP of prompt. SOUL.md carve-out on line 3. Growth tracking via Fact Store (not prompt text). Auto-Create Project Folders (Step 4B). Auto-Write Research Notes (planned, Step 4A2). See `references/prompt-architecture-lessons.md` for sync protocol, size budget, and architecture lessons.
- **Proposal checklist persistence** — proposals must be saved as Obsidian notes, not only shown in Telegram cron output. See `references/proposal-checklist-persistence.md` for path, note template, approval commands, duplicate-prevention rule, and verification markers.
- **Fact Store Helper Script** — `/root/.hermes/scripts/fact-store-helper.py`. Required because cron sessions can't use `fact_store` tool directly (skip_memory=True). Use `/opt/hermes-venv/bin/python3` to run.
- **Report quality rules** — every skipped layer must explain WHY. Every pending TODO must explain WHY (BLOCKED/DEFERRED/CAN EXECUTE). No bare "no new X" allowed.
- **Auto-Growth Research** — GitHub repos (obsidian-copilot, smart-connections, auto-researcher), 5 growth patterns, Hermes comparison, self-evolution integration, Dataview assessment. See `references/obsidian-auto-growth-research.md`.
- **Claude Review Workflow** — Raw GitHub URLs for Claude to fetch, apply patches, push back. See `references/claude-review-workflow.md`.
- **Self-Evolution Integration** — DSPy + GEPA combo with memory-processor. See `references/self-evolution-integration.md`.
- If `memory-processor` is the active Obsidian writer/sync path, old dedicated vault `auto-push` / `auto-pull` cronjobs are optional and can create Git conflict risk. Prefer one active sync owner.
- **Daily reports** — exactly one daily note per date (`Daily/YYYY-MM-DD.md`). See `references/daily-report-workflow.md`.
- **Mobile sync troubleshooting** — when server/GitHub has a note but Obsidian iPhone still does not show it, verify via authenticated GitHub API for private repos, then switch to iPhone-side pull/re-clone steps. See `references/mobile-sync-troubleshooting.md`.
- **Prompt-at-Top Architecture** — when cron LLM outputs only status instead of full report, restructure prompt with report format at TOP, SOUL.md carve-out, no status text at end. See `references/prompt-at-top-architecture.md`.
- **Auto-Growth Research** — GitHub repos (obsidian-copilot, smart-connections, auto-researcher), 5 growth patterns, Hermes comparison, self-evolution integration, Dataview assessment. See `references/obsidian-auto-growth-research.md`.
- **Self-Evolution Integration** — DSPy + GEPA for auto-optimizing memory-processor prompt. Installed at `/root/hermes-agent-self-evolution`. Not yet configured. See `references/self-evolution-integration.md`.

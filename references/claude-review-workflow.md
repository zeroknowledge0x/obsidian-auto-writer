# Claude Review Workflow for Obsidian Auto-Writer

## How to Share with Claude App
1. Push skill to GitHub: `cd /root/.hermes/skills/obsidian-auto-writer && git add -A && git commit -m "update" && git push origin master`
2. Generate raw URLs with cache buster:
   - `https://raw.githubusercontent.com/zeroknowledge0x/obsidian-auto-writer/master/SKILL.md?t=TIMESTAMP`
   - `https://raw.githubusercontent.com/zeroknowledge0x/obsidian-auto-writer/master/templates/memory-processor-prompt.md?t=TIMESTAMP`
3. Share URLs to Claude app
4. Claude reviews → returns patches → apply to files → push → share new URLs

## Cache Busting
Claude's `web_fetch` caches aggressively. Always append `?t=YYYYMMDDHHMM` to raw URLs.

## What Claude Should Review
1. **SKILL.md** — structure, pitfalls, completeness
2. **memory-processor-prompt.md** — prompt architecture, rules, report format
3. **references/** — session-specific details

## GitHub Push Pattern
```bash
cd /root/.hermes/skills/obsidian-auto-writer
git add -A && git commit -m "description" && git push origin master
```
**Pitfall:** Can't push to ZKA-Labs org from zeroknowledge0x. Use user account directly.

## Key Learnings from Claude Reviews (2026-06-28)
1. Report format at TOP of prompt (prevents truncation)
2. SOUL.md RULE OVERRIDE (carve-out for cron verbosity)
3. [SILENT] response (no spam when nothing to process)
4. Metrics format → JSON (for GEPA self-evolution parsing)
5. Grep standardization (use `grep -rl` consistently)
6. Placeholder variables need explicit substitution instructions
7. Hybrid project creation (flat .md first, folder on 3+ mentions)
8. GROWTH contamination from Fact Store + MEMORY.md (not just prompt)

# Claude Review Workflow

## Pattern
User uses Claude app as external reviewer for Hermes skills/prompts.

## Flow
1. Hermes builds skill/prompt
2. User shares raw GitHub URLs with Claude app
3. Claude reviews → gives feedback + questions
4. User shares Claude's response with Hermes
5. Hermes applies fixes based on Claude's review
6. Push updated files to GitHub
7. Repeat if needed

## Rules
- **READ Claude's actual review FIRST** — don't write your own version
- Treat Claude's suggestions as authoritative input, not just suggestions
- Answer Claude's questions directly (e.g., "cron invoke via prompt or skill?")
- Apply fixes in priority order Claude specifies
- Push to GitHub after each fix batch so Claude can re-review

## Raw URL format
```
https://raw.githubusercontent.com/zeroknowledge0x/<repo>/master/<path>
```

## Session example (2026-06-28)
Claude reviewed `obsidian-auto-writer` skill (64K SKILL.md + memory-processor-prompt.md):
- Confirmed: report format at top, SOUL.md carve-out, [SILENT] response, fact-store-helper
- Flagged: SKILL.md too large, grep placeholder too abstract, project folder over-creation, metrics format not JSON
- Asked: cron invoke method, vault-timestamp-update.py timing, growth level
- Hermes answered + applied 3 fixes, pushed to GitHub

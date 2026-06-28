# Claude Review Workflow

## Pattern
User sends skill/prompt to Claude app for review → Claude returns feedback → Hermes applies fixes → push to GitHub → Claude re-fetches.

## How to Share Files with Claude
1. Push skill to GitHub (public repo under user account)
2. Generate raw URLs: `https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>`
3. Claude fetches via `web_fetch` tool
4. Claude returns review + specific patches

## Key Learnings from Claude Reviews (2026-06-28)
1. **Report format at TOP** — prevents truncation by lightweight models
2. **SOUL.md RULE OVERRIDE** — elegant carve-out for cron verbosity
3. **[SILENT] response** — efficient, no Telegram spam when nothing to process
4. **Metrics → JSON** — for GEPA self-evolution parsing (not free-text)
5. **Grep standardization** — use `grep -rl` consistently, not `find | xargs grep`
6. **Placeholder variables** — need explicit substitution instructions for lightweight models
7. **Hybrid project creation** — flat `.md` first, upgrade to folder on 3+ mentions
8. **GROWTH contamination** — comes from MEMORY.md AND Fact Store, not just prompt
9. **SKILL.md too large (64K)** — split: SKILL.md = triggers/rules only (~5-8K), cron uses prompt directly

## GitHub Push Pattern
```bash
cd /root/.hermes/skills/<name>
git init && git add -A && git commit -m "initial"
gh repo create <name> --public --source . --push
```
**Pitfall:** Can't push to ZKA-Labs org from zeroknowledge0x account. Use user account directly.

## Cache Busting
If Claude can't see updated files (web_fetch cache):
- Add `?t=<timestamp>` to raw URL
- Or ask Claude to re-fetch after 1 minute
- Or push to a different branch name

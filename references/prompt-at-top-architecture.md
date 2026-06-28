# Prompt-at-Top Architecture for Cron Jobs

## Problem
LLM running cron job outputs only a status snippet instead of full report format, even when prompt explicitly defines the report.

## Root Causes (discovered June 2026)
1. **Report format at bottom** — model stops reading before reaching it
2. **SOUL.md "no extras" conflict** — global behavioral rule suppresses verbose output
3. **Status text at prompt end** — model copies last visible text as output (e.g. `GROWTH: APPRENTICE`)
4. **Prompt too long** — >18K chars causes model to truncate processing

## Architecture: Report at TOP

Structure the cron prompt in this order:

```
1. RULE OVERRIDE (SOUL.md carve-out)
2. YOUR FINAL RESPONSE FORMAT (report template)
3. Step 0: Health Check
4. Steps 1-N: Processing instructions
5. Critical Rules
6. [ZKA] tag
```

### Why this works:
- Model reads report format FIRST — it knows the deliverable before reading instructions
- SOUL.md carve-out on line 3-5 prevents "no extras" from suppressing output
- No status text at end that could be copied as output
- Instructions come AFTER the model knows what to produce

## SOUL.md Carve-Out Template

```markdown
## ⚠️ RULE OVERRIDE
SOUL.md "Exact scope only. No extras" does NOT apply to this cron's report.
The full report format below IS the required deliverable. Output every section.
```

Must be the FIRST section of the prompt.

## Anti-Pattern: Status Text at End

WRONG:
```markdown
## Step 6: Self-Reflection
...
GROWTH: APPRENTICE — Apprentice — reliable with guidance
Next: JOURNEYMAN — needs higher success_rate and promoted_patterns.
```

RIGHT:
- Remove growth status from prompt entirely
- Track growth via Fact Store helper script
- Model has no tempting last-line to copy

## CAN EXECUTE Anti-Pattern

To prevent model from skipping CAN EXECUTE tasks:

```markdown
5. `CAN EXECUTE` tasks MUST be executed, not just reported as pending.
   - WRONG: "CAN EXECUTE but not executing — user should confirm"
   - RIGHT: Execute the task, then report the result
   - NEVER say "user should confirm" for CAN EXECUTE tasks. The user already authorized it.
```

Explicit WRONG/RIGHT examples are more effective than just stating the rule.

## Footer Suppression

Models often add CTA footers like "To stop or manage this job...". Add near end:

```markdown
NEVER add footer text like "To stop or manage this job..." to your output. End the report at the PROPOSAL section.
```

Note: This may not fully suppress — some models add it from training. Accept as minor noise if it persists.

## Tested Sizes
- 6K chars: works (compact, references external files)
- 8K chars: works (full instructions inline)
- 18K chars: FAILS (model outputs only growth status)
- Sweet spot: 6-10K chars with report-at-top

## Verification
After any prompt change, run 1 manual test and verify:
1. Full report format delivered (not just GROWTH/status)
2. All sections present
3. No "or:" alternatives used when content exists
4. CAN EXECUTE tasks executed (not skipped)

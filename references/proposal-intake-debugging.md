# Proposal Intake Debugging — Memory Processor

## When to use
Use this when the memory-processor cron report says a proposal is still pending, fails to detect user approval/rejection, repeats proposal blocks, or defers executable TODOs just because there were no new conversations.

## Durable lesson
The processor must not exit early on “no new conversations” until it has completed:
1. TODO processing.
2. Proposal approval intake.
3. Vault-wide pending TODO scan.
4. CAN EXECUTE status checks.

## Required proposal intake behavior
Before generating any new proposal, search recent **USER** messages (not cron outputs) for approval/rejection/edit replies:
- `proposal acc`
- `acc semua`
- `gas semua`
- `proposal [x] 1,2`
- copied checklist lines like `- [x] ...`
- `proposal skip`, `skip semua`, `tolak semua`
- `proposal edit: ...` or `edit: ...`

If a proposal is still pending and no user reply is found, the processor should not generate another proposal. It should report only the pending status and wait.

## Patch checklist
Patch all three surfaces, not just one:
1. Live cron job prompt in `/root/.hermes/cron/jobs.json`.
2. Canonical script prompt `/root/.hermes/scripts/memory-processor-prompt.md` if present.
3. Skill template `obsidian-auto-writer/templates/memory-processor-prompt.md`.

## Verification markers
Before claiming fixed, verify each surface contains:
- `IF NO NEW CONVERSATIONS FOUND → DO NOT exit early`
- `Step 2.5: Proposal Approval Intake`
- `Do NOT create a second new proposal`
- `For tasks you CAN execute: attempt it`

## Reporting style to user
Keep it short and concrete:
- State the root cause.
- State what was patched.
- Show only marker proof, not the whole prompt.
- Mention the next cron run time only if verified.

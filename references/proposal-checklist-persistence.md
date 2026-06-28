# Proposal checklist persistence for memory-processor

## Trigger
Use when the `memory-processor` cronjob generates or reports a proposal, especially if the user says they cannot find the proposal/checklist in Obsidian.

## Durable rule
A proposal is not complete if it only appears in a Telegram cron response. Persist it into the vault as a user-facing note.

## Canonical vault path
Because this vault uses the nested layout, write proposal notes under:

```text
/root/Documents/ObsidianVault/obsidian-vault/Proposals/Memory Processor Proposal #N.md
```

User-facing Obsidian path:

```text
Proposals/Memory Processor Proposal #N.md
```

## Minimum note shape
```markdown
---
date: YYYY-MM-DD
tags: [proposal, memory-processor, obsidian, automation]
related: [[Daily/YYYY-MM-DD]]
status: pending
---

# Memory Processor Proposal #N

Status: pending user approval
Source: cronjob `memory-processor` (`JOB_ID`), Telegram alert topic.

## How to approve from Telegram
- Approve all: `proposal acc` or `gas semua`
- Approve specific items: `proposal [x] 1,2`
- Reject all: `proposal skip`
- Edit then approve: `proposal edit: ...`

## Checklist
- [ ] 1. ...
```

## Prompt rules to keep in sync
Patch both the live prompt and the template when changing proposal behavior:

- `/root/.hermes/scripts/memory-processor-prompt.md`
- `/root/.hermes/skills/obsidian-auto-writer/templates/memory-processor-prompt.md`
- the live cron job prompt in `/root/.hermes/cron/jobs.json` if the job stores a snapshot of the prompt

Required behavior:

1. Before generating a new proposal, search for pending `Proposals/Memory Processor Proposal #*.md`.
2. If a pending proposal exists and no approval/rejection was found, do not create a duplicate proposal.
3. Report the pending proposal path in Telegram.
4. If a new proposal is created, create/update the vault note and report:
   `📋 PROPOSAL saved: Proposals/Memory Processor Proposal #N.md`
5. No-new-conversations must not early-exit before proposal approval intake and executable TODO processing.

## Verification pattern
Verify with minimal evidence:

```text
schedule {'kind': 'interval', 'minutes': 10, 'display': 'every 10m'}
proposal_saved_rule True
no_early_exit_rule True
proposal_intake_rule True
```

Also verify the proposal file exists and has `status: pending` until user approval is processed.

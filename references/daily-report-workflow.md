# Daily Report Workflow for Obsidian Vault

## Rule
Use exactly one daily note per calendar day: `Daily/YYYY-MM-DD.md`.

Before writing any daily report:
1. Check whether today's file exists.
2. If it exists, append/update sections inside that same file.
3. If it does not exist, create it from the daily template.
4. Never create duplicate daily files like `YYYY-MM-DD-setup.md`, `YYYY-MM-DD-2.md`, or separate report files for the same date.

## Vault Workflow File
If `/root/Documents/ObsidianVault/WORKFLOW.md` exists, treat it as the user-facing source of truth for daily report, TODO, and sync behavior.

Background processors that update the vault should read/follow `WORKFLOW.md` before writing notes.

## TODO Handling
Only mark TODO items as complete after verified execution:
- completed: `- [x]`
- failed/blocked: leave `- [ ]` and add a short blocker note

## Cleanup Pattern
If an earlier run created duplicate daily files, merge or preserve the useful content in `Daily/YYYY-MM-DD.md`, then remove the duplicate file from the vault so Obsidian shows one daily note for the day.

## Reporting
When reporting back, keep proof minimal:
- changed files
- commit/output line if pushed
- blocker if any

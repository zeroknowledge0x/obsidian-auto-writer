# Obsidian Git Conflict Resolution

## When Conflicts Happen
Server auto-push + iPhone auto-pull editing same file → Git merge conflict.

## Symptoms
- iPhone shows: "Modifying the index is not possible because you have unmerged files"
- Obsidian Git plugin can't commit/pull

## Fix (iPhone)
1. Open Obsidian
2. Command Palette (swdown on note area)
3. Type: "Git: CAUTION: Delete repository and re-clone"
4. Tap → confirm

This deletes local repo + re-clones from GitHub. No manual file deletion needed.

## Alternative (if above doesn't work)
1. Close Obsidian
2. Files app → On My iPhone → Obsidian → zka-brain → Delete
3. Open Obsidian → Open vault from cloud → clone again

## Prevention
- Server auto-push: 10 min intervals
- iPhone auto-pull: 5 min intervals
- Avoid editing same file on both devices simultaneously
- If editing on iPhone, wait for pull to complete first

## Server-side check
```bash
cd /root/Documents/ObsidianVault && git status
```
If clean → conflict is iPhone-side only.

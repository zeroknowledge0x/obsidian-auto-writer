# Obsidian Mobile Sync Troubleshooting

Use when the user says the note exists on server/GitHub but Obsidian iPhone still does not show it.

## Verify before claiming
1. Check local vault file exists in `/root/Documents/ObsidianVault`.
2. Check `git status --short --branch` and confirm local branch tracks remote.
3. Check remote branch HEAD with `git ls-remote --heads origin`.
4. For private repos, do **not** rely on unauthenticated `raw.githubusercontent.com` URLs — they return 404 even when the file exists. Verify via authenticated GitHub API `/repos/{owner}/{repo}/contents/{path}?ref={branch}` or `git show HEAD:path`.
5. Check whether the file is in root vault or a folder; tell the user the exact location to search.

## Common causes
- iPhone Obsidian is opening the wrong vault/folder.
- Obsidian Git mobile has local merge/index conflicts and cannot pull.
- User expects a note under `Kuliah/`, but the note was written at vault root (`Jadwal Kuliah.md`).
- Mobile file explorer/search cache has not refreshed after pull.

## iPhone fix sequence to give user
1. Obsidian → Command Palette → `Git: Pull`.
2. If unchanged: Command Palette → `Git: Open source control view` and inspect red errors.
3. If error mentions unmerged files, index, or cannot pull: Command Palette → `Git: CAUTION: Delete repository and re-clone`.
4. Reopen vault and search exact path/name.
5. If still missing after re-clone, suspect wrong vault/repo opened on iPhone.

## Agent pitfall
Do not keep repeating “server is updated” after the user says mobile still does not show it. Switch to mobile-side troubleshooting and give concise iPhone steps. If offering to move/duplicate files for discoverability (e.g. `Kuliah/Jadwal Kuliah.md`), ask before pushing because GitHub writes are side-effectful.
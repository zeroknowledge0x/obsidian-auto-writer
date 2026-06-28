#!/usr/bin/env python3
"""Batch-update TODO 'Checked:' timestamps across the Obsidian vault.

Usage:
    python3 scripts/vault-timestamp-update.py [--vault PATH] [--from OLD] [--to NEW]

Defaults:
    --vault  /root/Documents/ObsidianVault/obsidian-vault
    --from   any previous timestamp (regex-matches Checked: YYYY-MM-DD HH:MM UTC)
    --to     current UTC time in YYYY-MM-DD HH:MM UTC format

Scans all .md files in vault for lines containing 'Checked:' and replaces
the timestamp portion. Safe to run multiple times (idempotent).
"""
import argparse
import os
import re
import sys
from datetime import datetime, timezone


def update_timestamps(vault_path: str, old_pattern: str, new_ts: str) -> list[str]:
    """Update Checked: timestamps in all .md files under vault_path.

    Returns list of files that were modified.
    """
    updated_files = []
    regex = re.compile(r"Checked: \d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC")

    for root, dirs, files in os.walk(vault_path):
        # Skip .git and .obsidian
        dirs[:] = [d for d in dirs if d not in (".git", ".obsidian")]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath) as f:
                content = f.read()

            if "Checked:" not in content:
                continue

            if old_pattern:
                new_content = content.replace(f"Checked: {old_pattern}", f"Checked: {new_ts}")
            else:
                new_content = regex.sub(f"Checked: {new_ts}", content)

            if new_content != content:
                with open(fpath, "w") as f:
                    f.write(new_content)
                updated_files.append(fpath)

    return updated_files


def main():
    parser = argparse.ArgumentParser(description="Batch-update TODO timestamps in vault")
    parser.add_argument("--vault", default="/root/Documents/ObsidianVault/obsidian-vault")
    parser.add_argument("--from", dest="old_pattern", default=None,
                        help="Old timestamp string (e.g. '2026-06-27 11:15 UTC'). Omit to update ALL timestamps.")
    parser.add_argument("--to", dest="new_ts", default=None,
                        help="New timestamp. Defaults to current UTC time.")
    args = parser.parse_args()

    new_ts = args.new_ts or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    updated = update_timestamps(args.vault, args.old_pattern, new_ts)

    if updated:
        print(f"Updated {len(updated)} file(s) to Checked: {new_ts}")
        for f in updated:
            print(f"  - {f}")
    else:
        print(f"No files contained matching Checked: timestamps")


if __name__ == "__main__":
    main()

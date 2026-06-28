# Prompt Architecture Lessons — Memory Processor

## Three-Way Sync Protocol
When editing memory-processor prompt, ALWAYS sync 3 files:
1. `/root/.hermes/scripts/memory-processor-prompt.md` (working copy)
2. `/root/.hermes/skills/obsidian-auto-writer/templates/memory-processor-prompt.md` (canonical template)
3. `/root/.hermes/cron/jobs.json` embedded prompt (what cron actually reads)

Verify with sha256:
```bash
python3 -c "
import json, hashlib, pathlib
script = pathlib.Path('/root/.hermes/scripts/memory-processor-prompt.md').read_text()
template = pathlib.Path('/root/.hermes/skills/obsidian-auto-writer/templates/memory-processor-prompt.md').read_text()
data = json.loads(pathlib.Path('/root/.hermes/cron/jobs.json').read_text())
jobs = next(j['prompt'] for j in data['jobs'] if j.get('name')=='memory-processor')
s1 = hashlib.sha256(script.strip().encode()).hexdigest()
s2 = hashlib.sha256(template.strip().encode()).hexdigest()
s3 = hashlib.sha256(jobs.strip().encode()).hexdigest()
print(f'script={s1[:12]} template={s2[:12]} jobs={s3[:12]} equal={s1==s2==s3}')
"
```

## Sync Script (Copy + JSON update)
```python
import json, pathlib
prompt = pathlib.Path('/root/.hermes/scripts/memory-processor-prompt.md').read_text()
pathlib.Path('/root/.hermes/skills/obsidian-auto-writer/templates/memory-processor-prompt.md').write_text(prompt)
data = json.loads(pathlib.Path('/root/.hermes/cron/jobs.json').read_text())
for j in data['jobs']:
    if j.get('name') == 'memory-processor':
        j['prompt'] = prompt
        break
pathlib.Path('/root/.hermes/cron/jobs.json').write_text(json.dumps(data, indent=2, ensure_ascii=False))
```

## Prompt Size Budget
- Sweet spot: 7-8K chars
- Below 5K: too terse, model skips layers
- Above 10K: model starts skipping report format, outputs GROWTH only
- Above 18K: guaranteed degradation

## Claude App Review (2026-06-27)
External Claude (claude.ai) reviewed the memory-processor system and produced a superior prompt. Key improvements over ZKA's version:
1. Report format with "or:" alternatives (not just template)
2. Step 6 broken into 6A/6B/6C/6D (performance, vault health, proposals, growth)
3. Fact Store extract rules (when to extract vs when not to)
4. Proposal template with Evidence + Effect sections
5. Cleaner Critical Rules (numbered, no duplicates)

Lesson: External review catches prompt blindness. When user has Claude app access, leverage it for prompt review.

## Cron Toolset Verification
Enabled toolsets for memory-processor: `terminal`, `file`, `skills`, `session_search`, `memory`
- `file` toolset includes `read_file`, `write_file`, `patch`, `search_files` — all available in cron
- `session_search` available for conversation reading
- `fact_store` NOT available (skip_memory=True) — use helper script
- `mcp_mempalace_*` NOT available — don't reference in prompt

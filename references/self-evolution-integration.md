# Self-Evolution Integration with Obsidian Auto-Writer

## Overview
Use `hermes-agent-self-evolution` (DSPy + GEPA) to auto-optimize memory-processor prompt based on execution traces.

## Status (2026-06-28)
- ✅ Installed: `pip install -e .` from `/root/hermes-agent-self-evolution`
- ✅ DSPy 3.2.1 + GEPA 0.0.27 + LiteLLM 1.90.0
- ⏳ Waiting for 10+ runs with JSON metrics before first optimization
- ⏳ Evaluation dataset not yet built

## How It Works
1. Memory processor runs → outputs JSON metrics to Fact Store
2. After 10+ runs → collect metrics as evaluation dataset
3. GEPA mutates prompt (add/remove/reorder rules)
4. Evaluate each mutation against metrics
5. Select best variant → replace prompt
6. Repeat

## Cost
- Mimo v2.5 Pro: ~$0.20-0.50 per optimization run
- GPT-4: ~$2-10 per run
- Claude Sonnet: ~$1-3 per run

## Metrics Format (JSON for GEPA parsing)
```json
{
  "run_ts": "2026-06-28T14:00Z",
  "notes_written": 3,
  "notes_updated": 5,
  "links_added": 7,
  "duplicates_avoided": 2,
  "todos_executed": 2,
  "todos_blocked": 1,
  "facts_added": 5
}
```

## Trigger Optimization
```bash
cd /root/hermes-agent-self-evolution
# Run optimization with mimo-v2.5-pro
python3 -m hermes_self_evolution.optimize \
  --prompt /root/.hermes/scripts/memory-processor-prompt.md \
  --metrics-source fact-store \
  --model xiaomi/mimo-v2.5-pro \
  --generations 5
```

## Key Insight
Self-evolution needs CONSISTENT metrics format. If metrics change format between runs, GEPA can't parse them. Always use the JSON schema above.

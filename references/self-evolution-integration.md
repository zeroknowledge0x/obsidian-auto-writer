# Self-Evolution Integration for Obsidian Auto-Writer

## Overview
`hermes-agent-self-evolution` (DSPy + GEPA) can auto-optimize the memory-processor prompt based on execution traces.

## Installed
- Repo: `/root/hermes-agent-self-evolution`
- Dependencies: DSPy 3.2.1, GEPA 0.0.27, LiteLLM 1.90.0
- Install: `pip3 install -e /root/hermes-agent-self-evolution`

## Architecture
```
memory-processor run → execution trace (report output)
    ↓
Self-Evolution reads trace → detect failure pattern
    ↓
GEPA proposes mutations → e.g. "add rule X to Step 4"
    ↓
Evaluate → is output better?
    ↓
Best variant → update prompt/skill
    ↓
Repeat
```

## What to Optimize
1. **Prompt clarity** — reduce misclassification of TODOs
2. **Project detection** — auto-create folders more reliably
3. **Fact extraction** — better granularity, fewer misses
4. **Linking heuristic** — cross-reference accuracy

## Cost
- Mimo v2.5 Pro: ~$0.20-0.50 per optimization run
- GPT-4: ~$2-10 per run
- Claude Sonnet: ~$1-3 per run

## Data Source
Step 7 (Metrics Tracking) logs per-run data to Fact Store:
- Notes created vs updated
- Wikilinks added
- Duplicates avoided
- TODO execution rate

This data powers the evolution loop.

## Status (2026-06-28)
- Installed but not yet configured
- Needs: model provider config, evaluation dataset from 10+ runs
- Target: push success_rate from 61% to 80%+

## Combo with Other Systems
- RAG pipeline (vault embedding) → better context for evolution
- Auto-linking → provides linking accuracy metric for evolution
- Metrics tracking → provides raw data for evaluation

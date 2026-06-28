# Obsidian Auto-Growth Research (2026-06-28)

## GitHub Repos for Auto-Growth

| Repo | Stars | Fitur |
|------|-------|-------|
| logancyang/obsidian-copilot | ~3.5k | Chat with vault, auto-summarize, multi-LLM |
| brianpetro/obsidian-smart-connections | ~3k+ | Semantic search, auto-linking, AI chat |
| ScientistFdo/Auto-Researcher | ~500+ | Autonomous research → auto-writes Obsidian notes |

## 5 Auto-Growth Patterns

1. **RAG Pipeline** — Embed vault → retrieve context → generate notes
2. **Cron-based Processing** — Periodic jobs creating notes (Hermes memory-processor = this)
3. **Multi-agent Research** — Agents research + write structured findings
4. **Knowledge Graph Enrichment** — Auto-add backlinks, tags, connections
5. **Conversation Mining** — Process chat logs → knowledge notes (Hermes memory-processor = this)

## What Hermes Already Has vs What's Missing

| Feature | Obsidian Copilot | Smart Connections | Auto-Researcher | Hermes |
|---------|------------------|-------------------|-----------------|--------|
| Auto-summarize | ✅ | ✅ | ✅ | ✅ |
| Auto-write notes | ❌ | ❌ | ✅ | ✅ |
| Chat with vault | ✅ | ✅ | ❌ | ✅ (session_search) |
| Cron automation | ❌ | ❌ | ❌ | ✅ |
| Fact Store | ❌ | ❌ | ❌ | ✅ |
| Self-improvement | ❌ | ❌ | ❌ | ✅ (proposal system) |

## What Could Be Added

1. **RAG pipeline** — embed vault ke vector store, retrieve context sebelum nulis
2. **Auto-linking** — detect koneksi antar notes, tambahin wikilink otomatis
3. **Semantic search** — cari notes berdasarkan makna, bukan keyword
4. **Self-Evolution** — DSPy + GEPA optimize memory-processor prompt automatically

## Self-Evolution Integration

**Repo:** hermes-agent-self-evolution (NousResearch)
**Engine:** DSPy + GEPA (Genetic-Pareto)
**Cost:** ~$0.20-0.50 per optimization run with mimo-v2.5-pro (vs $2-10 with GPT-4)
**What it optimizes:** memory-processor-prompt.md, obsidian-auto-writer skill, Fact Store extraction
**Flow:** execution traces → detect failure patterns → GEPA propose mutations → evaluate → select best → update prompt/skill

## Dataview Plugin Assessment

**What it does:** Query engine for Obsidian. Can aggregate all unchecked tasks into one view.
**Critical for auto-execute?** NO — memory processor already handles task aggregation via grep/search.
**Value:** UX improvement for user (see all tasks in one note). Doesn't improve auto-execute functionality.
**Why auto-execute has 0 CAN EXECUTE tasks:** Not missing tooling — existing tasks genuinely need external resources (funding, tmux, user action). Fix: write tasks AI CAN execute (research, summarize, update).

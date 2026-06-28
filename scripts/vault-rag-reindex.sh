#!/bin/bash
# vault-rag-reindex.sh — Nightly RAG re-index
python3 /root/.hermes/scripts/vault-embedder.py index 2>&1
echo "---"
python3 /root/.hermes/scripts/vault-embedder.py status

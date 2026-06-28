#!/usr/bin/env python3
"""
vault-embedder.py — RAG pipeline untuk Obsidian vault
Usage:
  python3 vault-embedder.py index              # embed semua .md files
  python3 vault-embedder.py search "query"     # semantic search
  python3 vault-embedder.py search "query" --limit 5
  python3 vault-embedder.py status             # berapa docs ter-index
"""

import argparse
import os
import sys
from pathlib import Path

VAULT_PATH = Path("/root/Documents/ObsidianVault/obsidian-vault")
CHROMA_PATH = Path("/root/.hermes/vault-index")
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "obsidian_vault"

def get_collection():
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

def index_vault():
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)
    collection = get_collection()

    md_files = [
        f for f in VAULT_PATH.rglob("*.md")
        if ".git" not in str(f) and ".obsidian" not in str(f)
    ]

    print(f"Indexing {len(md_files)} files...")

    batch_ids, batch_docs, batch_metas = [], [], []
    BATCH_SIZE = 50

    for fp in md_files:
        try:
            content = fp.read_text(encoding="utf-8").strip()
            if not content:
                continue
            # chunk: first 1000 chars (title + summary cukup untuk retrieval)
            chunk = content[:1000]
            doc_id = str(fp.relative_to(VAULT_PATH))

            batch_ids.append(doc_id)
            batch_docs.append(chunk)
            batch_metas.append({"path": str(fp), "rel": doc_id})

            if len(batch_ids) >= BATCH_SIZE:
                embeddings = model.encode(batch_docs).tolist()
                collection.upsert(
                    ids=batch_ids,
                    documents=batch_docs,
                    embeddings=embeddings,
                    metadatas=batch_metas
                )
                print(f"  Indexed {len(batch_ids)} docs...")
                batch_ids, batch_docs, batch_metas = [], [], []

        except Exception as e:
            print(f"  Skip {fp}: {e}", file=sys.stderr)

    if batch_ids:
        embeddings = model.encode(batch_docs).tolist()
        collection.upsert(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=embeddings,
            metadatas=batch_metas
        )

    total = collection.count()
    print(f"Done. Total indexed: {total} docs")

def search_vault(query: str, limit: int = 5):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)
    collection = get_collection()

    if collection.count() == 0:
        print("ERROR: vault not indexed yet. Run: vault-embedder.py index", file=sys.stderr)
        sys.exit(1)

    embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=embedding,
        n_results=min(limit, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        score = round(1 - dist, 3)
        print(f"\n[{i+1}] {meta['rel']} (score: {score})")
        print(doc[:300].replace("\n", " "))

def status():
    collection = get_collection()
    count = collection.count()
    print(f"Indexed docs: {count}")
    print(f"Vault path: {VAULT_PATH}")
    print(f"Index path: {CHROMA_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["index", "search", "status"])
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    if args.command == "index":
        index_vault()
    elif args.command == "search":
        if not args.query:
            print("ERROR: query required", file=sys.stderr)
            sys.exit(1)
        search_vault(args.query, args.limit)
    elif args.command == "status":
        status()

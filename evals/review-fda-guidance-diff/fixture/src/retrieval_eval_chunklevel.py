"""
Retrieval Strategy Evaluation - Chunk-Level Labels

Compare dense vs sparse (BM25) vs hybrid (RRF) retrieval.
Uses precise chunk-level ground truth (exact chunk_id match).
"""

import os
import json
import math
from pathlib import Path
from collections import defaultdict
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import re

import sys
sys.path.insert(0, str(Path(__file__).parent))
from chunking_strategies import FDAChunker

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")


def tokenize(text: str) -> list[str]:
    """Simple tokenizer for BM25"""
    tokens = re.findall(r'\b[a-z0-9]+\b', text.lower())
    return [t for t in tokens if len(t) > 2]


class RetrievalIndex:
    """Index supporting dense, sparse, and hybrid retrieval"""

    def __init__(self, chunks: list, embedding_model: SentenceTransformer):
        self.chunks = chunks
        self.chunk_ids = [c.chunk_id for c in chunks]
        self.texts = [c.text for c in chunks]

        # Dense: embed all chunks
        print("  Creating dense index (embeddings)...")
        self.embeddings = embedding_model.encode(self.texts, show_progress_bar=False)
        self.embeddings = np.array(self.embeddings)
        # Normalize for cosine similarity
        self.embeddings_norm = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)

        # Sparse: BM25 index
        print("  Creating sparse index (BM25)...")
        self.tokenized_corpus = [tokenize(text) for text in self.texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

        self.embedding_model = embedding_model

    def search_dense(self, query: str, k: int = 10) -> list[tuple[str, float]]:
        """Dense retrieval using cosine similarity"""
        query_emb = self.embedding_model.encode([query], show_progress_bar=False)[0]
        query_emb = query_emb / np.linalg.norm(query_emb)

        similarities = np.dot(self.embeddings_norm, query_emb)
        top_indices = np.argsort(similarities)[::-1][:k]

        return [(self.chunk_ids[i], float(similarities[i])) for i in top_indices]

    def search_sparse(self, query: str, k: int = 10) -> list[tuple[str, float]]:
        """Sparse retrieval using BM25"""
        query_tokens = tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        top_indices = np.argsort(scores)[::-1][:k]
        return [(self.chunk_ids[i], float(scores[i])) for i in top_indices]

    def search_hybrid_rrf(self, query: str, k: int = 10, retrieval_k: int = 20) -> list[tuple[str, float]]:
        """Hybrid retrieval using Reciprocal Rank Fusion (RRF)"""
        rrf_k = 60  # Standard RRF constant

        dense_results = self.search_dense(query, k=retrieval_k)
        sparse_results = self.search_sparse(query, k=retrieval_k)

        rrf_scores = defaultdict(float)

        for rank, (chunk_id, _) in enumerate(dense_results):
            rrf_scores[chunk_id] += 1.0 / (rrf_k + rank + 1)

        for rank, (chunk_id, _) in enumerate(sparse_results):
            rrf_scores[chunk_id] += 1.0 / (rrf_k + rank + 1)

        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:k]


def compute_mrr(retrieved_ids: list[str], relevant_id: str, k: int = 10) -> float:
    """MRR: Reciprocal rank of the correct chunk"""
    for rank, (chunk_id, _) in enumerate(retrieved_ids[:k], 1):
        if chunk_id == relevant_id:
            return 1.0 / rank
    return 0.0


def compute_recall_at_k(retrieved_ids: list[str], relevant_id: str, k: int = 10) -> float:
    """Recall@K: Is the correct chunk in top K?"""
    ids = [chunk_id for chunk_id, _ in retrieved_ids[:k]]
    return 1.0 if relevant_id in ids else 0.0


def compute_ndcg(retrieved_ids: list[str], relevant_id: str, k: int = 10) -> float:
    """NDCG: For single relevance"""
    for rank, (chunk_id, _) in enumerate(retrieved_ids[:k], 1):
        if chunk_id == relevant_id:
            return (1.0 / math.log2(rank + 1)) / 1.0
    return 0.0


def main():
    print("=" * 60)
    print("Retrieval Strategy Evaluation (Chunk-Level Labels)")
    print("=" * 60)
    print(f"Embedding model: {EMBEDDING_MODEL}")

    # Load chunk-level queries
    print("\nLoading chunk-level queries...")
    with open("data/eval/chunk_queries_cleaned.json") as f:
        queries = json.load(f)
    print(f"  Queries: {len(queries)}")

    # Chunk the 2025 document
    print("\nChunking with parent_child strategy...")
    chunker = FDAChunker(
        Path("data/raw/cybersecurity_2023.pdf"),
        "cybersecurity_2025",
        "2025"
    )
    chunks = chunker.chunk_parent_child()
    print(f"  Chunks: {len(chunks)}")

    # Load embedding model
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Build index
    print("\nBuilding retrieval index...")
    index = RetrievalIndex(chunks, model)

    # Evaluation settings
    K = 10

    # Strategies to test
    strategies = {
        "dense": lambda q: index.search_dense(q, k=K),
        "sparse_bm25": lambda q: index.search_sparse(q, k=K),
        "hybrid_rrf": lambda q: index.search_hybrid_rrf(q, k=K, retrieval_k=K*2),
    }

    # Run evaluation
    print(f"\nEvaluating with K={K}...")
    results = {}

    for strategy_name, search_fn in strategies.items():
        print(f"\n  Testing {strategy_name}...")

        mrr_scores = []
        recall_scores = []
        ndcg_scores = []

        for item in queries:
            query = item["question"]
            relevant_chunk_id = item["chunk_id"]

            search_results = search_fn(query)

            mrr_scores.append(compute_mrr(search_results, relevant_chunk_id, K))
            recall_scores.append(compute_recall_at_k(search_results, relevant_chunk_id, K))
            ndcg_scores.append(compute_ndcg(search_results, relevant_chunk_id, K))

        results[strategy_name] = {
            "mrr": np.mean(mrr_scores),
            "recall_at_k": np.mean(recall_scores),
            "ndcg": np.mean(ndcg_scores),
            "num_queries": len(mrr_scores),
        }

        print(f"    MRR: {results[strategy_name]['mrr']:.3f}")
        print(f"    Recall@{K}: {results[strategy_name]['recall_at_k']:.3f}")
        print(f"    NDCG: {results[strategy_name]['ndcg']:.3f}")

    # Summary table
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY (Chunk-Level Labels)")
    print("=" * 60)
    print(f"\n{'Strategy':<15} {'MRR':>8} {'Recall@K':>10} {'NDCG':>8}")
    print("-" * 45)

    for strategy_name, metrics in results.items():
        print(f"{strategy_name:<15} {metrics['mrr']:>8.3f} {metrics['recall_at_k']:>10.3f} {metrics['ndcg']:>8.3f}")

    # Find winner
    best_strategy = max(results.items(), key=lambda x: x[1]['mrr'])
    print(f"\n→ Best by MRR: {best_strategy[0]} ({best_strategy[1]['mrr']:.3f})")

    # Save results
    output_path = Path("data/eval/retrieval_eval_chunklevel_results.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()

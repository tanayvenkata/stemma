"""
Chunking Evaluation Pipeline

Evaluates chunking strategies against query-region pairs using:
- Hit Rate: Any relevant result in top-k?
- MRR: Position of first relevant result
- NDCG: Positions of all relevant results (normalized)
"""

import os
import json
import math
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer

from chunking_strategies import chunk_all_strategies, Chunk

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
DATA_DIR = Path("data")
EVAL_DIR = DATA_DIR / "eval"


@dataclass
class EvalResult:
    """Evaluation results for a strategy"""
    strategy: str
    num_chunks: int
    avg_chunk_size: int
    hit_rate: float
    mrr: float
    ndcg: float


def load_test_set() -> list[dict]:
    """Load query-region pairs"""
    with open(EVAL_DIR / "query_region_pairs.json") as f:
        return json.load(f)


def load_regions() -> dict[str, list[dict]]:
    """Load region definitions"""
    regions = {}
    for f in (DATA_DIR / "regions").glob("*.json"):
        with open(f) as file:
            data = json.load(file)
            for r in data:
                regions[r["region_id"]] = r
    return regions


def chunk_overlaps_region(chunk: Chunk, region: dict) -> bool:
    """Check if a chunk overlaps with a region (same doc + overlapping pages)"""
    if chunk.doc_id != region["doc_id"]:
        return False

    chunk_pages = set(chunk.pages)
    region_pages = set(region["pages"])

    return bool(chunk_pages & region_pages)


def compute_hit_rate(retrieved_chunks: list[Chunk], relevant_regions: list[dict], k: int = 10) -> float:
    """
    Hit Rate: Did ANY of the top-k chunks overlap with relevant regions?
    Returns 1 if hit, 0 if miss
    """
    top_k = retrieved_chunks[:k]

    for chunk in top_k:
        for region in relevant_regions:
            if chunk_overlaps_region(chunk, region):
                return 1.0

    return 0.0


def compute_mrr(retrieved_chunks: list[Chunk], relevant_regions: list[dict], k: int = 10) -> float:
    """
    MRR: Reciprocal rank of first relevant result
    Returns 1/rank if found, 0 if not found in top-k
    """
    top_k = retrieved_chunks[:k]

    for rank, chunk in enumerate(top_k, 1):
        for region in relevant_regions:
            if chunk_overlaps_region(chunk, region):
                return 1.0 / rank

    return 0.0


def compute_dcg(relevances: list[int], k: int) -> float:
    """Compute Discounted Cumulative Gain"""
    dcg = 0.0
    for i, rel in enumerate(relevances[:k], 1):
        dcg += rel / math.log2(i + 1)
    return dcg


def compute_ndcg(retrieved_chunks: list[Chunk], relevant_regions: list[dict], k: int = 10) -> float:
    """
    NDCG: Normalized Discounted Cumulative Gain
    Considers positions of ALL relevant results
    """
    top_k = retrieved_chunks[:k]

    # Build relevance scores for retrieved chunks (1 if relevant, 0 if not)
    # A chunk is relevant if it overlaps with ANY relevant region
    relevances = []
    for chunk in top_k:
        is_relevant = any(chunk_overlaps_region(chunk, r) for r in relevant_regions)
        relevances.append(1 if is_relevant else 0)

    # Compute DCG
    dcg = compute_dcg(relevances, k)

    # Compute ideal DCG
    # The ideal is: how many relevant chunks could we possibly have in top-k?
    # This is the number of chunks that actually matched (not regions)
    num_relevant_found = sum(relevances)

    # For IDCG, we assume all relevant items are at top positions
    # But we can't have more relevant items than we actually found in top-k
    ideal_relevances = [1] * num_relevant_found + [0] * (k - num_relevant_found)
    idcg = compute_dcg(ideal_relevances, k)

    if idcg == 0:
        return 0.0

    return min(dcg / idcg, 1.0)  # Cap at 1.0


class ChunkIndex:
    """Simple in-memory chunk index with embedding search"""

    def __init__(self, chunks: list[Chunk], model: SentenceTransformer):
        self.chunks = chunks
        self.model = model
        self.embeddings = None
        self._build_index()

    def _build_index(self):
        """Embed all chunks"""
        texts = [c.text for c in self.chunks]
        self.embeddings = self.model.encode(texts, show_progress_bar=False)

    def search(self, query: str, k: int = 10) -> list[Chunk]:
        """Search for top-k similar chunks"""
        query_embedding = self.model.encode([query], show_progress_bar=False)[0]

        # Compute cosine similarities
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        # Get top-k indices
        top_indices = np.argsort(similarities)[-k:][::-1]

        return [self.chunks[i] for i in top_indices]


def evaluate_strategy(
    strategy_name: str,
    chunks: list[Chunk],
    test_set: list[dict],
    regions: dict[str, dict],
    model: SentenceTransformer,
    k: int = 10
) -> EvalResult:
    """Evaluate a single chunking strategy"""

    # Build index
    index = ChunkIndex(chunks, model)

    # Evaluate each query
    hit_rates = []
    mrrs = []
    ndcgs = []

    for item in test_set:
        query = item["query"]
        relevant_region_ids = [r["region_id"] for r in item["relevant_regions"]]
        relevant_regions = [regions[rid] for rid in relevant_region_ids if rid in regions]

        if not relevant_regions:
            continue

        # Retrieve
        retrieved = index.search(query, k=k)

        # Score
        hit_rates.append(compute_hit_rate(retrieved, relevant_regions, k))
        mrrs.append(compute_mrr(retrieved, relevant_regions, k))
        ndcgs.append(compute_ndcg(retrieved, relevant_regions, k))

    # Aggregate
    avg_chunk_size = sum(len(c.text) for c in chunks) // len(chunks) if chunks else 0

    return EvalResult(
        strategy=strategy_name,
        num_chunks=len(chunks),
        avg_chunk_size=avg_chunk_size,
        hit_rate=np.mean(hit_rates) if hit_rates else 0,
        mrr=np.mean(mrrs) if mrrs else 0,
        ndcg=np.mean(ndcgs) if ndcgs else 0,
    )


def main():
    print("="*70)
    print("Chunking Strategy Evaluation")
    print("="*70)

    # Load test set and regions
    print("\nLoading test set...")
    test_set = load_test_set()
    regions = load_regions()
    print(f"  {len(test_set)} queries, {len(regions)} regions")

    # Load embedding model
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Chunk both documents with all strategies
    print("\nChunking documents...")
    docs = [
        (Path("data/raw/cybersecurity_2014.pdf"), "cybersecurity_2014", "2014"),
        (Path("data/raw/cybersecurity_2023.pdf"), "cybersecurity_2025", "2025"),
    ]

    all_strategies = {}
    for pdf_path, doc_id, version in docs:
        strategies = chunk_all_strategies(pdf_path, doc_id, version)
        for name, chunks in strategies.items():
            if name not in all_strategies:
                all_strategies[name] = []
            all_strategies[name].extend(chunks)

    for name, chunks in all_strategies.items():
        print(f"  {name}: {len(chunks)} chunks")

    # Evaluate each strategy
    print("\nEvaluating strategies...")
    results = []

    for strategy_name, chunks in all_strategies.items():
        print(f"\n  Evaluating: {strategy_name}...")
        result = evaluate_strategy(
            strategy_name, chunks, test_set, regions, model, k=10
        )
        results.append(result)
        print(f"    Hit Rate: {result.hit_rate:.1%}")
        print(f"    MRR: {result.mrr:.3f}")
        print(f"    NDCG: {result.ndcg:.3f}")

    # Summary table
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    print(f"\n{'Strategy':<25} {'Chunks':>8} {'Avg Size':>10} {'Hit Rate':>10} {'MRR':>8} {'NDCG':>8}")
    print("-"*70)

    # Sort by MRR
    results.sort(key=lambda x: x.mrr, reverse=True)

    for r in results:
        print(f"{r.strategy:<25} {r.num_chunks:>8} {r.avg_chunk_size:>10} {r.hit_rate:>10.1%} {r.mrr:>8.3f} {r.ndcg:>8.3f}")

    # Winner
    winner = results[0]
    print(f"\n{'='*70}")
    print(f"WINNER: {winner.strategy}")
    print(f"  Best MRR: {winner.mrr:.3f}")
    print(f"  Hit Rate: {winner.hit_rate:.1%}")
    print(f"  NDCG: {winner.ndcg:.3f}")
    print(f"{'='*70}")

    # Save results
    results_path = EVAL_DIR / "chunking_eval_results.json"
    with open(results_path, "w") as f:
        json.dump([{
            "strategy": r.strategy,
            "num_chunks": r.num_chunks,
            "avg_chunk_size": r.avg_chunk_size,
            "hit_rate": r.hit_rate,
            "mrr": r.mrr,
            "ndcg": r.ndcg
        } for r in results], f, indent=2)
    print(f"\nResults saved to: {results_path}")


if __name__ == "__main__":
    main()

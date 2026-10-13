---
type: llm
weight: 1
---

PASS if the answer identifies both problems:
- cosine similarity and BM25 scores are on different, unnormalized scales, so a weighted sum is dominated by one of them; it suggests normalization or rank-based fusion such as reciprocal rank fusion;
- running BM25 only over the embedding results means keyword search can never recover documents the embedding search missed, which defeats the purpose of hybrid retrieval; both retrievers should search the full index independently before fusion.

FAIL if either problem is missing.

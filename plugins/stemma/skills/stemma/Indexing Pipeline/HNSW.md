---
tags: [indexing]
---
# HNSW

Hierarchical Navigable Small World is an approximate nearest-neighbor index built from layered proximity graphs. Search enters a sparse upper layer, greedily approaches the query neighborhood, then explores denser lower layers to produce candidates.

Approximate search does not guarantee the exact nearest neighbors. Its purpose is a favorable quality–latency tradeoff.

## Main Controls

| Control | Effect |
|---|---|
| graph connectivity (`M` or equivalent) | higher values usually increase memory/build cost and can improve navigability |
| construction search effort | more work can build a higher-quality graph at greater indexing cost |
| query search effort | explores more candidates, generally trading latency for recall |

Names, defaults, limits, and filter behavior vary by implementation. Dataset geometry, insertion order, deletions, quantization, concurrency, and metadata selectivity also matter.

## Evaluation

1. Build exact-search results for representative queries as the neighbor reference.
2. Compare HNSW configurations on ANN recall, final task ranking, latency percentiles, memory, build/update time, and failure behavior.
3. Test production-like filters and selective subsets; graph traversal can degrade under constraints.
4. Test incremental inserts, deletes/tombstones, rebuilds, persistence, and recovery.
5. Select a Pareto point from application requirements rather than copying parameter ranges.

If exact search itself misses labeled evidence, changing HNSW tuning will not repair the embedding or chunking problem.

Primary reference: [Efficient and Robust Approximate Nearest Neighbor Search Using HNSW](https://arxiv.org/abs/1603.09320).

## Part of

← [[Vector Index]]

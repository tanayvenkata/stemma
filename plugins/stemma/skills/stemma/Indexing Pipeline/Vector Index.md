---
tags: [indexing]
reviewed: 2026-10-11
---
# Vector Index

Data structures and algorithms designed for **Approximate Nearest Neighbor (ANN)** search in multi-dimensional vector spaces.

---

## The Fundamental Problem

Comparing a query vector against $N$ document vectors (Brute Force / Flat Search) requires $O(N)$ operations. At some combination of collection size, dimension, hardware, and concurrency exhaustive search stops meeting latency or throughput targets. Find that point by measurement (see [[Flat Index]]), not a fixed vector count.

A **Vector Index** organizes vectors into geometric graphs, trees, or clusters to trade exactness, build/update cost, memory, and query latency. Complexity and latency depend on algorithm, implementation, data distribution, hardware, concurrency, and tuning. IVF scans roughly the `nprobe` probed lists out of $K$; HNSW's roughly logarithmic scaling is an empirical result reported in the [HNSW paper](https://arxiv.org/abs/1603.09320), not a worst-case guarantee.

```
                           Vector Index Types
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
[[Flat Index]]              [[IVF]]                     [[HNSW]]
• Brute-force exhaustive    • Voronoi clustering        • Multi-layer graph
• Exact within vector space • Low graph overhead        • Strong ANN baseline
• $O(N)$ search time        • ~nprobe/K of N scanned    • ~log N (empirical)
• Small collections         • Best for RAM-constrained  • Default if RAM permits
```

---

## Comparison Matrix

| Index Algorithm | Search Latency | Recall @ 10 | RAM Overhead | Build Time | Best For |
|---|---|---|---|---|---|
| **[[Flat Index]]** | Slow ($O(N)$) | **100%** (Exact) | **None** (Base vectors) | **Instant** ($0\text{ build}$) | Collections where exhaustive search meets latency needs (measure; see [[Flat Index]]), exact-recall baselines for evaluation |
| **[[IVF]]** | Tunable ANN | Measure vs exact | Lower graph overhead | Requires training | Memory-sensitive or very large collections after benchmarking |
| **[[HNSW]]** | Tunable ANN | Measure vs exact | Graph overhead depends on parameters | Graph construction | Strong general ANN baseline when memory permits |

Treat exact search on a representative sample as the recall oracle. Plot recall@k against p50/p95 latency, throughput, RAM, build/update cost, and filtered-query selectivity rather than copying generic percentages.

---

## Components
- [[HNSW]]
- [[IVF]]
- [[Flat Index]]

## Part of
← [[Indexing]]

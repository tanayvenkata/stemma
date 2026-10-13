---
tags: [indexing]
---
# Flat Index

A flat index computes the configured distance from the query to every stored vector. Ignoring hardware optimizations, its work grows approximately as $O(ND)$ for $N$ vectors of dimension $D$.

## Roles

- simple search for workloads where exhaustive computation meets latency and cost constraints;
- diagnostic reference for how much neighbor recall an approximate index loses;
- baseline before operational complexity is justified;
- exact rescoring of a smaller candidate set.

“Exact” means exact under the stored representation, precision, metric, and implementation. It does not imply perfect semantic retrieval, complete labels, or an absence of numerical effects.

## Decision Procedure

Benchmark realistic vector count, dimension, hardware, batching, concurrency, filters, and updates. Measure end-to-end latency, throughput, memory, and task outcomes. Switch to an approximate structure when the measured workload requires it, not at a universal vector-count boundary.

Use flat results to calculate ANN recall only after confirming that the representation and metric are correct for the task.

## Part of

← [[Vector Index]]

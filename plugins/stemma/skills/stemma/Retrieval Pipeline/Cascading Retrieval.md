---
tags: [retrieval]
---
# Cascading Retrieval

A retrieval cascade spends increasing computation on a shrinking candidate set. A broad inexpensive stage protects recall; later stages refine representation, ranking, policy, or evidence packaging.

```text
broad candidate generation
→ optional representation/full-vector refinement
→ expressive reranking
→ context-budget selection
```

Stages may use different dimensions, precision, retrieval methods, filters, or rankers. The design is justified by a measured resource bottleneck, not a collection-size threshold.

## Stage Contract

For each boundary record candidate identities, scores, required-evidence recall, latency, cost, and failures. A later stage cannot repair evidence removed earlier.

## Experiment

1. Establish the strongest affordable direct baseline.
2. Measure candidate recall at each proposed width.
3. Add one stage and compare total latency, throughput, memory, cost, and final evidence/answer quality.
4. Sweep widths and search effort on development cases.
5. Test filters, concurrency, timeouts, partial failure, and fallback.
6. Remove stages whose incremental value does not justify their complexity.

Keep mandatory authorization scope active at every stage; never broaden it as a fallback.

## Part of

← [[Retrieval]]

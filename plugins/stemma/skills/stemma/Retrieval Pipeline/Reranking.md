---
tags: [retrieval]
---
# Reranking

Reranking applies a more expressive or expensive relevance function to a fixed candidate set. It can improve ordering but cannot recover evidence absent from that set.

## Families

- pairwise query-document scorers;
- late-interaction or multi-vector refinement;
- listwise models that compare several candidates jointly;
- generative or instruction-conditioned rankers;
- deterministic business/source-priority rules combined with relevance.

Architecture labels do not guarantee latency or quality. Input truncation, candidate width, batching, score semantics, language, and domain determine behavior.

## Experiment

1. Record identical raw candidates for every reranker.
2. Measure the required-evidence ceiling in that pool.
3. Compare baseline and reranked order at context-relevant cutoffs using paired cases.
4. Inspect NDCG/MRR, required-evidence coverage, complementary evidence, helped/harmed slices, latency, cost, timeout, and fallback.
5. Sweep candidate width on development cases, then test the selected policy on protected cases.
6. Pass finalists through fixed context assembly and generation.

Adopt when downstream value on the diagnosed slices pays for added compute and failure modes. If relevant evidence is missing from the candidate pool, repair retrieval. If rank lift does not improve answers, inspect labels, effect size, context assembly, and evidence diversity.

Scores are model-specific and generally not calibrated probabilities. Any cutoff or abstention policy requires held-out calibration and drift monitoring.

## Part of

← [[Post-Retrieval Processing]]

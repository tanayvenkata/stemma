---
tags: [evaluation]
---
# Reranking Evaluation

A reranker can only reorder candidates surfaced upstream. Its evaluation must separate candidate recall from ordering quality and charge the added stage for latency, cost, failure behavior, and operational complexity.

## When This Enters the Build

Consider reranking when retrieval already places the necessary evidence somewhere in a feasible candidate pool but orders it too late or mixes it with hard negatives. Do not add it when candidate recall is poor: a reranker cannot recover absent evidence.

Leave with a justified retriever width `K1`, final context width `K2`, fallback behavior, and paired evidence that improved ordering survives the downstream context budget. Revisit it when the retriever, labels, traffic mix, context budget, or latency envelope changes.

## Cases and Labels

Reuse versioned query–candidate relevance judgments where possible, with graded labels for directly sufficient, partially supporting, and irrelevant evidence. Enrich the set with hard negatives: lexically similar but wrong passages, conflicting dates or entities, near duplicates, stale versions, and candidates satisfying only part of a multi-constraint query.

Pool candidates from multiple retrievers and rerankers before labeling to reduce system bias. Include queries with no relevant candidate and queries with several valid orderings. Keep training or prompt-tuning examples out of protected evaluation.

## Before/After Design

Let `K1` be retriever candidate width and `K2` the final context width:

1. Record the identical raw top-`K1` candidates for every reranker.
2. Measure whether each required evidence item exists anywhere in `K1`—the reranker’s recall ceiling.
3. Rerank the fixed set and compare raw versus reranked top-`K2` using MRR, NDCG, Recall, and evidence-token ratio.
4. Track helped, harmed, and unchanged queries plus movement of each relevant item.
5. Sweep `K1` on development cases while holding `K2` to the product context budget.
6. Evaluate the chosen setting on protected cases and a fixed downstream generation/citation setup.
7. Load-test batching, concurrency, timeout, malformed output, and fallback to raw ranking.

```python
raw = retriever.search(query, top_k=k1)
assert same_candidate_ids(raw, candidates_given_to_every_reranker)
reranked = reranker.rank(query, raw)
delta = ndcg(reranked[:k2], labels) - ndcg(raw[:k2], labels)
```

For stochastic or generative reranking, repeat runs and report ordering instability. Audit truncation: a candidate may be scored incorrectly because only part of its text reached the reranker.

## Interpret the Pattern

| Observation | Likely next action |
|---|---|
| Required evidence absent from K1 | fix candidate retrieval or widen K1 if affordable |
| Present in K1 but consistently ranked late | reranking is a plausible intervention |
| NDCG rises but Recall@K2 falls | reranker favors one strong item while dropping complementary evidence |
| Offline rank lift does not improve answers | inspect context assembly, labels, and effect size |
| Gains vanish under load | batching, timeout, truncation, or fallback is part of the component failure |
| Only one slice improves | consider conditional invocation instead of universal reranking |

## Decision Rule

Adopt a reranker when paired gains at the actual K2 are credible and meaningful on motivating slices, required-evidence coverage and high-risk slices stay within constraints, and downstream benefit pays for added latency, cost, and failure modes. Prefer the simpler candidate when differences are practically indistinguishable.

Do not validate a universal score threshold: score scales vary by reranker, query mix, and domain. If a score controls cutoff or abstention, calibrate that decision on held-out cases and monitor drift. Change reranking only when candidate recall is adequate and ordering is the diagnosed bottleneck.

## Part of

← [[Component Evaluation Harness]]

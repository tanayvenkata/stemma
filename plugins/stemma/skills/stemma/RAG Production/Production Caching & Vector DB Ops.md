---
tags: [production]
reviewed: 2026-10-11
---
# Production Caching & Vector DB Ops

Caches and vector indexes are derived state. Their operational contract is correctness under change, authorization, overload, and recovery—not a fixed latency number.

## Cache Layers

| Layer | Key question | Common invalidators |
|---|---|---|
| Provider prompt/prefix cache | Is an eligible prefix identical under this provider's rules? | prefix, model, account/project, TTL |
| Exact application cache | Are request semantics and authorization identical? | query, tenant/user scope, corpus/index, prompt/model/policy versions |
| Semantic answer cache | Is reuse safe despite non-identical wording? | all above plus time, locale, intent, entities, transactional state |
| Retrieval cache | Can candidate IDs/scores be reused? | index generation, filters, ACLs, retriever configuration |

Never authorize from cached output. Recheck the current principal and policy on every read. Semantic similarity alone is insufficient for reuse; a high score can join questions with opposite intent, different dates, or different permissions.

Store dependency metadata with cached answers so source updates, deletes, ACL changes, policy changes, and model/prompt releases can invalidate affected entries. Prefer short TTLs or no semantic cache for volatile and high-risk facts.

Provider cache discounts, eligibility, minimum prefix size, and retention differ and change over time. Keep them in dated implementation records rather than as universal architecture constants.

## Vector Index Operations

- Benchmark index type and parameters on the real embedding dimension, corpus, filters, update rate, and recall target.
- Measure recall and tail latency together; approximate-search tuning trades one for the other.
- Validate pre-filter and post-filter semantics, especially for tenant and ACL constraints.
- Monitor memory, index build time, tombstones/dead tuples, write amplification, compaction/vacuum behavior, replication lag, and query saturation.
- Separate bulk ingestion from latency-sensitive reads with quotas or resource isolation.

Database defaults and example HNSW settings are starting points, not production standards. Record the database/version, dataset, hardware, and benchmark that justified each value.

## Migrations and Recovery

Build incompatible indexes in shadow, dual-process live changes, reconcile expected identities and ACLs, then shift reads gradually. Retain the previous generation for rollback; the full procedure lives in [[Indexing Lifecycle & Migrations]]. Periodically prove that the index can be rebuilt from authoritative data and versioned transformations.

## Part of
← [[RAG Production]]

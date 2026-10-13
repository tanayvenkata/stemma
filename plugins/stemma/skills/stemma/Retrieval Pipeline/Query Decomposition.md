---
tags: [retrieval]
---
# Query Decomposition

Breaking complex, multi-part, or comparative user questions into independent sub-queries that are searched separately and synthesized together.

---

## Why Single Vector Search Fails on Compound Queries

A vector embedding compresses an entire query into a single coordinate point. If a user asks:
> *"How does Company A's refund policy compare to Company B's warranty policy?"*

A single vector search lands in the geometric middle between Company A and Company B, failing to retrieve clean evidence for either.

```
Compound Question: "Compare 401k vs HSA limits for 2026"
                               │
                               ▼
            [ LLM Decomposition (JSON Parser) ]
                               │
         ┌─────────────────────┴─────────────────────┐
         ▼                                           ▼
Sub-Query 1: "401k limit 2026"             Sub-Query 2: "HSA limit 2026"
         │                                           │
         ▼                                           ▼
[ Vector Search 1 ]                         [ Vector Search 2 ]
         │                                           │
         ▼                                           ▼
Results for 401k                            Results for HSA
         │                                           │
         └─────────────────────┬─────────────────────┘
                               │
                               ▼
        [ Labeled Multi-Block Context Assembly for LLM ]
```

---

## Production Execution
- **Parallel Execution**: Independent sub-queries can execute concurrently (for example with `asyncio.gather()`), reducing wall-clock time relative to serial calls. Actual latency depends on the retriever, network, fan-out, and concurrency limits.
- **Context Partitioning**: Results are presented to the generation model in labeled blocks (`<context_subquery_1>`, `<context_subquery_2>`), preventing cross-contamination.

---

## Part of
← [[Query Transformation]]

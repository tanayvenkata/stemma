---
tags: [retrieval]
reviewed: 2026-10-11
---
# Multi-Query Retrieval

Generating multiple rephrased variations of the same user question to overcome vocabulary mismatches and probe different regions of embedding space.

---

## How It Works

```
User Query: "PTO policy?"
     │
     ▼
[ Fast LLM Prompt ] ──> Generates 3 Perspectives:
                          • Q1: "Paid time off allowance"
                          • Q2: "Vacation day accrual rules"
                          • Q3: "Time-off request process"
     │
     ▼
[ 3 Parallel Vector Searches ] ──> asyncio.gather(Search(Q1), Search(Q2), Search(Q3))
     │
     ▼
[ Union & Deduplicate ] ──> Unique candidate chunks by ID
     │
     ▼
[ Cross-Encoder Reranker ] ──> Top 5 Final Chunks
```

---

## When to Use Multi-Query
- **Short, vague queries** where user intent is ambiguous and a baseline run shows the single query missing evidence.
- **Enterprise Search with Diverse Jargon**: When marketing, legal, and engineering use different terms for the same product feature.

---

## Part of
← [[Query Expansion]]

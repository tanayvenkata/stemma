---
tags: [retrieval]
reviewed: 2026-10-11
---
# Query Expansion

Techniques that broaden or enrich an incoming search query with synonyms, related concepts, or sub-questions to improve retrieval recall.

---

## The 3 Expansion Archetypes

```
                             Query Expansion
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
1. [[Multi-Query Retrieval]]  2. [[Step-Back Prompting]]   3. Query Decomposition
 • Synonym variations          • High-level abstraction     • Sub-question partitioning
 • "PTO" -> ["vacation", ...]  • "NYC policy" -> "Company"  • "Compare A vs B" -> [QA, QB]
```

---

## Decision Framework: When to Expand

- **Vague or very short queries** (*"Benefits?"*): candidate for **[[Multi-Query Retrieval]]** to explore multiple interpretation angles; compare against the original query first.
- **Specific queries whose answer also depends on general policy or definitions**: candidate for **[[Step-Back Prompting]]**, after a baseline shows the broad documentation being missed.
- **Comparative / Compound Queries**: Use **[[Query Decomposition]]** (a sibling transformation owned by [[Query Transformation]]) to prevent semantic blending in vector space.

---

## Components

- [[Multi-Query Retrieval]]
- [[Step-Back Prompting]]

---

## Part of
← [[Query Transformation]]

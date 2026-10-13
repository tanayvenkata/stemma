---
tags: [retrieval]
reviewed: 2026-10-11
---
# Self-Query

Using an LLM to parse natural language queries into a **clean search string** AND a **structured metadata filter DSL** (JSON expression).

---

## The Mental Model: Structured SQL Meets Unstructured Vectors

When an authenticated user asks:
> *"Show me revenue reports published **after January 2025** for **client Acme Corp**."*

- **Naive Vector Search**: Embeds `"revenue reports published after January 2025 for client Acme Corp"`. Vectors cannot reliably guarantee exact numerical date comparisons or client isolation.
- **Self-Querying**: Deconstructs the query into two distinct components:

```
Trusted application context:                         User query:
{ "tenant_id": "tenant_123",                       "Show me revenue reports published
  "allowed_doc_ids": [...] }                         after January 2025 for Acme Corp"
              │                                                │
              │                                                ▼
              │                                  [ LLM Schema Extractor ]
              │                                                │
              │                         ┌──────────────────────┴─────────────────────┐
              │                         ▼                                            ▼
              │               Semantic search string:                    User-intent filter:
              │               "revenue reports"                          {
              │                                                           "created_at": { "$gte": "2025-02-01" },
              │                                                           "doc_type": "financial_report"
              │                                                         }
              └──────────────────────────────┬────────────────────────────┘
                                             ▼
                              [ Server-side policy composition ]
                              trusted ACL AND validated user filter
```

The LLM may extract search intent, but it must not choose or relax `tenant_id`, user identity, document ACLs, or other authorization scope. Those constraints come from authenticated server-side context and are conjoined outside model control. Validate the model-produced DSL against an allowlist of fields, operators, types, ranges, and complexity limits before execution.

Treat names such as “Acme Corp” in the query as semantic intent unless trusted application data maps them to an authorized internal identifier. Never authorize access from the text of the request.

## Execution with Vector Databases

Filtering behavior differs by database, index type, selectivity, and configuration. A system may pre-filter candidates, apply filters during approximate traversal, post-filter retrieved candidates, or combine these strategies. Therefore:

- Verify filter semantics and recall against exact-search ground truth.
- Test highly selective, empty-result, and adversarial filter cases.
- Recheck authorization before returning content; vector-store filters are defense in depth, not the entire security boundary.
- Log the trusted policy and user-intent filter separately so access decisions remain auditable.

See the `Filtered Retrieval` branch for search behavior. The `Production Security, Privacy & Tenant Isolation` note owns the broader authorization boundary.

---

## Part of
← [[Query Transformation]]

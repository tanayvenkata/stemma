---
tags: [retrieval]
reviewed: 2026-10-11
---
# Filtered Retrieval

Restricting vector similarity search to a subset of chunks that satisfy explicit metadata attributes (e.g. `tenant_id`, `created_at`, `user_role`, `department`).

---

## Filtering Strategies

```
1. Pre-Filtering (Metadata First)
   ├── Query the metadata SQL/Inverted index first to find matching doc IDs.
   └── Search within the permitted candidate set using exact or approximate search.
   *Tradeoff: Selective filters can make exact search cheap; very large candidate sets may need a filtered ANN strategy.*

2. Post-Filtering (Vector First)
   ├── Query the vector index for a candidate pool.
   └── Filter out all chunks that do not match metadata constraints.
   *Risk: Selective filters can remove most candidates, producing too few results even when matching vectors exist.*

3. Filter-Aware Approximate Search
   └── The engine combines metadata constraints with ANN search or iteratively scans more candidates.
   *Tradeoff: Behavior is engine- and index-specific. Satisfying the filter does not guarantee exact nearest-neighbor recall.*
```

There is no universal best implementation. Measure recall@k, latency, candidate shortfall, and resource use across the filter-selectivity distribution in the real workload. Compare approximate results against an exact-search sample. For example, the [pgvector README](https://github.com/pgvector/pgvector) documents filtering applied after the approximate index scan, plus iterative index scans (from 0.8.0), partial indexes, and partitioning as selectivity-dependent options (verified 2026-10).

## Authorization Is a Separate Boundary

Filtered retrieval can enforce an already-authorized candidate scope, but an LLM must not originate or weaken that scope.

1. Resolve the authenticated principal, tenant, roles, and document ACLs in trusted application code.
2. Compose those mandatory constraints with optional user-intent filters from self-query parsing.
3. Enforce policy before or within retrieval and recheck it before returning content.
4. Test cross-tenant leakage, stale ACL propagation, malformed filters, cache-key isolation, and side channels.

Collection-per-tenant, metadata filters, and vector namespaces can provide useful isolation layers; none is automatically a complete authorization system.

---

## When to Use Filtered Retrieval
- **Enterprise Multi-Tenancy**: Applying trusted tenant scope during retrieval (`tenant_id = trusted_tenant_id`).
- **Access-Control-Aware Retrieval**: Restricting candidates to documents already authorized for the principal.
- **Temporal Windows**: Restricting search to recent events (`created_at >= NOW() - 30_DAYS`).
- **Multi-Agent Simulations (Ego-Centric Perspective Filtering)**: Restricting memory retrieval to recorded observations such as `witnessed_by CONTAINS agent_id`. This supports the simulation's information model but does not prove that upstream observations were recorded correctly.

## See Also

The `Production Security, Privacy & Tenant Isolation` note covers the broader threat model, least privilege, and defense in depth.

---

## Part of
← [[Retrieval]]

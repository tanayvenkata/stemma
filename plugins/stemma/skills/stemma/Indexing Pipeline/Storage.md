---
tags: [indexing]
---
# Storage

Storage owns the durable relationship among source content, chunks, representations, metadata, and searchable indexes. A vector engine is one part of this system; it is not automatically the source of truth.

## Practical Starting Point

For a first system, keep canonical source artifacts and versioned metadata authoritative, store chunks and representations as reproducible derived records, and treat search indexes as rebuildable views. Add a specialized retrieval service, replication topology, or distributed data path only when measured scale, filtering, availability, or operational requirements justify it.

The stage is complete enough to proceed when an operator can trace any result to its source version, apply an update or deletion without leaving unexplained remnants, rebuild the search state from preserved inputs, and identify which versions produced a query result.

## Architecture Categories

| Category | Strength | Cost or risk | Use when |
|---|---|---|---|
| Embedded search library | Minimal dependency and direct algorithm control | You own persistence, replication, filtering, updates, and recovery | Local experiments or specialized systems with explicit lifecycle code |
| Purpose-built retrieval service | Integrated vector search, filtering, scaling, and operations | Additional service, data model, migration path, and vendor/runtime behavior | Retrieval requirements justify a dedicated operational boundary |
| Existing database/search platform with vector support | Reuses transactions, identity, backup, and operational expertise | Vector behavior may be less specialized; workload contention matters | Existing system meets measured retrieval and scale requirements |
| Object/source store plus rebuildable indexes | Clear durable source and recoverable derived state | Requires manifests, replay, and rebuild tooling | Indexes are derived artifacts and recovery correctness matters |

Do not select from product-name lists. Compare the capabilities and failure model required by the workload.

## Minimum Data Model

- immutable or versioned source object;
- stable document, region, chunk, and representation identifiers;
- parent/sibling/source relationships;
- trusted authorization and lifecycle metadata;
- parser, chunker, embedding, and index versions;
- content hashes and ingestion provenance;
- tombstone or deletion state;
- build manifest and reconciliation status.

## Decision Questions

1. Which store is authoritative, and can every index be rebuilt from it?
2. Are updates, deletes, and permission changes atomic enough for the risk?
3. Can filtering occur before or during candidate search without silent recall loss?
4. How are backups, point-in-time recovery, regional failure, and corruption tested?
5. Can old and new representation versions coexist during migration?
6. What are memory, storage, egress, build, query, and operator costs at realistic load?
7. Can per-result provenance and version be recovered for audit and citation?

Prefer the simplest architecture that satisfies measured correctness, lifecycle, recovery, and scale requirements. Adding a specialized database is justified by demonstrated capability or operational need, not by the presence of vectors.

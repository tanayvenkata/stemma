---
tags: [indexing]
reviewed: 2026-10-11
---
# Indexing Lifecycle & Migrations

Production indexing is a versioned data pipeline, not a one-time batch job. Every retrieved chunk should be traceable to source bytes and reproducible under a declared pipeline version.

## Identity and Lineage

Store stable document identity, content hash, source revision, parser/chunker/embedding versions, timestamps, and source offsets. Derive deterministic chunk IDs when possible. This enables idempotent retries, exact deletes, stale-version detection, citations, and replay.

## Change Handling

- **Create:** Parse and validate before making the version searchable.
- **Update:** Build the new version, atomically switch the active revision, then retire old chunks.
- **Delete:** Tombstone the source immediately and remove all derived chunks by stable identity.
- **Failure:** Keep partially built versions non-searchable; retry from durable stage outputs.

## Embedding and Schema Migration

Never mix incompatible vectors in one searchable field. Build a shadow index with the new pipeline, backfill it while dual-processing live changes into both generations, reconcile expected identities and ACLs, compare it against the current index on a fixed evaluation set, canary reads, and retain rollback until correctness and coverage are proven.

Track retrieval quality by query cohort, indexed-document coverage, filtered-search behavior, latency/QPS, storage/RAM, and update/delete correctness. Exact search on a representative subset provides ground truth for ANN recall.

## Operational Invariants

- A source has at most one active revision per policy scope.
- Every searchable chunk has complete lineage and an authoritative access-policy reference.
- Reprocessing the same source revision is idempotent.
- Deletes and policy changes propagate within a defined freshness SLO.
- Migration completion is proved by coverage and behavior, not only row counts.

## Evaluated by

Use the component-evaluation workflow in the `Evaluation` cluster to compare migration coverage, retrieval behavior, latency, and rollback safety.

## Part of
← [[Indexing]]

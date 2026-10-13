---
tags: [production]
---
# Production Data Lifecycle, Lineage & Freshness

The retrieval index is a derived view, not the source of truth. It must be possible to explain, rebuild, reconcile, and delete every indexed artifact.

## Identity and Lineage

Use stable source identifiers plus explicit versions. A content hash is useful for deduplication, but reprocessing must also account for parser, chunker, metadata schema, embedding model, and policy versions.

```text
source record/version
  → raw immutable artifact
  → parse run/version
  → chunk IDs and offsets
  → embedding/index version
  → retrieved evidence
  → answer and citations
```

Keep enough provenance to map a citation back to the exact source version and to find every derived object when a source changes or must be deleted.

## Ingestion Correctness

- Separate ingestion from request serving; use bounded queues for expensive OCR, parsing, and embedding.
- Make each stage idempotent and checkpointed. Retrying a partial job must not duplicate chunks or lose deletes.
- Quarantine corrupt or unsupported inputs with actionable reason codes.
- Validate parse coverage, page/table structure, metadata, language, and ACLs before publication.
- Publish a new index generation only after completeness and integrity checks pass.

## Updates and Deletes

Model create, update, delete, permission change, and legal hold as first-class events. Deletes must propagate through raw stores, chunks, embeddings, graph edges, caches, replicas, and backups according to policy. Use tombstones or version barriers when eventual consistency could resurrect removed content.

## Freshness and Reconciliation

Track timestamps for source observation, ingestion start, indexing completion, and read availability. Reconcile independently:

- expected source records vs ingested records
- ingested versions vs indexed versions
- ACL state vs searchable metadata
- deletes/tombstones vs remaining derived artifacts

Freshness alerts should be tied to the source's change rate and user promise. Periodically rebuild a sample or full index from authoritative data and compare it with the incremental path.

## Recovery

Document restore order and test it. Back up authoritative inputs, configuration, metadata, and lineage; a vector index may be rebuilt if the inputs and transformation versions are preserved. Define recovery-point and recovery-time objectives from business impact.

## Part of
← [[RAG Production]]

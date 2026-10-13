---
tags: [indexing]
---
# Indexing

Indexing turns versioned content representations into searchable structures. The design must preserve retrieval quality while meeting build, update, memory, latency, filtering, deletion, and recovery requirements.

## When This Enters the Build

Use this after the first versioned chunks and representations exist. Begin with the simplest searchable structure that can run exact or otherwise trustworthy baseline retrieval; do not start by tuning an approximate index before confirming that the representation retrieves the right neighbors.

Leave this stage with a reproducible build manifest, reconciled item counts and identities, measured exact-versus-approximate loss where applicable, defined filter/update/delete behavior, and a recovery path. Return when scale, filters, update rate, representation, latency, memory, or failure requirements change.

## Separate the Search Structures

- **Dense vector indexes** organize geometric neighbors for semantic retrieval.
- **Sparse inverted indexes** organize terms and learned lexical weights for exact and vocabulary-sensitive retrieval.
- **Metadata indexes** support typed filtering, routing, freshness, and operational lookup.
- **Source stores** retain canonical content, provenance, relationships, and versions returned after search.

A production system may combine them, but each has its own consistency and failure modes. Search success does not prove that the underlying source version, permissions, or returned payload is correct.

## Index Contract

Record representation version, distance/scoring convention, indexed fields, filter semantics, build parameters, source snapshot, expected item count, update/delete behavior, and recovery procedure. Reconcile expected and indexed identities after every build.

Choose an exact or approximate dense index from the measured quality–latency–memory frontier. Exact search provides a diagnostic reference for approximation loss; approximate indexes trade some neighbor fidelity for resource savings and must be tuned on production-like filters, concurrency, and updates.

## Build and Selection Workflow

1. Build a small exact or transparent baseline and reconcile it against the source/chunk manifest.
2. Verify scoring direction, distance convention, filters, payload resolution, and deletion behavior with known cases.
3. Measure retrieval quality before optimizing search infrastructure.
4. Introduce an approximate, sparse, metadata, or composite index only for a demonstrated capability or resource requirement.
5. Compare quality, tail latency, throughput, memory, build/update cost, and failure behavior under realistic filters and concurrency.
6. Shadow-build incompatible changes, reconcile the new generation, shift reads gradually, and retain rollback.

If exact search fails on the same chunks and labels, repair the representation or evidence units. If exact search succeeds but the production index fails, tune or replace the index. This boundary prevents expensive infrastructure work from masking an upstream retrieval problem.

## Components

- [[Vector Index]]
- [[Sparse Index]]
- [[Metadata Index]]
- [[Indexing Lifecycle & Migrations]]

## Next

→ [[Storage]]

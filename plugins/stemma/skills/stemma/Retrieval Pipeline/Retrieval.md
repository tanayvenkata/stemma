---
tags: [retrieval]
---
# Retrieval

Retrieval produces a candidate set of evidence under relevance, authorization, freshness, latency, and cost constraints. It is a policy over representations, indexes, filters, fusion, and search effort—not one default algorithm.

## Representation Families

| Family | Strength | Limitation |
|---|---|---|
| Dense single-vector | semantic similarity and efficient indexing | can blur exact identifiers and fine-grained interactions |
| Sparse lexical | exact terms, transparent token contributions | vocabulary mismatch and analyzer dependence |
| Learned sparse | lexical index with learned expansion/weights | model and index complexity; vocabulary behavior must be audited |
| Multi-vector/late interaction | fine-grained token or patch matching | larger indexes and more expensive scoring |
| Structured/relational | explicit graph, SQL, temporal, or metadata constraints | depends on reliable schema and routing |

Multimodal and reasoning-intensive retrieval extend these choices; they do not eliminate the need for in-domain relevance labels.

## Compose Only What Earns Its Place

- dense or sparse retrieval alone can be the correct baseline;
- fusion helps when methods recover complementary evidence;
- filtering enforces trusted scope and may improve precision, but can remove valid evidence;
- cascades spend additional computation only after a broad candidate stage;
- calibration maps scores/features to answer, abstain, escalate, or retrieve-more decisions.

## Retrieval Contract

Version corpus, chunks, representations, indexes, analyzers, filters, fusion, candidate depth, scoring conventions, and fallback. Retain per-query rankings and source identities so missed evidence can be localized.

Evaluate pooled relevance judgments, required-evidence coverage, early ranking, unjudged candidates, false exclusions, authorization invariants, latency percentiles, throughput, failure behavior, and downstream context utility. Sweep candidate depth as a resource frontier; no fixed top-$K$ is universally correct.

## Components

- [[Dense Retrieval]]
- [[Sparse Retrieval]]
- [[Hybrid Fusion]]
- [[Filtered Retrieval]]
- [[Cascading Retrieval]]
- [[Retrieval Calibration, Abstention & Authorization]]

## Next

→ [[Post-Retrieval Processing]]

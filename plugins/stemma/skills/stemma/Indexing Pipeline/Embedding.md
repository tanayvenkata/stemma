---
tags: [indexing]
---
# Embedding

An embedding model maps a query or content unit into vectors whose geometry is trained to support a task such as retrieval. Similarity is useful only insofar as nearby vectors correspond to evidence users need; a vector is not a semantic truth representation.

## Representation Contract

Version together:

- model and revision;
- query and document instructions or prefixes;
- tokenizer, truncation, pooling, and preprocessing;
- output dimensionality and any supported truncation scheme;
- normalization and distance function;
- language, modality, and sequence-length assumptions;
- precision or quantization;
- corpus, chunking, and index version built from the vectors.

Vectors produced under incompatible contracts must not share one searchable field. During migrations, build a parallel versioned field or index and compare it before switching reads.

## Candidate Selection

Public benchmarks are screening evidence, not deployment evidence. Use retrieval-specific results from heterogeneous and task-relevant benchmarks, then evaluate candidates on the target corpus. Include exact identifiers, paraphrases, domain ambiguity, languages, long inputs, hard negatives, and reasoning-intensive queries that surface-form matching may miss.

Compare:

- exact-search retrieval quality before approximate-index effects;
- behavior by query and document slice;
- maximum usable input and truncation failures;
- dimension, storage, memory, build time, and query latency;
- batch throughput, concurrency, privacy, licensing, and operational control;
- stability under quantization and the intended distance metric.

Hosted and self-operated models are deployment choices, not quality categories. Evaluate data transit, service versioning, observability, capacity, unit economics, hardware, and maintenance alongside task results.

## Geometric Choices

For unit-normalized vectors, cosine similarity and dot product produce the same ranking:

$$
\frac{A}{\lVert A\rVert_2}\cdot\frac{B}{\lVert B\rVert_2}=\cos(\theta)
$$

Normalize only when the model contract and index metric require it. Vector magnitude may carry signal for some representations.

Some models support nested or otherwise truncatable representations. Smaller vectors reduce storage and bandwidth, but retained quality is model-, corpus-, task-, and quantization-dependent. Compare each allowed dimension with the full representation using identical cases.

## Decision Rule

Adopt a representation when its protected in-domain gains are meaningful, important slices and exact-match needs remain covered, and the complete quality–latency–storage–operations tradeoff is preferable. If exact vector search fails, inspect representation or chunks; if exact search succeeds but approximate search fails, inspect the index.

## Components

- [[Model Selection Criteria]]
- [[Dimensionality Tradeoffs]]
- [[Normalization]]
- [[Matryoshka Embeddings]]
- [[Late Interaction Models]]

## Next

→ [[Indexing]]

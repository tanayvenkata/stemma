---
tags: [indexing]
---
# Matryoshka Embeddings

Matryoshka Representation Learning trains an embedding so selected prefixes of the vector remain useful representations. A system can store or search a supported prefix dimension without retraining a separate model, trading representation capacity for memory, bandwidth, and compute.

This property must be part of the model's training contract. Arbitrarily slicing a conventional embedding is not Matryoshka retrieval.

## Mechanics

For a full vector $v\in\mathbb{R}^D$, a supported prefix uses:

$$
v_{1:d}=[v_1,\ldots,v_d], \qquad d<D
$$

Apply the model's required normalization after truncation. Query and indexed document vectors compared in one field must use the same dimension, preprocessing, normalization, and metric.

## Deployment Patterns

- store only a smaller supported prefix when its measured quality loss is acceptable;
- retain full vectors and build a smaller parallel index for candidate generation;
- search a compact prefix, then rescore candidates with full vectors or another ranking model;
- vary dimension by versioned index, not silently within one vector field.

Full-dimensional rescoring requires the full representation to be stored or reproducible. It cannot recover information that was discarded and never retained.

## Experiment

1. Freeze chunks, queries, relevance labels, metric, and index algorithm.
2. Compare only dimensions explicitly supported by the model.
3. Re-normalize as required and build independent indexes.
4. Measure paired retrieval quality by slice, memory, storage, build/query latency, and transfer cost.
5. If using two stages, measure candidate recall before full-vector or reranker lift.
6. Test quantization jointly because dimension and precision losses can interact.

There is no universal retained-quality percentage or best prefix dimension. Choose from the measured quality–resource frontier and keep rollback through migrations.

Primary reference: [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147).

## Part of

← [[Embedding]]

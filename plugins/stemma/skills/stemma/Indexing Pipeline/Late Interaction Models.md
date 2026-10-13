---
tags: [indexing]
---
# Late Interaction Models

Late-interaction retrieval encodes queries and documents into multiple token-, region-, or patch-level vectors and combines their pairwise matches at query time. It preserves finer-grained interactions than one vector while allowing document representations to be precomputed.

A common MaxSim form is:

$$
\operatorname{score}(q,d)=\sum_{i\in q}\max_{j\in d} q_i^\top d_j
$$

## Tradeoff

| Compared with | Potential gain | Added cost |
|---|---|---|
| single-vector retrieval | fine-grained term/region matching and reduced representation bottleneck | many vectors per document, larger index, more scoring |
| cross-encoder reranking | precomputable document side and broader candidate search | less full cross-attention and still costlier than a bi-encoder |

Text systems such as ColBERT and visual-document descendants illustrate the family; names and implementations are examples, not selection rules.

## Evaluation

Compare with a strong single-vector and reranking baseline on fixed labels. Measure required-evidence coverage, ranking, token/patch attribution quality, index size, compression loss, build/update/query cost, latency under load, and downstream outcomes. For multimodal pages, label decisive regions rather than only document identity.

Adopt when fine-grained retrieval produces meaningful value that cannot be recovered more simply through better chunks, hybrid retrieval, or reranking.

Primary reference: [ColBERT](https://arxiv.org/abs/2004.12832).

## Part of

← [[Embedding]]

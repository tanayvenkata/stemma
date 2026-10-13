---
tags: [indexing]
---
# SPLADE

SPLADE is a learned sparse retrieval family. A transformer assigns weights to vocabulary terms for queries and documents, including expansion terms not literally present in the input, and the resulting sparse vectors are searched with inverted-index machinery.

Compared with BM25, learned expansion can bridge vocabulary mismatch while retaining term-level score decomposition. It also adds model inference, training/domain assumptions, index growth, and possible misleading expansions.

## Evaluation

Freeze corpus, queries, pooled relevance judgments, analyzer, and candidate depth. Compare BM25, learned sparse, dense, and justified fusion. Measure required-evidence coverage, ranking, unique relevant contributions, expansion sparsity, index size, build/query cost, language/domain slices, and harmful expansion examples.

Use learned sparse retrieval when it adds evidence beyond strong lexical and dense baselines and its operational cost is justified.

Primary reference: [SPLADE v2](https://arxiv.org/abs/2109.10086).

## Part of

← [[Sparse Index]]

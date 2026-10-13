---
tags: [retrieval]
---
# Dense Retrieval

Dense retrieval embeds a query and searchable units into continuous vectors and ranks them under a compatible distance function and index.

For unit-normalized vectors, dot product equals cosine similarity:

$$
q\cdot d=\sum_{j=1}^{D}q_jd_j
$$

## Strengths and Boundaries

Dense representations can recover paraphrase, conceptual similarity, multilingual alignment, and domain relationships learned by the model. They may blur exact identifiers, rare entities, numeric distinctions, negation, or concepts outside their training/adaptation distribution.

## Evaluation

Version the complete query/document representation contract. Compare exact search before approximate-index effects, then production search under realistic filters and load. Use pooled in-domain judgments with paraphrase, identifier, reasoning-intensive, language, hard-negative, and no-answer slices. Measure required-evidence coverage, ranking, latency, cost, and downstream utility.

Add sparse retrieval, query transformation, or fine-tuning only for diagnosed failures. Dense retrieval alone may be the simplest adequate policy.

## Part of

← [[Retrieval]]

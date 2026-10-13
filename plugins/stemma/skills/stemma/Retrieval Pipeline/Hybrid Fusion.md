---
tags: [retrieval]
---
# Hybrid Fusion

Hybrid fusion combines rankings from retrieval methods that may recover complementary evidence, commonly lexical and dense search. It is useful only when complementarity survives fusion and downstream use.

## Fusion Choices

- **Score fusion:** normalize or calibrate scores onto a comparable scale, then combine them.
- **Rank fusion:** combine rank positions without assuming comparable raw scores.
- **Learned fusion:** train a policy from query features and relevance labels.
- **Conditional fusion:** invoke additional retrievers only for diagnosed query slices.

Reciprocal Rank Fusion uses:

$$
\operatorname{RRF}(d)=\sum_{r\in R}\frac{1}{k+\operatorname{rank}_r(d)}
$$

The constant $k$ controls how strongly top ranks dominate; it is a tunable parameter, not a universal default.

## Evaluation

Pool candidates from every method before judging relevance. Compare each retriever and fusion on paired cases, unique relevant evidence contributed, required-evidence coverage, ranking, candidate volume, latency, cost, and downstream outcomes. Tune only on development cases.

Fusion can worsen results by adding distractors or drowning a strong retriever. Retain a single method when the second adds no meaningful complementary evidence.

Primary reference: [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf).

## Part of

← [[Retrieval]]

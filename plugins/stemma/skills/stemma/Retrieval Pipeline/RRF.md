---
tags: [retrieval]
---
# RRF

Reciprocal Rank Fusion combines result lists using rank positions rather than incomparable raw scores:

$$
\operatorname{RRF}(d)=\sum_{m\in M}\frac{1}{k+r_m(d)}
$$

$r_m(d)$ is the one-based rank in method $m$; absent documents contribute nothing. The constant $k$ smooths the advantage of very high ranks. Its value and each input depth must be tuned for the task.

RRF avoids score normalization, but it is not guaranteed to reward consensus correctly: one strong retriever can be diluted, duplicate document identities can be mishandled, and relevant items outside input depths remain absent.

Pool candidates before relevance judging. Compare each input ranker and fusion on paired cases, unique relevant evidence, required-evidence coverage, downstream outcomes, latency, and candidate volume.

Primary reference: [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf).

## Part of

← [[Hybrid Fusion]]

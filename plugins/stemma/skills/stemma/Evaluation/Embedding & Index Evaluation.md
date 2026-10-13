---
tags: [evaluation]
---
# Embedding & Index Evaluation

Separate two questions: does the representation place relevant evidence near the query, and does the search index recover those neighbors under production constraints? Public benchmarks shortlist candidates; in-domain labels decide.

## When This Enters the Build

Use this after chunking is versioned and query–chunk judgments can be materialized. First compare representations with exact search; only then compare approximate-index settings against that exact result. Leave with a representation/index pair, its quality–latency–memory frontier, and update/rebuild behavior.

Return when the corpus domain, language, modality, chunking policy, representation, distance convention, quantization, or index implementation changes. Do not replace embeddings to fix evidence that parsing or chunking never made searchable.

## Cases and Labels

Begin only after a chunking policy has been selected and versioned. Freeze those chunks and materialize query–chunk relevance judgments from the durable source-region evidence, retaining the mapping so the judgments can be regenerated after rechunking. Include exact terminology, paraphrase, abbreviations, identifiers, numbers, languages in scope, domain ambiguity, near-duplicate distractors, and out-of-domain queries. Use graded labels when passages differ in usefulness.

Pool top results from meaningfully different retrieval runs for annotation so labels do not favor one candidate. Unjudged results are unknown, not automatically irrelevant. Separate tuning from protected evaluation, including any exemplars or queries used for adaptation.

For multimodal or multi-vector representations, label the decisive page, region, frame, timestamp, table, or patch—not only a document ID. Evaluate cross-modal queries separately from within-modal retrieval and charge fine-grained late interaction for its index, memory, and query cost.

## Factor the Experiment

1. **Representation:** run exact nearest-neighbor search for each embedding candidate while holding chunks, queries, labels, distance convention, and depth fixed.
2. **Index:** for a selected representation, compare approximate-index configurations against exact search on identical queries.

This distinguishes representation loss from approximation loss. Record dimensionality, normalization, truncation, query/document instructions, quantization, and preprocessing as part of the candidate.

## Metrics and Diagnosis

| Signal | Meaning |
|---|---|
| Hit Rate/Recall@K | required evidence reachable in candidate budget |
| MRR | first relevant result appears early |
| NDCG@K | graded ordering quality |
| ANN recall versus exact search | loss caused by approximation |
| Query/index latency percentiles | online and rebuild feasibility |
| Memory, index size, build/update cost | operational footprint |
| Failure rate and freshness lag | update and fault behavior |

High exact-search quality with poor ANN recall points to the index. Weak exact-search quality points to representation, labels, or chunks. Strong recall with weak early ordering suggests fusion or reranking before replacement.

## Practical Protocol

1. State the domain behavior and smallest meaningful improvement.
2. Shortlist using task-relevant public evidence plus license, deployment, and resource constraints—not one leaderboard rank.
3. Embed the immutable corpus independently and reconcile expected versus indexed items.
4. Run exact evaluation, then production-like approximate search with filters and concurrency.
5. Tune only on a development set; evaluate the selected setting once on protected cases.
6. Stress updates, deletes, duplicate IDs, dimension/configuration mismatch, failover, and freshness.
7. Recalibrate any similarity threshold after representation changes; raw similarity is not a probability and does not transfer across candidates.
8. Compare paired query outcomes and the quality–latency–memory frontier.

## Decision Rule

Adopt a combination when it yields a credible, product-relevant improvement on protected in-domain cases, respects must-not-regress slices, and occupies an acceptable operational frontier. Prefer the simpler or cheaper candidate when quality is practically indistinguishable.

Change embeddings when exact-search failures expose missing domain distinctions. Change the index when exact search succeeds but approximate search loses neighbors or violates constraints. Change neither when required evidence was never encoded as a usable chunk. Treat projection plots as hypothesis generators, not retrieval evidence, and document expansion as a separate index variant.

Primary references: [MTEB](https://arxiv.org/abs/2210.07316), [BEIR](https://arxiv.org/abs/2104.08663), and [TREC relevance judgments](https://trec.nist.gov/data/reljudge_eng.html).

## Part of

← [[Component Evaluation Harness]]

---
tags: [evaluation]
---
# Retrieval & Metadata Evaluation

Retrieval evaluation asks whether relevant evidence is found, ranked early, and scoped correctly before generation obscures the cause. Evaluate the search policy against a fixed corpus and judgments, then test whether its quality–latency–context tradeoff improves the product.

## When This Enters the Build

Use this once a searchable baseline index and chunk-level judgments exist. Begin with the simplest direct retriever and sweep the candidate budget; introduce sparse retrieval, fusion, metadata policies, or other mechanisms only for an observed failure slice. Leave with a retrieval policy, candidate budget, empty-result behavior, and evidence showing which query classes it helps or harms.

Run retrieval metrics frequently because they are cheap and diagnostic, but recheck finalists through the product’s downstream context or ranked-results surface. High recall obtained by flooding the next stage is not automatically useful.

## Cases and Relevance Labels

Represent the query distribution, not merely easy fact lookups. Include lexical matches, paraphrases, identifiers, ambiguous terms, rare topics, multi-evidence questions, freshness-sensitive requests, explicit metadata constraints, and queries that should return nothing.

Include reasoning-intensive cases where relevance cannot be recognized from surface similarity alone. If query-time reasoning, decomposition, or hypothetical text is used, preserve that intermediate representation and evaluate intent/constraint preservation, evidence gain, latency, and answer leakage against the original-query baseline.

For each query label chunks or stable source regions as irrelevant, supporting, or directly sufficient where graded relevance matters. Record all required evidence for synthesis cases. Pool candidates from lexical, semantic, hybrid, and prior-production runs for annotation; otherwise the judged set may favor the system that produced it. Track unjudged candidates explicitly.

For metadata tests, label the user’s intended scope independently of the router or filter: permitted sources, tenant, document type, jurisdiction, language, effective date, and valid alternatives. Include missing, stale, malformed, contradictory, and unauthorized metadata.

## Choose Metrics from the Task

| Need | Primary signal | Diagnostic companion |
|---|---|---|
| At least one usable passage | Hit Rate@K or MRR | miss categories |
| Every required evidence item | set/region Recall@K | uncovered requirements |
| Graded ordering | NDCG@K | helped/harmed queries |
| Clean context budget | Precision@K, evidence-token ratio | duplicate evidence |
| Correct scope | inclusion and false-exclusion rates | confusion by metadata field |
| Safe no-answer behavior | false-positive retrieval/abstention utility | score distribution by slice |
| Operational fitness | latency percentiles, throughput, error rate | cost and fallback rate |

K is a product resource, not a universal constant. Sweep it against evidence coverage, latency, reranking cost, and final context budget.

## Controlled Protocol

1. State the failure and mechanism—for example, lexical retrieval should recover exact policy codes that semantic search misses.
2. Freeze chunks, query set, judgments, filters, and evaluation code.
3. Compare a simple baseline with justified dense, sparse, hybrid, or other candidates. For fusion, tune parameters only on development cases.
4. Retain complete per-query rankings and compare paired differences, uncertainty, and important slices.
5. Test metadata as a policy: no metadata, soft boost, and hard filter where each is legally or semantically admissible.
6. Measure false exclusions separately. Precision gains achieved by hiding valid evidence are not improvements.
7. Run production-like concurrency, updates, permissions, timeouts, and empty-result behavior.
8. Send finalist rankings through a fixed downstream context/generation setup to verify that retrieval lift survives composition.

## Failure Interpretation

- Relevant chunks absent at all K: inspect corpus coverage, parsing, chunking, representation, or filters.
- Relevant chunks present but late: ranking/fusion problem; a reranker may help if candidate recall is already sufficient.
- Hard filter improves precision but harms valid scope: metadata inference or policy is too aggressive.
- Offline gains disappear downstream: inspect context budget, redundancy, evidence order, and question type.
- Improvement exists only on queries used to tune fusion: selection overfit.

## Decision Rule

Adopt a retrieval policy when its protected-set gains are meaningful on the motivating tasks, no high-risk slice violates a predeclared constraint, and latency, cost, and operational complexity are acceptable. Prefer the simplest policy on an indistinguishable frontier. Change retrieval when evidence exists as good searchable units but is not surfaced appropriately; repair upstream components when those units do not exist.

Primary references: [TREC’s test-collection and pooling practice](https://trec.nist.gov/howto.html) and [BEIR’s heterogeneous retrieval evaluation](https://arxiv.org/abs/2104.08663).

## Part of

← [[Component Evaluation Harness]]

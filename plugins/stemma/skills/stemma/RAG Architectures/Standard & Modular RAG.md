---
tags: [architectures]
---
# Standard & Modular RAG

The reference architecture is a transparent, replaceable sequence:

```text
ingest → parse → chunk → embed/index
query → retrieve → rerank/filter → prepare context → generate → validate
```

“Standard” does not mean naive. Each stage can use strong components, but the request follows a legible path with minimal conditional control flow. “Modular” means every stage has an explicit contract, version, trace, and component evaluation so it can be replaced without redesigning the whole system.

## What "Standard" Means Here

Standard RAG is the comparator for the other notes: one known evidence plan is selected in advance, then retrieval and generation follow a legible path. It can still use authorization filters, hybrid retrieval, reranking, context compression, citation mapping, and an answerability policy. Those improve components inside the path; they do not change its basic control flow.

```text
query → retrieve once → select/assemble evidence → answer or abstain
```

The other architectures earn their complexity only when they change that contract: they select among distinct evidence plans, test whether a retrieved set is sufficient, represent relationships explicitly, or choose the next evidence request after seeing an observation.

## Why Start Here

- It provides the cheapest and clearest experimental baseline.
- Component failures remain attributable.
- Latency, cost, and authorization paths are easier to reason about.
- More complex architectures can be evaluated by their incremental lift over it.

## Reference Contracts

| Boundary | Minimum contract |
|---|---|
| Indexing → Retrieval | stable document/chunk IDs, embedding/index version, metadata and ACLs |
| Retrieval → Generation | ordered evidence, scores, source IDs, authorization scope, token budget |
| Generation → Validation | answer or structured payload, claim/citation mapping, model/prompt version |
| Evaluation → Production | candidate manifest, regression evidence, release and rollback criteria |

## Escalation Test

Do not add a router, graph, corrective fallback, reflection gate, or agent loop merely because it is available. Escalate when:

1. a repeatable failure remains after the relevant components are reasonably optimized;
2. the failure is structural rather than a local configuration defect;
3. a candidate architecture has a falsifiable hypothesis and simpler baseline;
4. measured quality or capability justifies added cost, latency, state, and failure modes.

Examples:

- Global corpus questions remain weak despite strong local retrieval → test hierarchical or graph retrieval.
- Distinct query classes require incompatible retrieval plans → test a calibrated router.
- Multi-hop questions require evidence acquired conditionally → test an iterative loop.
- Retrieval sometimes adds harmful noise → test a retrieval gate against unconditional and no-retrieval baselines.

## Evaluated by

Use the component and end-to-end workflow in the Evaluation cluster. Report architectural lift by query slice, not only one aggregate score.

## Part of

← [[RAG Architectures]]

---
tags: [architectures]
reviewed: 2026-10-11
---
# RAG Architectures

A RAG architecture is a hypothesis about **control flow and evidence topology**: when to retrieve, which sources and representations to use, whether to iterate, and how to verify or stop. It composes the indexing, retrieval, and generation pipelines; it does not replace them.

Start with [[Standard & Modular RAG]] unless requirements already rule it out. Then use [[RAG System Design & Improvement Loop]] to test whether failures are local component problems or evidence that the control flow itself should change.

## Design by Capability, Not Brand Name

| Design dimension | Baseline | Escalation question |
|---|---|---|
| Retrieval timing | retrieve once | Should retrieval be skipped, repeated, or triggered mid-generation? |
| Evidence topology | independent passages | Do relationships, hierarchy, time, or corpus-wide themes matter? |
| Source composition | one corpus | Must the system route across search, SQL, APIs, graphs, or distinct corpora? |
| Correction | pass retrieved evidence forward | Should weak evidence trigger filtering, abstention, or another source? |
| Execution | one planned path | Does the next evidence request depend on an intermediate result? |
| Parallelism | one context and answer path | Would diverse evidence subsets and drafts improve the quality/latency frontier? |

These dimensions compose. A system can use graph retrieval inside an agentic loop and apply a corrective gate to its evidence. Treat each added mechanism as a separate hypothesis so its contribution can be removed or measured.

## Reference Architectures

| Reference | Mechanism worth learning | Test it when |
|---|---|---|
| [[Standard & Modular RAG]] | transparent single-pass contracts | establishing the baseline or serving bounded evidence tasks |
| [[Adaptive & Composite Retrieval]] | bounded routing among evidence plans and source types | query classes need different retrieval, document, or structured-source plans |
| [[Evidence Sufficiency & Correction]] | evidence-quality gate with corrective actions | retrieval failures can be detected early enough to change course |
| [[Knowledge Graph RAG]] | graph/summary representations and structured traversal | relations or corpus-wide sensemaking defeat passage retrieval |
| [[Agentic RAG]] | stateful, conditional evidence acquisition and tool use | tasks require a sequence that cannot be planned completely in advance |

Named papers are concrete reference designs, not permanent market categories. Copy the mechanism only after reproducing its motivating failure on your workload.

## Selection Instinct

```text
Can a strong one-shot evidence path answer the task?
→ [[Standard & Modular RAG]]

Do recognizable query classes need different known evidence plans?
→ [[Adaptive & Composite Retrieval]]

Can the selected evidence be plausible yet insufficient for a safe answer?
→ [[Evidence Sufficiency & Correction]]

Is the answer fundamentally a relationship, path, temporal constraint, or corpus-wide pattern?
→ [[Knowledge Graph RAG]]

Does each intermediate observation determine the next useful evidence request?
→ [[Agentic RAG]]
```

## Architecture Selection Protocol

1. **Define the task distribution and constraints.** Include answerability, source authority, relationships, freshness, permissions, latency, cost, and consequences of error.
2. **Implement a legible comparator.** Usually this is modular single-pass RAG; if it is infeasible, preserve the simplest valid alternative.
3. **Localize failure.** Use component oracles and controlled substitutions before blaming the architecture.
4. **State one structural hypothesis.** Name the query slice expected to improve and the new mechanism responsible.
5. **Compare paired end-to-end results.** Measure quality, abstention, latency, cost, state growth, security surface, and new failure modes.
6. **Keep removal criteria.** Complexity that provides no durable lift should be deleted, even if the pattern is fashionable.

## Durable Families Beyond the Reference Papers

- **Adaptive/router RAG** selects retrieval plans by query class and calibrated evidence need. [Self-RAG](https://arxiv.org/abs/2310.11511) is a research reference for a learned, fine-tuned version of this controller; production systems normally begin with explicit gates and evidence checks instead. See [[Adaptive & Composite Retrieval]].
- **Iterative/interleaved RAG** alternates evidence acquisition and reasoning under explicit budgets and stopping rules.
- **Hierarchical and multi-representation RAG** retrieves summaries, parents, chunks, tables, or images at different stages.
- **Federated/composite RAG** combines keyword, vector, SQL, graph, API, and multi-corpus sources while preserving authorization and provenance.
- **Temporal RAG** represents validity intervals, supersession, event time, and as-of queries.
- **Long-context hybrids** use retrieval for selection and provenance while retaining broader context for synthesis.

## Branches

- [[Standard & Modular RAG]]
- [[RAG System Design & Improvement Loop]]
- [[Adaptive & Composite Retrieval]]
- [[Evidence Sufficiency & Correction]]
- [[Knowledge Graph RAG]]
- [[Agentic RAG]]

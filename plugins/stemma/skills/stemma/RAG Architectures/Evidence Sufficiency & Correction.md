---
tags: [architectures]
---
# Evidence Sufficiency & Correction

Evidence sufficiency and correction insert an evidence-quality decision between retrieval and generation. Corrective RAG (CRAG) is one paper-specific design using a retrieval evaluator, three confidence regions, selective evidence refinement, and external search when local evidence is weak. The durable lesson is the **measure → decide → correct** control pattern, not a universal score or fallback source.

## How It Differs from Standard RAG

Standard RAG may rerank retrieved candidates, but reranking asks which candidates are most relevant *within the retrieved pool*. It does not decide whether the final evidence set contains every authoritative claim needed for an acceptable answer. A set can contain the best available passages and still omit a required rule, use the wrong jurisdiction, or be stale.

```text
standard: retrieve → rerank/select → answer or ordinary abstention
corrective: retrieve → rerank/select → assess evidence-set sufficiency
                                         ├─ answer
                                         ├─ one bounded correction → reassess
                                         └─ abstain or escalate
```

The distinct architecture change is an explicit, testable insufficient-evidence state with permitted corrective actions. Keep those actions bounded and source-authorized; an unbounded retrieve-and-reflect loop becomes [[Agentic RAG]].

## Control Flow

```text
query → retrieve → evaluate evidence
                       ├─ sufficient → refine/select → generate
                       ├─ uncertain  → supplement, retry, or abstain
                       └─ inadequate → replace source, escalate, or abstain
```

Define the actions from the application's source policy. External search may be prohibited, less authoritative, privacy-sensitive, or unavailable; alternatives include another internal corpus, a structured system of record, human escalation, or an explicit unanswerable response.

## Build the Gate

1. Define labels from downstream usefulness: whether the evidence contains sufficient, authoritative support for an acceptable answer.
2. Label representative retrieval sets, including partial, conflicting, stale, poisoned, and unanswerable cases.
3. Train or prompt an evaluator, but retain its score as a prediction rather than truth.
4. Calibrate decision regions against the cost of false acceptance, unnecessary fallback, and abstention.
5. Attach a typed action and provenance policy to each region.
6. Re-evaluate after retriever, corpus, evaluator, or query-distribution changes.

Per-passage relevance is not identical to set sufficiency. A set can contain individually relevant passages yet omit a required claim, or contain one highly authoritative answer among distractors.

## Evidence Refinement

The original design decomposes retrieved documents into smaller “knowledge strips,” filters them, and recomposes context. In a general implementation, preserve source offsets and citations, avoid stripping qualifiers or surrounding definitions, and compare refinement against reranking plus ordinary context selection. More granular evidence is not automatically more faithful.

## Evaluation and Decision Rule

Measure gate calibration, false-accept and false-correct rates, answer quality after each action, abstention, source authority, citation integrity, latency, and cost. Include oracle experiments:

- give generation known-sufficient evidence to isolate the gate from generation;
- give the gate gold relevance/sufficiency labels to estimate its possible value;
- compare no correction, retry, alternate-source, and abstention policies on the same cases.

Keep the gate when it improves expected task utility or risk on the target slices—not because it reproduces the paper's three labels.

## Primary Source

- Corrective Retrieval Augmented Generation: https://arxiv.org/abs/2401.15884

## Part of

← [[RAG Architectures]]

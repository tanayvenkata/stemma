---
tags: [architectures]
---
# Adaptive & Composite Retrieval

Adaptive and composite retrieval selects a bounded evidence plan from known alternatives. It is not a free-form agent: trusted routing policy or a calibrated classifier chooses a plan, each plan has an explicit contract, and the system returns to a deterministic answer path.

```text
request + identity + mandatory scope
        ↓
classify evidence need and query shape
        ↓
choose authorized plan
  ├─ no retrieval / direct transformation
  ├─ passage retrieval + reranking
  ├─ whole-document or long-context retrieval
  ├─ structured query or API lookup
  └─ one or more authorized corpora
        ↓
assemble evidence with provenance → answer, abstain, or escalate
```

## How It Differs from Standard RAG

Standard RAG uses one evidence plan for every request. A simple query router that only rewrites a query or selects corpus A versus B can remain a retrieval-pipeline component. This architecture begins when routing selects a genuinely different end-to-end evidence path: for example, retrieved chunks versus a whole document, a database/API query, several fused sources, or no retrieval.

```text
standard: query → one predetermined retrieval path → answer
adaptive: query → choose one known evidence path → answer
```

The plan is normally chosen once from the query and trusted context. If the next useful action can be known only after inspecting an intermediate result, use [[Agentic RAG]] instead.

## Why It Is a Separate Architecture

A single retrieval index assumes every task has the same evidence shape. Real workloads mix exact identifiers, local factual lookup, document synthesis, structured facts, multi-corpus questions, and requests that do not need retrieval. Routing changes the control flow and source topology; hybrid search, chunking, and reranking remain component choices inside a selected plan.

The router never expands trusted scope. Identity, tenant, ACLs, source authority, and action permissions are applied by trusted code before and after a model expresses intent.

## Credible Baseline

Start with two explicit routes supported by measured query slices—for example, passage retrieval versus document-level context. Keep a deterministic fallback and abstention behavior. Add a third route only when a residual failure has a distinct evidence shape that the existing plans cannot serve.

Use a classifier, rules, or a small model only when its routing errors cost less than the query-time work it avoids. A model-produced route is a prediction, not authorization or ground truth.

## Common Plans

| Evidence need | Candidate plan | Failure boundary |
|---|---|---|
| precise local fact or identifier | lexical/dense/hybrid passage retrieval, then rerank | wrong scope, miss, or distractor dominance |
| summary or document-level reasoning | retrieve a whole document or section hierarchy | omitted section, context dilution, or stale version |
| authoritative structured fact | schema-constrained database/API query | semantic routing hides a required constraint |
| several bounded corpora | per-source retrieval then authorized fusion | source confusion, duplicate evidence, or ACL leakage |
| no external evidence | direct transformation or a clarification | unnecessary retrieval adds noise or unsupported claims |

## Evaluation

Label task type, evidence shape, valid routes, required sources, authorization scope, answerability, and false-route costs. Compare the router against every fixed plan and an oracle route. Measure route accuracy and calibration, required-evidence coverage, answer/citation quality, abstention, source authority, latency, cost, and harmed slices.

Test ambiguous, adversarial, stale, cross-tenant, and distribution-shifted requests. Inspect whether apparent router lift merely compensates for a weak retriever that should instead be repaired.

## Boundary with Agentic RAG

Use this architecture when the evidence plan can be chosen up front from a finite set. Use [[Agentic RAG]] only when an intermediate observation changes which query, tool, or source is useful next. A router may send a narrow slice to an agentic loop, but it should not turn routine lookup into open-ended planning.

## Part of

← [[RAG Architectures]]

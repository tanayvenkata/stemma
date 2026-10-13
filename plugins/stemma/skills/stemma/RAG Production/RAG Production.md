---
tags: [production]
---
# RAG Production & RAGOps

Production RAG is the discipline of keeping a changing corpus, retrieval stack, model layer, and user-facing application correct, available, secure, observable, and economically sustainable. The hard part is not deploying a demo; it is preserving evidence and behavior while every layer changes independently.

This cluster is intentionally RAG-specific. General compute platforms, networking, accelerator scheduling, and organization-wide AI infrastructure belong elsewhere unless they change the correctness or operation of the corpus-to-answer path.

## Operating Model

```text
requirements and risk budget
        ↓
versioned data and models → evaluated release candidate → progressive delivery
        ↑                          ↓                         ↓
reconciliation and repair ← production traces ← incidents and user feedback
```

Treat these as separate versioned artifacts: source document, parser, chunker, metadata schema, embedding model, index, retriever, reranker, prompt, generator, guardrail policy, and application code. A trace should identify the versions that produced an answer.

## How to Use This Cluster

Enter through requirements before hardening a prototype: decide whether RAG is warranted, define intolerable failures and service objectives, then follow the lifecycle through design, build, offline validation, progressive release, and operation. The branches are concurrent operating concerns rather than a second linear pipeline; consult the one implicated by the current risk or change.

A credible production baseline is not every possible control. It is a versioned, observable system with authoritative data, bounded dependencies, tested authorization, reproducible evaluation, a staged release path, rollback, and an owner who can diagnose and recover it. Add redundancy, caching, provider routing, review queues, or specialized governance when workload and failure evidence justify them.

## Branches

- [[Production Requirements & SLOs]] — decide whether RAG is appropriate and define success, risk, and service objectives.
- [[Production Data Lifecycle, Lineage & Freshness]] — maintain source-to-answer provenance, deletion, reconciliation, and freshness.
- [[Production Reliability, Capacity & Failure Handling]] — bound failures, overload, retries, dependencies, and recovery.
- [[Production Evaluation Gates & Release Engineering]] — test components and ship coordinated changes safely.
- [[Production Observability & Incident Response]] — trace behavior, define alerts, diagnose failures, and learn from incidents.
- [[Production Security, Privacy & Tenant Isolation]] — enforce authorization and trust boundaries around untrusted data and tools.
- [[Production Caching & Vector DB Ops]] — operate caches and vector indexes without serving stale or unauthorized answers.
- [[Production Cost, Provider & Model Ops]] — manage spend, quotas, model changes, fallbacks, and provider risk.
- [[Production Human Oversight & Governance]] — design escalation, review, accountability, and controlled change.

## Lifecycle

[[RAG Production Lifecycle]] connects the branches into an iterative delivery and maintenance loop.

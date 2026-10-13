---
tags: [production]
reviewed: 2026-10-11
---
# RAG Production Lifecycle

RAG development is iterative: discoveries in evaluation and production feed back into requirements, data, and architecture. The stages are checkpoints, not a one-way waterfall.

```text
TRIAGE → DESIGN → BUILD → OFFLINE VALIDATION → PROGRESSIVE RELEASE → OPERATE
   ↑                                                                  │
   └──────────── incidents, drift, feedback, and new requirements ────┘
```

## 1. Triage

- Identify the user task, source of truth, cost of a wrong answer, and acceptable abstention behavior.
- Compare RAG with long-context prompting, database queries, search without generation, fine-tuning, and a deterministic workflow.
- Confirm data access, update/delete requirements, authorization boundaries, and source ownership.
- Define quality, latency, availability, freshness, and cost objectives by traffic or risk class.

RAG is favored when queries need selective access to private, changing, or citable evidence. Corpus token count or update frequency alone is not a decision rule.

## 2. Design

- Design asynchronous, idempotent ingestion with quarantine or dead-letter handling for failures.
- Specify stable document and chunk identities, lineage, ACL propagation, and deletion semantics.
- Establish timeout, retry, fallback, and degraded-mode policies for each dependency.
- Define an evaluation plan before choosing advanced retrieval techniques.

## 3. Build

- Make major components independently testable, but define explicit contracts between them.
- Version configuration and data transformations alongside code.
- Emit structured traces containing request, corpus, index, prompt, and model versions.
- Start with the smallest system that establishes a meaningful baseline.

## 4. Offline Validation

- Use representative and adversarial cases, not only convenient factoid questions.
- Evaluate ingestion, retrieval, reranking, generation, citations, abstention, security, latency, and cost separately and end to end.
- Compare candidates with paired examples, uncertainty estimates, and important slices.
- Require hard safety or integrity properties separately from average quality metrics.

## 5. Progressive Release

- Replay production-like traces in shadow mode where privacy policy permits.
- Use canary, blue-green, or staged traffic rollout according to blast radius and rollback speed.
- For incompatible embedding changes, build a shadow index, dual-process live changes, reconcile completeness, switch reads gradually, and retain the old index through the rollback window (see [[Indexing Lifecycle & Migrations]]).
- Release code, prompts, models, and indexes as a tested compatibility set.

## 6. Operate

- Reconcile sources and indexes, monitor freshness and quality slices, and cluster recurring failures.
- Maintain runbooks, restore tests, on-call ownership, and incident reviews.
- Add confirmed production failures to regression sets without letting the test set become a biased copy of recent complaints.
- Revisit the original system choice when the workload changes.

## Part of
← [[RAG Production]]

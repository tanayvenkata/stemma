---
tags: [production]
reviewed: 2026-10-11
---
# Production Evaluation Gates & Release Engineering

Every change to data, parsing, retrieval, architecture, prompts, models, or policies is a candidate release. A gate should detect meaningful regressions without pretending one global score describes the system.

## Release Manifest

Record compatible versions of application/orchestration code; corpus and metadata schema; parser, chunker, embedding model, and index; retriever, reranker, prompt, generator, and guardrail policy; and the evaluation dataset, evaluator, and threshold configuration.

## Evaluation Layers

1. **Contract tests** — schemas, ACL propagation, citation IDs, tool arguments, deletion behavior.
2. **Component evaluation** — parsing, retrieval, reranking, generation, and guardrails in isolation.
3. **End-to-end evaluation** — representative tasks, abstention, citations, latency, cost, and failure recovery.
4. **Adversarial evaluation** — prompt injection, poisoning, tenant leakage, malformed documents, and resource exhaustion.
5. **Production comparison** — shadow replay, canary metrics, user outcomes, and incident signals.

Use paired comparisons and report uncertainty. Gate critical slices separately; an average improvement can conceal a severe regression for one tenant, language, source type, or risk class. Hard integrity properties may require zero observed violations plus targeted testing, while quality metrics usually need workload-calibrated tolerances rather than universal cutoffs.

## Progressive Delivery

Choose among shadow, canary, blue-green, rolling, and controlled A/B deployment based on blast radius, state compatibility, and rollback time. Define promotion and rollback criteria before sending traffic.

For online comparisons, log assignment, eligibility, exposure, system manifest, and downstream outcome separately. Analyze the users and requests actually exposed to the candidate; assignment without execution is not evidence of treatment. Guardrails and rollback triggers remain active even when the experiment's primary metric improves.

Embedding or schema migrations require a shadow index, dual processing of live changes, reconciliation, and a retained rollback generation. Do not destroy the old index immediately after switching reads. The full procedure lives in [[Indexing Lifecycle & Migrations]].

## Learning Without Test-Set Collapse

Add verified production failures to regression suites, but maintain stable benchmark sets and fresh holdouts. Version human labels and automated judges; monitor evaluator drift when models or prompts change.

## Part of
← [[RAG Production]]

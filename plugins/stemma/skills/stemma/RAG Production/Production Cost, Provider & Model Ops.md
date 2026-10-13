---
tags: [production]
---
# Production Cost, Provider & Model Ops

Optimize for cost per successful user task under quality and reliability constraints. Cheap requests that fail, retry repeatedly, or create review work are not cheap.

## Cost Model

Attribute spend to:

- parsing, OCR, embedding, graph extraction, and re-indexing
- vector storage, replicas, backups, and data transfer
- routing, rewriting, reranking, generation, validation, and tools
- cache infrastructure and invalidation
- evaluation, human review, observability, and incident recovery

Track input, cached-input, reasoning, and output tokens where applicable, but also request count, wall time, provisioned accelerators, and idle capacity. Reconcile internal estimates with provider billing.

## Budgets and Admission

Set per-request and aggregate limits for tokens, tool calls, retrieval fan-out, loop turns, elapsed time, and spend. Reserve capacity for high-priority traffic and maintenance. Use early estimates to reject or downgrade work that cannot fit the remaining budget.

## Model and Provider Lifecycle

- Pin explicit model versions where supported; treat aliases as mutable dependencies.
- Maintain capability tests for context limits, structured output, tools, safety behavior, latency, and regional availability.
- Shadow-test replacements on representative and adversarial cases.
- Record data-use, retention, residency, quota, and deprecation constraints.
- Design fallback by capability and risk, not by nominal model tier alone.

A fallback model may change formatting, tool semantics, safety behavior, or answer quality. Validate degraded behavior explicitly and do not route sensitive traffic to a provider that violates its data policy.

## Build, Buy, and Portability

Managed services reduce time to market; self-hosting can improve control, privacy, or unit economics at sufficient scale but adds capacity, patching, and on-call responsibilities. Abstract stable application contracts and retain evaluation fixtures, but do not force lowest-common-denominator portability when provider-specific capability creates real value.

## Part of
← [[RAG Production]]

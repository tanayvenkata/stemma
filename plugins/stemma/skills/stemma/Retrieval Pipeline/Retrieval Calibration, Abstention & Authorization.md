---
tags: [retrieval]
---
# Retrieval Calibration, Abstention & Authorization

Retrieval scores are ranking signals, not universal probabilities. A safe production retriever must learn when evidence is sufficient, preserve trusted policy scope, and make uncertainty observable.

## Calibrate on the Actual Pipeline

Embedding similarities, fused ranks, and reranker scores have different scales. Calibrate after the complete retrieval configuration is fixed, using held-out answerable and unanswerable queries stratified by query and document type.

Measure retrieval recall/precision, answer-span coverage, calibration by score band, and selective risk versus coverage. Choose thresholds for the cost of false evidence versus false abstention; never copy a global cutoff between models.

## Abstention Contract

Abstain when evidence is missing, contradictory, stale, outside policy scope, or below the calibrated support threshold. Preserve the reason and candidate scores in traces. Generation must still cite and verify the surviving evidence; retrieval gating alone cannot guarantee a faithful answer.

## Authorization Boundary

1. Resolve principal, tenant, roles, and policy scope from authenticated application context.
2. Construct mandatory filters outside model control.
3. Validate any LLM-derived semantic DSL against an allowlisted schema.
4. Conjoin mandatory and semantic constraints before retrieval.
5. Recheck authorization before returning text, metadata, citations, counts, or existence signals.

Test cross-tenant leakage, stale ACL propagation, malformed DSL, prompt-injected filter requests, cache-key isolation, and side channels from result counts or latency.

## Simulation Boundary

Perspective filters such as `witnessed_by` model what an agent could know; they are simulation semantics, not enterprise authorization. Log immutable observations separately from derived beliefs and reflections so replay can explain why an agent retrieved a memory.

## Consumed by

The `Generation Pipeline` consumes authorized, calibrated evidence during context preparation.

## Evaluated by

Use the component-evaluation workflow in the `Evaluation` cluster to measure risk/coverage, false abstention, leakage, and downstream faithfulness.

## Part of
← [[Retrieval]]

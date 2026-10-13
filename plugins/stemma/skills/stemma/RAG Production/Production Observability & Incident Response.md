---
tags: [production]
---
# Production Observability & Incident Response

Observability should make a bad answer reproducible: which evidence, transformations, policies, and dependencies produced it, and what changed from the last known-good behavior?

## Trace Model

Instrument the request as nested spans for routing, retrieval, reranking, prompt assembly, model/tool calls, validation, and cache operations. OpenTelemetry provides transport and tracing infrastructure; projects such as OpenInference add AI-oriented semantic conventions. Treat convention maturity and backend support as implementation choices, not universal guarantees.

Useful trace attributes include:

- privacy-safe request, session, and tenant identifiers
- corpus, index, retriever, prompt, model, and policy versions
- candidate and selected document IDs, scores, filters, and citation mapping
- latency, queue time, attempts, tokens, cache status, and cost
- tool authorization, outcome, and bounded error category
- evaluator results and final disposition: answer, abstain, escalate, or degrade

Do not log raw prompts, documents, or user identifiers by default. Apply redaction, sampling, retention, encryption, and access controls appropriate to the data.

## Metrics and Alerts

Monitor workload-specific distributions and slices:

- availability, timeout, retry, and degraded-mode rates
- end-to-end and per-stage tail latency
- ingestion lag, reconciliation mismatch, and deletion lag
- zero-result, low-evidence, abstention, and citation-error rates
- token/cost consumption and quota headroom
- negative feedback and verified failure categories

Derive alert thresholds from SLOs, historical baselines, and error budgets. A zero-result rate is not intrinsically bad if many questions are legitimately unanswerable.

## Incident Workflow

```text
detect → contain → preserve evidence → diagnose → repair → validate → restore → learn
```

Containment may disable a source, model, tool, tenant, or release while preserving safe read-only behavior. Retain relevant traces and version manifests. Afterward, document impact, timeline, root and contributing causes, detection gaps, recovery evidence, and owned follow-ups; add a regression test when the failure can be represented safely.

## See Also

- OpenTelemetry documentation: https://opentelemetry.io/docs/
- OpenInference specification: https://github.com/Arize-ai/openinference

## Part of
← [[RAG Production]]

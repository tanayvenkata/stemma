---
tags: [production]
---
# Production Reliability, Capacity & Failure Handling

RAG requests cross multiple failure domains. Reliability comes from explicit deadlines, bounded work, isolation, and recoverable state—not from retrying everything.

## Request Budget

Allocate an end-to-end deadline across routing, retrieval, reranking, tools, generation, and validation. Include network and queueing time and reserve time for graceful fallback. Tail latency matters more than a single average.

## Failure Policy per Dependency

For each call, define:

- timeout and cancellation behavior
- which errors are retryable
- maximum attempts and exponential backoff with jitter
- idempotency key or side-effect protection
- circuit-breaker and concurrency limits
- fallback, abstention, or fail-closed behavior
- telemetry and operator ownership

Retry only transient failures. Invalid requests, authorization failures, exhausted budgets, and deterministic data errors need correction or quarantine. Hedged requests can reduce tail latency but increase load and must be bounded.

## Isolation and Degraded Modes

- Use separate worker pools and quotas for ingestion, interactive queries, batch evaluation, and background maintenance.
- Bound queues and shed low-priority load before saturation cascades.
- Isolate tenants and expensive query classes so one workload cannot consume all capacity.
- Define degraded responses: skip optional reranking, use a smaller model, return sources without synthesis, or abstain. Never silently drop authorization or integrity checks.

## Capacity Planning

Load-test realistic distributions of prompt size, output length, filter selectivity, cache hit rate, tool fan-out, and provider latency. Measure saturation points and P50/P95/P99 behavior. Capacity models must include request duration: rate limits such as tokens per minute do not directly determine safe concurrency.

## Recovery Engineering

Maintain runbooks for provider outage, index corruption, stale ingestion, runaway cost, authorization leakage, and bad model/prompt release. Test backup restore, index rebuild, dependency failover, and rollback. Chaos tests should verify bounded failure and recovery evidence, not merely inject faults.

## Part of
← [[RAG Production]]

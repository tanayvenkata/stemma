---
tags: [generation]
---
# Prompt Caching & Compression

Prompt caching reuses computation for repeated prefixes; compression reduces input tokens or representations. They solve different constraints and can interact with correctness, privacy, freshness, and observability.

## Prompt Caching

Cache effectiveness depends on the runtime's exact prefix-matching, minimum size, expiration, routing, accounting, and privacy rules. Arrange stable trusted instructions before volatile content when the provider/runtime benefits from it, but do not reorder semantically required content solely for a presumed discount.

Version cache identity with model, prompt, tools, policies, tenant scope, corpus/evidence version, and any provider-required fields. Test cross-tenant isolation, invalidation, stale policy, regional routing, and reported versus observed hit behavior.

## Compression

- deterministic removal of boilerplate or duplicates;
- extractive selection of source spans;
- structure-aware pruning;
- generated summaries or learned compressed representations.

Every derived form must retain provenance and be evaluated for missing qualifiers, contradictions, citation mapping, and adversarial content. Preserve canonical evidence separately.

## Budget from Measurement

Build a request budget from observed tokenization, time-to-first-visible-output, generation rate, concurrency, cache behavior, and required response length on the deployed runtime. Provider prices and discounts are snapshots; record them in experiment manifests rather than as timeless rules.

Adopt caching or compression when measured latency/cost benefit survives correctness, freshness, isolation, and operational tests.

## Part of

← [[Context Preparation]]

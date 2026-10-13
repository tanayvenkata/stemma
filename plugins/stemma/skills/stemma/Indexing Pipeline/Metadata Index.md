---
tags: [indexing]
---
# Metadata Index

A metadata index organizes typed fields such as source identity, version, time, document class, language, and trusted authorization scope so search can restrict or rank candidates without scanning every payload.

## Filtering Strategies

| Strategy | Mechanism | Failure to test |
|---|---|---|
| Pre-filter | restrict eligible items before vector search | approximate index may behave poorly on a sparse/disconnected subset |
| Integrated filter | evaluate constraints during index traversal | engine-specific recall and performance under selectivity |
| Post-filter | retrieve broadly, then discard ineligible items | valid results may never enter the initial candidate pool |
| Partitioned index | search a physically/logically isolated subset | duplication, routing, skew, and migration complexity |

Selectivity, cardinality, update rate, missing values, and index implementation determine the tradeoff. Benchmark representative filters, especially rare authorized subsets.

## Schema Principles

- preserve stable source and version identity plus anchors needed for citations;
- use typed, normalized values and explicit missing/unknown states;
- version derived classifications and record provenance;
- index fields shown to improve routing, filtering, ranking, or operations;
- distinguish semantic metadata from trusted authorization policy.

An LLM may propose semantic filters, but authenticated server-side context owns tenant, user, ACL, and other mandatory scope. The application must conjoin those constraints outside model control.

Evaluate inclusion, false exclusion, authorization integrity, latency, freshness, and behavior under malformed or stale metadata. More indexed fields are not automatically better.

## Part of

← [[Indexing]]

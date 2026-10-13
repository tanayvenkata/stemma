---
tags: [retrieval]
---
# Query Transformation

Query transformation creates one or more search representations while preserving the original information need. The best representation is case-dependent; the unchanged request is always the comparator.

## Families

- [[Query Rewriting]] resolves conversational or syntactic ambiguity.
- [[Query Expansion]] adds related terms or broader views.
- [[Query Decomposition]] separates evidence requirements or dependent subproblems.
- [[HyDE]] produces a hypothetical document-style representation at query time.
- [[Reverse HyDE]] creates source-derived question representations at index time.
- [[Self-Query]] extracts allowable semantic filters into a validated DSL.

## Transformation Contract

Retain the original query, generated representations, model/rule version, entities, dates, quantities, negation, scope, and mapping from each representation to returned candidates. Mandatory authorization constraints remain outside model control.

Compare each candidate with no transformation on intent preservation, required-evidence coverage, ranking, new distractors, query volume, latency, cost, and instability. Use conditional invocation when benefit is confined to a recognizable slice.

## Components

- [[HyDE]]
- [[Reverse HyDE]]
- [[Query Expansion]]
- [[Query Decomposition]]
- [[Self-Query]]
- [[Query Rewriting]]

## Part of

← [[Query Understanding]]

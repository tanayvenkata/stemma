---
tags: [retrieval]
---
# Step-Back Prompting

Step-back prompting derives a broader question or governing principle from a specific request, then retrieves using both specific and abstract views.

It can help when local facts depend on a general policy, definition, mechanism, or theory. It can hurt when abstraction drops an entity, jurisdiction, date, exception, or exact identifier.

## Protocol

Preserve the original query and generate a labeled abstract query. Retrieve each separately, retain provenance by query, and combine only after measuring whether the abstract view contributes required evidence.

Compare original-only, step-back-only, and combined policies on intent/constraint preservation, unique evidence, multi-level coverage, distractors, latency, cost, and downstream synthesis. Use it for demonstrated broad-plus-specific failure patterns rather than every detailed query.

Primary reference: [Take a Step Back](https://arxiv.org/abs/2310.06117).

## Part of

← [[Query Expansion]]

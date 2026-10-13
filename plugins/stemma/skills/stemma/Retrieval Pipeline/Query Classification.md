---
tags: [retrieval]
---
# Query Classification

Query classification assigns observable request properties that may justify a different retrieval policy. Classes should express decision-relevant structure, not force every query into one technique.

## Possible Labels

- lookup, comparative, multi-evidence, exploratory, aggregation, temporal, ambiguous, or unanswerable;
- exact-identifier versus conceptual matching;
- required source/corpus and language;
- need for clarification, decomposition, structured computation, or retrieval;
- risk, cost, and escalation class.

Labels can overlap, and several routes may be acceptable. Define each class, its evidence, allowed policies, error costs, and abstention behavior before training or prompting a classifier.

## Evaluation

Build boundary cases, overlapping intents, paraphrases, class imbalance, unavailable destinations, and out-of-distribution requests. Measure per-class precision/recall, confusion pairs, consistency, cost-weighted error, downstream success, latency, and fallback.

Add classification only when conditional policies outperform a direct baseline enough to justify misclassification and operational complexity.

## Part of

← [[Query Understanding]]

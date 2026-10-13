---
tags: [retrieval]
---
# Query Routing

Query routing selects a capability, corpus, retriever, or policy from the request and trusted application state. A route is correct when it improves task outcome or resource use without violating mandatory scope.

## Router Families

- deterministic rules for explicit contracts and high-precision cases;
- classifiers for stable intent taxonomies;
- embedding similarity to route descriptions or exemplars;
- model-based structured decisions for nuanced or evolving routes;
- cascades that begin cheaply and escalate uncertain cases.

## Design

Define route eligibility, acceptable alternatives, error costs, abstain/escalate behavior, and destination failure handling. Keep authorization, tenant, and policy constraints outside model control.

Evaluate per-route precision/recall, confusion pairs, cost-weighted error, downstream success, latency, instability, out-of-distribution requests, and fallback. Similarity or model confidence is not automatically calibrated; learn decision boundaries on held-out cases when confidence controls escalation.

Add routing only when direct handling wastes meaningful resources or produces identifiable failure slices. An extra router can create a new single point of misclassification.

## Part of

← [[Query Understanding]]

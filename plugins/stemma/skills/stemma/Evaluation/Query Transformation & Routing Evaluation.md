---
tags: [evaluation]
---
# Query Transformation & Routing Evaluation

Query transforms and routers are decision components. Evaluate both whether the decision preserves the user’s problem and whether it improves downstream utility. Fluent rewrites and plausible route names are not evidence of correctness.

## When This Enters the Build

This is an escalation stage, not a greenfield prerequisite. Start with the user’s original query and a direct path. Add a transform when failures reveal a repeatable mismatch between user wording and retrievable evidence; add a router when distinguishable request classes benefit from different corpora, retrievers, pipelines, optional stages, or a no-retrieval path.

Leave with explicit route or transformation eligibility, an unchanged-path baseline, safe abstention/fallback behavior, and downstream evidence that the added decision earns its latency and new failure modes.

## Query Transformation Labels

Build cases across short/underspecified queries, conversational references, exact identifiers, negation, dates, quantities, languages, ambiguous entities, multi-part requests, and requests that should remain unchanged. For each case record:

- invariant intent, entities, constraints, time scope, and required output;
- acceptable interpretations or decompositions;
- source regions required to answer each interpretation;
- transformations that would introduce an unsupported assumption.

Human labels or rubric-based judging can assess preservation, but the decisive test is usually paired retrieval utility against stable evidence labels.

## Transformation Protocol

1. Freeze the original queries, evidence labels, corpus, retriever, and downstream settings.
2. Compare no transform with each justified rewrite, expansion, decomposition, hypothetical-document, or multi-query policy.
3. Score entity/number/date/negation retention and constraint violations before retrieval.
4. Compare evidence Recall/NDCG, unique relevant evidence gained, irrelevant candidates added, latency, cost, and total query volume.
5. Track helped, harmed, and unchanged cases. For stochastic transforms, repeat enough runs to estimate decision instability.
6. Test prompt injection and content that attempts to alter routing or rewrite instructions.

A transform is worth changing only when it fixes a defined failure slice, preserves non-negotiable constraints, and produces a meaningful downstream gain that justifies added variance, latency, and debugging complexity. If the original retrieval already succeeds, prefer no transform unless another product requirement demands it.

## Router Cases and Labels

Define route eligibility and consequences before labeling. A label may be one valid route, a set of acceptable routes, or “abstain/escalate.” Include boundary cases, overlapping intents, class imbalance, paraphrases, out-of-distribution requests, unavailable destinations, and high-cost misroutes. Split related paraphrases or user sessions together to prevent leakage.

Do not introduce a learned or semantic router merely because multiple components exist. First run a direct or deterministic path and inspect its failures. Routing becomes a justified hypothesis when failures cluster into distinguishable request classes and an alternate corpus, retriever, complete pipeline, optional stage, or no-retrieval path demonstrably helps those classes. This discovery order keeps the route taxonomy grounded in observed behavior rather than imagined categories.

Use accuracy only when classes are balanced and error costs are similar. Otherwise inspect per-route precision/recall, macro-F1, a confusion matrix, coverage versus selective risk under abstention, top-k accuracy for legitimate alternatives, and cost-weighted error. Always measure downstream success conditional on the chosen route plus latency, cost, timeout, and fallback behavior.

## Router Protocol and Decision

1. Establish a simple deterministic or direct-route baseline.
2. Freeze route definitions, examples, policy constraints, and test cases; version any exemplar set.
3. Tune on development data, then evaluate once on protected and adversarial/OOD slices.
4. Review confusion pairs and near-boundary cases rather than only the aggregate.
5. Simulate destination failure and verify safe fallback or abstention.
6. Repeat nondeterministic routers and report route-consistency as well as mean quality.

Adopt a router when the reduction in downstream error or resource use exceeds the cost of its own mistakes and operation, with must-not-route violations at the product’s required risk level. Change route definitions when labels are intrinsically ambiguous; change the router when definitions are sound but decisions fail. Similarity scores from exemplar routers are not calibrated probabilities—calibrate a decision policy on held-out cases if confidence controls escalation.

## Part of

← [[Component Evaluation Harness]]

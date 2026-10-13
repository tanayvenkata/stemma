---
tags: [retrieval]
reviewed: 2026-10-11
---
# Query Understanding

Query understanding decides what information need, scope, and retrieval plan—if any—should be sent downstream. Its job is not to rewrite every request; every transformation can erase identifiers, constraints, negation, or conversational intent.

## Decision Sequence

```text
request + conversation + trusted application context
→ determine task and whether retrieval is needed
→ establish mandatory scope and authorization outside model control
→ detect ambiguity, missing references, or separable subproblems
→ choose original, rewritten, expanded, decomposed, or reasoning-assisted query
→ preserve the original request and transformation trace
```

The original query is the baseline. Add a transform only for a diagnosed failure slice and measure downstream evidence gain against intent preservation, latency, cost, and variance.

## Common Decisions

| Condition | Candidate action | Main failure to test |
|---|---|---|
| clear, self-contained information need | retrieve the original query | unnecessary routing or transformation overhead |
| conversational reference | rewrite with only necessary history | invented referent or dropped constraint |
| several independently answerable parts | decompose and retain labeled subqueries | lost relationship or incomplete synthesis |
| vocabulary mismatch | expansion or hypothetical-document representation | semantic drift and noisy candidate pool |
| reasoning-intensive relevance | generate a concise retrieval rationale, plan, or subquestions | answer leakage, cost, and overconstrained search |
| structured operation or no retrieval need | route to appropriate capability or direct policy | confident misroute and unsafe fallback |

Reasoning-intensive retrieval is distinct from ordinary paraphrase: the system may need to infer what evidence would solve the problem before matching documents. Public results such as BRIGHT (2024; standings change, so re-check before citing numbers) are useful warnings that generic embedding rankings do not transfer automatically; target cases decide whether additional query-time reasoning helps.

## Evaluation Contract

Label invariant intent, entities, dates, quantities, negation, acceptable interpretations, required evidence, valid routes, and escalation conditions. Compare no-transform and candidate policies on intent preservation, evidence coverage/ranking, route utility, query volume, latency, cost, instability, and important slices.

Authorization filters are not query understanding. Models may extract semantic intent, but authenticated identity and mandatory scope are conjoined by trusted code.

Primary reference: [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).

## Components

- [[Query Transformation]]
- [[Query Routing]]
- [[Query Classification]]

## Next

→ [[Retrieval]]

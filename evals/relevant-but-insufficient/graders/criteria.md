---
type: llm
weight: 1
---

PASS if the answer does both of the following:
- explains that per-passage relevance does not mean the set of passages is sufficient to answer: a set of individually relevant passages can still miss a required fact, or contain one authoritative answer among distractors, so sufficiency must be judged for the evidence set (or the question's required facts), not passage by passage;
- proposes a way to localize the failure, such as giving generation known-sufficient (oracle) evidence to separate retrieval or gating failures from generation failures, or measuring coverage of required facts.

FAIL if it attributes the problem only to grader accuracy or generation without raising the set-sufficiency point.

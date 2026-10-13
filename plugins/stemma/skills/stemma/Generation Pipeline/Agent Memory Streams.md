---
tags: [generation]
---
# Agent Memory Streams

An agent memory stream is a versioned record of observations, actions, communications, and derived beliefs that can be retrieved into later decisions. Memory design determines what the agent can know, forget, revise, and attribute to a source.

## Separate Record Types

| Record | Example | Required properties |
|---|---|---|
| observation | environment event or tool result | source, time, perspective, confidence |
| action | tool call or world transition | actor, authorization, result, side effects |
| communication | statement from a user or agent | speaker, audience, provenance, hearsay status |
| derived belief/reflection | summarized pattern or hypothesis | supporting memories, derivation version, validity state |
| stable profile/world fact | confirmed preference or rule | authority, effective interval, correction history |

Keep immutable observations separate from derived summaries so consolidation can be replayed, challenged, or corrected. A repeated statement is not independent corroboration.

## Retrieval Policy

A baseline may combine relevance, recency, importance, source reliability, perspective, and task state:

$$
\operatorname{score}(m,q)=f(\operatorname{relevance},\operatorname{recency},\operatorname{importance},\operatorname{provenance},\operatorname{state})
$$

Features need comparable semantics before weighting. Candidate-relative normalization can change when the pool changes; rank fusion, fixed transforms, calibration, or learned ranking are alternatives. Compare every composite policy with simple relevance-only and recency-only baselines.

## Consolidation

Trigger reflection or summarization from a measurable condition such as unresolved task state, memory volume, elapsed time, or novelty. Store links to supporting records, preserve contradictions, and avoid creating generic summaries that match every query and crowd out specific evidence.

## Multi-Agent Integrity

- enforce perspective and authorization before retrieval;
- distinguish witnessed events from statements and derived beliefs;
- track source chains to detect rumor amplification and circular citation;
- represent corrections and temporal validity rather than overwriting history;
- prevent one agent's private memory from entering another's candidates;
- make world truth, agent belief, and evaluator truth separate concepts.

## Evaluation

Use seeded, replayable scenarios and compare memory policies on task success, evidence provenance, perspective leakage, correction, rumor amplification, retrieval starvation, latency, storage, and behavioral stability. Perturb time, misleading statements, missing observations, and consolidation schedules.

Adopt additional memory tiers or scoring features only when they repair a demonstrated failure without creating unacceptable leakage or self-reinforcement.

Primary reference: [Generative Agents](https://arxiv.org/abs/2304.03442).

## Part of

← [[Agentic Loops]]

---
tags: [generation]
---
# Prompt Construction

Prompt construction defines the behavioral contract presented to the selected model. Durable prompting states the objective, authoritative inputs, constraints, allowed actions, uncertainty behavior, and output contract clearly enough to test.

## Modular Contract

```text
role or operating scope
task and success condition
trusted instructions and policy constraints
untrusted evidence with source identity
tool definitions and side-effect boundaries, if any
missing/conflicting-evidence behavior
output schema or user-facing form
```

Use the native message roles and structured-output mechanisms of the runtime rather than assuming one textual markup works everywhere.

## Reasoning Guidance

Do not expose or require hidden chain-of-thought as an evaluation artifact. Ask for observable outputs: answer, citations, tool calls, concise rationale where appropriate, checks, or uncertainty. Explicit decomposition can help when the workflow requires auditable intermediate products or separable subproblems; it can also overconstrain a capable model. Compare it empirically.

## Evidence Policies

- distinguish supplied evidence from external knowledge permissions;
- require abstention or clarification when decisive evidence is absent;
- preserve conflicts rather than silently selecting a source by recency alone;
- state which source-authority, time, or policy rule resolves conflicts;
- treat retrieved instructions as data unless trusted policy explicitly says otherwise;
- define citation granularity and required claim coverage.

## Experiment

Version every prompt and exemplar. Compare one contract change at a time on paired cases while holding model, evidence, and decoding fixed. Measure task success, claim support, instruction adherence, abstention, tool/schema reliability, verbosity, latency, tokens, and regressions by slice.

Prompt length, user-query position, delimiter style, and number of examples are model- and task-dependent. Prefer the shortest contract that produces reliable behavior and remains understandable to operators.

## Components

- [[Few-shot & In-Context Learning]]

## Next

→ [[Generation Strategy]]

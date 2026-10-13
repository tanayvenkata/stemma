---
tags: [generation]
---
# Agentic Loops

Agentic loops let a model repeatedly inspect state, retrieve or call tools, update memory, and decide whether to continue. They turn generation into a controller and therefore require explicit state, budgets, authorization, recovery, and stopping—not merely a prompt that says “act autonomously.”

## Escalation Ladder

```text
deterministic workflow
→ single model call
→ model with one bounded tool step
→ iterative controller
→ planner/workers or asynchronous orchestration
```

Move right only when later decisions genuinely depend on observations and measured task gains justify the added failure surface.

## Loop Contract

- versioned goal, environment state, tools, permissions, and budgets;
- typed actions validated by trusted code;
- observation provenance and error taxonomy;
- checkpoints, retries, idempotency, and side-effect controls;
- termination, escalation, cancellation, and human-approval rules;
- trajectory records sufficient for replay and evaluation.

Evaluate terminal success and trajectory safety together. Perturb tools, evidence, ordering, and budgets; measure invalid/unsafe actions, recovery, loops, steps, time, tokens, cost, and run-to-run variance.

## Components

- [[ReAct & Tool Orchestration]]
- [[Agent Memory Streams]]
- [[Plan-Execute-Reflect Loops]]

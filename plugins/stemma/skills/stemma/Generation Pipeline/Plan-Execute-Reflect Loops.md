---
tags: [generation]
---
# Plan-Execute-Reflect Loops

Plan–execute–reflect separates goal decomposition, action, observation, and policy revision. It is useful when tasks have dependencies, uncertain intermediate state, or expensive mistakes; it is unnecessary overhead for fixed or single-step work.

## Loop Contract

1. **Plan:** produce bounded subgoals, dependencies, success conditions, and budgets.
2. **Execute:** validate and perform the next permissible action.
3. **Observe:** convert results and failures into trusted structured state.
4. **Reflect:** compare state with success conditions and decide continue, replan, retry, escalate, or stop.

Reflection is another fallible model decision, not automatic self-correction. It can rationalize mistakes, loop, or expand scope. Limit iterations, cost, time, tool calls, and replans; preserve a deterministic terminal policy.

## Architecture Choices

- single controller with explicit state;
- planner plus deterministic executor;
- planner and specialized workers;
- event-driven/asynchronous workflow with checkpoints;
- human approval at consequential boundaries.

Add multiple agents only when specialization, parallelism, isolation, or organizational boundaries provide measured value. More agents do not imply better reasoning.

## Evaluation

Compare with the simplest direct or ReAct baseline on matched tasks. Measure terminal success, valid trajectories, unsafe/irreversible actions, recovery, redundant work, loops, step count, wall time, tokens, cost, and outcome variance. Perturb tools, observations, budgets, and ordering to test robustness.

Adopt the loop when task improvement and recovery justify its orchestration and failure surface. Constrain it to the slices where that evidence holds.

## Part of

← [[Agentic Loops]]

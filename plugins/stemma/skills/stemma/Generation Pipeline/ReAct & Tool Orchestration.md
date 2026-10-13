---
tags: [generation]
---
# ReAct & Tool Orchestration

ReAct interleaves model decisions with external actions and observations. The durable engineering pattern is a controlled state machine: the model proposes an action, trusted code validates and executes it, and the result becomes the next observation.

```text
state and goal
→ model proposes tool + arguments or finish
→ authorize and validate
→ execute with idempotency/timeout controls
→ record observation and side effects
→ continue, recover, escalate, or stop
```

Do not require or store hidden chain-of-thought. Persist observable decisions, tool calls, arguments, results, policy checks, state transitions, and concise justifications where useful.

## Tool Contract

- narrow description and typed schema;
- explicit read/write and side-effect class;
- authenticated identity and authorization handled outside model arguments;
- timeout, retry, idempotency, compensation, and rate limits;
- bounded output with provenance and error taxonomy;
- confirmation policy for consequential or irreversible actions.

Tool lists can be static, routed, or discovered, but routing itself can hide required capabilities or expose dangerous ones. Evaluate tool selection, argument validity, task success, unsafe action rate, recovery, loops, steps, latency, and cost on representative environments.

Use a loop when later actions genuinely depend on observations. Prefer direct deterministic code or a single model call for fixed workflows; autonomy adds failure modes and should earn its place.

Primary reference: [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629).

## Part of

← [[Agentic Loops]]

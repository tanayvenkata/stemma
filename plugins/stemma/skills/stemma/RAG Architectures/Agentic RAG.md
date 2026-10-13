---
tags: [architectures, agents]
---
# Agentic RAG

Agentic RAG makes evidence acquisition a **stateful policy**. The system observes the current task state, selects a bounded action such as retrieving, querying a structured source, or decomposing a subproblem, records the result, and decides whether to continue.

## How It Differs from Standard RAG

Standard RAG executes one planned retrieval path: it can use strong retrievers and rerankers, but it knows the evidence request before retrieval starts. Agentic RAG changes that into a stateful loop where an observation determines the next authorized query, tool, or stopping decision.

```text
standard: task → retrieve once → answer
agentic:  task → retrieve/tool → observe → choose next action → ... → answer or escalate
```

For example, resolving an entity may be necessary before querying its transactions, and the returned transaction state may determine whether the next source is a policy document, a payment API, or an escalation queue. If a finite plan can be selected up front, prefer [[Adaptive & Composite Retrieval]] instead.

## When the Loop Is Actually Needed

Use a conditional loop when the next useful query or source depends on an intermediate observation—for example, resolving an entity before querying its transactions. Do not add one merely to rewrite a query or call a fixed sequence of retrievers; a deterministic pipeline is easier to test and operate.

```text
task + policy + budget
        ↓
observe state → choose authorized action → execute → validate observation
      ↑                                      ↓
      └──────── update state or stop ────────┘
```

## Implementation Contract

- **State:** original task, subgoals, evidence with provenance, unresolved claims, actions, errors, and remaining budget.
- **Action space:** typed, least-privilege tools with schemas, authorization, deadlines, and explicit side-effect classes.
- **Controller:** chooses among retrieve, route, decompose, verify, answer, abstain, or escalate.
- **Evidence policy:** distinguishes observations from model inferences and detects duplicates, conflicts, and stale results.
- **Termination policy:** hard bounds plus task-aware completion, impossibility, and escalation conditions.

A turn limit guarantees termination, not correctness. Exact-query duplicate detection is only one signal: semantically repeated actions, cycling states, and unchanged evidence also matter. A self-reported confidence score is not a convergence proof.

## Failure Modes

- planning consumes work without improving evidence
- tools return valid but irrelevant or unauthorized data
- early mistaken observations steer later retrieval
- repeated queries or tool cycles exhaust budget
- the final answer omits or overstates accumulated evidence
- nondeterministic trajectories make failures difficult to reproduce

Persist the action/observation trajectory, tool and policy versions, authorization decisions, and final evidence mapping. Treat retrieved text and tool output as untrusted data, not instructions.

## Evaluation

Compare against a fixed pipeline and, where possible, an oracle plan. Evaluate task outcome, evidence coverage, action validity, unnecessary actions, trajectory length, recovery from perturbed observations, latency, cost, and termination. Slice results by tasks that truly require conditional acquisition; aggregate gains can hide regressions on simple queries.

Adopt the loop only if its incremental capability or quality justifies the larger security, reliability, and evaluation surface.

## Part of

← [[RAG Architectures]]

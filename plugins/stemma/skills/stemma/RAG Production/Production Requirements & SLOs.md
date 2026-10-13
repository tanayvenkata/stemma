---
tags: [production]
---
# Production Requirements & SLOs

Production design begins with an explicit task and failure budget, not a vector database choice.

## Decide What the System Must Do

Capture:

- users, tasks, and decisions influenced by the answer
- authoritative sources and ownership
- expected query and corpus distributions
- citation, freshness, and completeness requirements
- acceptable abstention, escalation, and degraded behavior
- regulatory, residency, retention, and tenant-isolation constraints
- traffic, concurrency, cost, and recovery expectations

## Does This Need RAG?

Use RAG when a request needs selective evidence from a corpus that is private, changing, too large or too structured to include wholesale, or must support source attribution. Prefer simpler mechanisms when they suffice:

| Need | Often simpler starting point |
|---|---|
| Exact transactional facts | Typed API or database query |
| Small stable packet of evidence | Long-context prompt |
| Document discovery without synthesis | Search interface |
| New style or behavior, not new facts | Prompting or fine-tuning |
| Deterministic policy execution | Rules/workflow engine |

Hybrid designs are normal. A system may query SQL for balances, retrieve policy text for explanation, and use an LLM only for synthesis.

## SLIs, SLOs, and Error Budgets

Define objectives from user impact and measure them by relevant slice. Useful indicators include:

- answer correctness, groundedness, and citation correctness
- answerability detection and appropriate abstention
- source/index freshness and deletion propagation lag
- end-to-end and time-to-first-token latency distributions
- availability and successful degraded responses
- cost per successful task, not only cost per request
- security-policy and tenant-boundary violations

Avoid universal thresholds. A support search, clinical reference tool, and background research report require different objectives. Record the measurement window, denominator, exclusions, and error budget for every SLO.

## Go/No-Go Artifact

Before architecture work, retain a short decision record containing assumptions, alternatives rejected, owners, measurable success criteria, intolerable failures, and the conditions that require re-evaluation.

## Part of
← [[RAG Production]]

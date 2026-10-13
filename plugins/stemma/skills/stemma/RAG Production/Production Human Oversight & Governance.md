---
tags: [production]
---
# Production Human Oversight & Governance

Human oversight is an operational system with queues, permissions, evidence, latency, and failure modes—not a generic promise that a person remains “in the loop.”

## Choose the Human Role

| Pattern | Human responsibility |
|---|---|
| Human-in-command | Defines policy, access, and deployment authority |
| Human-on-the-loop | Monitors bounded automation and can intervene |
| Human-in-the-loop | Must approve a decision or action before execution |
| Human escalation | Reviews only low-confidence, high-risk, or disputed cases |

Use deterministic approval for irreversible, regulated, high-impact, or privileged actions. Do not ask reviewers to rubber-stamp volumes they cannot meaningfully inspect.

## Review Queue Design

Provide the query, proposed response/action, cited evidence, source versions, relevant policy, uncertainty or trigger reason, and prior decisions. Measure queue age, reviewer agreement, override rate, downstream outcomes, and capacity. Define what happens when reviewers are unavailable; high-risk work should normally fail closed or remain pending.

## Accountability and Change Control

- Assign owners for corpus sources, retrieval, models/prompts, security policy, evaluation, and on-call response.
- Record material architecture and threshold decisions with evidence and review dates.
- Require scoped approval for changes that alter data access, user impact, or risk posture.
- Preserve audit trails for automated decisions, human overrides, and tool actions.
- Document system limitations and intended use for operators and users.

## Feedback Quality

User feedback and reviewer labels are noisy and selected. Maintain labeling guidance, adjudicate disagreements, sample apparently successful traffic, and watch for automation bias. Separate a user's preference signal from a verified factual or safety failure.

## Part of
← [[RAG Production]]

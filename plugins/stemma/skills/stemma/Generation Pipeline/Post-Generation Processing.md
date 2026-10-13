---
tags: [generation]
---
# Post-Generation Processing

Post-generation processing turns a raw model result into a deliverable response or safe action. It verifies the contracts that cannot be guaranteed during decoding, attaches provenance, applies destination-specific encoding, and chooses repair, abstention, escalation, or failure behavior.

## When This Enters the Build

Begin with deterministic parsing, schema, citation-identifier, and destination-safety checks required by the interface. Add claim/evidence verification when unsupported or contradictory content is a measured risk. Keep the raw output, validation results, repairs, and served output separate so evaluation can identify whether generation or post-processing caused a failure.

Leave with an explicit failure policy and evidence that validation catches important errors without silently corrupting valid answers or creating an unbounded regeneration loop.

## Post-Generation Control Layers

```
                       Post-Generation Processing
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         ▼                                                     ▼
1. [[Hallucination Detection & Verification]]   2. [[Citation & Output Formatting]]
 • Claim/evidence checks                        • Citation coverage and source alignment
 • Selective verification                      • Schema, rendering, and destination encoding
 • Abstention and escalation                    • Provenance-preserving transformations
```

## Why Post-Generation Verification is Essential

Even with pristine context and low temperature, LLMs can fabricate subtle details (*"The revenue was $4.2B"* when text says *"Projected revenue is $4.2B"*).

Post-generation controls are one layer, not a perfect firewall. Separate:

- **Syntax validation** — can the output be parsed?
- **Semantic validation** — do fields, claims, units, and citations mean what the contract requires?
- **Business-rule validation** — are cross-field invariants, permissions, and state transitions valid?
- **Evidence validation** — are material claims supported by authoritative cited spans, and is important evidence omitted?
- **Delivery validation** — is output safely encoded and appropriate for the UI, API, database, or tool sink?

On failure, use a bounded policy: deterministic repair when possible, one or more measured regeneration attempts, abstention, degraded output, or human escalation. Preserve the original evidence and validation failures for evaluation rather than silently repairing them away.

Streaming complicates validation because unsafe or invalid content may already be visible. Buffer fields that require complete validation, or design events so provisional content cannot trigger side effects.

## Components

- [[Hallucination Detection & Verification]]
- [[Citation & Output Formatting]]

## Evaluated by

Use the `Generation & Citation Evaluation` workflow in the `Evaluation` cluster to measure claim support, citation coverage, semantic validation, and repair behavior.

## Next

→ [[Agentic Loops]]

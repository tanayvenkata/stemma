---
tags: [generation]
reviewed: 2026-10-11
---
# Model Selection & Reasoning Tiers

Model selection compares deployable configurations by measured capability, reliability, latency, cost, privacy, and control. “Fast,” “flagship,” and “reasoning” are temporary market labels; the durable design is a task policy over verified capabilities.

## Two Useful Capability Axes

- **Learned capability:** knowledge and transformations encoded through training, architecture, and adaptation.
- **Test-time computation:** additional inference work used to search, verify, or deliberate on the supplied problem.

Neither substitutes for accessible evidence. More inference compute cannot recover a missing source, broken parse, unauthorized document, or omitted tool observation. It can help reconcile, calculate, or plan over evidence that is present.

## Candidate Roles

| Role | Selection question |
|---|---|
| direct/efficient path | Can the configuration meet task and integrity requirements with lower latency/cost? |
| general path | Does it cover the common workload without specialized routing? |
| deliberative path | Do complex or high-risk slices gain enough from additional compute to justify variability and cost? |
| specialized/local path | Do domain adaptation, privacy, modality, or deployment constraints justify a separate model? |
| non-generative classifier/verifier | Can a bounded decision (route, pass/fail, pick a label) run on a model that returns label probabilities instead of text, typically at lower latency and cost and without free-text parsing failures? |

These are measured roles, not fixed model tiers. One configuration may occupy several roles.

## Cheapest Sufficient Decider

For a bounded decision, climb only as far as validation requires. If an LLM call already happens on that path, adding the decision as a structured-output field is usually cheapest; a separate classifier pays off when the decision must happen before or outside that call, at high volume, or on a latency-critical path.

| Step | Use when | Watch for |
|---|---|---|
| rules or exact checks | the decision is mechanical and stable | silent coverage gaps |
| zero-shot typed classifier | no labels yet; binary or few-option decisions; high volume | weak on many labels and graded scales; reported confidence is not a calibrated probability; long input may be truncated silently |
| supervised small classifier (embeddings + linear model, few-shot fine-tuning, or a fine-tuned encoder) | enough representative labels exist to train and hold out a validation set (a few hundred is a cheap starting assumption; confirm with a learning curve) and the label set is stable | domain shift and shortcut features; retrain when labels or traffic change |
| specialized checker | a task-specific model fits, such as claim-support checking | public benchmark parity does not transfer automatically; validate in-domain |
| model judge or generator | graded judgments, multi-step reasoning, near-miss detection, or open-ended output | cost, variance, prompt sensitivity |

A zero-shot classifier is usually a starting point, not an endpoint. Once labels accumulate, compare it against a supervised baseline, which often wins on a stable label set; confirm with a held-out comparison. Hosted zero-shot classifier products change quickly and their category names are marketing labels; select by measured behavior on protected tasks, not by the category name.

## Routing Protocol

1. Define observable features available before routing and the cost of each misroute.
2. Establish one-model baselines before adding a router.
3. Compare direct and escalated outcomes on paired cases by complexity and risk slice.
4. Calibrate abstention/escalation and test unavailable-model, timeout, quota, and downgrade behavior.
5. Record actual route, model revision, compute settings, tokens, latency, cost, and outcome.
6. Shadow upgrades and revalidate prompts, tools, schemas, and retrieval with the new configuration.

Simple evidence extraction may regress under unnecessary deliberation; complex synthesis may benefit. Decide from protected application tasks, not parameter count, public branding, or one general benchmark.

## Part of

← [[Model Configuration]]

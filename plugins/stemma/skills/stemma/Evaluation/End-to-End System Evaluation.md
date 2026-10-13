---
tags: [evaluation]
---
# End-to-End System Evaluation

Component improvements are necessary but not sufficient. End-to-end evaluation tests whether a complete, versioned system satisfies the user's task under realistic operating constraints.

## When This Enters the Build

Run a small end-to-end set as soon as a thin vertical slice exists, then rerun it after meaningful component changes. It is an integration check during development, not a ceremony reserved for production. Expand to the protected release suite only when the assembled candidate may ship.

Use component evaluation to decide *where* and *why* to change the system; use this note to decide whether the complete candidate is actually better. Leave with a system-level adopt, constrain, reject, or inconclusive decision and the component hypotheses needed to explain failures.

## Write the System Contract

Define target users, tasks, corpus state, languages, risk classes, and deployment conditions; acceptable outcomes and justified abstention; quality, evidence, authorization, freshness, latency, reliability, and cost constraints; which metrics are objectives, diagnostics, or non-compensable gates; and the smallest effect that would change the release decision.

## Build a Representative Evaluation Matrix

Cross task classes with meaningful slices such as answerability, corpus version, source type, tenant/authorization state, language, difficulty, recency, and harm severity. Include ordinary traffic, important rare cases, known failures, and boundary cases. Weight aggregate reporting to a declared target distribution, but display critical slices separately.

## Compare Complete Manifests

1. Freeze baseline and candidate manifests: corpus, parser/index, retrieval, context assembly, prompt, model, policies, caches, and evaluators.
2. Run both on the same cases in matched order or with controlled randomization.
3. Preserve case-level outputs, traces, evidence, costs, and failures.
4. Apply invariant checks before quality scoring.
5. Estimate paired changes and uncertainty overall and by prespecified slice.
6. Review severe failures, metric disagreements, and unexpected gains.

Repeat runs when sampling, tools, or infrastructure add meaningful variance. Report failure probability and run-level variation rather than hiding them in a mean.

## Measure the Whole Outcome

- task success or answer correctness;
- evidence sufficiency, claim support, and citation completeness;
- answerability, calibrated abstention, and escalation quality;
- authorization, privacy, safety, and policy integrity;
- latency distributions, cost, retries, availability, and timeouts;
- consistency across repeated runs and critical slices.

Do not collapse these into one score unless its weights represent an explicit utility model. Safety, authorization, and severe-harm conditions usually remain separate gates.

## Diagnose Interactions

Good components can combine badly: recall may add distractors, reranking may remove complementary evidence, compression may break citations, a stronger generator may over-answer, and caching may cross authorization or freshness boundaries. Use controlled component substitutions to locate the interaction rather than guessing from the terminal answer.

## Interpret the Result

- **Adopt:** decision-relevant improvement with every gate satisfied.
- **Constrain:** benefit is localized and routing can safely limit exposure.
- **Reject:** a gate fails or harm outweighs demonstrated gain.
- **Inconclusive:** uncertainty, evaluator disagreement, or sparse critical slices cannot distinguish candidates.

## Decision Output

Produce a reviewable record containing manifests, dataset and evaluator versions, paired results with uncertainty, critical-slice outcomes, invariant violations, representative failures, rationale, rollout constraints, rollback signals, and cases for regression testing.

## Next

→ [[Robustness & Adversarial Testing]]

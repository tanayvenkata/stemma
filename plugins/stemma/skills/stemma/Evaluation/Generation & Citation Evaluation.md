---
tags: [evaluation]
---
# Generation & Citation Evaluation

Evaluate generation against fixed evidence before changing retrieval. This isolates whether context preparation, prompting, generation, citation, or post-processing caused the observed difference.

## When This Enters the Build

Use this as soon as the thin vertical slice produces answers. Begin with fixed evidence packets so retrieval cannot hide generation failures; establish deterministic format and citation checks plus the smallest necessary semantic rubric. Then evaluate the generator on live retrieved context and add claim-level or specialized criteria only when the product needs them.

Leave with a versioned answer contract, rubric/evaluator manifest, answerable and unanswerable cases, and evidence showing whether failures arise from supplied context or from generation. Revisit after context assembly, prompt, model, decoding, citation, post-processing, or abstention changes.

## Define the Case Contract

Each case should contain the user request and conversation state; the exact evidence visible to the generator, including source identity and authorization; required, optional, and forbidden claims; expected behavior for full, partial, conflicting, stale, and absent evidence; output and safety constraints; and a severity-aware scoring rubric.

Do not require one reference wording. Label the facts and behaviors that matter so a valid paraphrase can pass.

## Run a Controlled Comparison

1. Freeze cases, evidence, sampling policy, evaluators, and runtime environment.
2. Change one decision surface: context preparation, prompt, generator/settings, or post-processing.
3. Run baseline and candidate on the same cases. Repeat stochastic generation or declare a deterministic setting; retain run-level results.
4. Apply deterministic checks first, then claim-level human or calibrated-judge labels.
5. Compare paired changes overall and by answerability, source conflict, risk, language, and response length.
6. Inspect disagreements and severe failures before deciding.

| Decision surface | Hold fixed | Diagnose with |
|---|---|---|
| Context preparation | request, evidence set, generator | required-claim coverage, evidence use, position sensitivity, latency |
| Prompt or policy | request, evidence, generator | correctness, supported abstention, instruction adherence |
| Generator/settings | request, evidence, prompt | quality distribution, run-to-run stability, cost, tail latency |
| Post-processing | raw generation | schema validity, citation mapping, false correction, information loss |

## Label the Answer at Claim Level

Break an answer into independently verifiable claims. For each material claim, record correctness, support by supplied evidence, relevance, importance, citation mapping, and failure reason. Useful failure labels include contradiction, unsupported addition, omission, stale evidence, ambiguity, and instruction violation.

Report error incidence and severity. One unsupported high-impact claim can outweigh many correct incidental claims, so never release from an average alone.

## Evaluate Citations Separately

- **Citation entailment:** does the cited passage support the associated claim?
- **Citation completeness:** what share of important externally verifiable claims have adequate support?
- **Citation placement:** can the reader identify which citation supports which claim?
- **Evidence coverage:** are all regions needed for a multi-part claim cited?
- **Source suitability:** is the source authoritative, current enough, and authorized?

Measure precision and recall over claim-citation pairs, but retain the underlying labels. A citation can be correctly formatted and still fail entailment; an answer can be factually correct but unsupported by the supplied corpus.

## Calibrate Semantic Evaluation

Create a human-adjudicated sample containing clear passes, clear failures, and boundary cases. Compare judge decisions with humans by class and severity, not only total agreement. Preserve evaluator prompt, model, parameters, evidence presentation, and rubric version. Recalibrate after material domain, language, or judge changes.

## Decision Output

Record the winning manifest, paired effect by slice, uncertainty or run-to-run variation, severe regressions, representative failures, and next experiment. Decisions are **adopt**, **reject**, **constrained rollout**, or **inconclusive—collect discriminating evidence**.

## Part of

← [[Component Evaluation Harness]]

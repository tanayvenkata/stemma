---
tags: [generation]
reviewed: 2026-10-11
---
# Hallucination Detection & Verification

Verification tests observable claims and actions against allowed evidence and rules. No detector proves that an answer is hallucination-free; every verifier has coverage, calibration, latency, and shared-error limits.

## Decompose the Output

1. identify material externally verifiable claims;
2. map each claim to cited or allowed evidence;
3. label supported, contradicted, unsupported, ambiguous, or not applicable;
4. check required claims and important omissions;
5. validate numbers, units, dates, entities, calculations, and source authority;
6. choose pass, repair, regenerate, abstain, or escalate under a bounded policy.

## Verification Methods

| Method | Strength | Limitation |
|---|---|---|
| deterministic schema/business checks | precise for explicit invariants | limited semantic coverage |
| source-span/citation validation | auditable evidence link | retrieved source may itself be wrong or incomplete |
| entailment or classifier | scalable claim-level signal | domain shift and threshold calibration |
| independent retrieval | can seek missing/counter evidence | repeats retrieval failure and adds latency |
| model critic/judge | flexible semantic review | shared bias, prompt sensitivity, cost, variance |
| human review | handles ambiguity and high stakes | slow, costly, and not perfectly consistent |

Use the cheapest method valid for the risk. Offline model judging and online verification are not separated by a universal latency boundary; some semantic checks may run synchronously, selectively, asynchronously, or only before consequential actions.

Small specialized claim-support checkers can approach general model judges on public faithfulness benchmarks at a fraction of the cost (for example, [MiniCheck](https://arxiv.org/abs/2404.10774) reports GPT-4-level accuracy on its grounding benchmark with a much smaller model), but that parity does not transfer automatically. Validate on in-domain claims, especially near-miss answers that are mostly correct with one material error, and check input limits: a verifier that truncates long evidence can return a confident verdict about only part of it.

## Repair Policy

Deterministically repair syntax only when meaning is unchanged. For semantic failures, preserve the original output and evidence, limit regeneration attempts, and ensure repeated calls do not merely produce a different unsupported answer. High-impact claims may require human approval.

Evaluate verifier precision/recall by failure class, claim coverage, false confidence, latency/cost, and the complete policy outcome—not only detector accuracy.

## Part of

← [[Post-Generation Processing]]

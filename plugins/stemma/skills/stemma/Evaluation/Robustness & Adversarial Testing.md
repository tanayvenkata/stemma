---
tags: [evaluation]
---
# Robustness & Adversarial Testing

Robustness testing measures how behavior degrades as realistic conditions vary. Adversarial testing asks whether a capable opponent can exploit the system. They overlap, but require different sampling and interpretations.

## When This Enters the Build

Introduce matched perturbations once the clean thin slice behaves well enough that degradation is interpretable. Test critical authorization, privacy, destructive-action, and data-integrity invariants earlier; those are design constraints, not polish. Before release, expand from a few mechanism checks into threat-model-driven families and intensity curves.

Leave with known robustness boundaries, attack success by valid attempt and consequence, required mitigations, and regression families. Return when capabilities, tools, permissions, corpus sources, user populations, defenses, or attacker assumptions change.

## Start with a Threat and Variation Model

For each risk, specify the protected asset, source of variation or actor, capability, attack surface, expected safe behavior, impact, and observable evidence. Cover accidental stress—noise, drift, missing data, service failure—and intentional abuse such as poisoned documents, indirect prompt injection, authorization probing, or tool manipulation.

Do not claim that a finite suite proves safety. A clean run establishes only that no covered attack succeeded under tested conditions.

## Construct Test Families

| Family | Controlled variations | Required interpretation |
|---|---|---|
| Answerability | absent, partial, ambiguous, stale, or conflicting evidence | unsafe answer and unnecessary refusal separately |
| Distractors | overlap, plausibility, count, position, authority, contradiction | degradation curve relative to clean matched case |
| Corpus manipulation | poisoned passages, duplicated claims, forged authority, hidden instructions | success by attack family and defense layer |
| Access control | unauthorized documents, tenant boundaries, cache keys, metadata omissions | any exposure is an invariant violation |
| Operational faults | timeouts, partial indexes, stale caches, malformed tool output | recovery, safe degradation, and escalation |
| Distribution shift | new topics, languages, formats, user populations | slice-specific drift, not only aggregate change |

Create paired clean and stressed variants so the perturbation's effect is observable. Vary intensity across several levels; one arbitrary distractor count does not reveal a robustness boundary.

## Execute the Protocol

1. Freeze system, corpus, attack generator, and evaluator manifests.
2. Run clean controls and matched perturbations, repeating stochastic cases when needed.
3. Record attempted attacks, valid attacks, system exposures, successful impacts, false alarms, latency, and recovery.
4. Report degradation by stress intensity and critical slice.
5. Manually validate apparent bypasses and defense successes; broken fixtures create false attacks and false confidence.
6. Retest mitigations against original cases, nearby variants, and untouched holdouts.

## Metrics Without False Comfort

- unsafe-answer and unnecessary-refusal rates for answerability;
- paired quality degradation across distractor intensity;
- attack success among valid attempts, stratified by family and capability;
- exposure and impact severity for authorization or sensitive-data failures;
- detector false-positive and false-negative rates;
- safe recovery and time to recovery for operational faults.

For zero observed critical failures, report the number, diversity, and provenance of valid trials and an uncertainty bound where appropriate. “Zero observed” is not “impossible.” Derive gates from impact tolerance, policy, coverage, and uncertainty—not a universal percentage.

## Red-Team Learning Loop

Keep attack development capable of challenging the builders. Cluster failures by mechanism, fix the earliest reliable control boundary, and turn verified failures into versioned regression families. Refresh hidden attack sets to reduce overfitting.

Indirect prompt injection through retrieved documents is a first-class RAG threat, but test the full consequence chain: malicious content is retrieved, interpreted as instruction, granted capability, and able to create impact. Repeating an injected phrase and disclosing a secret are different severities.

Primary references: [NIST AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) and [OWASP Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

## Next

→ [[Regression & Production Feedback]]

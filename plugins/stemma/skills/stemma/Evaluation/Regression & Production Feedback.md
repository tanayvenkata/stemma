---
tags: [evaluation]
---
# Regression & Production Feedback

Offline evaluation and production evidence form a loop. Production reveals workload, environment, and interaction failures; controlled evaluation determines whether a proposed change addresses the mechanism without creating unacceptable regressions.

## When This Enters the Build

Design the evidence capture before launch, because missing manifests and traces cannot be reconstructed reliably after an incident. The full feedback loop begins with staged or production exposure: observe a signal, verify the outcome, minimize the causal case, reproduce it offline, test a remediation, and promote the case into the appropriate regression family.

Leave with traceable evidence from exposure to release decision. Do not copy every complaint or low-quality proxy directly into the benchmark; review it first so production feedback improves the measurement system rather than contaminating it.

## Define Production Evidence Before Launch

Specify the decisions monitoring must support and log the minimum evidence needed: task class, authorization context, corpus/index/prompt/model/policy/cache versions, source identities, structured decisions, latency and cost, outcome signals, and trace identifiers. Apply privacy, retention, and access controls; do not collect sensitive content merely because it may be useful later.

Separate direct outcomes (verified completion, adjudication, incident impact), behavioral signals (correction, escalation, abandonment, retry), system proxies (retrieval or judge scores, latency, errors), and exposure (who encountered which version). Proxies can trigger investigation but do not prove user harm or improvement.

## Turn a Production Failure into a Regression Case

1. Preserve the trace and version manifest before mutable state disappears.
2. Verify outcome and impact; distinguish product failure from instrumentation or evaluator failure.
3. Minimize, redact, synthesize, or access-control the artifact while retaining the causal mechanism.
4. State expected and prohibited behavior, severity, and the narrowest reliable check.
5. Reproduce against the implicated version when possible.
6. Add the minimized case to its component slice and an end-to-end family; add neighboring variants to prevent one-example patching.
7. Keep untouched holdouts and refresh representative samples so the suite does not become an incident scrapbook.

## Detect Drift and Feedback Bias

Monitor input mix, corpus composition and freshness, authorization distribution, outcomes and proxies, evaluator distributions, latency, and errors by version and slice. Compare like-for-like cohorts and account for exposure: changed routing alters which cases receive labels. User feedback is selected, delayed, and sometimes strategic, so analyze who could provide it and which outcomes remain unobserved.

Investigate when a signal's magnitude, persistence, impact, or novelty could change an operational decision. Fixed thresholds belong to explicit service or safety requirements; otherwise use baselines, uncertainty, and expected variation.

## Change Triggers and Test Selection

Rerun affected component suites plus targeted end-to-end cases for changes to corpus, parsing, indexing, retrieval, context assembly, prompts, models, tools, policies, caches, routing, or stopping. Dependency-aware selection accelerates feedback but cannot prove absence of interactions, so run the complete release suite at declared checkpoints.

## Release Feedback as an Experiment

Where risk permits, use shadowing, staged exposure, or randomized comparison with prespecified success, guardrail, rollback, and observation rules. Check novelty, interference, delayed outcomes, and allocation or logging failures before interpreting results. Online uplift cannot compensate for authorization, safety, or severe reliability violations.

### Choose the exposure design from consequence

| Design | What it can establish | Main limitation |
|---|---|---|
| Replay on recent production traces | behavior on real inputs without new user exposure | mutable tools/corpus and missing counterfactual outcomes |
| Shadow evaluation | candidate decisions under live traffic without executing effects | cannot measure user interaction or downstream consequences faithfully |
| Interleaving or blinded preference | relative quality with efficient within-request comparison | preference may not represent task success and designs are domain-specific |
| Randomized controlled exposure | causal effect on declared user/business outcomes | requires traffic, time, valid instrumentation, and acceptable risk |
| Staged rollout | detects severe operational failure while limiting blast radius | before/after changes confound causal interpretation |

For randomized exposure, define the randomization unit—request, user, account, team, or time block—to prevent cross-condition contamination. Preserve assignment, eligibility, exposure, noncompliance, missing outcomes, and analysis population. Check sample-ratio mismatch before interpreting uplift.

Do not optimize only immediate clicks or preferences when success is delayed task completion, retained trust, lower review burden, or fewer incidents. Define observation windows and guardrails in advance. If users or agents interact with one another, interference can invalidate an ordinary independent-user analysis.

Repeatedly inspecting an experiment and stopping when favorable inflates false discoveries unless a sequential design or stopping rule accounts for it. Segment and metric exploration can generate hypotheses, but confirm decision-critical claims on fresh exposure or under a declared multiple-testing policy.

### Connect online and offline evidence

When online and offline results disagree, investigate population shift, evaluator validity, product adaptation, latency, interaction effects, novelty, and logging before choosing the preferred story. A/B uplift can validate the complete product decision but is weak at locating mechanism; offline traces and component substitutions provide diagnosis.

Promote confirmed online failures and successes into reviewed offline cases. Refresh traffic weights without allowing the current production policy to define the entire benchmark; otherwise behavior the system never attempts remains invisible.

## Decision Output

Maintain a record containing exposure, manifests, signal definitions, uncertainty, confirmed incidents, drifted slices, regression cases, mitigations, and the next monitoring or experiment decision. Preserve provenance from production observation to minimized case to release gate.

Production release and incident-response notes consume and supply this evidence, but remain separate graph clusters.

Primary references: [Google Rules of ML: monitoring and training-serving skew](https://developers.google.com/machine-learning/guides/rules-of-ml) and [Microsoft Research: trustworthy post-experiment analysis](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-post-experiment-stage/).

## Next

→ [[Failure Diagnosis & Error Analysis]]

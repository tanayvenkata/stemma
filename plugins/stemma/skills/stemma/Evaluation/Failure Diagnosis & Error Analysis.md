---
tags: [evaluation]
---
# Failure Diagnosis & Error Analysis

Diagnosis converts an observed failure into a tested causal explanation. The terminal symptom rarely identifies the broken component: one wrong answer can arise from missing content, authorization filtering, parsing, retrieval, context assembly, generation, post-processing, or an incorrect label.

## When This Enters the Build

Use this whenever a component metric, end-to-end case, production signal, or evaluator disagreement reveals a consequential failure whose cause is unclear. Start at the first observable boundary, preserve the complete manifest and trace, then substitute verified inputs one stage at a time.

Leave with a supported mechanism, not merely a plausible story; a remediation experiment; nearby and holdout cases; and the monitoring or regression signal that would detect recurrence. If the evidence instead shows a bad label or evaluator, repair and version the measurement instrument rather than tuning the system to satisfy it.

## Preserve Evidence Before Explaining

Capture request and conversation state, expected outcome and label provenance, system manifest, corpus/index versions, candidate and retrieved documents with scores, context actually sent, raw and post-processed outputs, policy decisions, tool observations, timing, retries, and evaluator outputs. First reproduce the failure or establish why replay cannot match the original environment.

## Triage Invariants First

Check authorization, privacy, and tenant isolation; data and index completeness/freshness; schema, timeout, retry, cache, and version integrity; evaluation-label or fixture errors; and whether the expected answer was knowable under the available evidence and policy. An invalid oracle or stale corpus can masquerade as a model failure.

## Build Competing Hypotheses

| Stage | Hypothesis | Discriminating evidence or intervention |
|---|---|---|
| Corpus/ingestion | information is absent, stale, corrupted, or unauthorized | inspect source and parsed regions; replay verified snapshot |
| Query/routing | system searched the wrong scope or representation | compare original and oracle route/query with index fixed |
| Candidate retrieval | evidence never entered the candidate set | measure region recall at a diagnostic cutoff; inspect filters |
| Ranking/context | evidence was demoted, truncated, duplicated, or obscured | inject evidence at controlled positions; swap ranking/context only |
| Generation | adequate evidence was visible but omitted, contradicted, or embellished | run generator on an oracle evidence packet; label claims |
| Post-processing | correct raw output was damaged, miscited, or rejected | compare raw and served output plus validator decisions |
| Evaluation | reference, judge, or metric is wrong | independent adjudication and rubric review |

Do not stop at the first plausible story. Rank hypotheses, state what each predicts, and run the cheapest intervention that separates them.

## Use Counterfactual Substitution

Replace one stage at a time with a verified corpus region, oracle query/route/scope, oracle candidate set/ranking, oracle context packet, or reference generation/post-processing result. If replacement repairs the failure repeatedly on matched cases, that stage is implicated—but its inputs may still be causal. Test nearby cases and reverse the substitution before claiming causality.

## Classify the Failure Mechanism

Use a multi-label taxonomy. Record symptom, earliest implicated boundary, contributing conditions, severity, detectability, reproducibility, affected slices, and confidence. Examples include content absence, parsing loss, metadata/filter error, query mismatch, retrieval miss, ranking loss, context competition, unsupported claim, omission, unsafe non-abstention, citation mismatch, policy violation, and operational fault.

## Choose a Remediation Experiment

Generate multiple candidate fixes when practical. Define the mechanism each should change, cases it should improve, likely collateral regressions, required component and end-to-end checks, and rollback condition. A technique name is not a diagnosis: hybrid retrieval, reranking, prompt changes, larger context, or verification may help some mechanisms and worsen others.

Validate on reproduced failures, neighboring variants, representative benchmarks, critical slices, and untouched holdouts. Reject a fix that only memorizes the incident or moves failure downstream.

## Diagnosis Record

Close with the symptom and impact; evidence and manifest; hypotheses and experiments; supported explanation with confidence and remaining uncertainty; selected remediation and rejected alternatives; regression cases, monitoring signals, ownership, and follow-up date.

The goal is not merely to make one case pass. It is to learn a reusable failure mechanism and establish evidence that the repair improves the intended system boundary.

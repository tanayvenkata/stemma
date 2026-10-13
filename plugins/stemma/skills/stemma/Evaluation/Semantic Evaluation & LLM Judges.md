---
tags: [evaluation]
---
# Semantic Evaluation & LLM Judges

## Contents

- The Map: Five Different Roles
- Choose the Evaluation Path
- Greenfield RAG: What to Add and When
- Write One Rubric for One Construct
- Choose a Judgment Design
- Minimal Implementation
- Framework and Telemetry Boundary
- Practical Completion Check
- Branches

Semantic evaluation begins when ordinary code and retrieval labels cannot validly decide an important property such as claim support, completeness, or usefulness. An LLM judge is one scalable scorer for that property—not the ground truth and not the starting point for every evaluation.

## The Map: Five Different Roles

```text
what should happen?       → reference, evidence, constraints, or human judgment
what property matters?    → one construct and rubric
how is it scored?         → code, semantic model, LLM judge, or human
how are outputs compared? → pointwise, pairwise, or reference-guided design
can the scorer be trusted?→ validation against independent human labels
```

Do not collapse these roles. A reference answer is an input to evaluation, not a scorer. Pointwise and pairwise are comparison designs that either a human or a model can apply. A framework runs the process but does not decide what quality means.

## Choose the Evaluation Path

```text
Can ordinary code decide the property correctly?
├─ yes → deterministic assertion or task metric
└─ no
   ├─ Is known evidence or expected content available?
   │  └─ yes → reference/evidence-guided comparison
   └─ Does the property require semantic judgment?
      ├─ low volume, novel, or high consequence → human review
      └─ repeated at scale → rubric-based model judge, validated against humans
```

Methods compose when they answer different questions. A RAG answer can receive deterministic citation checks, evidence-coverage metrics, a claim-support judge, and human escalation for severe uncertainty.

## Greenfield RAG: What to Add and When

| Stage | Use now | Add only when this trigger appears |
|---|---|---|
| Thin retrieval baseline | source-region labels and ranking metrics | semantic relevance judgment when retrieved evidence is useful but labels cannot capture it reliably |
| First generated answers | deterministic schema/citation checks, required claims, manual review | one judge for a recurring semantic failure that manual review cannot scale |
| Repeated candidate comparison | validated judge on its accepted slices, paired case results | pairwise judging when relative quality is easier to decide than an absolute score |
| Release preparation | protected cases, hard constraints, human review of severe failures | broader judging only for release-relevant criteria and slices |
| Production learning | traces, sampled audits, verified user outcomes | online scoring after privacy, selection bias, drift, and incident handling are defined |

Do not add a judge because generation exists. Add one because an important semantic decision is otherwise unmeasured and repeated human review is impractical.

## Write One Rubric for One Construct

Separate groundedness, correctness, completeness, relevance, usefulness, and style. For one construct, specify:

- the question the evaluator must answer;
- allowed evidence and what must be ignored;
- observable labels or score anchors;
- critical failures and boundary examples;
- `insufficient evidence` or abstention behavior;
- structured output: verdict, cited evidence, and a concise rationale.

The rationale makes a verdict inspectable; it does not prove the verdict.

### Grader analogy

A teacher first decides whether the assignment measures factual accuracy, argument quality, or writing style. Only then can a rubric be written. Asking an automated grader to emit one “overall quality” score hides which assignment it graded and why.

## Choose a Judgment Design

| Design | Plain-language question | Use when | What it cannot establish |
|---|---|---|---|
| **Pointwise** | Does this output meet fixed anchors? | absolute requirements, failure labels, release floors | whether another output is relatively better |
| **Pairwise** | Is A better than B, or are they tied? | comparing a candidate with a baseline | whether either output is acceptable in absolute terms |
| **Reference-guided** | Does the output contain the required claims or follow the allowed evidence? | bounded expected behavior | open-ended quality outside the reference's scope |

They can be combined. For example, require pointwise groundedness, compare baseline and candidate pairwise for usefulness, and use reference claims for completeness.

## Minimal Implementation

```yaml
criterion: claim_groundedness
allowed_evidence: retrieved_context_only
labels:
  supported: the cited evidence entails the claim
  contradicted: the evidence conflicts with the claim
  unsupported: the evidence does not establish the claim
  insufficient_evidence: the supplied inputs cannot be judged
output:
  claim: string
  verdict: enum
  evidence_spans: list
  rationale: string
```

Run this first on human-labeled development and validation cases. If the judge is accepted for the intended slices, run it on baseline and candidate outputs from the same cases, retain every verdict and scorer error, and report paired differences. The separate judge-calibration node explains how to validate and operate it.

## Framework and Telemetry Boundary

- An evaluation framework stores cases, invokes scorers, compares runs, and reports results.
- A judge adapter sends the rubric and inputs to a model and parses its verdict.
- Telemetry records what happened: retrieval, prompt construction, model calls, verdicts, latency, and cost.
- Your evaluation specification defines the construct, ground truth, rubric, and decision rule.

No framework or trace automatically establishes correctness.

## Practical Completion Check

Before using a semantic score to make a decision:

- [ ] The construct and allowed evidence are explicit.
- [ ] A cheaper valid method was considered first.
- [ ] The comparison design matches the decision.
- [ ] The scorer was validated on representative independent labels.
- [ ] Its severe false-pass cases and accepted scope are known.
- [ ] Raw per-case verdicts, evidence, versions, failures, latency, and cost are retained.

Primary references: [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685), [G-Eval](https://arxiv.org/abs/2303.16634), and [NIST AI RMF measurement guidance](https://airc.nist.gov/AI_RMF_Knowledge_Base/Playbook/Measure).

## Branches

- [[Judge Calibration & Validation]]

## Part of

← [[Evaluation Strategy & Experimental Design]]

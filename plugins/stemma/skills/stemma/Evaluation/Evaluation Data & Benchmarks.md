---
tags: [evaluation]
reviewed: 2026-10-11
---
# Evaluation Data & Benchmarks

## Contents

- Where This Enters a Zero-to-One Build
- 1. Define the Case Before the Dataset
- 2. Build Three Datasets for Three Jobs
- 3. Construct the Dataset
- 4. Synthetic Coverage Expansion
- 5. Split, Promote, and Maintain
- Sources
- Branches
- Next

Evaluation data is the evidence used to make a specific system decision. A useful benchmark represents the behavior, traffic, risks, and failure boundaries that matter; a large collection of easy or ambiguous questions does not.

## Where This Enters a Zero-to-One Build

Start the case schema during task and corpus discovery, before optimizing any pipeline component. At that point, create only enough reviewed cases to exercise the important behaviors and risks through a thin vertical slice. The first parser, region-based chunker, representation, retriever, and minimal answer surface make those cases runnable; they are a baseline, not individually optimized components.

Then expand the evidence alongside the build:

```text
task and corpus discovery
→ define cases, slices, expected behavior, and stable source evidence
→ build the thinnest complete path that can run those cases
→ compare chunking with region-level labels
→ lock and version the selected chunking policy
→ derive chunk-level judgments for embedding, retrieval, and reranking
→ add claim-level and end-to-end judgments as generation becomes real
→ promote stable cases into regression and release suites
```

Evaluation owns the decision evidence; the pipeline clusters own how each component is built. Work can therefore move back and forth: corpus inspection reveals needed slices, component experiments reveal ambiguous labels, and production failures become reviewed regression cases.

## 1. Define the Case Before the Dataset

Each case should preserve enough information to reproduce the task and diagnose a failure:

```json
{
  "case_id": "stable-identifier",
  "task": "the user intent or operation being evaluated",
  "input": "the exact query or request",
  "expected_behavior": "answer, abstain, retrieve, route, or act",
  "evidence": "source regions or other grounds for the expectation",
  "labels": "component-specific relevance, claims, actions, or constraints",
  "slices": ["source-type", "difficulty", "risk", "language"],
  "provenance": "human, production, synthetic, or transformed",
  "versions": "corpus, parser, labels, rubric, and relevant configuration"
}
```

Not every field must be stored in one JSON object, but each must be recoverable. The evaluation unit must also be explicit: query, query-document pair, answer, session, trajectory, user, or another independent unit.

## 2. Build Three Datasets for Three Jobs

The tiers describe how a dataset is used, not fixed query counts.

| Dataset tier | How to construct and size it | What it can justify |
|---|---|---|
| **Tier 1: Smoke / Sanity Set** | Include at least one decisive case for every critical path, invariant, and previously observed catastrophic failure. Keep it small enough for frequent local runs. | Detect obvious breakage quickly. It cannot establish average quality or a general improvement. |
| **Tier 2: Component Benchmark** | Cover the slices relevant to the component decision. Pilot the comparison, inspect paired-result variance, and add cases until uncertainty is narrow enough around the smallest effect that would change the decision. | Compare chunkers, retrievers, rerankers, prompts, models, or policies and diagnose where their behavior differs. |
| **Tier 3: Release Suite** | Use a broad, versioned, risk-weighted distribution with protected cases, important rare slices, end-to-end invariants, and operational guardrails. | Support a release decision within the represented scope. It does not prove behavior outside that scope. |

### How to Size Without Guessing a Universal Number

1. Define the smallest difference that would be worth adopting after latency, cost, and risk are considered.
2. Identify the slices on which the decision must be valid; ensure each has enough independent cases to be interpreted.
3. Run a pilot on paired cases, because evaluating baseline and candidate on the same cases isolates case difficulty.
4. Examine the distribution and interval of per-case differences, not only the difference between aggregate means.
5. Add cases where the interval is too wide, coverage is weak, or failures cluster ambiguously.
6. Stop when the evidence can support the decision—or explicitly report that the result remains unresolved.

Smoke-set size is governed mainly by behavioral coverage. Component and release-suite size is governed by coverage, observed variance, failure cost, and the precision needed for the decision. Repeated stochastic runs characterize model variance but do not replace independent cases or missing traffic slices.

## 3. Construct the Dataset

### A. Start with a Coverage Plan

List the dimensions that could change behavior:

- task or user intent;
- answerable, ambiguous, and unanswerable requests;
- source type, structure, quality, language, and recency;
- modality and whether decisive evidence is textual, visual, spatial, tabular, audio, or cross-modal;
- single-source versus multi-source reasoning;
- surface-match versus reasoning-intensive retrieval, where the system must infer what evidence would solve the problem;
- common traffic versus rare high-consequence cases;
- permissions, tenant boundaries, and other integrity constraints;
- known failures and plausible adversarial conditions.

Create a coverage table before generating cases. Sampling hundreds of examples without one can repeatedly test the easiest slice while omitting the decision boundary.

### B. Mix Evidence Sources Deliberately

| Source | Strength | Main risk | Typical use |
|---|---|---|---|
| Reviewed production cases | Real language and behavior | Historical system and traffic bias; privacy concerns | Represent actual traffic and failures |
| Expert-authored cases | Precise intent and high-risk coverage | Expensive; author expectations can leak into wording | Define critical behaviors and edge cases |
| Source-derived synthetic cases | Scalable corpus coverage | Artificial phrasing, unsupported answers, and generator bias | Fill identified coverage gaps |
| Transformed cases | Controlled difficulty and counterfactuals | Transformation may change answerability or realism | Stress a particular capability or boundary |

No source is sufficient alone. Keep provenance so results can be sliced by origin; a candidate that improves synthetic questions but regresses production cases has not demonstrated a general improvement.

### C. Label at the Stable Layer

Attach ground truth to the behavior being evaluated. For rechunking experiments, source regions are more durable than chunk IDs. For generation, expected claims and supporting evidence are usually more diagnostic than one reference string. For routing or agents, several actions or trajectories may be valid.

The labeling schema, provenance, adjudication, and migration rules live in [[Ground-Truth Labeling & Label Lifecycle]].

## 4. Synthetic Coverage Expansion

Synthetic generation is a method for filling a known coverage gap. It should begin with a target behavior and supporting evidence—not with an instruction to generate many questions.

### Evolutionary Transformations

“Evol-Instruct” is a name used for iteratively making an existing instruction more demanding. The durable technique is **controlled transformation**:

- add a constraint, population, role, or time boundary;
- require comparison or synthesis instead of lookup;
- introduce a realistic ambiguity that should trigger clarification;
- create an unanswerable variant by removing necessary evidence;
- vary surface wording while retaining the same underlying intent.

Use transformations when a valid simple case exists and the harder case represents plausible use. Revalidate the expected answer after every transformation; adding difficulty can silently make a question ambiguous or unsupported.

### Relational Sampling and Graph Walks

A graph walk samples a connected path such as entity A → relation B → entity C, then constructs a question whose answer requires evidence along that path. It is useful when the real task genuinely depends on relationships distributed across sources.

Do not build a knowledge graph merely to generate ordinary single-passage questions. A document-link graph, entity index, manually specified evidence bundle, or direct sampling of related sections may be sufficient. The graph is a sampling aid, not ground truth.

### End-to-End Generation Workflow

```text
choose a missing behavior or slice
→ select the source regions that support it
→ draft the query, expected answer or behavior, and evidence labels
→ optionally apply one controlled transformation or relational hop
→ answer using only the selected corpus evidence
→ verify support, answerability, difficulty, realism, and uniqueness
→ review or adjudicate according to risk
→ assign provenance and place into the appropriate tier
```

### Acceptance Gates

Reject or repair a generated case when:

- the expected answer requires knowledge absent from the cited corpus;
- the question exposes wording copied from the answer or source unnaturally;
- a supposedly multi-hop question can be answered from one passage;
- several answers are reasonable but the rubric allows only one;
- it duplicates or nearly duplicates an existing case;
- the generating model, prompt, or source has contaminated a protected split;
- humans cannot agree on the task after inspecting the evidence and rubric.

For high-consequence cases, synthetic generation proposes candidates; qualified human review establishes the label.

## 5. Split, Promote, and Maintain

1. Split cases before repeatedly tuning candidates. Protect a release set from routine inspection.
2. Develop against the smoke and component sets; compare candidates on paired cases and important slices.
3. Promote stable, well-understood cases into regression suites without allowing repeated incidents to consume the entire holdout.
4. Run the release suite only at meaningful decision points and record every exposure to it.
5. Version corpus, cases, labels, rubrics, and split membership together.
6. When the corpus or parsing changes, migrate derived labels explicitly and preserve the prior benchmark for comparison.
7. Refresh from verified production failures and workload drift while retaining historical cases needed to detect regression.

### Keep capability and regression suites distinct

A capability suite should contain discriminating tasks that reveal what the system cannot yet do reliably. As it approaches saturation, inspect whether the remaining failures are valid and add harder, representative work before the score ceiling hides progress. Solved, stable tasks can graduate into regression coverage.

A regression suite protects behavior already relied upon and should ordinarily remain near its expected pass condition. Do not make it artificially difficult merely to create score variance. Track each suite's owner, intended decision, expected score range, last expert review, protected-set exposures, known blind spots, cost, runtime, and refresh trigger.

Monitor evaluation health itself:

- task solvability and reference-solution success;
- grader failures, disagreement, and changed verdicts;
- saturation and floor effects;
- near duplicates, source leakage, and benchmark contamination;
- mismatch between suite slices and current production traffic;
- harness/environment flakes and infrastructure-induced variance;
- cases that reward loopholes or implementation details rather than the intended outcome.

An evaluation can regress even when the product does not. Version task repairs and rerun historical systems where needed to distinguish instrument change from system change.

## Sources

- [NIST: Sample Sizes Required for a Desired Confidence-Interval Width](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm)
- [WizardLM: Original Evol-Instruct Method](https://arxiv.org/abs/2304.12244)
- [Ragas: One Implementation of Knowledge-Graph Scenario Generation](https://docs.ragas.io/en/latest/getstarted/rag_testset_generation/) (page checked 2026-10)

## Branches

- [[Ground-Truth Labeling & Label Lifecycle]]

## Next

→ [[Component Evaluation Harness]]

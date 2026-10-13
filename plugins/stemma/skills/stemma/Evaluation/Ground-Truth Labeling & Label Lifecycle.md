---
tags: [evaluation]
---
# Ground-Truth Labeling & Label Lifecycle

## Contents

- Label at the Stable Layer
- Specify the Judgment Task
- Annotation and Adjudication Protocol
- Design human evaluation as a study
- Lifecycle
- Quality Checks
- Minimal Label Record
- Sources

Ground truth is a versioned data product. It must identify the behavior being judged, preserve provenance, and change deliberately when the corpus or task changes.

## Label at the Stable Layer

| Evaluation target | Preferred label | Why |
|---|---|---|
| Parsing | Source page/block plus expected text, table, or field | Compares conversion to the source artifact. |
| Chunking | Document regions | Chunk IDs change across strategies. |
| Embedding/retrieval/reranking | Relevant chunk or passage IDs after chunking is fixed | Supports exact rank metrics. |
| Generation | Reference answer, required claims, forbidden claims, and evidence | Separates correctness, completeness, and faithfulness. |
| Routing/agents | Valid actions or routes plus constraints | Often more than one trajectory is acceptable. |

A robust region label combines document version, page/block anchors, a quoted span or content hash, and optional character offsets. Offsets alone drift when the parser changes.

The move from regions to chunks is a deliberate handoff, not a choice between two competing truths. Preserve source-region anchors as the durable authority while chunkers are changing. Once a chunking policy is selected and versioned, map those anchors into the resulting chunks and adjudicate query–chunk relevance for exact ranking evaluation. These chunk-level judgments are a derived operational layer: they enable precise retrieval metrics, but they must be regenerated or migrated whenever chunk boundaries change.

## Specify the Judgment Task

Before annotation, define:

- the evaluation unit and the question annotators must answer;
- allowed labels, including ambiguous, insufficient-evidence, and abstain states;
- whether relevance is binary, graded, passage-level, or claim-specific;
- what evidence annotators may inspect and in which order;
- examples near each decision boundary, not only obvious positives;
- which disagreements require adjudication and who is qualified to decide them;
- whether the label represents one acceptable answer or an exhaustive set.

For retrieval, an unlabeled document is **unjudged**, not necessarily irrelevant. Exhaustive judgment is often impossible, so build a candidate pool from several retrieval methods and human discovery, judge that pool, and track its provenance. When a new candidate retrieves previously unjudged evidence, send it for judgment rather than scoring it automatically as a false positive.

For generation, one reference answer should not become a brittle string target. Represent required and optional claims, acceptable variants, forbidden claims, supporting evidence, and abstention conditions where the task permits them.

## Annotation and Adjudication Protocol

1. Create a small pilot spanning easy, ambiguous, negative, and high-risk cases.
2. Have multiple annotators label the same pilot independently before discussing it.
3. Inspect disagreements by slice and distinguish unclear instructions from legitimate task ambiguity.
4. Revise the rubric and examples; relabel affected pilot cases rather than silently carrying incompatible versions forward.
5. Run production annotation with blinded case order and source provenance where practical.
6. Adjudicate consequential disagreements with a recorded rationale and retain the original labels.
7. Sample accepted labels for ongoing quality control and increase review where annotator or slice drift appears.

Agreement is diagnostic, not a universal gate. A high coefficient can coexist with shared bias or easy cases; low agreement may reveal an underspecified construct rather than careless annotators. Always inspect the disagreement examples.

## Design human evaluation as a study

Human judgment may serve different purposes: establish a reference label, compare two outputs, assess real task utility, discover failures, or validate an automated judge. Name the purpose before recruiting reviewers.

Choose reviewers who match the claim. Domain experts are required when correctness depends on specialized knowledge; representative users are required when usability, trust, or workflow value is the construct. Internal builders are useful for diagnosis but may know the intended system and overlook failures that users experience.

For comparative studies:

- blind system identity and randomize or counterbalance presentation order where possible;
- define whether the unit is a claim, answer, session, artifact, or completed real task;
- separate absolute acceptability from pairwise preference;
- include ties, abstention, and insufficient-evidence states;
- train on shared examples, then measure independently before discussion;
- cap workload, rotate order, and monitor fatigue or learning effects;
- preserve time spent, comments, confidence, and disagreement—not only the final vote;
- analyze reviewer and item effects when several ratings share the same people or tasks.

A preference for fluent output is not evidence of correctness. Whenever possible, give reviewers authoritative outcomes and source evidence, or observe task completion in the real workflow. For high-stakes use, preserve an appeal or adjudication path and document whose values the rubric encodes.

## Lifecycle

1. Define the intended traffic slices and failure costs.
2. Seed with reviewed production examples and expert-written edge cases.
3. Use synthetic generation to expand coverage, then filter for answerability, novelty, and leakage.
4. Track annotator, rubric version, corpus version, parser/chunker version, and adjudication state.
5. Split before tuning. Keep a hidden or rarely inspected release set.
6. After locking chunking, materialize and version chunk-level judgments for embedding, retrieval, and reranking. Regenerate them after rechunking; never discard or silently rewrite their source-region anchors.
7. Add production failures through a review queue, not directly into every benchmark.

Use explicit states such as `draft → independently_labeled → adjudicated → accepted → superseded`. Never overwrite an accepted label without retaining its prior value, rubric version, reason for change, and affected benchmark results.

## Quality Checks

- Measure human-human disagreement before judge-human agreement.
- Record ambiguous and multi-answer cases instead of forcing false certainty.
- Audit coverage by task, source type, language, recency, difficulty, and risk.
- Detect near-duplicate questions and train/test leakage.
- Report slice scores and confidence intervals; an aggregate can hide a critical regression.
- Audit whether benchmark authors or generating models exposed answer wording that the deployed system would not receive.
- Rejudge a sample of stable cases over time to detect rubric, annotator, corpus, or domain drift.

## Minimal Label Record

```json
{
  "case_id": "case-017",
  "evaluation_target": "retrieval",
  "label": "highly_relevant",
  "evidence_anchor": {
    "document_version": "manual-v3",
    "page": 14,
    "quoted_span_hash": "..."
  },
  "annotator": "reviewer-id",
  "rubric_version": "retrieval-rubric-v2",
  "state": "adjudicated",
  "rationale": "Contains the complete warranty exception",
  "supersedes": null
}
```

## Sources

- [TREC: Relevance Judgment Data and Pooling Context](https://trec.nist.gov/data/reljudge_eng.html)
- [National Academies: Reproducibility, Replicability, and Transparent Reporting](https://www.nationalacademies.org/read/25303/chapter/3)
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

## Part of

← [[Evaluation Data & Benchmarks]]

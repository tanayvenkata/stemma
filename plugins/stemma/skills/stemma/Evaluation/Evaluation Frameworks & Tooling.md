---
tags: [evaluation]
reviewed: 2026-10-11
---
# Evaluation Frameworks & Tooling

## Contents

- 1. Specify the Harness Before Selecting a Product
- 2. Capability Families
- 3. Named Frameworks: Orientation, Not Ranking
- 4. About G-Eval and Other Packaged Metrics
- 5. Build a Minimal Framework-Neutral Harness First
- 6. Release-Gate Design
- 7. Upgrade and Replacement Protocol
- Practical Selection Rule

Frameworks execute and record an evaluation design; they do not supply a valid question, representative data, calibrated rubric, or justified release rule. Treat every framework as a replaceable adapter around a framework-neutral evaluation specification.

> [!note] Current snapshot
> Named products and capabilities below were checked in August 2026 and will change. Recheck official documentation, licenses, data handling, and behavior before adoption or upgrade.

---

## 1. Specify the Harness Before Selecting a Product

A portable evaluation case should be able to represent:

```yaml
case_id: stable-id
input: user request
expected:
  evidence_regions: []
  required_claims: []
  forbidden_behaviors: []
slice_labels: []
risk_level: low | medium | high
```

A portable run record should add:

- dataset, corpus, pipeline, prompt, model, judge, rubric, and code versions;
- retrieved regions, answer, component traces, and deterministic measurements;
- per-metric score, verdict, rationale, and scorer error;
- latency, token use, cost, seed or repeat identifier, and timestamp.

Keep these records in an exportable format under your control. If changing tools changes the meaning of a metric or loses per-example history, the abstraction boundary is too weak.

## 2. Capability Families

Choose capabilities from the workflow problem:

| Need | Capability | Questions to ask |
|---|---|---|
| Run repeatable offline suites | Dataset runner and test harness | Can it pair candidates with baselines, repeat stochastic cases, and export every result? |
| Score semantic criteria | Custom rubric or model-judge adapter | Can you control evidence, prompt, judge, parsing, abstention, and calibration? |
| Check objective contracts | Deterministic assertion layer | Can ordinary code compute the rule without a model call? |
| Diagnose components | Tracing/span instrumentation | Are retrieval, reranking, prompt context, generation, and tool calls independently inspectable? |
| Generate candidate cases | Synthetic-data workflow | Are provenance, validation, deduplication, leakage checks, and human review preserved? |
| Gate releases | CI integration and baseline comparison | Can it distinguish hard constraints from uncertain aggregate regressions? |
| Monitor production | Sampling, feedback, alerts, and drift slices | What can be scored without live ground truth, and how are incidents promoted into labeled regression cases? |

No single product must own all of these layers.

## 3. Named Frameworks: Orientation, Not Ranking

As of this snapshot (August 2026; individual product descriptions not rechecked since):

- **Ragas** focuses on RAG-oriented metrics, experiment/evaluation workflows, and test-data generation. Its metric prompts and required fields are implementations that must still be validated for the domain.
- **DeepEval** provides a test-oriented Python workflow, custom and built-in metrics, synthetic data, tracing, and command-line/CI execution.
- **Pydantic Evals** provides a code-first Python workflow for versioned cases, deterministic and custom evaluators, model judges, experiments, and span-based evaluation. It is usable independently of Pydantic AI and can consume OpenTelemetry traces through its observability integration.
- **TruLens** emphasizes instrumented application traces and feedback functions for development and production observability.
- **ARES** is a research method that trains lightweight judges on synthetic examples and uses a smaller human-labeled set to statistically correct estimates from the larger automatically labeled set, an approach called prediction-powered inference. It is more involved than importing a metric library.
- **OpenAI Evals platform:** do not adopt it as a new durable system in this snapshot. OpenAI's documentation states that the platform becomes read-only for existing users on October 31, 2026 and is scheduled to shut down on November 30, 2026 (dates re-verified 2026-10; check OpenAI's deprecations page for changes); migrate any dependency behind the framework-neutral case, scorer, and result interfaces above.

**OpenTelemetry is instrumentation, not an evaluator.** It standardizes how traces, metrics, and logs are emitted and exported. An evaluation framework can read those spans to score retrieval, tool use, or trajectories, but the trace itself does not define groundedness, correctness, or a release decision. Its GenAI semantic conventions have been evolving (check their current status before relying on any attribute name), so preserve internal semantic events and map them through versioned adapters instead of making one external attribute schema your canonical evaluation record.

Do not choose from a feature-count table. Build a small proof against representative cases and evaluate:

1. Does the implementation match your metric definition?
2. Can it reproduce a run and expose raw per-example evidence?
3. Can you supply custom deterministic and judged metrics?
4. Does it support the traces and slices required for diagnosis?
5. What data leaves your environment, and under which retention policy?
6. What happens when a judge call times out, returns malformed output, or changes behavior?
7. Can you export data and replace the framework without relabeling the corpus?
8. What are the runtime cost, concurrency, and rate-limit consequences?

## 4. About G-Eval and Other Packaged Metrics

G-Eval is a judge-prompting procedure, not a universal quality measure. Its original formulation uses task-specific criteria, generated evaluation steps, and—in environments exposing suitable token probabilities—an expected score over allowed rating tokens:

$$
\mathbb{E}[S]=\sum_{k\in\mathcal{K}} k\,P(S=k)
$$

This can make an ordinal score less quantized. It does not establish that the rubric measures the desired construct, that rating-token probabilities are calibrated, or that another framework's similarly named metric is equivalent. Many provider interfaces do not expose comparable token probabilities; record the actual implementation rather than assuming the paper's procedure.

## 5. Build a Minimal Framework-Neutral Harness First

```python
for case in dataset_version:
    baseline = run(system="baseline", case=case)
    candidate = run(system="candidate", case=case)

    for output in (baseline, candidate):
        output.checks = deterministic_checks(output, case)
        output.judgments = calibrated_judges(output, case)

    save_case_record(case, baseline, candidate, run_manifest)

report_paired_deltas()
report_slice_failures()
apply_release_policy()
```

Then use a framework to remove plumbing: parallel execution, caching, trace capture, dashboards, dataset management, or CI reporting. Preserve your own schema and semantics.

## 6. Release-Gate Design

A reliable gate distinguishes:

- **Hard constraints:** no critical safety failure, schema violation, missing citation contract, or unacceptable operational error.
- **Non-regression constraints:** no practically material deterioration in protected metrics or risk slices, under a declared uncertainty rule.
- **Improvement evidence:** a useful paired effect on the target metric, not merely a higher point estimate.
- **Diagnostic output:** retained case-level diffs, traces, failure categories, and scorer errors.

Do not install dependencies from the network on every evaluation run without a lockfile. Pin the harness environment and action versions, cache only inputs whose identity is included in the key, and fail visibly when scorer infrastructure fails. “No scores produced” is not a passing evaluation.

Start with a fast smoke suite on each change and run broader or expensive suites at release boundaries or on a schedule. Determine suite membership from risk and empirical runtime, not a universal case count.

## 7. Upgrade and Replacement Protocol

When changing a framework, judge, built-in metric, or major version:

1. Run old and new implementations on the frozen calibration and regression sets.
2. Compare per-example verdicts, not only mean scores.
3. Investigate disagreements by slice and severe-failure class.
4. Recalibrate thresholds or release rules; never assume numerical continuity.
5. Record the migration boundary in run metadata.
6. Keep the prior evaluator available long enough to reproduce historical decisions when practical.

## Practical Selection Rule

Adopt the smallest toolset that lets you define metrics explicitly, run versioned cases, capture component evidence, compare paired outputs, quantify uncertainty, and export results. Add a platform when coordination or observability pain is demonstrated—not because a library has a long metric menu.

Primary sources: [Ragas documentation](https://docs.ragas.io/), [DeepEval documentation](https://deepeval.com/docs/introduction), [Pydantic Evals documentation](https://pydantic.dev/docs/ai/evals/evals/), [TruLens documentation](https://www.trulens.org/), [OpenAI Evals documentation and deprecation notice](https://developers.openai.com/api/docs/guides/evals), [OpenTelemetry documentation](https://opentelemetry.io/docs/specs/semconv/gen-ai/), [ARES paper](https://aclanthology.org/2024.naacl-long.20/), and [G-Eval](https://arxiv.org/abs/2303.16634).

---

## Part of

← [[Evaluation Strategy & Experimental Design]]

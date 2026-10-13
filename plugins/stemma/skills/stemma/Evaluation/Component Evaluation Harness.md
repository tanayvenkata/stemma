---
tags: [evaluation]
---
# Component Evaluation Harness

## Contents

- Preconditions
- Upstream-First, with Interaction Rechecks
- Controlled Comparison
- Component Decision Matrix
- Metric Interpretation
- Minimal Harness Shape
- Sources
- Branches
- Next

A component harness compares one pipeline decision under controlled, observable conditions. Its purpose is not to declare a universal winner; it determines which candidate works better for a defined workload, why, and at what cost.

## Preconditions

Do not begin with a framework or metric. Preserve:

| Input | Required decision |
|---|---|
| Experiment contract | Hypothesis, baseline, candidate, primary outcome, guardrails, and decision rule |
| Dataset manifest | Split, slices, labels, provenance, and corpus versions |
| Component boundary | Exact input and output observed around the component |
| Controlled manifest | Everything held fixed, including downstream context and budgets |
| Reproduction fields | Code, data, configuration, model or service version, seeds, and timestamp |

Use the Tier 2 component benchmark for comparison, the Tier 1 set for fast breakage checks, and periodic end-to-end tests to detect interactions. Do not tune on the protected release suite.

## Upstream-First, with Interaction Rechecks

```text
parse and ingest
→ chunk and represent
→ embed and index
→ retrieve and filter
→ transform, route, and rerank
→ assemble evidence and generate
→ execute agentic or custom behavior
```

Upstream outputs constrain every downstream stage, so diagnosing from the earliest failing boundary is efficient. This is not a rule to optimize every component once in strict order. Revisit an upstream choice when the corpus, workload, architecture, or downstream objective changes, and rerun end-to-end evaluation after each meaningful local win.

### Greenfield systems: build a thin vertical comparator

During initial construction, use component checks before downstream stages exist: parser fidelity does not require a generator, and ingestion invariants should not wait for a complete application. But do not permanently select an upstream representation solely from intrinsic scores. As soon as practical, assemble the simplest valid path from source to the product's actual output and use it as a downstream probe.

For generative RAG, that thin path may be parse → simple chunks → basic index/retrieval → fixed context template → one generator. For a search product, ranked evidence is already the end-to-end output and no generator is required. The purpose is not production completeness; it is to reveal interactions before local choices harden into expensive dependencies.

## Controlled Comparison

For every baseline/candidate pair:

1. Run both on the same versioned cases.
2. Vary the intended decision and record any coupled changes it necessarily causes.
3. Preserve per-case inputs, intermediate outputs, scores, latency, cost, and errors.
4. Compute paired differences and uncertainty across independent cases; repeat runs where stochastic variance matters.
5. Inspect wins, losses, ties, and failure slices—not only the aggregate.
6. Rerun the assembled pipeline to test whether local gains survive downstream interactions.
7. Adopt, reject, narrow to particular slices, or gather more evidence according to the predeclared rule.
8. Add informative failures to the regression workflow.

When several factors plausibly interact, use a small factorial or staged experiment instead of claiming that a long sequence of one-variable tests found a global optimum. A factorial experiment runs selected combinations of factor levels so you can estimate whether the effect of one choice depends on another; it need not test every possible pipeline combination.

## Component Decision Matrix

| Target | Example variable | Hold fixed where possible | Evidence needed |
|---|---|---|---|
| Parsing and ingestion | extraction or routing policy | source files, expected regions, downstream representation | text/structure/field fidelity, provenance, failure and cost slices |
| Chunking | boundary and contextualization policy | parsed representation, retrieval budget, evaluation regions | region coverage, retrieval outcomes, context integrity, storage and latency |
| Embedding and index | representation or index configuration | chunks, query set, candidate budget | rank/coverage metrics, stability, memory, build/query cost, update behavior |
| Retrieval and metadata | retrieval, fusion, or filtering policy | corpus snapshot, chunks, query labels | relevant-evidence coverage and ranking, authorization integrity, latency |
| Query transformation and routing | rewrite, decomposition, or route policy | original requests, available routes, downstream candidates | intent preservation, route utility, abstention, added latency and cost |
| Reranking | ranking policy and candidate depth | candidate pool, query labels, downstream budget | paired ranking lift, evidence diversity, latency, downstream effect |
| Generation and citation | context, instruction, or decoding policy | retrieved evidence and task cases | correctness, faithfulness, evidence coverage, abstention, citation validity |
| Agentic or custom behavior | policy, tool, memory, or stopping rule | task environment and constraints | task success, trajectory validity, safety invariants, resource use |

## Metric Interpretation

Metrics are instruments for a hypothesis:

- A parsing score can hide a critical numeric field error.
- Retrieval recall can improve by flooding generation with distractors.
- Ranking metrics depend on label completeness and gain definitions.
- Judge scores inherit rubric ambiguity and judge error.
- Mean latency can conceal tail failures and retries.

Pair every primary metric with integrity and resource guardrails. Before trusting a metric change, inspect raw examples near the decision boundary and verify that the measurement still represents the intended behavior.

## Minimal Harness Shape

```python
for case in versioned_cases:
    baseline = run_component(case, baseline_manifest)
    candidate = run_component(case, candidate_manifest)

    record({
        "case_id": case.id,
        "slice": case.slices,
        "baseline": score_and_trace(baseline, case.labels),
        "candidate": score_and_trace(candidate, case.labels),
        "paired_delta": compare(candidate, baseline),
    })

summarize_aggregate_slices_uncertainty_and_failures()
rerun_end_to_end_on_selected_candidates()
```

The implementation may use a dataframe, test runner, experiment tracker, or evaluation framework. The invariant is the versioned case-level record and reproducible comparison—not the library.

## Sources

- [NIST: Analysis of Paired Observations](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm)
- [NIST: Selecting an Experimental Design for the Objective](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm)

## Branches

- [[Parsing & Ingestion Evaluation]]
- [[Chunking Evaluation]]
- [[Embedding & Index Evaluation]]
- [[Retrieval & Metadata Evaluation]]
- [[Query Transformation & Routing Evaluation]]
- [[Reranking Evaluation]]
- [[Generation & Citation Evaluation]]
- [[Agent System Evaluation]]

## Next

→ [[End-to-End System Evaluation]]

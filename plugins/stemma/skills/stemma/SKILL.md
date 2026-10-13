---
name: stemma
description: Practitioner decision notes for building and evaluating RAG and search-backed LLM systems. Use before recommending or changing how documents are parsed, chunked, embedded, indexed, retrieved, fused, reranked, filtered, or cited, and when deciding whether a retrieval or RAG change is actually better, designing evaluation cases, metrics, or LLM judges, or setting pass/fail gates. Also covers abstention, score thresholds, access control in retrieval, and corpus versioning, freshness, and rollback.
argument-hint: "[plan | eval-plan | review | diagnose] [what to work on]"
license: CC-BY-4.0 (notes and SKILL.md); MIT (scripts)
---

# Stemma

Practitioner notes on RAG, organized as folders next to this file. Every path below is relative to the directory containing this SKILL.md. Open only the notes the current decision needs, using the command or decision table to pick them. Inside a note, a link `[[Note Name]]` resolves to `<some folder>/Note Name.md`; note names are unique.

The idea behind every note: a RAG system is judged by the decision it supports. Start from the simplest baseline that could serve that decision, write down how it will be measured, and add a mechanism (hybrid search, reranking, query rewriting, agents) only when a measurement on the actual pipeline shows it earns its place.

## How to use these notes

- Treat them as a checklist of decisions, failure modes, and tradeoffs, not as settled facts. They are a synthesis; verify model names, library APIs, benchmark numbers, and vendor behavior against current primary documentation.
- They deliberately avoid universal thresholds and defaults. When a note says to measure or tune something, propose a cheap starting point, state it as an assumption, and name the measurement that would confirm or overturn it.
- Prefer the simplest baseline the notes allow, and add a mechanism only when a measurement shows it earns its place.
- When advice here conflicts with the user's project instructions or evidence, the project wins; say where they disagree.
- When an input is missing, make a reasonable assumption, state it, and continue. Checks described in the notes are options to choose from, not a mandatory procedure.

## Mistakes seen in practice

Each has made a working-looking RAG system wrong. Look for them when reviewing or planning; the owning note has the reasoning and the fix.
- A raw similarity cutoff copied from elsewhere instead of calibrated on the actual pipeline: `Retrieval Pipeline/Retrieval Calibration, Abstention & Authorization.md`.
- Thresholds or improvements measured on a stand-in retriever or configuration rather than the one that ships: same note.
- No abstention path, so the system answers when evidence is missing or below the calibrated support: same note.
- Authorization applied after retrieval or by the prompt, or leaking through citations, snippets, or result counts: same note, and `RAG Production/Production Security, Privacy & Tenant Isolation.md`.
- A weighted sum of BM25 and cosine scores that are not on a comparable scale, or lexical search run only over the dense hits instead of pooling candidates from each method: `Retrieval Pipeline/Hybrid Fusion.md`.
- Queries and documents embedded with different models, versions, or prefixes: `Indexing Pipeline/Embedding.md`.
- Reindexing in place so users query a half-built index, or no record of which index and model versions served an answer: `Indexing Pipeline/Indexing Lifecycle & Migrations.md`.
- Caches keyed without the user's access scope or the corpus, model, and prompt versions: `RAG Production/Production Caching & Vector DB Ops.md`.
- Retrieved text obeyed as instructions: `Evaluation/Robustness & Adversarial Testing.md`.
- "Better" claimed from a handful of cases without paired comparison or a stated uncertainty: `Evaluation/Statistical Decision-Making for Evaluation.md`.

## Commands

Use a command when the user names it (for example `/stemma plan <what>`) or the task clearly matches it. Otherwise use the decision table below.

### plan

For planning a new RAG system, a major change to one, or its path to production.

Start from the project: read its instructions, existing code, data sources, and any evaluation cases, and plan from where it actually is rather than from a blank slate.

Read `RAG Production/RAG Production Lifecycle.md` and `RAG Architectures/RAG System Design & Improvement Loop.md`, then the notes for the concerns the plan raises: `RAG Architectures/Standard & Modular RAG.md`, `RAG Production/Production Evaluation Gates & Release Engineering.md`, `RAG Production/Production Data Lifecycle, Lineage & Freshness.md`, `Indexing Pipeline/Indexing Lifecycle & Migrations.md`, `Retrieval Pipeline/Retrieval Calibration, Abstention & Authorization.md`.

Cover what applies to this system, and say briefly why anything is left out:
- the decisions the system supports and the failures it cannot tolerate;
- the simplest baseline, and the measurement that would justify each addition (hybrid search, reranking, query rewriting, agents);
- the evaluation cases and gates, written before the components they judge and rerun on every later change to a component, prompt, model, or corpus;
- the data lifecycle: raw sources, versioned processed records and indexes, freshness, deletion, and rebuilding without serving a partial index;
- authorization enforced in retrieval and on everything returned, and when to abstain or escalate;
- the release path: candidate, validation, promotion, rollback, and traces that record which versions produced each answer.

Order the work as steps, each ending in something that can be checked. Before finishing, reread the plan as a reviewer would: it names the baseline, the measurement that justifies each addition, and every assumption made.

### eval-plan / gate

For writing evaluation gates before a baseline run, or judging results against gates already written.

Start from the project: find and read its existing evaluation cases, schemas, and stated claims before proposing anything, and build gates on those cases rather than on generic categories. A threshold without a stated practical margin is a placeholder; label it as one.

Read `Evaluation/Statistical Decision-Making for Evaluation.md`, `Evaluation/Evaluation Strategy & Experimental Design.md`, and `RAG Production/Production Evaluation Gates & Release Engineering.md`. Add `Evaluation/Ground-Truth Labeling & Label Lifecycle.md` when labels are not yet settled.

Produce, in the project's own format if it has one:
- the estimand for each gate: what quantity, over which cases, and the decision it changes;
- slices mapped to the seed cases that cover them, and slices with no coverage;
- each gate with its threshold, the practical margin that justifies it, and whether it is protected (any failure blocks) or aggregate;
- what the sample can and cannot show: with few cases, report exact counts and a sparse-failure bound (rule of three or a Wilson interval) instead of significance claims;
- the allowed verdicts, including `unresolved` when the data cannot decide.

Gates are written and frozen before results are seen. When judging results, compare against the frozen gates and do not revise them in the same step. Before finishing, check that every threshold has a margin or is labelled a placeholder, and that no conclusion claims more than the sample can show.

To compute pass-rate intervals, zero-failure bounds, or a paired bootstrap on per-case results, run `scripts/gate_stats.py` (next to this file; `--help` for usage) instead of estimating them.

### review

For auditing an existing RAG or search codebase before shipping or changing it. Report findings; edit code only if asked.

Start from the project: read its instructions, README claims, and evaluation code, then trace one request end to end through the code that actually serves it, which is often not the path a script or eval exercises. Use "Mistakes seen in practice" above and the notes for the stages the code contains, but read the code rather than matching patterns: the most damaging bugs are often plain wiring errors, such as a computed filter that is never applied, an exception swallowed into a fallback, or a field the indexing code writes under a different name than the query path reads.

Produce:
- findings ranked by harm to users (wrong or missing answers and leaks first, then misleading evidence, then hygiene), each with the file and symbol, the quoted code, the consequence, and a query, test, or measurement that would confirm it;
- whether the project's evaluation measures the path that ships and supports the claims made from it;
- what is done well, so a correct design is not "fixed".

Before finishing, check each finding against the code once more, and drop or label anything not confirmed.

### diagnose

For a reported failure, such as wrong citations or results that disappeared after a change.

Read `Evaluation/Failure Diagnosis & Error Analysis.md`. Localize before fixing: follow the request through routing, query transformation, retrieval, filtering and thresholds, reranking, context assembly, and generation, and find the first stage whose output is already wrong, by reading the code, inspecting traces, or substituting a known-good input at one stage at a time. Then read the note for that stage.

Produce the stage and mechanism with the evidence for it, a fix at that stage rather than a compensating change elsewhere, and a regression case or check that would have caught the failure.

## Route by decision

| Decision | Start with | Then, as needed |
|---|---|---|
| Planning a RAG system or its path to production, end to end | `RAG Production/RAG Production Lifecycle.md`, `RAG Architectures/RAG System Design & Improvement Loop.md` | `Standard & Modular RAG` (start from a simple baseline), `Production Evaluation Gates & Release Engineering`, `Production Data Lifecycle, Lineage & Freshness`, `Indexing Lifecycle & Migrations` (reindex without serving a partial index), `Retrieval Calibration, Abstention & Authorization` |
| Whether RAG fits, requirements, failure budget | `RAG Production/Production Requirements & SLOs.md` | `RAG Production/RAG Production Lifecycle.md` |
| Overall architecture and control flow | `RAG Architectures/RAG Architectures.md` | `Standard & Modular RAG`, `RAG System Design & Improvement Loop`, `Evidence Sufficiency & Correction`, `Adaptive & Composite Retrieval`, `Agentic RAG`, `Knowledge Graph RAG` |
| Parsing, cleaning, chunking, metadata | `Indexing Pipeline/Document Processing.md`, `Indexing Pipeline/Chunking Strategy.md` | `Recursive Chunking`, `Document-Aware Chunking`, `Parent-Child Chunking`, `Semantic Chunking`, `Late Chunking`, `Proposition-based Chunking`, `Metadata Extraction`, `Table Handling`, `PDF Extraction`, `Contextual Retrieval` |
| Embeddings and index structures | `Indexing Pipeline/Indexing.md` | `Embedding`, `Model Selection Criteria`, `Vector Index`, `HNSW`, `IVF`, `Sparse Index`, `SPLADE`, `BM25`, `Late Interaction Models`, `Indexing Lifecycle & Migrations` |
| Retrieval method, hybrid fusion, reranking | `Retrieval Pipeline/Retrieval.md` | `Dense Retrieval`, `Sparse Retrieval`, `Hybrid Fusion`, `RRF`, `Cascading Retrieval`, `Reranking`, `MMR`, `Diversity Selection` |
| Query rewriting, routing, decomposition, HyDE | `Retrieval Pipeline/Query Understanding.md` | `Query Transformation`, `Query Routing`, `Query Decomposition`, `Multi-Query Retrieval`, `HyDE`, `Reverse HyDE`, `Step-Back Prompting`, `Self-Query` |
| Score thresholds, abstention, access control | `Retrieval Pipeline/Retrieval Calibration, Abstention & Authorization.md` | `Threshold Filtering`, `Filtered Retrieval`, `RAG Production/Production Security, Privacy & Tenant Isolation.md` |
| Context assembly, prompting, citations | `Retrieval Pipeline/Post-Retrieval Processing.md` | `Context Assembly`, `Contextual Compression`, `Generation Pipeline/Prompt Construction.md`, `Citation & Output Formatting`, `Hallucination Detection & Verification`, `Structured Output & Constrained Decoding` |
| Model execution: streaming, structure, caching | `Generation Pipeline/Generation Strategy.md` | `Model Selection & Reasoning Tiers`, `Inference & Sampling Parameters`, `Prompt Caching & Compression` |
| Evaluation plan, metrics, datasets | `Evaluation/Evaluation Strategy & Experimental Design.md` | `Evaluation Data & Benchmarks`, `Evaluation Metrics & The RAG Triad`, `Component Evaluation Harness`, `End-to-End System Evaluation` |
| Labeling ground truth | `Evaluation/Ground-Truth Labeling & Label Lifecycle.md` | `Chunking Evaluation`, `Retrieval & Metadata Evaluation` |
| Component-level evaluation | the matching note in the Evaluation folder | `Parsing & Ingestion Evaluation`, `Chunking Evaluation`, `Embedding & Index Evaluation`, `Retrieval & Metadata Evaluation`, `Reranking Evaluation`, `Query Transformation & Routing Evaluation`, `Generation & Citation Evaluation` |
| LLM judges | `Evaluation/Semantic Evaluation & LLM Judges.md` | `Judge Calibration & Validation`, `Deterministic & Reference-Based Evaluation` |
| Pass/fail gates, sample size, significance | `Evaluation/Statistical Decision-Making for Evaluation.md` | `RAG Production/Production Evaluation Gates & Release Engineering.md`, `Regression & Production Feedback` |
| Diagnosing a failure | `Evaluation/Failure Diagnosis & Error Analysis.md` | `Robustness & Adversarial Testing`, `RAG System Design & Improvement Loop` |
| Corpus versioning, freshness, lineage, deletion | `RAG Production/Production Data Lifecycle, Lineage & Freshness.md` | `Indexing Pipeline/Indexing Lifecycle & Migrations.md` |
| Release, rollback, operations | `RAG Production/RAG Production.md` | `Production Evaluation Gates & Release Engineering`, `Production Observability & Incident Response`, `Production Reliability, Capacity & Failure Handling`, `Production Caching & Vector DB Ops`, `Production Cost, Provider & Model Ops`, `Production Human Oversight & Governance` |

Cluster hubs, for orientation when no row fits: `Indexing Pipeline/Indexing.md`, `Retrieval Pipeline/Retrieval.md`, `Generation Pipeline/Generation Strategy.md`, `RAG Architectures/RAG Architectures.md`, `RAG Production/RAG Production.md`, `Evaluation/Evaluation Strategy & Experimental Design.md`.

To find a note by topic, search the directory containing this file, for example `grep -ril "abstain" <that directory>`.

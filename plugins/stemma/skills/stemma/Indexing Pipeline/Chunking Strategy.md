---
tags: [indexing]
---
# Chunking Strategy

Chunking strategy chooses the searchable and resolvable evidence units for each document class. There is no corpus-independent winner: boundaries interact with parsing, representation, retrieval depth, context budget, and the questions users ask.

## First Decide Whether One Policy Is Enough

Route by document class only when meaningful topology differs—prose, code, tables, transcripts, rulebooks, or visually structured pages—and a controlled comparison shows benefit. Every extra route adds classification errors, versioning, migration, and debugging work.

All chunks within one vector field must use a compatible representation contract. Different chunking policies may coexist if their identifiers, provenance, labels, and embedding/index versions remain explicit.

## Strategy Families

| Family | Mechanism | Plausible use | Main risk |
|---|---|---|---|
| Fixed windows | Cut by a uniform unit | logs, streams, controlled baselines | breaks semantic or structural units |
| Recursive/structure-aware | Prefer document separators, then fall back to smaller units | general prose and markup baseline | separator hierarchy may not match meaning |
| Semantic boundaries | Split when adjacent units change representation | weakly structured discourse or transcripts | threshold instability and extra embedding cost |
| Document-aware | Use syntax, layout, rows, clauses, turns, or world hierarchy | code, tables, legal text, simulation state | variable sizes and parser dependence |
| Parent-child | Search small units, return a larger related unit | precise search needing broader explanation | duplication and incorrect parent resolution |
| Proposition or model-derived | Rewrite/extract atomic or contextualized units | dense facts or context-dependent passages | cost, drift, hallucinated transformations |
| Hierarchical/tree summaries | Search multiple abstraction levels | broad-to-specific questions over long collections | expensive construction and provenance complexity |
| Late chunking or multi-vector | preserve longer context during representation | context-dependent or visually rich sources | representation/index resource cost |

## Pre-Retrieval Checks

- Can every required source region be cleanly represented?
- Are headings, table headers, qualifiers, and code scopes attached?
- How often is content duplicated by overlap or hierarchy?
- What are chunk-size and chunks-per-document distributions by source class?
- Can every chunk map back to immutable source anchors?

These checks detect structural damage, but they do not select a winner. Use query-based retrieval and end-to-end evidence for that.

## Controlled Experiment

1. State a boundary-related failure hypothesis.
2. Label stable source regions for representative and high-risk queries.
3. Rechunk identical parsed input under a simple baseline and justified candidates.
4. Hold representation, retrieval policy, candidate/context budget, and evaluation code fixed where possible.
5. Compare region coverage, early ranking, evidence concentration, redundancy, index size, latency, and downstream outcomes.
6. Inspect helped and harmed cases; rerun after changing embeddings or retrieval because interactions can reverse a result.

Overlap is not a default insurance policy. It may protect boundary-sensitive evidence, but it also duplicates search surface and context. Sweep it only when the corpus supplies a mechanism and measure the resulting tradeoff.

## Components

- [[Fixed Chunking]]
- [[Recursive Chunking]]
- [[Semantic Chunking]]
- [[Document-Aware Chunking]]
- [[Proposition-based Chunking]]
- [[Agentic Chunking]]
- [[Parent-Child Chunking]]
- [[RAPTOR]]
- [[Late Chunking]]
- [[Contextual Retrieval]]

## Part of

← [[Chunking]]

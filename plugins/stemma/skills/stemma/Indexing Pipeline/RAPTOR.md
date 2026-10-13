---
tags: [indexing]
---
# RAPTOR

RAPTOR builds a hierarchy by clustering lower-level text units, summarizing clusters, and recursively repeating the process. Retrieval can search original evidence and summaries at several abstraction levels.

## Intended Mechanism

Broad questions may match a summary that represents evidence distributed across many leaves, while specific questions still retrieve the leaves. The tree is a derived navigation and retrieval structure—not a replacement for source evidence.

## Failure Modes

- clustering groups unrelated material or separates dependent evidence;
- summaries omit qualifiers, invent connections, or erase minority details;
- errors propagate upward through recursive summaries;
- updates require partial or full tree reconstruction;
- summary matches improve topical relevance without supporting the final claim.

## Evaluation

Compare flat retrieval and the hierarchy on explicitly broad, multi-evidence, and specific queries. Measure required leaf-evidence coverage, summary support, provenance back to leaves, retrieval and answer quality, build/update cost, and failure slices. Require generation citations to resolve to source evidence rather than treating generated summaries as authority.

Adopt only when multi-level retrieval provides meaningful value over simpler parent-child or multi-query approaches.

Primary reference: [RAPTOR](https://arxiv.org/abs/2401.18059).

## Part of

← [[Chunking Strategy]]

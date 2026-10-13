---
tags: [evaluation]
reviewed: 2026-10-11
---
# Chunking Evaluation

Chunking defines the evidence units available to retrieval and generation. Evaluate whether boundaries preserve useful source regions while controlling redundancy, context waste, indexing cost, and downstream failure. “Semantically coherent” is not sufficient unless it improves a product-relevant task.

## When This Enters the Build

Use this after parser output is credible and before treating chunk IDs as stable ground truth. Build a simple region-based baseline, label the source regions that answer representative queries, and compare candidate boundary policies through the same provisional retriever. Leave with one versioned chunking policy per justified document class and a mapping from durable source regions to its chunks.

Do not hold the entire build hostage while searching for a perfect chunker. Select a credible baseline, continue through the thin vertical slice, and revisit chunking when retrieval or generation failures point to broken, diluted, or redundant evidence units.

## Labels That Survive Strategy Changes

Label evidence as stable source regions—document plus page/section and character, bounding-box, row, or timestamp spans—not as candidate chunk IDs. For each query record required regions, optional support, acceptable boundary slack, and whether the answer requires one region, every region, or relationships among them.

Include long sections, definitions, lists, tables crossing pages, heading-dependent passages, code, dialogue, and separated evidence. Cover important corpus and query slices; do not infer adequacy from an arbitrary case count.

## What to Measure

| Question | Useful signal |
|---|---|
| Was any usable unit surfaced? | region Hit Rate@K or MRR |
| Was all required evidence surfaced? | region coverage/Recall@K |
| How clean is the evidence? | precision and evidence-token ratio (tokens inside labeled evidence regions ÷ all retrieved tokens) |
| Are boundaries usable? | split-unit, orphan-heading, boundary precision/recall |
| Is context duplicated? | duplicate-region coverage and overlap redundancy |
| What does it cost? | chunks/document, token distribution, index size, build/update and query cost |

Any overlap is too permissive: a huge chunk can touch the gold span while burying it. Measure both coverage of the labeled region and concentration within the chunk.

```python
def overlap_scores(chunk, region):
    intersection = max(0, min(chunk.end, region.end) - max(chunk.start, region.start))
    return (
        intersection / (region.end - region.start),
        intersection / (chunk.end - chunk.start),
    )
```

## Controlled Experiment

1. State the mechanism, such as structural boundaries preserving heading-qualified evidence.
2. Select a simple baseline and candidates justified by observed corpus failures.
3. Re-chunk identical parser output; hold queries, region labels, embedding, retrieval logic, and evaluation code fixed.
4. Rebuild each index and retrieve at the same K and filter policy.
5. Compare paired per-query deltas, uncertainty, important slices, and helped/harmed cases.
6. Inspect whether gains come from better units or merely more chunks and search surface.
7. Run a fixed-context-budget generation check for finalists; redundant or oversized chunks can erase retrieval gains.

## Interpret and Decide

- A gold region never cleanly contained in a chunk indicates a boundary problem.
- A clean evidence chunk that is not retrieved points downstream.
- Recall rising while evidence-token ratio falls suggests oversized or redundant chunks.
- Generation degrading despite retrieval lift calls for inspection of duplication, ordering, surrounding definitions, and budget.

Adopt a strategy when improvement is credible and meaningful on motivating slices, must-not-regress slices remain within tolerance, and storage, latency, and maintenance are justified. Prefer the simplest candidate on an indistinguishable frontier. Different document classes may warrant routing rather than one global strategy.

Change chunking when evidence units are broken, diluted, or redundantly represented—not merely because a technique is new or an aggregate score moved without a boundary-related mechanism.

## After Selection: Hand Off to Chunk-Level Judgments

Region labels are the fair comparison layer while chunk IDs change across candidates. Once the winning policy is locked and versioned, materialize query–chunk relevance judgments for the resulting index:

1. Map every required and optional source region to the chunks that cover it; retain the source anchors and mapping version.
2. Pool plausible chunks from several retrieval runs and human discovery, then judge their usefulness. A previously unseen chunk is unjudged, not automatically irrelevant.
3. Record graded relevance when one chunk merely overlaps the evidence while another contains the complete, usable answer context.
4. Use this derived layer for exact Hit Rate, MRR, Recall, and NDCG comparisons in embedding, retrieval, and reranking experiments.
5. If chunk boundaries change again, regenerate or migrate the chunk judgments and preserve the prior version for reproducibility.

The chunk labels replace region overlap as the precise scoring unit for later components; they do not replace the durable source evidence from which those labels were derived.

## Part of

← [[Component Evaluation Harness]]

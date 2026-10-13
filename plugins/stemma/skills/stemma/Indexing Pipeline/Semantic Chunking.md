---
tags: [indexing]
reviewed: 2026-10-11
---
# Semantic Chunking

Splits text based on semantic meaning rather than token counts by measuring the cosine distance between consecutive sentence embeddings.

---

## How It Works

1. **Sentence Tokenization**: The text is broken into individual sentences.
2. **Sequential Embedding**: Each sentence is embedded using a small local embedding model.
3. **Distance Calculation**: The algorithm computes the cosine distance between consecutive sentences $S_i$ and $S_{i+1}$.
4. **Threshold Splitting**: When the distance rises above a statistical percentile threshold (indicating a shift in subject matter), a new chunk boundary is placed.

Illustrative distances (not thresholds to copy):

```
Sentence 1 ──┐ (Distance: 0.12 - Same topic)
Sentence 2 ──┴ (Distance: 0.14 - Same topic)
               ──────── [ SPLIT: Distance Spike: 0.78 (Topic Changed) ] ────────
Sentence 3 ──┐ (Distance: 0.09 - New topic)
Sentence 4 ──┘
```

---

## When to Use
- **Spoken Transcripts & Rambling Audio**: Unedited podcast transcripts, stream of consciousness logs, or customer support phone recordings that lack punctuation and paragraph structure.

---

## Why It Is Often Avoided in General Production
- **Computational Overhead**: Requires embedding every individual sentence during indexing (embedding calls scale with sentence count rather than chunk count; the multiple over recursive chunking depends on sentences per chunk).
- **Threshold Brittleness**: A fixed percentile threshold that works on one document often produces tiny 1-sentence chunks or very large chunks on another document with different writing cadence.
- **Compare with Late Chunking**: Late Chunking preserves broader embedding context, while semantic chunking works without a long-context embedding model but pays a per-sentence embedding cost; compare total indexing cost as well as retrieval. Evaluate both when topic transitions are the dominant failure mode.

---

## Part of
← [[Chunking Strategy]]

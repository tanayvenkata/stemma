---
tags: [indexing]
reviewed: 2026-10-11
---
# Late Chunking

Embed the full document first, then chunk the embeddings — preserving cross-chunk context that traditional chunking loses.

## The Problem It Solves

Traditional chunking breaks documents before embedding. If "Berlin" appears in chunk 1 and "population: 3.5M" in chunk 2, neither chunk alone retrieves well for "Berlin's population."

Late chunking runs the full document through a long-context embedding model, then mean-pools the token embeddings inside each chunk span ([Late Chunking](https://arxiv.org/abs/2409.04701)) — each chunk vector is conditioned on the surrounding document.

## When to Use

| Situation | Late Chunking? |
|-----------|----------------|
| Documents with context spread across sections | Yes |
| Long documents whose chunks depend on earlier context, within the model's input limit (longer documents need overlapping macro-chunks) | Yes |
| Already using long-context embedding model | Yes |
| Short, self-contained documents | No — overhead not worth it |

Treat these as starting hypotheses: compare against the same chunk boundaries embedded independently, on context-dependent and ordinary query slices.

## Tradeoffs

| Pro | Con |
|-----|-----|
| Better retrieval for context-dependent content | Requires a long-context embedding model; document length is capped by its input limit |
| Reduces context loss at chunk boundaries (pooling still compresses detail) | Higher compute during indexing |

## Part of
← [[Chunking Strategy]]

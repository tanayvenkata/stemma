---
tags: [retrieval]
---
# HyDE

Hypothetical Document Embeddings generates a plausible document-like response to the query and embeds that text for retrieval. It attempts to bridge the representation gap between short questions and declarative source passages.

The hypothetical text is a search representation, not evidence and not an answer to show the user.

## When to Test It

- conceptual queries are poorly matched by their short surface form;
- the embedding model aligns document-style text more effectively than questions;
- generated domain vocabulary may help locate relevant sources.

## Failure Modes

- generated facts or vocabulary steer retrieval toward the wrong topic;
- exact identifiers, negation, dates, or constraints disappear;
- added latency and nondeterminism outweigh retrieval lift;
- the generator encodes assumptions unsupported by the corpus.

Compare original-query retrieval, a deterministic rewrite, and HyDE on identical evidence labels. Measure intent/constraint preservation, required-evidence coverage, helped/harmed slices, variance, latency, cost, and downstream outcomes. Preserve the generated representation for diagnosis.

Primary reference: [Precise Zero-Shot Dense Retrieval without Relevance Labels](https://arxiv.org/abs/2212.10496).

## Part of

← [[Query Transformation]]

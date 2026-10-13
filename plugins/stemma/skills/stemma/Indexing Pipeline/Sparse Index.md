---
tags: [indexing]
---
# Sparse Index

A sparse index stores postings only for nonzero vocabulary features, enabling efficient lexical or learned-sparse retrieval.

## Families

- [[BM25]] and related lexical scoring use observed terms, collection statistics, and analyzers.
- [[SPLADE]] and other learned sparse methods predict weighted vocabulary features and expansion terms.

Sparse retrieval is valuable for identifiers, names, jargon, quotations, and inspectable term contributions, but performance depends on tokenization, normalization, fields, language, and vocabulary. Dense retrieval is not automatically superior for meaning, nor is hybrid retrieval automatically superior to either alone.

Version analyzer/model, vocabulary, field weights, stopwords, stemming, scoring formula, and source snapshot. Rebuild or migrate deliberately when these change.

Evaluate lexical, learned sparse, dense, and fused candidates on pooled in-domain judgments, exact-term and paraphrase slices, latency, index size, updates, and downstream evidence utility.

## Components

- [[BM25]]
- [[SPLADE]]

## Part of

← [[Indexing]]

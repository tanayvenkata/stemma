---
tags: [retrieval]
reviewed: 2026-10-11
---
# Sparse Retrieval

Retrieval based on exact token matching and statistical term frequencies using inverted index data structures.

---

## The Core Mechanism

Sparse retrieval breaks text into discrete tokens and searches an **Inverted Index** (a dictionary mapping each unique word to the list of document IDs containing it):

```
Inverted Index Table:
"lithium" ──> [ Doc 12 (score: 4.2), Doc 88 (score: 2.1) ]
"battery" ──> [ Doc 12 (score: 3.8), Doc 45 (score: 1.5), Doc 99 (score: 0.9) ]
```

The primary algorithm is **BM25**, which scores documents based on:
1. **Term Frequency (TF)**: How often the word appears in the chunk.
2. **Inverse Document Frequency (IDF)**: How rare the word is across the entire corpus.
3. **Document Length Penalty**: Normalizes for short vs. long documents.

---

## Strengths & Failure Modes

| Strengths (Where Sparse Wins) | Failure Modes (Where Sparse Fails) |
|---|---|
| **Exact Token Matching**: Strong recall for SKUs (`#4829-X`), error codes (`ERR_404_TIMEOUT`), and UUIDs when tokenization preserves them. | **Vocabulary Mismatch Problem**: Recall can fail if user says *"doctor"* and text says *"physician"*. |
| **Cheap Incremental Indexing**: New documents can be indexed without embedding-model inference; when they become searchable depends on the engine's refresh or commit settings. | **Word Salad Sensitivity**: Can be tricked by keyword repetition (mitigated by BM25 saturation). |
| **Interpretability**: Exact explanation of why a document scored high (which words matched). | **Zero Syntactic / Semantic Context**: Cannot distinguish *"man bites dog"* from *"dog bites man"*. |

---

## Part of
← [[Retrieval]]

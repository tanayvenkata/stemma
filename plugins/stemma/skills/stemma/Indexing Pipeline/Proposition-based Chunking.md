---
tags: [indexing]
reviewed: 2026-10-11
---
# Proposition-based Chunking

Breaks dense compound paragraphs into discrete, standalone **atomic propositions** (factual assertions) using an LLM before embedding.

---

## The Mental Model

A single sentence in an encyclopedia or legal brief often packs multiple facts together:
> *"Founded in 1976 by Steve Jobs, Steve Wozniak, and Ronald Wayne, Apple developed the Apple I personal computer before incorporating in 1977."*

Proposition chunking extracts each fact into an independent, self-contained sentence:
1. *"Apple was founded in 1976."*
2. *"Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne."*
3. *"Apple developed the Apple I personal computer."*
4. *"Apple was incorporated in 1977."*

---

## When to Use
- **Fact-Verification & Automated Knowledge Graphs**: When an application needs to verify single atomic claims against an authoritative database.
- **Dense Encyclopedias & Biographical Databases**: Where compound sentences contain multiple entities that would otherwise dilute dense vector search.

---

## Tradeoffs

| Advantage | Consideration |
|---|---|
| Can improve retrieval for single-fact queries ([Dense X Retrieval](https://arxiv.org/abs/2312.06648) reports propositions outperforming passage units; confirm on your queries) | Multiplies the number of index entries, often several-fold; measure propositions per source chunk on a sample before committing |
| Each proposition is meant to be standalone (pronouns resolved); audit a sample, since LLM rewriting can leave ambiguity or introduce unsupported facts | High LLM cost at ingestion time (requires rewriting all source text) |

---

## Part of
← [[Chunking Strategy]]

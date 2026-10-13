---
tags: [retrieval]
---
# Reverse HyDE

Reverse HyDE generates plausible questions or search descriptions for a source unit at indexing time and indexes those derived representations alongside the source. It moves transformation work from query time to ingestion.

## Tradeoff

The method can bridge likely user language to formal source text without adding a generation call to each query. It also multiplies indexed representations, predicts a possibly narrow question distribution, and can introduce unsupported or misleading terms.

## Protocol

1. Generate versioned questions from source-bounded evidence under a constrained prompt.
2. Store each question as derived metadata linked to the canonical source; never treat it as evidence.
3. Deduplicate and audit answerability, realism, coverage, and leakage.
4. Compare source-only and source-plus-generated indexes on real and protected queries.
5. Measure evidence coverage, false matches, index growth, ingestion cost, updates, and query latency.

Use it when predictable query phrasing is a diagnosed retrieval gap and index-time expansion beats simpler metadata, lexical, or contextual augmentation.

## Part of

← [[Query Transformation]]

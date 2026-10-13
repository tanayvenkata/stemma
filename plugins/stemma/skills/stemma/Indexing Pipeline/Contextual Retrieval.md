---
tags: [indexing]
reviewed: 2026-10-11
---
# Contextual Retrieval

Contextual retrieval augments a searchable unit with information from its document or surrounding structure before embedding or sparse indexing. The aim is to make locally ambiguous passages retrievable without discarding their source context.

```text
source document + target chunk
→ derive a short context statement or inherited structural path
→ store original chunk and augmentation separately
→ index the augmented representation
→ return source-faithful content with provenance
```

Useful augmentation might identify the document, section, entity, time period, speaker, or role needed to interpret a fragment. It should not invent facts or replace the original evidence.

## When It Helps

- chunks contain pronouns, local labels, or section-dependent terminology;
- repeated templates are distinguishable only by document or entity context;
- precise queries name attributes absent from the local passage;
- small search units are required but parent expansion alone does not improve ranking.

It is less attractive when headings and metadata already provide the needed signal, passages are self-contained, or generated prefixes overwhelm the original content.

## Implementation Choices

- deterministic heading/breadcrumb inheritance;
- selected document metadata rendered into index text;
- extractive nearby context;
- model-generated context under a schema and evidence-only constraint;
- separate dense and sparse augmentation fields rather than one concatenated string.

Caching repeated document prefixes can reduce generation work, but provider discounts and latency are runtime-specific economics—not a prerequisite or durable percentage.

## Evaluate

Compare the same chunks with and without augmentation. Measure retrieval on context-dependent and ordinary slices, exact evidence coverage, false matches caused by repeated prefixes, index growth, generation cost, and migration complexity. Audit generated context for unsupported or source-confusing statements.

Adopt only when gains come from resolved ambiguity rather than benchmark leakage or expanded keyword surface. Preserve the original chunk, augmentation, generator/configuration, and source anchors independently.

Primary reference: [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) (Anthropic post, September 2024; a vendor report, not a peer-reviewed result).

## Part of

← [[Chunking Strategy]]

---
tags: [architectures]
---
# Knowledge Graph RAG

Graph-augmented RAG represents entities, events, claims, and relationships explicitly, then retrieves through that structure or through summaries derived from it. It is useful when **connections or corpus-level structure are part of the question**, not as a general replacement for passage retrieval.

## How It Differs from Standard RAG

Standard RAG retrieves independent passages because it assumes the answer is locally expressed in one or a few text regions. Graph RAG changes the evidence representation itself: entities and relations become retrievable objects, and paths, neighborhoods, or corpus-wide summaries can become evidence.

```text
standard: query → retrieve similar passages → answer
graph:    query → identify entities / traverse or summarize graph → source-backed answer
```

Use it when a relationship, temporal constraint, multi-hop path, or global pattern is required to answer the question. Do not use it merely because a corpus has named entities; ordinary passage retrieval remains the simpler baseline for local questions.

## Choose the Graph's Job First

| Job | Useful representation | Example query |
|---|---|---|
| precise relationship lookup | curated or extracted entities and typed edges | Who approved this contract? |
| multi-hop evidence acquisition | paths plus supporting source passages | Which supplier links these two incidents? |
| global sensemaking | communities, themes, and hierarchical summaries | What recurring risks appear across the corpus? |
| constraint or temporal reasoning | typed relations, validity intervals, provenance | What policy applied at the event time? |

A graph can be authoritative, extracted from text, or hybrid. An extracted edge is a model-produced claim until traced to source evidence; the graph is not automatically a source of truth.

## Construction Contract

```text
source versions → parse/chunk → extract candidates → resolve identities
       → validate and attach provenance → build graph/views/summaries → publish generation
```

Specify the schema, entity identity policy, relation direction and type, confidence/evidence fields, temporal semantics, update/delete behavior, and ownership. Entity resolution is often the dominant correctness problem: false merges invent relationships, while missed merges fragment the neighborhood.

Graph construction may use deterministic extractors, models, existing databases, or human curation. Measure cost and error for each stage on a representative sample before scaling. Preserve the text passages that justify nodes, edges, and summaries.

## Retrieval Patterns

- **Entity-local retrieval:** identify relevant entities, expand a bounded neighborhood, then return graph facts with source passages.
- **Path retrieval:** search for constrained paths and verify every edge against evidence.
- **Global retrieval:** use community or hierarchical summaries for corpus-wide questions, with drill-down to underlying claims.
- **Hybrid retrieval:** combine graph candidates with lexical/vector retrieval and reranking.

The local/global pattern popularized by GraphRAG is one implementation of entity-local and corpus-wide retrieval. Community summaries compress the corpus and can also propagate extraction or summarization errors, so answers still need provenance and coverage checks.

## When Not to Use It

Prefer ordinary or hierarchical passage retrieval when questions are locally answerable, relationships are incidental, the corpus changes faster than the graph can be reconciled, or no evaluation set demonstrates a graph-specific failure. If structured facts already live in a database, query that source rather than reconstructing it from prose.

## Evaluation

Evaluate construction and answering separately:

- entity/relation precision and coverage, resolution merge/split errors, provenance, and temporal validity;
- path validity, supporting-evidence coverage, global-theme coverage, answer/citation quality, and abstention;
- indexing/update cost, freshness, query latency, and failure under deletes or schema change.

Compare against strong vector, lexical, hierarchical-summary, and structured-query baselines on relation-heavy and global slices. Use oracle entities or edges to learn whether failure is in construction, retrieval, or generation.

## Primary Source

- From Local to Global — A Graph RAG Approach to Query-Focused Summarization: https://arxiv.org/abs/2404.16130

## Part of

← [[RAG Architectures]]

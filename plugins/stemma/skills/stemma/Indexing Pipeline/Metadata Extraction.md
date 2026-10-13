---
tags: [indexing]
reviewed: 2026-10-11
---
# Metadata Extraction

Extracting structured metadata from raw source documents during the initial ingestion phase.

## Why Metadata Is an Ingestion Decision

**Capture stable source facts now; decide how to use them through evaluation.** Metadata omitted at ingestion may require a full re-parse or reindex later. Metadata enables provenance and citations, lifecycle operations, filtering and ranking, but it must not be confused with authorization enforcement.

Use two tests before adding a field:

1. Will the system filter, rank, delete, migrate, audit, or display by it?
2. Can the value be extracted reliably enough to support that use?

Start with cheap, source-grounded metadata. Add model-derived topics, entities, or summaries only when a measured retrieval or product need justifies their cost and error surface.

| Class | Examples | Default posture |
|---|---|---|
| Source identity | Stable `document_id`, source URI, content hash | Capture |
| Position | Page, section path, character/bounding-box offsets | Capture when available |
| Time and version | Source update time, ingestion time, revision | Capture |
| Governance | Owner, classification, policy reference | Capture from authoritative systems |
| Derived semantics | Topics, entities, summaries | Evaluate before adopting |

---

## The Core Metadata Extraction Types

```
                           Metadata Extraction
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
1. Document Identifiers      2. Temporal & Provenance     3. Structural & Semantic
 • Title / Filename           • Publication Date           • Document Type / Genre
 • Author / Organization      • Ingestion Timestamp        • Section / Chapter Hierarchy
 • Content Hash (SHA-256)     • Version / Revision ID      • Language / Locale
```

---

## Methods of Extraction

1. **Rule-Based & Regex Pattern Matching**:
   - Extracting ISO dates (`YYYY-MM-DD`), copyright headers, author lines, and file system timestamps.
   - Fast and deterministic when source conventions are stable; test false matches and format drift.
2. **Document Object Model (DOM) & PDF Properties**:
   - Reading embedded PDF metadata dictionaries (`/Author`, `/CreationDate`, `/Title`).
3. **Model-Based Structured Extraction**:
   - For unstructured sources, a model can emit a constrained schema from the regions likely to contain the field. The inspected region, model, prompt, and validation policy are part of the extractor version; the beginning of a document is not guaranteed to contain authoritative metadata.

Model-extracted metadata should carry provenance, extractor version, and confidence or validation status. Never let an LLM invent tenant or access-control scope; those constraints come from trusted application identity and policy data.

## Minimum Useful Payload

```python
metadata = {
    "document_id": stable_document_id,
    "source_uri": source_uri,
    "content_hash": sha256_bytes,
    "source_updated_at": source_updated_at,
    "ingested_at": ingested_at,
    "parser_version": parser_version,
    "embedding_version": embedding_version,
    "page": page_number,
    "section_path": section_path,
}
```

The exact schema is domain-specific. The invariant is enough identity and lineage to reproduce, update, delete, cite, and migrate every chunk.

---

## Part of
← [[Document Processing]]

---
tags: [indexing]
---
# Parent-Child Chunking

Parent-child chunking separates the unit used for search from the larger unit resolved for generation. A child can provide precise matching while its parent restores headings, definitions, qualifiers, or neighboring evidence.

```text
canonical parent region
→ one or more searchable children with parent_id and source anchors
→ child retrieval
→ deduplicate/allocate by parent
→ fetch authorized, version-matched parent content
```

## Design Choices

- structural or size-based parent boundaries;
- child boundaries and overlap;
- whether one parent contains several distinct evidence requirements;
- maximum expanded context and deduplication behavior;
- handling of multiple matching children, siblings, and cross-parent questions;
- source-store consistency, authorization, and version checks during resolution.

Small units are not automatically better search representations, and larger units are not automatically more complete. Both depend on corpus structure and query needs.

## Evaluation

Compare child-only, parent-only, and child-search/parent-return policies on source-region coverage, early ranking, evidence concentration, duplicated parent content, context budget, citation precision, latency, storage, and downstream answers. Sweep sizes only on development cases.

Use the pattern when retrieval finds local evidence but generation consistently needs reliable surrounding context. Avoid it when parents are too broad, relationships are unstable, or direct structural chunks already work.

## Part of

← [[Chunking Strategy]]

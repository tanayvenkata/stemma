---
tags: [indexing]
---
# Metadata Attachment

Metadata attachment creates the versioned relationship between a chunk and its source, structure, lifecycle, and trusted policy context.

## Minimum Categories

- stable chunk, document, source-version, and representation identifiers;
- page/block/time offsets or other source anchors;
- parent, sibling, section, table, entity, or dialogue relationships needed for resolution;
- parser and chunker versions plus content hash;
- freshness, validity interval, and deletion state;
- trusted authorization-policy reference where required;
- provenance and confidence for derived semantic fields.

Not every chunk needs every field. Define the schema from citation, filtering, ranking, migration, deletion, recovery, and audit requirements. Avoid copying mutable display values into millions of payloads when a stable reference is safer.

Breadcrumbs can be indexed as context or retained only as metadata. Compare retrieval lift against repeated-prefix noise and index growth. Validate that every chunk resolves to its canonical source and that permission/freshness changes propagate correctly.

## Part of

← [[Chunking]]

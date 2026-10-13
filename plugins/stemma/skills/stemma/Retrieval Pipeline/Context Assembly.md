---
tags: [retrieval]
---
# Context Assembly

Context assembly resolves search candidates into source-faithful evidence objects before generation formatting. It may expand parents, merge siblings, deduplicate overlapping regions, or allocate a context budget across required evidence.

## Invariants

- every returned span maps to a canonical source and version;
- authorization and freshness remain valid after parent/sibling expansion;
- merging preserves document order, gaps, qualifiers, and citation anchors;
- deduplication does not remove complementary or corroborating evidence;
- truncation and omitted candidates are recorded.

Small-to-large resolution is useful when the searchable child identifies a fact but a larger parent contains necessary context. It is harmful when the parent floods the budget or includes unrelated/unauthorized material.

Compare raw candidates and assembly policies on required-evidence coverage, evidence-token ratio, duplication, citation mapping, authorization, downstream answers, latency, and harmed cases. Choose context count and size from the measured budget frontier rather than fixed chunk numbers.

## Part of

← [[Post-Retrieval Processing]]

---
tags: [indexing]
---
# PDF Extraction

PDF preserves visual rendering, not necessarily logical reading order or semantic structure. Text may be positioned glyphs, tables may be independent drawing operations, and pages may mix native text with scanned images.

## Classify at Page Level

| Class | Evidence | Likely extraction path |
|---|---|---|
| digital text | usable text objects and font mappings | native extraction plus layout reconstruction |
| scanned image | no trustworthy text layer | OCR plus layout analysis |
| mixed | text and image regions vary by page | region/page routing |
| visually semantic | charts, forms, diagrams, equations, spatial relationships | structured vision extraction or vision-native retrieval |

“Text exists” does not prove it is complete or ordered. Sample across the document and reconcile rendered pages with extracted regions.

## Common Failures

- columns, headers, footers, footnotes, or sidebars interleaved;
- font encodings producing garbled or invisible text;
- merged cells, spanning headers, borderless or multi-page tables;
- captions detached from figures or equations;
- watermarks and hidden layers entering content;
- encrypted, damaged, or truncated files failing silently;
- source coordinates lost, preventing audit and citation.

## Selection Protocol

Run several credible paradigms on representative and high-risk pages. Compare page/region completeness, reading order, critical fields, table relationships, provenance, downstream evidence recovery, latency, cost, and failure detectability. A vendor or benchmark result cannot substitute for the actual corpus.

Use selective escalation when a cheaper route has reliable gates; use a stronger default when silent failures are frequent or high consequence. Preserve per-region extractor provenance in hybrid output.

## Part of

← [[Parsing]]

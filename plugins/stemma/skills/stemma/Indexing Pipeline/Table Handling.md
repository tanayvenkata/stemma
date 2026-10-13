---
tags: [indexing]
---
# Table Handling

A table is a relational structure, not merely text arranged in rows. Retrieval and generation need cell values together with their row headers, column headers, units, spanning relationships, footnotes, and source anchors.

## Representation Contract

Preserve:

- table identity, page/region, title, caption, and surrounding reference;
- cell coordinates, spans, row/column hierarchy, and repeated headers;
- original string, normalized value, unit, and footnote links where required;
- continuation across pages;
- extraction method, confidence/validation state, and rendered source.

Markdown is useful for many modest rectangular tables, but it is not a universal canonical format. Wide, hierarchical, nested, or multi-page tables may require HTML, a cell graph, structured records, or several row-level search views linked to one canonical table.

## Retrieval Views

- whole-table representation for table-level discovery;
- row or logical-region representations with inherited headers;
- key-value serialization for narrow factual lookup;
- visual page/region representation when layout carries meaning.

Store derived search views separately from the canonical structure so a convenient serialization does not become false ground truth.

## Evaluate

1. Annotate critical tables and fields across layout classes.
2. Measure region detection, cell text, row/column/span structure, header association, and task-critical value accuracy.
3. Ask queries requiring specific cells, comparisons, units, footnotes, and cross-page continuation.
4. Verify citation back to the exact source region.
5. Inspect severe errors separately; one shifted numeric column can dominate many correct cells.

Choose extraction and serialization from corpus results, not a fixed tool ranking. Vision models can recover complex visual relationships but must be checked for omitted or invented values.

## Part of

← [[Parsing]]

---
tags: [indexing]
---
# Parsing

Parsing converts a source artifact into a structured representation. It is the earliest point at which content can be silently omitted, reordered, detached from its qualifiers, or assigned the wrong provenance. Downstream retrieval cannot recover evidence that never survived conversion.

## Output Contract

A useful parser emits more than plain text:

- ordered text with page, block, section, or timestamp anchors;
- headings and hierarchy;
- tables with cell, row, column, span, and header relationships;
- figures, equations, captions, and surrounding references where required;
- source identity, version, checksum, and extraction provenance;
- detected language, layout, OCR, and unresolved-failure signals;
- trusted policy metadata passed through without model invention.

Keep the rendered source available. Parsed output is a derived representation that must remain auditable and rebuildable.

## Extraction Paradigms

| Paradigm | Strength | Failure mode | Suitable role |
|---|---|---|---|
| Native/library extraction | Fast and deterministic on well-formed digital documents | Broken reading order, weak layout semantics, image-only pages | Baseline or first route for simple sources |
| OCR and layout models | Recovers scanned text and spatial regions | Recognition errors and incorrect region relationships | Scanned or layout-dependent documents |
| Vision-language extraction | Can interpret visually encoded structures and figures | Higher cost/variance; may normalize or invent content | Selective escalation for difficult pages and semantic extraction |
| Vision-native retrieval | Preserves page appearance without fully linearizing it | Requires multimodal indexing/retrieval and still needs provenance | Visual documents where layout is itself evidence |

These approaches can coexist at page or region level. Choose routes from observed document classes and failure mechanisms, not a universal tool hierarchy.

## Build a Routing Policy

1. Inventory formats, scan quality, layouts, languages, tables, figures, equations, handwriting, and high-risk fields.
2. Choose a simple credible baseline and run immutable representative sources through it.
3. Apply deterministic gates: page reconciliation, empty/duplicate output, text-density anomalies, encoding, missing required structures, and schema validity.
4. Inspect a stratified sample of passes and failures against rendered originals.
5. Route only the failing classes or pages to more capable extraction.
6. Preserve which extractor produced every region and any unresolved uncertainty.
7. Re-run downstream questions tied to labeled source regions.

Classification-first routing can save wasted work in stable, large corpora; parse-then-escalate can be simpler when the baseline is cheap and failures are detectable. Compare both policies if routing complexity matters.

## Evaluate at Three Levels

| Level | Examples | Limitation |
|---|---|---|
| Integrity | page counts, duplicate IDs, checksums, ACL/freshness propagation | Does not establish content fidelity |
| Representation | character/word error, region detection, reading order, table structure and field accuracy | Can miss whether the product can use the result |
| Task impact | retrieval of labeled regions and answers requiring parsed structures | Can hide the exact parsing mechanism unless traces are retained |

Weight critical numbers, units, dates, negation, identifiers, clauses, and permissions separately. A good average can conceal a single costly field shift.

## Failure Diagnosis

- **Missing source region:** extraction, OCR, routing, or ingestion failure.
- **Correct text, wrong order or association:** layout/structure failure.
- **Correct parse, failed retrieval:** investigate chunking, representation, filtering, or ranking.
- **Only downstream answer fails:** inject verified parsed evidence before blaming parsing.
- **Quality gate passes corrupted content:** improve detectability, not only the parser.

## Decision Rule

Adopt the simplest routing policy that satisfies critical fidelity and integrity constraints, improves the motivating document slices, and has acceptable latency, cost, escalation load, and reproducibility. Preserve serious failures as parser regression fixtures.

## Techniques

- [[PDF Extraction]]
- [[OCR]]
- [[Table Handling]]

## Part of

← [[Document Processing]]

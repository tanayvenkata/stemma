---
tags: [indexing]
---
# Cleaning

Cleaning removes extraction artifacts while preserving source meaning, structure, anchors, and auditability. It should be a versioned transformation, never an irreversible rewrite of canonical source content.

## Common Operations

- remove repeated headers, footers, page numbers, navigation, and duplicated boilerplate;
- repair encoding, null bytes, line-wrap hyphenation, and whitespace artifacts;
- normalize representations needed for indexing while retaining original strings;
- deduplicate pages or regions using content and structural identity;
- mark rather than silently discard uncertain or corrupted regions.

Rules can change meaning: a repeated disclaimer may be legally important, a hyphen may belong to an identifier, and whitespace can encode tables or code. Apply transformations by document class and keep before/after provenance.

Evaluate deterministic invariants, sampled diffs, critical fields, duplicated-token reduction, source-region coverage, and downstream retrieval. Adopt a rule only when it removes a demonstrated failure without damaging important slices.

## Part of

← [[Document Processing]]

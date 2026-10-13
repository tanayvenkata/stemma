---
tags: [indexing]
---
# Document-Aware Chunking

Document-aware chunking uses native structure—headings, layout regions, table rows, code syntax, legal clauses, dialogue turns, or simulation-world hierarchy—as candidate evidence boundaries.

## Examples

| Source | Structural unit | Context to inherit |
|---|---|---|
| markup | section, paragraph, list | heading path and anchors |
| code | symbol, function, class, syntax block | file, namespace, signature, selected dependencies |
| table | row group or logical region | table title, headers, units, footnotes |
| legal/policy text | clause or rule | jurisdiction, effective date, parent definitions |
| simulation state | entity, location, event, rule | perspective, time, world path, validity interval |

Structure is a strong prior, not a guarantee. A function can exceed the model limit; a section can contain several topics; imported context can overwhelm the target unit; parser errors can create false boundaries.

## Implementation

1. Parse the canonical structure and assign stable source anchors.
2. Choose atomic units that should not be split when possible.
3. Attach only context required to interpret or retrieve them.
4. Apply a documented fallback to oversized units while retaining parent relationships.
5. Store search units separately from larger content resolved for generation.

## Evaluate

Compare against a simple baseline on structure-dependent queries. Measure source-region coverage, broken-unit rate, inherited-context utility, variable-size tails, duplication, retrieval, and downstream outcomes. Test parser failures and migrations because the policy depends on structural extraction.

Use document-aware routing when structural preservation produces a meaningful benefit for a source class; do not claim that syntax boundaries are automatically semantically complete.

## Part of

← [[Chunking Strategy]]

---
tags: [indexing]
---
# Chunking

Chunking creates the evidence units that retrieval can find and generation can use. It is a joint design problem: search units should be discriminative, while resolved context must retain the definitions, qualifiers, structure, and neighboring evidence required to answer correctly.

## What a Chunking Policy Defines

- boundary source: tokens, sentences, paragraphs, headings, layout regions, code syntax, rows, turns, or learned signals;
- target and maximum size, including what happens to oversized atomic units;
- overlap or boundary context, if any;
- parent, sibling, and source-region relationships;
- metadata inherited or derived at each level;
- representation used for search versus content returned to generation;
- versioning and migration behavior when the policy changes.

## Failure Modes

| Symptom | Possible chunking cause | What to inspect |
|---|---|---|
| Required evidence is never retrieved | evidence was split, diluted, or omitted | source-region coverage by chunks |
| Retrieved text is locally relevant but unusable | heading, qualifier, table header, or neighboring definition was lost | resolved parent/sibling context |
| Recall rises but answers worsen | chunks are oversized, repetitive, or consume too much context | evidence-token ratio and downstream failures |
| Index and latency grow without quality lift | mechanical overlap or excessive fragmentation | duplicate-region coverage and cost |
| One document class fails disproportionately | one global policy ignores corpus structure | results by format and topology |

## Selection Workflow

1. Label stable source regions required by representative queries.
2. Begin with a simple structure-aware or recursive baseline.
3. Compare only strategies justified by an observed failure mechanism.
4. Hold parsed input, queries, embedding, retrieval policy, and context budget fixed where possible.
5. Measure region coverage, boundary integrity, redundancy, index cost, and downstream answer behavior.
6. Route by document class only when the evidence supports the added operational complexity.

Chunk size and overlap are experimental variables, not global defaults. Long model context does not remove the need for useful evidence units; it changes the quality–cost frontier and may allow larger resolved context after precise retrieval.

## Components

- [[Chunking Strategy]]
- [[Metadata Attachment]]

## Next

→ [[Embedding]]

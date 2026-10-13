---
tags: [generation]
---
# Context Preparation

Context preparation turns selected evidence and application state into an explicit, provenance-preserving input for generation. It allocates a finite attention and token budget while keeping instructions, trusted state, and untrusted retrieved content distinguishable.

## Context Contract

- source identity, version, authorization, and exact evidence spans;
- required evidence and known gaps;
- ordering and grouping rule;
- deduplication, parent resolution, truncation, and compression decisions;
- token budget reserved for instructions, evidence, tools, output, and runtime overhead;
- untrusted-content boundaries and injection policy;
- cache-relevant prefix identity and invalidation conditions.

## Preparation Workflow

```text
validated candidates
→ resolve source-faithful content and relationships
→ remove unjustified duplication
→ allocate budget across required evidence
→ group and delimit sources with provenance
→ order under a tested policy
→ validate coverage, truncation, and authorization
→ assemble the generation request
```

Delimiters help parsers and models distinguish sections, but XML is not a security boundary. Prompt injection defenses require instruction hierarchy, least-privilege tools, authorization outside model control, output/action validation, and adversarial testing.

Likewise, “place evidence at the edges” is not universal. Long-context position effects vary by model, task, content, and ordering. Compare relevance order, source grouping, chronological/logical order, and any edge-placement policy on matched cases.

## Components

- [[Context Formatting & Ordering]]
- [[Prompt Caching & Compression]]

## Next

→ [[Prompt Construction]]

---
tags: [retrieval]
---
# Contextual Compression

Contextual compression reduces retrieved content while attempting to retain all evidence and qualifiers needed for the query. It can be extractive, structural, or generative.

| Method | Strength | Main risk |
|---|---|---|
| select smaller source spans | source-faithful and auditable | boundary may omit definitions or exceptions |
| remove duplicates/boilerplate | saves budget with little semantic change | repetition may encode corroboration or scope |
| structure-aware pruning | retains headings/rows/fields | depends on correct parse and rules |
| generated summary | compact and query-focused | unsupported transformation and broken citations |

## Protocol

Freeze queries, source candidates, and context budget. Compare uncompressed and candidate policies on required-claim evidence coverage, contradiction/qualifier preservation, evidence-token ratio, citation mapping, generation quality, latency, and cost. Include adversarial and high-risk cases where a small omission changes meaning.

Store compressed text as a derived view with links to the exact source spans and compressor version. Do not overwrite canonical evidence.

Use compression when context waste is a diagnosed bottleneck and measured downstream gains exceed information loss and operational complexity.

## Part of

← [[Post-Retrieval Processing]]

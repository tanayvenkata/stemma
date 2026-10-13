---
tags: [indexing]
---
# Recursive Chunking

Recursive chunking tries preferred separators in order—such as sections, paragraphs, sentences, then tokens—until each unit fits the chosen maximum. It is a useful baseline because it is deterministic, inexpensive, and more structure-aware than blind fixed windows.

## Policy Decisions

- separator hierarchy for each source format;
- length function and tokenizer;
- target and hard maximum;
- behavior for oversized tables, code blocks, or paragraphs;
- optional overlap and source anchors;
- attachment of headings and other inherited context.

It does not guarantee semantic coherence: a paragraph can contain several topics, and a maximum-size fallback can still split a logical unit. Separator definitions may also fail on malformed parser output.

## Evaluation

Use it as the simple comparator in a controlled chunking experiment. Sweep size or overlap only over ranges justified by document structure and context budget. Measure region coverage, boundary failures, redundancy, chunks per document, retrieval, and downstream behavior.

Retain recursive chunking when more complex candidates do not produce a meaningful paired gain. Replace or route it when failures consistently require syntax-, layout-, discourse-, or hierarchy-aware boundaries.

## Part of

← [[Chunking Strategy]]

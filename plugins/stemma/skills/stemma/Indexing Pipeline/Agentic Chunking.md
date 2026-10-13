---
tags: [indexing]
reviewed: 2026-10-11
---
# Agentic Chunking

Uses an LLM agent to inspect document layout and dynamically determine where logical and semantic boundaries should be placed.

---

## The Problem It Solves
Heuristic chunkers (Fixed, Recursive) use static rules (like character counts or newline characters). However, complex real-world documents—such as clinical trial reports, messy legal filings, and mixed multi-topic memos—frequently transition between concepts without standardized headers or clean paragraph breaks.

Agentic chunking treats chunking as an **intelligent decision loop** rather than a mechanical text split.

---

## How It Works

1. **Sliding Evaluation Window**: The agent processes text sentence-by-sentence or paragraph-by-paragraph.
2. **Contextual Evaluation**: For each transition, the model evaluates: *"Does the next passage continue the current standalone concept, or does it introduce a new distinct proposition/topic?"*
3. **Dynamic Boundary Placement**: If a topic boundary is detected, the agent seals the current chunk and starts a new one.

```
Text Stream ──> [ LLM Decision Gate ]
                     │
         Topic shifted / new concept?
                  /          \
                NO            YES
               /                \
        [ Append to Chunk ]   [ Seal Chunk & Emit ]
```

---

## When to Use
Candidates to test against a recursive or structure-aware baseline, not settled wins:
- **Clinical & Medical Records**: Patient history notes, lab summaries, and clinician discharge memos where arbitrary splits separate medications from dosages.
- **Unstructured Transcripts & Meeting Notes**: Raw audio/video transcripts where speech transitions unpredictably between agenda items.
- **High-Stakes Legal Work**: Where cutting a paragraph mid-clause alters legal liability.

---

## Tradeoffs

| Advantage | Consideration |
|---|---|
| Can place more coherent boundaries on irregular documents (a hypothesis to confirm: compare boundary quality and retrieval against a recursive baseline on your own labeled regions) | Among the slowest and most expensive chunking methods (an LLM decision per candidate boundary during indexing) |
| Adapts dynamically to any document structure | Not practical for bulk millions-of-pages without heavy batch parallelization |

---

## Part of
← [[Chunking Strategy]]

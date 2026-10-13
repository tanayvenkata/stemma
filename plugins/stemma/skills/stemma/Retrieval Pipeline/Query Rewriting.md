---
tags: [retrieval]
reviewed: 2026-10-11
---
# Query Rewriting

Rephrasing, clarifying, or resolving conversational pronouns in a user's query using dialogue history before vector embedding.

---

## The Pronoun Resolution Trap

In multi-turn chat and voice agents, human queries are inherently conversational:
- User (Turn 1): *"Tell me about the Tesla Model 3 battery warranty."*
- Assistant (Turn 1): *"The battery warranty covers a set number of years or miles, whichever comes first."*
- User (Turn 2): *"How does **that** compare to the Model Y?"*

If you embed *"How does that compare to the Model Y?"*, the vector has zero idea what *"that"* refers to.

```
Conversation History: [ Turn 1: Tesla Model 3 battery warranty ]
User Turn 2: "How does that compare to the Model Y?"
                         │
                         ▼
        [ Fast Rewriter (Few-Shot Prompt) ]
                         │
                         ▼
Standalone Search Query: "Compare Tesla Model 3 battery warranty vs Tesla Model Y battery warranty"
```

---

## Key Production Rule
- **Gate rewriting by diagnosed need**: Pronouns and ellipses are common triggers, but spelling, jargon, conversational context, or vocabulary mismatch may also justify rewriting. Preserve the original query and compare rewritten retrieval against the fast path.

---

## Part of
← [[Query Transformation]]

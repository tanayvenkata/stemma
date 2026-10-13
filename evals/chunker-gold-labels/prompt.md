---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [niche]
---

We want to compare our current fixed-size chunker against a new semantic chunker. Our gold labels for 200 test queries are the IDs of the relevant chunks produced by the current chunker. How should we compute retrieval recall for the new chunker so the comparison is fair? Keep the answer short.

---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [generic]
---

My RAG retriever returns the top 20 chunks by cosine similarity, and a lot of them are irrelevant. What similarity cutoff should I use to drop the irrelevant ones before generation? Keep the answer short.

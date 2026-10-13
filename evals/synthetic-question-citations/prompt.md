---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [niche]
---

To improve retrieval we used an LLM to generate five likely user questions for each chunk and indexed those questions alongside the chunks. When a generated question matches the user's query, our answer cites the generated question text as the supporting evidence. Is that a reasonable design? Keep the answer short.

---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [niche]
---

Our enterprise RAG app retrieves the top 50 chunks for a query, then removes the ones the user isn't allowed to see before passing the rest to the LLM. The UI shows "Found N relevant documents" using the count from before filtering, and citations show document titles. The permission check runs in our backend, not in the prompt. Any security problems? Keep the answer short.

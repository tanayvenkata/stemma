---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [niche]
---

Our corrective RAG pipeline uses an LLM grader that labels each retrieved passage relevant or irrelevant, and we only pass relevant passages to generation. The grader is about 95% accurate per passage, yet many answers are still wrong or incomplete. What is likely going on, and how would we find out? Keep the answer short.

---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
tags: [generic]
---

For hybrid search I run BM25 and embedding search, then rank documents by 0.6 * cosine_similarity + 0.4 * bm25_score. BM25 only runs over the documents the embedding search returned. Any problems with this setup? Keep the answer short.

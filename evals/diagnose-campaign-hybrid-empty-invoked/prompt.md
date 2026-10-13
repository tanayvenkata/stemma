---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
tags: [diagnose-invoked]
---

Use the stemma skill's diagnose command. In local dev I set USE_HYBRID_RETRIEVAL=true. Now /search/unified never returns any voter quotes, not even for "What did Ohio voters say about the economy?", although strategy lessons still come back. With the flag off, quotes return fine. Did BM25 break retrieval?

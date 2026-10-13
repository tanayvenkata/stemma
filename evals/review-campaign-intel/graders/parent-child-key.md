---
type: llm
weight: 1
---

PASS if the answer flags that reindex_openai.py reads `child_chunk_ids` while the parent data uses `child_ids`, so parents in the production namespace have no children and hierarchical retrieval silently falls back to direct search. FAIL otherwise.

---
type: llm
weight: 1
---

PASS if the answer flags at least one indexing or lifecycle weakness found in the code: chunking per page splits content across page boundaries, the embedding model name is duplicated and not recorded with the index, or reindexing deletes the live collection before rebuilding. FAIL otherwise.

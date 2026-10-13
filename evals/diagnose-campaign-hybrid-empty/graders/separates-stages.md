---
type: llm
weight: 1
---

PASS if the answer establishes (from the code, or as a check to run) that the hybrid retriever does return focus-group results and that they are removed afterwards, rather than concluding BM25 or fusion returned nothing. FAIL if it blames BM25 recall or fusion without this separation.

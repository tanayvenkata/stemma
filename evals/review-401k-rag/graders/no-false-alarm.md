---
type: llm
weight: 1
---

PASS unless the answer claims that query and document embeddings use different models or settings (they do not: Chroma is created and queried with the same embedding function), or recommends embedding funds.csv into the vector store instead of querying it with SQL. FAIL if it makes either claim.

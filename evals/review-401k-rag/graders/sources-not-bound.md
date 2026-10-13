---
type: llm
weight: 1
---

PASS if the answer identifies that the sources shown to the user are not tied to the generated answer: either retrieval runs twice (retrieve and retrieve_with_context) with a non-deterministic LLM query rewrite so displayed sources can differ from the context used, or the model is never asked to cite. FAIL otherwise.

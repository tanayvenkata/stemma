---
type: llm
weight: 1
---

PASS if the plan enforces per-employee access inside retrieval (permission filters applied to the search itself, derived from authenticated identity, not left to the LLM) and also protects what is returned, such as citations, titles, snippets, or result counts. FAIL if access control is only mentioned generally or applied by the model or prompt.

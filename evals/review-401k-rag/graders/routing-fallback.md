---
type: llm
weight: 1
---

PASS if the answer identifies that the classifier's LLM fallback imports a module that does not exist (`unified_evaluator`), so low-confidence questions raise an error that the dispatcher catches and silently routes to document (RAG) search, meaning typical fund questions never reach the fund SQL path. FAIL if this is not identified.

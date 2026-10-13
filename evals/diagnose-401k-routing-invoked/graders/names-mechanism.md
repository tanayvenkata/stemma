---
type: llm
weight: 1
---

PASS if the answer names the mechanism: keyword confidence for this question falls below the 0.7 threshold, the LLM fallback imports a missing `unified_evaluator` module, and the dispatcher catches the error and silently defaults to RAG. FAIL if the missing module or the silent fallback is not identified.

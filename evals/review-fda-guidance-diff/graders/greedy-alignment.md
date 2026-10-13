---
type: llm
weight: 1
---

PASS if the answer identifies that alignment keeps only the top-1 old match and resolves conflicts greedily, so a new chunk that loses its match becomes NEW_REQUIREMENT (high impact) without trying other candidates, producing false NEW or REMOVED items when sections split, merge, or move. FAIL otherwise.

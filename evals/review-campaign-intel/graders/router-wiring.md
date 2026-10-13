---
type: llm
weight: 1
---

PASS if the answer flags at least one router-to-retrieval wiring bug: the router's race_ids are never applied to strategy retrieval, or the router-failure fallback constructs RouterResult with a `reasoning` field (and without race_ids) that the imported dataclass does not accept, so it raises instead of degrading. FAIL otherwise.

---
type: llm
weight: 1
---

PASS if the answer flags the fixed raw BM25 NO_MATCH_THRESHOLD (5.0) with whole-chunk queries as uncalibrated and not comparable across documents, or notes that MATCH_THRESHOLD is unused despite the claim that thresholds were validated. FAIL otherwise.

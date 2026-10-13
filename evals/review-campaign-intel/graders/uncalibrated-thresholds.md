---
type: llm
weight: 1
---

PASS if, beyond the RRF score-scale mismatch itself, the answer flags that the score thresholds (the 0.50, 0.75, or 0.55 cosine cutoffs, or the hybrid path's 0.50 × 0.01 cutoff) are hand-picked rather than calibrated on labelled relevant and irrelevant examples, or that the same values are reused across embedding models, namespaces, or reranker scores. FAIL otherwise.

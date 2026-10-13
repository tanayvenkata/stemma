---
type: llm
weight: 1
---

PASS if the answer identifies that with hybrid enabled the fused scores are RRF values (around 0.03 at most) but the API still drops focus groups whose top score is below the request's score_threshold of 0.50, so voter-quote results disappear. FAIL if this is not identified.

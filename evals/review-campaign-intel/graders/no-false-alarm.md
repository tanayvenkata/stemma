---
type: llm
weight: 1
---

PASS unless the answer claims the default hybrid fusion is a weighted sum of unnormalized BM25 and cosine scores (the default is RRF), claims BM25 only re-scores the dense hits (it scores the full corpus), or claims production queries and documents are embedded with different models. FAIL if it makes any of these claims as a current bug.

---
type: llm
weight: 1
---

PASS if the answer does all of the following:
- says there is no universal cosine cutoff, because raw similarity scores are not calibrated and their ranges differ across embedding models, corpora, or query types;
- tells the user to choose or validate a cutoff against labeled relevant and irrelevant examples from their own data, or to filter with a reranker or calibrated score instead.

Mentioning typical score ranges as an illustration, or offering a provisional starting point that the answer explicitly says must be validated on the user's data, is fine.

FAIL if the answer gives an absolute cosine value (such as 0.5 or 0.7) as the cutoff to use without making validation on the user's own data the main recommendation, or if it never explains why a fixed cutoff does not transfer.

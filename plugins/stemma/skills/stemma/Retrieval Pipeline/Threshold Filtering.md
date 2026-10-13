---
tags: [retrieval]
---
# Threshold Filtering

Threshold filtering uses a score or calibrated decision function to keep, reject, retrieve more, abstain, or escalate. Raw similarity and reranker scores are usually model-, corpus-, and query-dependent rather than probabilities.

## Calibration

Build held-out answerable, unanswerable, ambiguous, and high-risk cases. Examine score distributions and decision utility by slice. Measure:

- unsafe acceptance of insufficient evidence;
- unnecessary rejection of answerable cases;
- required-evidence coverage after filtering;
- calibration drift after model, corpus, or index changes;
- behavior when no candidate passes.

One global threshold may be inadequate when score distributions differ by route, language, query class, or retriever. Conditional thresholds or a learned policy add complexity and require protected evaluation.

Thresholding is valuable when the score contains stable decision information and a safe fallback exists. It is not a hallucination shield: generation can still misuse accepted evidence, and rejected evidence may have been valid but mislabeled or poorly scored.

## Part of

← [[Post-Retrieval Processing]]

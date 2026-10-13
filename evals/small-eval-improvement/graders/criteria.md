---
type: llm
weight: 1
---

PASS if the answer does all of the following:
- says a 2-question difference on 15 questions is not enough to conclude the new chunker is better;
- recommends a paired, per-question comparison (which questions flipped in each direction) rather than comparing totals;
- notes that questions drawn from the same documents are not independent, so the effective sample is smaller than 15;
- treats the ship decision as a judgment about risk and cost (for example "unresolved", ship only if no regressions on important cases, or collect more cases) rather than a statistical win.

FAIL if it declares the new chunker better or significantly improved, or misses the dependence between questions from the same documents.

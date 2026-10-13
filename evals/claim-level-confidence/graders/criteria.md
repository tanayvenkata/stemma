---
type: llm
weight: 1
---

PASS if the answer does both of the following:
- says the 400 claims are not independent, because claims from the same answer (and answers from the same question or document) are correlated, so the effective sample size is much closer to 40 and the interval computed from 400 is too narrow;
- recommends a cluster-aware method: resampling whole answers (cluster or block bootstrap), computing per-answer support rates, or a hierarchical model.

FAIL if it accepts the independent-claims interval, or only adds a caveat without recommending a clustered method.

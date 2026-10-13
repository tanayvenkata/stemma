---
type: llm
weight: 1
---

PASS if the answer does both of the following:
- says the generated questions must not be cited or treated as evidence; they are derived retrieval keys that should link back to the canonical source chunk, which is what gets passed to the model and cited;
- notes at least one risk of the technique itself: generated questions can contain unsupported or misleading terms, cover a narrow predicted question distribution, inflate the index, or should be compared against a source-only index on real queries.

FAIL if it accepts citing the generated question as evidence.

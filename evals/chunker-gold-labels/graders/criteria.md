---
type: llm
weight: 1
---

PASS if the answer does both of the following:
- says gold labels tied to the old chunker's chunk IDs cannot fairly score a different chunker, and recommends relabeling (or mapping) the evidence as chunker-independent source regions or spans (document plus character offsets, page or section, row, and so on);
- warns that counting any overlap between a retrieved chunk and the gold span as a hit is too permissive, because a large chunk can touch the span while burying it, so the metric should also account for how much of the chunk is relevant (coverage plus concentration, precision, or token efficiency).

FAIL if it proposes reusing the old chunk IDs directly, or if it treats any overlap as a full hit without flagging the large-chunk problem.

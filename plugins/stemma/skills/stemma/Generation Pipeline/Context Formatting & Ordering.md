---
tags: [generation]
reviewed: 2026-10-11
---
# Context Formatting & Ordering

Context formatting makes evidence boundaries, provenance, relationships, and trust level legible to both the model and downstream validators. Ordering allocates limited attention among those evidence units.

## Evidence Object

Retain a structured object before rendering:

```json
{
  "evidence_id": "stable-region-id",
  "source_id": "document-version",
  "text": "source-faithful content",
  "anchors": {"page": 14, "region": "..."},
  "retrieval": {"rank": 3, "method": "..."},
  "relationships": {"parent": "...", "siblings": []},
  "authorization_scope": "trusted-policy-reference"
}
```

Render into the model/runtime's preferred message or document format with explicit source boundaries. Escape or encode untrusted text so it cannot break the surrounding structure, while recognizing that delimiters do not neutralize malicious instructions by themselves.

## Ordering Policies

- retrieval or reranker relevance;
- grouping by source or evidence requirement;
- chronological, causal, or document order;
- interleaving complementary sources;
- position-aware arrangements tested for the chosen model.

Long-context models can still show position and distraction effects (Lost in the Middle measured them on 2023-era models; re-test on yours), but one universal “best evidence at both edges” rule does not follow. Compare policies on fixed evidence sets, required-claim coverage, citation mapping, order sensitivity, latency, and downstream answers.

Truncation must be visible. Allocate budget to required evidence and mark omitted sources rather than silently cutting the serialized string.

Primary reference: [Lost in the Middle](https://arxiv.org/abs/2307.03172).

## Part of

← [[Context Preparation]]

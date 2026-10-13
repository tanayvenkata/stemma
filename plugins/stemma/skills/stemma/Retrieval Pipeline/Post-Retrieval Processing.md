---
tags: [retrieval]
---
# Post-Retrieval Processing

Post-retrieval processing converts a broad candidate set into an evidence package for generation. Possible operations include rescoring, filtering, deduplication/diversity, parent resolution, compression, and ordering. They are conditional levers, not a mandatory sequence.

## Diagnose Before Adding a Stage

| Observation | Candidate intervention | Preconditions |
|---|---|---|
| required evidence is present but ranked late | reranking | candidate recall is already adequate |
| score distribution separates supported from unsupported queries | calibrated filtering/abstention | held-out labels and safe fallback exist |
| repeated passages crowd out complementary evidence | diversity or deduplication | duplicates are not meaningful frequency evidence |
| search unit lacks necessary surrounding context | parent/sibling resolution | relationships and source versions are reliable |
| relevant unit contains excessive irrelevant text | selective compression | extraction preserves qualifiers and citation mapping |
| correct evidence is lost under context budget | context assembly and budget allocation | required evidence labels are available |

## Controlled Pipeline

1. Freeze raw candidate rankings and labels.
2. Add one justified operation or designed combination.
3. Retain candidates before and after every stage.
4. Measure required-evidence coverage, ordering, evidence concentration, diversity, citation traceability, latency, cost, and failures.
5. Run a fixed downstream generation comparison.
6. Prefer conditional invocation when benefit is localized.

Long context capacity is not evidence that more candidates help. Position, distractors, redundancy, model behavior, and cost remain workload-dependent. Conversely, aggressively reducing to a few “pristine” chunks can destroy multi-evidence answers.

## Components

- [[Reranking]]
- [[Diversity Selection]]
- [[Threshold Filtering]]
- [[Context Assembly]]
- [[Contextual Compression]]

## Part of

← [[Retrieval]]

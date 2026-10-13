---
tags: [indexing]
reviewed: 2026-10-11
---
# Multimodal Handling

Multimodal indexing preserves evidence whose meaning depends on image, layout, audio, video, code execution, or structured data rather than text alone. Converting everything to text is one representation choice and can discard decisive information.

## Representation Strategies

| Strategy | Strength | Risk |
|---|---|---|
| extract/transcribe to text | reuses text retrieval and supports inspection | loses visual, acoustic, temporal, or spatial detail |
| shared multimodal embedding | cross-modal search in one space | modality-specific distinctions may be weak |
| modality-specific indexes | specialized fidelity | fusion and calibration complexity |
| multi-vector/late interaction | fine-grained token/patch matching | index and query cost |
| vision-native page retrieval | preserves full layout | large representations and model/runtime dependency |

Store raw artifacts or stable references, derived representations, timestamps/regions, modality relationships, and extractor/model versions. A caption, OCR text, page image, and table structure are complementary views, not interchangeable truth.

## Evaluation

Build cases requiring genuinely modality-dependent evidence. Measure cross-modal and within-modal retrieval, region/timestamp localization, source fidelity, task success, citation, latency, storage, and failures caused by conversion. Include visually similar distractors and text-only questions so multimodal complexity must demonstrate incremental value.

Multimodal retrieval research includes reasoning-intensive benchmarks and late-interaction models; treat these as directions to test, since model rankings remain workload-specific.

Primary reference: [ViDoRe: Visual Document Retrieval Benchmark](https://arxiv.org/abs/2407.01449).

## Part of

← [[Document Processing]]

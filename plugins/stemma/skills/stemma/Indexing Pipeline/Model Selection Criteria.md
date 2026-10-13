---
tags: [indexing]
---
# Model Selection Criteria

Embedding-model selection is a constrained in-domain retrieval experiment, not a leaderboard lookup.

## Screening Dimensions

| Dimension | Questions |
|---|---|
| task evidence | Does public evaluation include retrieval tasks resembling the target? |
| target corpus | How does it handle domain vocabulary, identifiers, hard negatives, and query/document asymmetry? |
| language and modality | Are every required language and evidence modality represented? |
| input contract | What tokenizer, instructions, truncation, pooling, and maximum input behavior apply? |
| vector contract | Dimension, normalization, metric, precision, and supported truncation/quantization? |
| deployment | Hosted or self-operated privacy, license, capacity, latency, batching, and version control? |
| lifecycle | Can old/new versions coexist, be rebuilt, compared, and rolled back? |

MTEB, BEIR, multilingual, multimodal, or reasoning-intensive benchmarks can shortlist candidates, but aggregate rank mixes tasks and distributions. Inspect the relevant subsets and then test protected in-domain cases.

## Selection Protocol

1. Freeze chunks, queries, pooled labels, and exact-search evaluation.
2. Implement every candidate's required query/document encoding correctly.
3. Compare paired retrieval results and critical slices before approximate indexing.
4. Measure sequence truncation, dimension/precision tradeoffs, throughput, memory/storage, latency, and cost.
5. Test the intended approximate index, filters, concurrency, updates, and failure behavior.
6. Prefer the simplest operational candidate when quality is practically indistinguishable.

Long input, Matryoshka support, multimodality, or open weights are capabilities to value only when the architecture uses them.

## Part of

← [[Embedding]]

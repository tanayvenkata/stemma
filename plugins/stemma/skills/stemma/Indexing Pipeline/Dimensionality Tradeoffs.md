---
tags: [indexing]
---
# Dimensionality Tradeoffs

Vector footprint has two independent axes: the number of dimensions and the number of bits used to store each value. Both affect memory and compute; both can remove retrieval signal.

## Memory Model

Ignoring index overhead, raw vector storage is approximately:

$$
\text{bytes}=N\times D\times \frac{b}{8}
$$

where $N$ is vector count, $D$ dimensions, and $b$ bits per stored component. Real indexes add identifiers, graph/list structures, metadata, alignment, replicas, and temporary build memory.

## Dimension Reduction

Use a smaller native model output, a training-supported truncated representation, or a separately learned projection. Do not assume the first dimensions of an arbitrary vector are meaningful. Compare exact-search quality before attributing loss to the approximate index.

## Precision Reduction

| Representation | Benefit | Risk |
|---|---|---|
| full or reduced floating point | stronger fidelity and simple scoring | larger memory/bandwidth |
| scalar/product quantization | compact approximate distance | reconstruction and ranking error depend on data and training |
| binary representations | very compact and fast bit operations | larger information loss; often needs candidate rescoring |

Quantization support and semantics vary by model and index. “Int8,” “binary,” or a compression ratio does not specify expected quality.

## Decision Procedure

1. Set the operational constraint: memory, storage, build time, throughput, or transfer.
2. Establish full-representation exact-search quality.
3. Test supported dimensions and precisions independently, then important combinations.
4. Measure candidate recall, final ranking, critical slices, index overhead, latency, and rebuild cost.
5. Use full-precision or stronger rescoring only if the compact stage preserves required candidates.
6. Prefer the least complex point satisfying quality and resource constraints.

Dataset size alone does not determine compression. Hardware, filter selectivity, concurrency, update rate, replication, and acceptable loss shape the frontier.

## Part of

← [[Embedding]]

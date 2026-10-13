---
tags: [indexing]
---
# Normalization

$L_2$ Normalization scales an embedding vector so that its Euclidean length ($\|v\|_2$) equals exactly $1.0$, turning the vector into a unit vector on the hypersphere.

---

## The Mathematical Principle

For vector $v = [v_1, v_2, \dots, v_d]$:

$$\hat{v} = \frac{v}{\sqrt{\sum_{i=1}^d v_i^2}} = \frac{v}{\|v\|_2}$$

---

## Why Normalization Can Simplify Cosine Search

Standard **Cosine Similarity** between vectors $A$ and $B$ requires three computations:

$$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\|_2 \cdot \|B\|_2}$$

When vectors are pre-normalized upon insertion ($\|A\|_2 = 1$ and $\|B\|_2 = 1$):

$$\text{Cosine Similarity}(A, B) = A \cdot B \text{ (Simple Dot Product)}$$

### Hardware Impact:
- Pre-normalized vectors let an implementation use dot product for cosine ranking.
- Actual latency depends on the engine, index, hardware, vector count and whether normalization is already built into the model or distance operator.

---

## When to Ensure Normalization
- Normalize when the embedding model and similarity metric require unit vectors. Do not normalize automatically when vector magnitude carries signal.
- Normalize explicitly in code or through a verified model/runtime option, and record where it occurs so vectors are not normalized inconsistently during migrations.

---

## Part of
← [[Embedding]]

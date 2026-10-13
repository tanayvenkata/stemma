---
tags: [indexing]
reviewed: 2026-10-11
---
# IVF

**Inverted File Index (IVF)** is a space-partitioning clustering index that groups high-dimensional vectors into Voronoi cells using $K$-Means clustering.

---

## The Mental Model: City Neighborhoods

Rather than comparing a query against every house in a country, IVF partitions the map into $K$ neighborhoods (Voronoi cells):

```
       ┌──────────────────┬──────────────────┐
       │   Cluster 1      │   Cluster 2      │
       │     (Centroid)   │     (Centroid)   │
       │   •  •  •        │    •   •   •     │
       ├──────────────────┼──────────────────┤
       │   Cluster 3      │   Cluster 4      │
       │   •   Query  •   │     (Centroid)   │
       │     (Centroid)   │    •   •   •     │
       └──────────────────┴──────────────────┘
```

1. **Training Phase**: Runs $K$-Means clustering across the corpus to compute $K$ centroid vectors (e.g. $K = 1,024$).
2. **Inverted List Creation**: Assigns each document vector to its closest centroid.
3. **Query Phase**:
   - The query vector finds its closest `nprobe` centroids (e.g. the 3 nearest clusters).
   - The search *only scans vectors inside those 3 clusters*, skipping the other 1,021 clusters.

---

## Key Tuning Parameters

| Parameter | What It Controls | Starting Point (tune on your data) | Impact |
|---|---|---|---|
| **`nlist` ($K$)** | Total number of cluster centroids | [FAISS guidance](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index): $4\sqrt{N}$ to $16\sqrt{N}$ below ~1M vectors, trained on 30–256 vectors per centroid (verified 2026-10) | More clusters = faster search, but requires larger training dataset. |
| **`nprobe`** | Number of adjacent clusters inspected during query | Start small; raise until recall against exact search meets the target | Higher `nprobe` generally raises recall; scan work grows with the number of lists probed. |

---

## When to Use IVF
- **Large-Scale Memory-Constrained Systems**: When the collection is large enough that HNSW graph memory is unaffordable; measure memory and recall for both on your data rather than assuming a fixed overhead or size cutoff.
- **Often Combined with Quantization (`IVF-PQ`)**: Product quantization stores each vector as short sub-vector codes, cutting memory enough for very large collections at some recall cost; measure that cost against exact search.

---

## Part of
← [[Vector Index]]

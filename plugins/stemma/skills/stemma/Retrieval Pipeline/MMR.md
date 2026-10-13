---
tags: [retrieval]
reviewed: 2026-10-11
---
# MMR

**Maximal Marginal Relevance (MMR)** balances query relevance with information diversity, preventing redundant chunks from monopolizing the LLM context window.

---

## The Core Dilemma: Redundancy Traps

Standard vector search can return several nearly identical chunks (e.g. slightly different versions of the same paragraph from different document drafts). Passing them all wastes tokens and crowds out other relevant viewpoints.

---

## The Mathematical Formula

$$\text{MMR} = \arg\max_{d_i \in R \setminus S} \left[ \lambda \cdot \text{Sim}_1(d_i, Q) - (1 - \lambda) \cdot \max_{d_j \in S} \text{Sim}_2(d_i, d_j) \right]$$

Where:
- $Q$ is the search query.
- $R$ is the candidate pool of retrieved chunks.
- $S$ is the set of chunks already selected.
- $\lambda \in [0, 1]$ is the diversity tuning parameter and must be selected on development cases for the intended relevance–coverage tradeoff.
  - $\lambda = 1.0$: Pure vector similarity (zero diversity).
  - $\lambda = 0.0$: Pure diversity (ignores query relevance and picks, from the retrieved pool, the candidate least similar to those already selected).

---

## When to Use MMR
- **News, Web Search, & Multi-Source Synthesis**: When merging articles from 10 different news outlets reporting on the same event.
- **Whole-Corpus Exploratory Queries**: *"Summarize all employee complaints from Q3"* (reduces the chance that near-duplicate grievances crowd out distinct ones).

Compare MMR with the original ranking on required-evidence coverage, relevance, duplicate-region rate, source/claim breadth, and downstream answers. Embedding dissimilarity is only a proxy for useful diversity; repeated sources may represent corroboration rather than waste.

---

## Part of
← [[Diversity Selection]]

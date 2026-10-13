---
tags: [retrieval]
---
# Diversity Selection

Diversity selection trades some individual relevance for broader evidence coverage. It is useful when near-duplicates crowd out distinct subtopics, sources, time periods, or required evidence units.

Maximal Marginal Relevance is one common greedy objective:

$$
\operatorname{MMR}(d)=\lambda\,\operatorname{rel}(d,q)-(1-\lambda)\max_{s\in S}\operatorname{sim}(d,s)
$$

$\lambda$ controls the relevance–novelty tradeoff and must be tuned for the task.

Define diversity semantically: source identity, evidence requirement, entity, stance, time, or representation distance may matter more than embedding dissimilarity. Repeated evidence can also indicate corroboration or prevalence, so deduplication is not always correct.

Compare the original ranking and diversity policy on required-evidence coverage, ranking, duplicate-region rate, source/claim breadth, downstream answers, and harmed cases. Use it when complementary evidence is missing from the final context despite existing in the candidate pool.

## Part of

← [[Post-Retrieval Processing]]

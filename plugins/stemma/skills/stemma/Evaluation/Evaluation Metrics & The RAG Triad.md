---
tags: [evaluation]
---
# Evaluation Metrics & The RAG Triad

## Contents

- 1. Start With the Construct, Not the Metric Name
- 2. The RAG Triad Is a Diagnostic Map
- 3. Retrieval Metrics
- 4. Generation and Task-Outcome Measures
- 5. Operational Measures
- 6. Comparison Protocol
- Practical Checklist

Metrics turn a quality claim into recorded evidence. They do not decide what “good” means: begin with the decision, failure costs, evaluation unit, and labels, then choose the smallest set of measures that can distinguish the relevant failure modes.

---

## 1. Start With the Construct, Not the Metric Name

Before calculating anything, write a **measurement contract**:

| Field | Question |
|---|---|
| Decision | What will change because of this measurement? |
| Unit | Query, retrieved region, claim, answer, conversation, or session? |
| Construct | Relevance, evidence coverage, groundedness, task correctness, utility, latency, or cost? |
| Reference | Which labels, source regions, expected claims, or rubric define success? |
| Aggregation | Mean, percentile, worst slice, failure rate, or risk-weighted loss? |
| Uncertainty | How will variation across examples, runs, judges, and annotators be represented? |

Identically named metrics can use different prompts, relevance units, denominators, or judge models. Record the metric definition and version; never compare scores from incompatible implementations as if they shared a scale.

It is reasonable to compute every **applicable, valid, inexpensive diagnostic metric** and retain the full per-case panel. Before viewing results, still name the primary outcome that decides the hypothesis and the guardrails that can veto adoption. The broader panel explains tradeoffs and failures; it must not become a menu from which to select whichever score happened to improve.

## 2. The RAG Triad Is a Diagnostic Map

```text
query ── relevance/precision ──> retrieved evidence
  │                                  │
  └──── answer relevance/utility ─> answer
                                     ▲
retrieved evidence ── groundedness ──┘
```

The triad separates three relationships:

1. **Query ↔ context:** did retrieval return useful evidence and rank it well?
2. **Context ↔ answer:** are the answer's externally verifiable claims supported by the supplied evidence?
3. **Query ↔ answer:** does the answer satisfy the user's request?

It is not a complete scorecard. A grounded answer can still be wrong if the context is wrong, incomplete if evidence is missing, or unsafe despite being relevant. Preserve component metrics, end-to-end task outcomes, and operational constraints separately instead of collapsing everything into one average.

## 3. Retrieval Metrics

First define the relevance unit—document, region, passage, or fact—and whether relevance is binary or graded.

For query set $Q$, relevance label $rel_q(i)$ at rank $i$, and cutoff $K$:

| Metric | Definition | Use when | Blind spot |
|---|---|---|---|
| **Hit Rate@K** | $\frac{1}{\lvert Q\rvert}\sum_q \mathbb{1}[\exists i\le K: rel_q(i)>0]$ | One useful result may be sufficient. | Ignores rank within $K$ and missing additional evidence. |
| **Recall@K** | $\frac{1}{\lvert Q\rvert}\sum_q \frac{\lvert R_q@K\cap G_q\rvert}{\lvert G_q\rvert}$ | The answer needs all or several known evidence regions. | Requires reasonably complete ground truth. |
| **Precision@K** | $\frac{1}{\lvert Q\rvert}\sum_q \frac{\lvert R_q@K\cap G_q\rvert}{K}$ | Distracting context consumes budget or misleads generation. | Penalizes useful unlabeled evidence. |
| **MRR@K** | $\frac{1}{\lvert Q\rvert}\sum_q \frac{1}{\text{rank of first relevant result}}$, or $0$ if absent by $K$ | The first useful result dominates user or generator behavior. | Ignores every relevant result after the first. |
| **Average Precision@K** | For each query, average precision at ranks containing relevant items, normalized by $\min(\lvert G_q\rvert,K)$; then average over queries. | Binary relevance and the ordering of multiple useful results both matter. | Depends on complete binary labels. |
| **NDCG@K** | $DCG@K/IDCG@K$, where $DCG@K=\sum_{i=1}^{K}\frac{2^{rel_q(i)}-1}{\log_2(i+1)}$ | Relevance is graded and high ranks matter more. | Grade definitions strongly shape the score. |

### Library-search intuition

Imagine asking a librarian for books needed to answer a research question:

| Metric | Intuition |
|---|---|
| **Hit Rate@K** | Did the first stack contain at least one useful book? It does not care whether the rest of the required books were missed. |
| **Recall@K** | Of all useful books known to exist in the library, how many did the librarian bring? Returning the entire library can score perfectly. |
| **Precision@K** | Of the books brought to the desk, how many were useful? It counters the “bring everything” strategy, but can punish useful books missing from the labels. |
| **MRR@K** | How far down the stack was the first useful book? It ignores every useful book after that first success. |
| **Average Precision@K** | As each useful book appears, how clean was the stack up to that position? It rewards repeatedly placing useful books ahead of distractors. |
| **NDCG@K** | Were the most valuable books near the top, with merely helpful books later? It requires defensible grades of usefulness. |

No metric dominates the others because each encodes a different definition of a good stack. A task needing one decisive source may emphasize Hit Rate or MRR; a task requiring several sources needs coverage or Recall; a tight context budget makes Precision and ranking quality more important. Use multiple diagnostics when their blind spots differ, while keeping the experiment's decision metric tied to the actual task.

Report the full curve over decision-relevant cutoffs when choosing $K$. A better score at $K=20$ may not help a system that can afford only five regions.

### Evidence coverage rather than chunk-ID matching

Chunk boundaries change when parsing or chunking changes. Durable ground truth identifies source regions or atomic evidence requirements. A candidate chunk receives credit when it overlaps or entails the required evidence under a documented matching rule.

For required evidence units $E_q$:

$$
\text{Evidence Coverage@K}(q)=
\frac{|\{e\in E_q:\text{covered}(e,R_q@K)\}|}{|E_q|}
$$

Inspect uncovered units. A single average cannot distinguish a retriever that misses one optional detail from one that systematically omits decisive evidence.

## 4. Generation and Task-Outcome Measures

Do not confuse the **construct**, **test scope**, and **scorer**:

| Axis | Examples | What it tells you |
|---|---|---|
| Construct being measured | groundedness, correctness, completeness, instruction satisfaction | Which property the score represents |
| Scope under test | one component, an interface between components, or the assembled system | Which parts could have caused the result |
| Scorer | deterministic rule, learned similarity/entailment model, model judge, human, or observed task outcome | How the property is converted into a label or number |

The same construct can appear at several scopes. Groundedness measured with a fixed context isolates generation; groundedness measured after the candidate system retrieves its own context is end to end and includes upstream evidence failures.

### Software-testing intuition

- **Unit/component test:** freeze the input to one stage. Give the generator fixed evidence to test claim support, or test the retriever directly against labeled source regions.
- **Integration test:** exercise a boundary, such as retrieval → context assembly → generation, to learn whether selected evidence survives budgeting and is actually used.
- **End-to-end test:** begin with the real request and corpus, run the assembled pipeline, and score the user-visible outcome. It is closest to system utility but least able to localize the cause of failure.

Run cheap deterministic component checks frequently. Run selected integration checks after meaningful component changes, and run the representative end-to-end suite before adopting a candidate. Cost is common but not the only reason for this pyramid: broader tests are also noisier and make root-cause attribution harder.

### Groundedness or faithfulness

Decompose the answer into atomic, externally verifiable claims $S(A)$. Label each claim as supported, contradicted, unsupported, or not applicable against the provided context.

$$
\text{Supported-Claim Rate}=
\frac{\sum_{s\in S(A)} w_s\,\mathbb{1}[s\text{ supported}]}{\sum_{s\in S(A)} w_s}
$$

Weights $w_s$ may represent claim importance or risk, but must be fixed before comparing systems. Also report contradiction and unsupported-claim rates; two systems can have the same supported rate with different safety implications.

Groundedness asks whether the answer follows from its context—not whether the context itself is true. Evaluate source correctness and task correctness separately.

### Answer relevance and instruction satisfaction

This is a construct, not one canonical formula. Score observable requirements such as:

- answers the asked question rather than a nearby one;
- covers required subparts;
- obeys scope, format, abstention, and citation instructions;
- avoids irrelevant material that obstructs use.

Possible scorers include deterministic checks, rubric-based human or model judgments, and task-specific semantic comparisons. Reverse-question generation plus embedding similarity is one proxy, not the definition; it can reward topical overlap while missing incorrect or incomplete answers.

### Correctness, completeness, and utility

Use references only when they represent the acceptable answer space. Exact match suits normalized identifiers or constrained facts; claim-level comparison suits answers with several valid phrasings; task success or user action may be the best measure for open-ended assistance. If several answers are valid, a single reference answer must not be treated as exhaustive ground truth.

## 5. Operational Measures

Quality must be joined—not averaged blindly—with service constraints:

| Measure | Record |
|---|---|
| Latency | End-to-end and component latency; report median and tail percentiles. |
| Time to first token | Queueing, retrieval, preprocessing, and model prefill contributions. |
| Cost | Per request and per successful task, with input, output, retrieval, and judge cost separated. |
| Context efficiency | Retrieved tokens, evidence-bearing tokens, truncation, and unused-context rate under a stated labeling method. |
| Reliability | Timeout, malformed-output, empty-retrieval, fallback, and retry rates. |

Choose budgets from user needs, risk, and observed baselines. A universal latency, cost, or quality threshold is not evidence.

## 6. Comparison Protocol

1. Freeze the dataset version, ground truth, scorer versions, prompts, and system configuration.
2. Run baseline and candidate on the **same examples**; fix seeds where supported and repeat stochastic stages when variability matters.
3. Retain per-example results and paired deltas, not just aggregate means.
4. Report uncertainty with paired bootstrap intervals or another method whose assumptions match the data.
5. Inspect meaningful slices and severe failures; averages can hide regressions in rare or high-risk cases.
6. Require hard safety or reliability constraints separately from improvement metrics.
7. Treat an interval containing zero as inconclusive about direction—not proof of equivalence. Use an equivalence or non-inferiority design when that is the actual claim.
8. Diagnose with examples before changing the pipeline. Metrics identify where to look; they rarely identify the cause by themselves.

### Reading uncertainty in a paired comparison

A paired bootstrap repeatedly samples evaluation cases **with replacement**, keeps each case's baseline and candidate outputs together, and recomputes the aggregate difference. The resulting distribution shows how sensitive the estimated change is to which cases happened to enter the dataset. It does not correct an unrepresentative benchmark or dependent duplicate cases.

Choose the claim before the statistical procedure:

- **Improvement:** is the candidate better by a decision-relevant amount?
- **Non-inferiority:** can we rule out degradation larger than a predeclared acceptable margin, perhaps in exchange for lower cost?
- **Equivalence:** can we rule out differences outside a predeclared band in either direction?

The margin must come from product consequences, not from the observed result. More decimal places or a narrow interval around the wrong population do not create valid evidence.

## Practical Checklist

- [ ] The metric corresponds to a written claim and decision.
- [ ] Evaluation unit, cutoff, relevance grades, and denominator are explicit.
- [ ] Ground truth survives reasonable pipeline changes.
- [ ] Scorer behavior is calibrated against representative human decisions where judgment is subjective.
- [ ] Per-example outputs, uncertainty, slices, and severe failures are retained.
- [ ] Quality, safety, latency, reliability, and cost are not hidden in one composite score.

Primary references: [Stanford IR evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html), [NIST experimental comparison guidance](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm), and [RAGChecker](https://arxiv.org/abs/2408.08067).

---

## Part of

← [[Evaluation Strategy & Experimental Design]]

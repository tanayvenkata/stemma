---
tags: [evaluation]
---
# Statistical Decision-Making for Evaluation

## Contents

- Define the estimand before the estimator
- Identify the independent unit
- Prefer paired comparisons
- Separate case variance from run variance
- Quantify uncertainty appropriately
- Design for practical power
- Prevent false discoveries and evaluation overfitting
- Convert evidence into a product decision
- Decision record
- Sources

Statistical evaluation asks what can be inferred about a target workload from finite, noisy, and often dependent cases. Decision analysis asks whether the supported difference is large enough—and safe enough—to justify changing the system.

This note applies general scientific inference to AI evaluation. It does not replace representative data, valid labels, failure analysis, or domain judgment. Precise uncertainty around the wrong population is still wrong.

## Define the estimand before the estimator

An **estimand** is the population quantity the evaluation intends to learn. Examples include:

- average paired change in task success over next quarter's expected traffic;
- change in unsupported-claim rate for high-consequence policy questions;
- probability an agent completes a task safely on an ordinary first attempt;
- tail latency among successful requests;
- expected cost per acceptable outcome.

Then choose an estimator—mean, weighted rate, percentile, ratio, survival curve, or model—that approximates it from observed cases.

Write:

| Field | Required choice |
|---|---|
| Target population | Users, tasks, corpus, environments, and time period covered by the claim |
| Sampling unit | Independent unit drawn from that population |
| Treatment | Complete candidate behavior or the one controlled component change |
| Outcome | Observable success, failure, safety, resource, or utility variable |
| Aggregation | Traffic-weighted mean, critical-slice rate, percentile, or another declared summary |
| Comparison | Improvement, non-inferiority, equivalence, or descriptive estimation |
| Practical margin | Smallest gain or largest loss that changes the decision |

An evaluation set assembled for coverage is not automatically a probability sample. Report results as conditional on the represented suite unless weighting and sampling justify a population estimate.

## Identify the independent unit

AI evaluation records often have nested dependence:

```text
source or customer
└── task
    └── trial / repeated model run
        └── turns, claims, retrieved items, or tool calls
```

Ten claims from one answer are not ten independent task outcomes. Five questions about one document contain less independent information than five questions about unrelated documents. Repeated trials estimate within-task stochasticity; they do not replace more independent tasks.

Cluster uncertainty at the level whose sampling could plausibly change—for example customer, document, conversation, or task family. When several levels matter, use a hierarchical model or a cluster-aware bootstrap rather than pretending every row is independent.

## Prefer paired comparisons

Run baseline and candidate on the same cases when possible. For case $i$:

$$
d_i=y_{i,candidate}-y_{i,baseline}
$$

Estimate the distribution of $d_i$, not only the difference between two unrelated aggregate means. Pairing removes much of the variance due to case difficulty and makes helped/harmed inspection direct.

Keep execution order, shared caches, rate limits, and mutable environment state from favoring one condition. Randomize or counterbalance order where contamination is possible. If conditions cannot share the same environment safely, describe the resulting confound rather than calling the comparison paired.

## Separate case variance from run variance

For stochastic systems, decide what the product actually does:

- **one ordinary attempt:** estimate per-attempt success;
- **up to $k$ attempts allowed:** evaluate the exact retry/selection policy and total cost;
- **consistency required:** estimate all-runs success or failure probability;
- **human selects among candidates:** include selection quality and reviewer cost.

Run multiple trials on a representative subset to estimate within-task instability. Allocate additional budget between more tasks and more trials according to which variance dominates and which estimand matters. Averaging many trials on a few easy tasks can produce narrow but irrelevant intervals.

## Quantify uncertainty appropriately

Useful options include:

- paired bootstrap over independent cases or clusters;
- confidence intervals for paired means or proportions when assumptions fit;
- hierarchical or mixed-effects models for nested tasks, customers, and trials;
- Bayesian posterior intervals when priors and likelihood are explicit and reviewable;
- exact or conservative binomial intervals for sparse failures.

Report the point estimate, interval, unit of resampling, case and trial counts, missing/error handling, and important distributional shape. For tail latency, ratios, and heavily skewed cost, a mean-only normal approximation can mislead.

If zero failures are observed in $n$ independent trials, the rough 95% “rule of three” upper bound is $3/n$. It is an approximation, assumes representative independent trials, and does not prove absence of failure. For catastrophic risks, scenario coverage, adversarial search, and architectural controls matter more than shrinking an average rate.

## Design for practical power

Before a large run:

1. define the smallest effect worth acting on;
2. pilot representative paired cases;
3. estimate case variance, within-task variance, prevalence, and clustering;
4. choose cases and repeats that can distinguish the practical margin with useful probability;
5. oversample important rare slices for diagnosis, while keeping their reporting separate from traffic-weighted estimates;
6. declare what an underpowered result will mean: unresolved, not “no difference.”

Power analysis is a planning model, not an oracle. Recalculate when the task mix, metric distribution, grader reliability, or candidate similarity changes.

## Prevent false discoveries and evaluation overfitting

Testing many metrics, slices, prompts, judges, models, and checkpoints creates opportunities to select a lucky improvement.

- predeclare the primary outcome and hard guardrails;
- label secondary analyses exploratory;
- preserve every attempted candidate and holdout exposure;
- use correction, hierarchical testing, or confirmation on untouched data when many claims are made;
- avoid repeatedly peeking at a fixed release suite and stopping on a favorable fluctuation;
- use sequential designs with explicit stopping rules when evidence is reviewed continuously;
- refresh capability sets before saturation and retain solved tasks as regression tests.

The main defense is not one correction formula. It is an honest record of the search process plus independent confirmation of the final claim.

## Convert evidence into a product decision

Keep quality, safety, latency, reliability, and cost as a vector first. Identify the Pareto frontier: a system is dominated if another is at least as good on every important dimension and better on one.

For remaining candidates, use explicit consequences:

```text
expected successful tasks × value of success
− runtime and infrastructure cost
− human review and exception cost
− expected failure and remediation cost
− migration and maintenance cost
```

Run scenarios for uncertain volumes, values, and failure costs. Report the break-even point—for example, the minimum success lift or task volume needed to repay added review and latency. This is usually more decision-useful than asserting one universal “good” score.

Possible decisions are:

- **adopt** when the target gain exceeds the practical margin and all gates hold;
- **constrain** when benefit is credible only for identifiable slices;
- **prefer the cheaper/simpler candidate** under demonstrated non-inferiority or equivalence;
- **reject** when a hard gate fails or expected harm outweighs value;
- **remain unresolved** when uncertainty spans materially different decisions;
- **collect targeted evidence** only when its expected value can change the decision.

## Decision record

Preserve the estimand, target population, sampling and clustering units, manifests, practical margins, case/trial allocation, interval method, missing/error policy, primary and exploratory analyses, slice results, utility assumptions, sensitivity analysis, decision, and conditions requiring reevaluation.

## Sources

- [Anthropic: A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- [NIST: Selecting an experimental design for the objective](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm)
- [NIST: Sample sizes for confidence-interval width](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm)

## Part of

← [[Evaluation Strategy & Experimental Design]]

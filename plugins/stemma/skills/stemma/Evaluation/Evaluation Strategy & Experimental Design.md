---
tags: [evaluation]
---
# Evaluation Strategy & Experimental Design

## Contents

- From stakeholder value to an evaluation contract
- Where to Start in a Zero-to-One System
- The Workbook Loop
- Experiment Contract
- Methods
- Ownership Boundaries
- Specialized entry paths
- Sources
- Next

Evaluation owns the shared scientific workflow for deciding whether an AI-system component, policy, configuration, or architecture deserves to enter or remain in the system. RAG, agents, and simulations supply different evaluands; they reuse the same discipline of task contracts, representative evidence, controlled comparison, uncertainty, robustness, and regression.

The purpose is a decision under uncertainty, not a leaderboard. Begin with whose outcome matters, what action the evidence could change, and what failure costs cannot be traded away. A technically valid metric that cannot alter a product, client, research, or operating decision is usually diagnostic at most.

## From stakeholder value to an evaluation contract

Before choosing cases or metrics, work backward:

```text
user or business outcome
→ task and decision the system supports
→ acceptable, unacceptable, and safe-failure states
→ observable artifact or environment state
→ construct and evaluator
→ dataset and experiment
→ adoption, constraint, or release rule
```

Record target users and affected parties; current human or software baseline; task frequency and slice mix; value of successful completion; costs of delay, review, abstention, error, and incident; authority and non-compensable constraints; and the smallest improvement worth operational complexity.

Where values are defensible, estimate expected net value per task:

$$
\mathbb{E}[V]=\sum_{s,o}P(s)P(o\mid s,\pi)V(o,s)-C_{runtime}-C_{review}-\mathbb{E}[C_{failure}]
$$

Here $s$ is a task slice, $o$ an outcome, and $\pi$ the complete system policy. Use ranges or scenarios when probabilities and costs are uncertain. Do not bury privacy, authorization, or catastrophic harm inside an average dollar value when they are hard constraints.

## Where to Start in a Zero-to-One System

Do not wait until the pipeline is finished, and do not build the full evaluation program before anything runs. Grow both together:

| Build state | Evaluation work now | Evidence you should leave with |
|---|---|---|
| Problem and environment understood, no system | Define intended behavior, risks, slices, and a small set of grounded or executable cases. For RAG, preserve source evidence; for agents, version initial state, actions, permissions, and terminal outcomes. | A task/environment contract and runnable smoke cases. |
| No runnable baseline | Build the thinnest complete path with deliberately simple components. | A baseline manifest and traces, not a claim that its components are optimal. |
| Improving one component | Use its component leaf: change one decision, preserve inputs and controls, inspect paired wins and losses. | An adopt, reject, constrain, or unresolved decision. |
| Complete path exists | Run periodic end-to-end checks so local improvements do not combine badly. | Evidence that the assembled behavior improved. |
| Candidate may ship | Run the protected release suite, robustness families, and non-compensable gates. | A release decision, rollout constraints, and rollback signals. |
| System is operating | Convert verified incidents and drift into hypotheses and regression cases. | A production-to-evaluation learning loop. |

The order is therefore **thin vertical slice → controlled component improvement → frequent system rechecks**. For RAG this avoids “perfect all indexing, then begin retrieval, then begin generation, then evaluate.” A search-only product may end at ranked evidence. An agent starts with terminal outcomes, invariants, and sandboxed actions, then adds trajectory evaluation when model-selected tools, policies, memory, or multi-step actions appear. A simulation additionally needs seeds, interventions, sensitivity, and validity arguments owned by its domain cluster.

## The Workbook Loop

```text
observed problem or opportunity
→ falsifiable hypothesis
→ representative cases and ground truth
→ baseline and candidate
→ vary one decision; hold confounders constant
→ component metrics plus end-to-end outcomes
→ uncertainty and failure-slice analysis
→ adopt, reject, or gather more evidence
→ preserve the case as a regression test
```

## Experiment Contract

Before running an experiment, record:

| Field | Question |
|---|---|
| Decision | What implementation or policy choice will this result change? |
| Hypothesis | Which measurable outcome should improve, for which slice, and why? |
| Baseline | What is the simplest credible comparator? |
| Independent variable | What changes between conditions? |
| Controls | What data, labels, versions, budgets, and downstream components stay fixed? |
| Primary metric | Which measure decides the hypothesis? |
| Guardrails | Which integrity, safety, latency, or cost outcomes must not regress? |
| Uncertainty | How will stochastic and sampling variation be represented? |
| Decision rule | What result means adopt, reject, or remain unresolved? |
| Target population and estimand | For which workload does the claimed effect apply, and what population quantity is being estimated? |
| Practical margin | What smallest gain or largest tolerable regression would change the decision? |

LLM stochasticity does not remove experimental control. Use deterministic checks where possible, paired cases, repeated runs where model variance matters, versioned configurations, and preserved per-example failures.

## Methods

```text
define the construct and metric
        ↓
can code or a bounded reference decide it validly?
        ├─ yes → deterministic/reference-based evaluation
        └─ no  → semantic human or model judgment
                         ↓ if a model judge is used
                    calibration and validation

frameworks and telemetry execute, record, and automate either path
```

- [[Deterministic & Reference-Based Evaluation]] — implement objective contracts, bounded comparisons, and executable checks
- [[Semantic Evaluation & LLM Judges]] — implement criteria that require interpretation; its calibration branch validates model judges
- [[Evaluation Frameworks & Tooling]] — choose replaceable runners, scorer adapters, tracing, and regression automation
- [[Statistical Decision-Making for Evaluation]] — connect target populations, repeated trials, uncertainty, practical margins, and business consequences to an adoption decision

Human review can create references, make semantic judgments, calibrate automation, and adjudicate risk. Production outcomes provide later evidence about real task success. They are evidence sources and operating layers, not competing scorer products.

## Ownership Boundaries

| Layer | Owns |
|---|---|
| Strategy and method branches | decision, construct, scorer type, comparison design, and validation requirements |
| Data & Benchmarks | representative cases, tiers, coverage, provenance, splits, and synthetic expansion |
| Ground-Truth Labeling | annotation schema, reviewers, adjudication, versions, and label migration |
| Component Harness | controlled baseline/candidate execution and component-specific protocols |
| End-to-End and Robustness | assembled-system outcomes, interactions, perturbations, and threats |
| Regression & Production Feedback | release evidence, drift, incidents, and promotion of verified failures |

## Specialized entry paths

- **RAG:** begin with [[Evaluation Metrics & The RAG Triad]] to define retrieval, evidence, generation, and operational constructs, then use parsing, chunking, embedding/index, retrieval, transformation/routing, reranking, and generation/citation component branches as the pipeline is assembled.
- **Agents:** use [[Agent System Evaluation]] once the system selects actions over time; score authoritative outcomes and side effects before adding semantic trajectory judgment.
- **Simulations:** use the general experiment/data/system machinery here while the `Simulations` cluster owns model validity, environment mechanics, seeds, interventions, and claim boundaries.

These paths are written as prose unless a cross-cluster link materially improves the working path. The graph is a navigation aid, not a reason to hide a dependency.

## Sources

- [OpenAI Docs: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

## Next

→ [[Evaluation Data & Benchmarks]]

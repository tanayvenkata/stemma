---
tags: [generation]
---
# Model Configuration

Model configuration selects and versions the generator/runtime behavior used by the rest of the pipeline. Model family, endpoint, prompt contract, context limits, decoding controls, tool support, structured output, privacy, latency, and cost form one deployable configuration.

## Model Contract

Record:

- provider or runtime, model identifier, revision, and deployment region;
- input/output and total context limits as actually enforced;
- supported sampling or reasoning controls and their semantics;
- tool-calling, multimodal, streaming, log-probability, and structured-output behavior;
- system/developer/user instruction precedence and truncation policy;
- safety, retention, privacy, and data-residency settings;
- timeout, retry, fallback, rate-limit, and concurrency behavior;
- price and capacity snapshot, which must be rechecked rather than memorized.

## Selection Procedure

1. Define task and failure slices plus hard integrity, latency, privacy, and cost constraints.
2. Establish the simplest credible configuration as baseline.
3. Compare candidates on identical evidence and cases, with repeated runs where behavior is stochastic.
4. Measure claim support, task success, abstention, schema/tool reliability, latency distributions, token use, cost per successful task, and severe failures.
5. Test long context, conflicting evidence, prompt injection, tool failure, and output limits.
6. Route among configurations only when slice-specific benefit pays for router error and operations.

A larger or more deliberative model may reduce some errors while increasing latency, cost, or over-answering. A smaller model may work without elaborate few-shot prompting. These are hypotheses to measure, not tier invariants.

## Components

- [[Model Selection & Reasoning Tiers]]
- [[Inference & Sampling Parameters]]

## Next

→ [[Context Preparation]]

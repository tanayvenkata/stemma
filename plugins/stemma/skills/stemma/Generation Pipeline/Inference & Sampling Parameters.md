---
tags: [generation]
---
# Inference & Sampling Parameters

Inference parameters shape the runtime distribution, effort, length, and stopping behavior of a model. Their availability and semantics vary by provider and model revision; unsupported controls may be ignored or rejected.

## Main Controls

| Control | Effect to verify |
|---|---|
| temperature | flattens or sharpens token sampling distribution |
| top-p / top-k | restricts sampling to a probability mass or candidate set |
| maximum output | bounds generation but can truncate schemas or citations |
| stop sequences | terminate on matched text and can fire inside valid content |
| penalties/biases | alter token preferences and can damage factual strings |
| reasoning/compute effort | allocates model-specific deliberation, often changing latency and token accounting |
| seed/deterministic mode | may improve repeatability without guaranteeing identical service behavior |

For constrained factual or structured tasks, start with runtime defaults or low-variance settings recommended for that model, then measure. Creative persona behavior may benefit from broader sampling, but diversity must be evaluated alongside consistency and safety.

## Tuning Protocol

Freeze prompt, evidence, model revision, and cases. Vary a small number of supported controls, repeat stochastic runs, and retain output distributions. Measure task success, claim support, schema validity, refusal/abstention, diversity where relevant, output length, latency, and cost.

Do not transfer numeric settings across model families as if scales were equivalent. Revalidate after model or endpoint changes.

## Part of

← [[Model Configuration]]

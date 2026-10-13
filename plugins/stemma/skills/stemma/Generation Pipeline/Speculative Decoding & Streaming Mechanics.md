---
tags: [generation]
---
# Speculative Decoding & Streaming Mechanics

Speculative decoding proposes several tokens with a cheaper draft process and verifies them with the target model. Under a correct rejection-sampling implementation, accepted and corrected tokens preserve the target distribution; real systems must still test implementation, numerical, batching, and sampling compatibility.

Speedup depends on draft acceptance, target/draft cost, sequence length, hardware, batching, memory traffic, and runtime overhead. There is no universal model-size boundary, acceptance rate, or multiplier.

## Evaluate Speculation

Compare the same target model with and without speculation on representative prompts. Measure output-distribution correctness or deterministic equality where applicable, accepted tokens per target step, time to first visible token, inter-token latency, total latency, throughput, memory, cost, and behavior under concurrency. Disable it when overhead exceeds saved target passes.

## Streaming Is a Product Protocol

Define typed events such as `response.started`, `text.delta`, `tool_call.ready`, `citation.final`, `error`, and `response.completed`. Handle:

- partial JSON, Unicode, markdown, and citations;
- disconnect, cancellation, retry, and duplicate events;
- usage and finish metadata arriving after text;
- provisional text that has not passed semantic or safety validation;
- tool calls and side effects that must wait for complete validation.

Time to first backend token can differ materially from time to first user-visible content when models deliberate, buffer, or validate. Measure the user-facing event contract.

Primary reference: [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192).

## Part of

← [[Generation Strategy]]

---
tags: [generation]
---
# Generation Strategy

Generation strategy governs how the configured model produces and delivers an output: free text or constrained structure, bounded length and stopping, batch or stream, and optional runtime acceleration. It does not choose what the answer should mean; prompt, evidence, validation, and product contracts still own that.

## When This Enters the Build

Use runtime defaults and a non-streaming request as the first baseline unless the product contract already requires structured output or incremental delivery. Add constraints when malformed structure is a real interface failure; add streaming for user-perceived latency or progressive events; add speculative decoding only when generation throughput is a measured bottleneck and the deployed runtime can preserve target behavior.

Leave with a versioned execution contract: output mode, supported controls, stopping and truncation behavior, event schema, cancellation semantics, validation boundary, and measured latency/throughput under representative load.

## Decision Workflow

1. Define whether the consumer needs prose, a typed payload, tool arguments, or a stream of events.
2. Establish the simplest valid execution and measure task quality, schema validity, truncation, latency, and failure recovery.
3. Prefer provider/runtime-native constrained decoding for syntactic guarantees, followed by semantic and business-rule validation in trusted code.
4. Treat streaming as a protocol: provisional text must not trigger side effects, and partial JSON, disconnects, retries, and cancellation need explicit handling.
5. Compare acceleration with the same target behavior under realistic batching and concurrency; disable it when overhead or incompatibility erases the gain.

Do not transfer temperature, token limits, speculative settings, or streaming assumptions across model/runtime revisions without revalidation.

## Components

- [[Structured Output & Constrained Decoding]]
- [[Speculative Decoding & Streaming Mechanics]]

## Next

→ [[Post-Generation Processing]]

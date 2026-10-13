---
tags: [indexing]
---
# Fixed Chunking

Fixed chunking cuts a sequence by a uniform unit such as tokens, characters, time, samples, or bytes. It is simple and deterministic but ignores semantic or structural boundaries unless the source itself is naturally windowed.

## Plausible Uses

- a baseline that reveals whether more complex boundaries add value;
- telemetry, audio, genomic, packet, or other continuous sequences with meaningful window/stride definitions;
- controlled records whose units already align with the window;
- fallback for oversized units after a preferred structural split.

For prose, code, tables, and rules, fixed windows can separate negation, qualifiers, headers, or syntax. Even continuous signals require domain-specific window length, stride, padding, and boundary handling.

Compare window and stride policies on coverage of labeled source events/regions, boundary loss, redundancy, retrieval, downstream outcomes, and cost. Use fixed chunking when uniform windows match the evidence unit or remain indistinguishable from more complex policies.

## Part of

← [[Chunking Strategy]]

---
tags: [generation]
---
# Structured Output & Constrained Decoding

Structured output constrains or validates the visible response against a schema or grammar. Correct constrained decoding can guarantee syntactic membership in the supported grammar; it cannot guarantee truthful values, complete fields, authorized actions, or valid world-state transitions.

## Enforcement Levels

| Level | Mechanism | Remaining risk |
|---|---|---|
| prompt instruction | asks for a format | syntax can drift |
| parse and retry | validates after free generation | cost, loops, and semantic errors |
| token-level grammar/schema constraint | masks tokens invalid under compiled grammar | schema expressiveness and semantic validity |
| application validation | checks types, ranges, relations, authorization, state | validator gaps and race conditions |

Provider APIs and self-hosted runtimes implement reasoning, schema subsets, streaming, refusal, and tool calls differently. Treat behavior as a versioned runtime contract.

## Implementation Protocol

1. Minimize the schema and define optional, nullable, and failure states explicitly.
2. Test supported grammar features, recursion, enums, lengths, Unicode, and large payloads.
3. Validate semantic and business invariants after parsing.
4. Authorize and execute side effects outside the model.
5. Bound repair/retry and preserve raw failures.
6. Test streaming, truncation, refusal, tool-call, and upgrade behavior.

Compare prompt-only, constrained, and validated policies on syntax success, semantic correctness, latency, cost, and failure recovery. Use constraints when reliable machine consumption justifies the runtime coupling.

## Part of

← [[Generation Strategy]]

---
tags: [production]
reviewed: 2026-10-11
---
# Production Security, Privacy & Tenant Isolation

Retrieved text, user input, model output, and tool results are untrusted data. Delimiters and classifiers can reduce risk, but security boundaries must be enforced in deterministic application code.

## Threat Model

- direct and indirect prompt injection
- malicious or poisoned corpus content
- cross-tenant retrieval and cache leakage
- excessive tool agency and confused-deputy behavior
- insecure handling of model output by downstream systems
- secrets or personal data in prompts, traces, and provider logs
- unauthorized inference from embeddings or metadata
- compromised parsers, models, packages, connectors, or source integrations
- denial of service and unbounded model/tool consumption

## Authorization Before Retrieval

Authenticate the principal and enforce document/row/collection permissions inside every retrieval path. Propagate ACL changes through indexes and caches and test negative cases. Metadata filters are security controls only when the datastore and query path enforce them reliably. A collection per tenant improves isolation but does not by itself guarantee it.

## Untrusted Content and Tool Boundaries

- Mark retrieved content as untrusted and instruct the model not to follow embedded commands.
- Minimize tool privileges, credentials, arguments, accessible resources, and network egress.
- Validate tool calls and model outputs against schemas and business rules in code.
- Require human approval for high-impact or irreversible actions.
- Preserve provenance so suspicious source content can be located and quarantined.

No prompt-only defense fully separates instructions from data. Test the complete application with adversarial documents and multi-step attacks.

## Privacy and Data Governance

- Minimize data before sending it to a model or telemetry system.
- Define provider retention/training controls, residency, encryption, and deletion obligations.
- Prefer irreversible redaction when re-identification is unnecessary; protect token maps when reversible pseudonymization is required.
- Apply retention and access policy to prompts, embeddings, caches, traces, human-review queues, and backups.
- Treat compliance as a system-level evidence process, not a property conferred by a PII library.

## Security Verification

Run authorization matrices, tenant-isolation tests, corpus-poisoning tests, prompt-injection suites, tool-abuse tests, dependency scanning, and incident exercises. Track false accepts and false rejects for classifiers; a guardrail model is one signal, not the trust boundary.

Record the origin and version of parsers, models, indexes, policies, dependencies, and external sources in the release manifest. Restrict who can publish each artifact, verify integrity where supported, and make rollback or quarantine possible without rebuilding trust from an opaque current state.

## See Also

- OWASP prompt-injection guidance: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- OWASP vector and embedding risks (LLM08:2025; the list is revised periodically, verified 2026-10): https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/

## Part of
← [[RAG Production]]

# Stemma

Stemma helps coding agents plan, review, and debug RAG and search systems the way production demands. Strong models already know what BM25 and reranking are; what they skip unless asked is the production work. Stemma makes the agent cover it: authorization inside retrieval, evaluation gates written before the components they judge, reindexing without serving a half-built index, abstention when evidence is missing, and traces that record which versions produced each answer.

It is one skill backed by 123 practitioner notes on indexing, retrieval, generation, architecture, evaluation, and production. The skill routes each decision to the few notes that own it, so the agent reads only what the task needs.

## Use

- `/stemma plan <what>`: a plan from the project's current state to production, each step ending in a check.
- `/stemma eval-plan <what>`: evaluation gates with frozen thresholds and what the sample can show.
- `/stemma review <what>`: an audit of an existing RAG codebase, findings ranked by harm.
- `/stemma diagnose <what>`: the first failing stage, a fix there, and a regression check.

Without a command, the skill loads on its own for tasks about parsing, chunking, embedding, retrieval, reranking, citations, RAG evaluation, or release gates.

## What it runs

Stemma has no hooks, MCP servers, or network access, and it reads no credentials. Its only executable is `skills/stemma/scripts/gate_stats.py` (Python standard library), which the agent may run locally to compute confidence intervals for evaluation gates.

## More

Measured results, the evaluation cases, and how to contribute: https://github.com/tanayvenkata/stemma. The notes are CC BY 4.0 and the script is MIT.

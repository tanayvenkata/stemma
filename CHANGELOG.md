# Changelog

## 0.2.0 (2026-10-12)

- Renamed from `rag-field-guide` to Stemma. Install with `claude plugin install stemma@tanayv` and invoke with `/stemma plan …`.
- `review` command: audit a RAG codebase by tracing the path that actually serves requests, with findings ranked by harm and a list of what is done well.
- `diagnose` command: localize the first failing stage before fixing, and end with a regression check.
- `SKILL.md` states the core idea and lists mistakes seen in practice, each pointing to the note that owns its reasoning. Plans rerun their evaluation gates on every later change.
- `scripts/gate_stats.py`: Wilson intervals, the exact zero-event bound, and a paired bootstrap, so gate verdicts are computed rather than estimated.
- Content pass over all 123 notes: unsourced numbers sourced, restated as assumptions, or removed; stale vendor specifics dated or generalized; contradictions between notes resolved (`docs/hygiene-ledger.md`). Fixes include the direction of the semantic-chunking threshold, the length limit for late chunking, and IVF `nlist` guidance.
- Evaluation: cases built from real projects for `review` and `diagnose`, and a held-out planning case. `scripts/run_evals.sh` runs them.
- Packaging: `license` in `SKILL.md`, CI that validates the plugin and marketplace manifests and checks that the version and changelog agree, a release procedure in `CONTRIBUTING.md`, a case list in `evals/README.md`, `docs/design.md` in place of the earlier design draft, and `scripts/trigger_test.sh`.

## 0.1.0 (2026-10-06)

- First packaged release: notes on indexing, retrieval, generation, architectures, evaluation, and production, routed by decision from `SKILL.md`, with `plan` and `eval-plan` commands.

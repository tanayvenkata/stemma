# Stemma

**Practitioner notes that make coding agents plan, review, and debug RAG systems the way production demands.** 123 notes on retrieval-augmented generation and search, packaged as an agent skill that routes each decision to the few notes it needs.

*A stemma is the family tree scholars draw to trace copies of a manuscript back to the original. A trustworthy RAG system needs the same thing: every answer traceable to the documents, and the versions of them, it came from.*

[![CI](https://github.com/tanayvenkata/stemma/actions/workflows/ci.yml/badge.svg)](https://github.com/tanayvenkata/stemma/actions/workflows/ci.yml)
[![Notes: CC BY 4.0](https://img.shields.io/badge/notes-CC_BY_4.0-1b1b19?style=flat-square)](plugins/stemma/LICENSE)
[![Code: MIT](https://img.shields.io/badge/code-MIT-1b1b19?style=flat-square)](LICENSE)
[![Agent Skills compatible](https://img.shields.io/badge/Agent_Skills-compatible-1b1b19?style=flat-square)](https://agentskills.io)

Strong models already know what BM25 and reranking are. What they skip when nobody asks is the production work: authorization inside retrieval, evaluation gates written before the components they judge, reindexing without serving a half-built index, abstention when evidence is missing, and traces that say which versions produced an answer. Stemma makes the agent ask those questions, and it is measured, not asserted.

## Quick start

```bash
claude plugin marketplace add tanayvenkata/stemma
claude plugin install stemma@tanayv
```

Then, in Claude Code:

```text
/stemma plan take this prototype to production for 40 analysts
/stemma review the retrieval path before we turn on hybrid search
/stemma diagnose answers cite the wrong plan document
```

Without a command, the agent loads the skill on its own when a task involves parsing, chunking, embedding, retrieval, reranking, citations, RAG evaluation, or release gates.

## Results

Each case runs an agent with and without the skill, 3 runs per arm, scored by an LLM judge on one criterion per production practice ([`evals/`](evals), per-run results for every sweep cited here in `evals/results/`, full history in [`docs/usage-log.md`](docs/usage-log.md)).

**Held out.** A planning case built from a real 10-K risk-search project ([sec-risk-analysis](https://github.com/tanayvenkata/sec-risk-analysis)). Its graders were committed before any run, and the skill was never tuned on it.

One case, 3 runs per arm, 7 criteria per run:

| Model | With the skill | Without | Criteria passed (7 × 3 runs) |
|---|---|---|---|
| Opus, unprompted | **1.00** | 0.24 | 21/21 vs 5/21 |
| Haiku, `plan` named | **0.76** | 0.24 | 16/21 vs 5/21 |

A rerun of the with-skill arm on version 0.2.0 reproduced this: 20/21 on Opus and 18/21 on Haiku with `plan` named.

A single case shows the effect on one realistic request, not a rate across projects; more held-out cases are the next step.

Haiku did not load the skill on its own for this request (0/3 runs), so name the command on smaller models.

Without the skill, Opus wrote a capable plan: key companies by CIK rather than ticker, poll EDGAR, handle 10-K/A amendments. With it, the plan also caught what would hurt users, for example:

> - The rebuild overwrites `vector_store/` in place, so the running app can read a half-built index.
> - `tests/run_eval.py` uses plain top-5 retrieval with no filters, which is not the app's filtered path.
> - The code uses 0.75/0.55 (`app.py:38`, `app.py:487`), but the UI caption says 0.7/0.5 (`app.py:1014`). Neither was measured on this pipeline.

**Tuned on.** Two planning cases that earlier `SKILL.md` changes were tuned against, so treat these as in-sample: an HR assistant over policies and per-employee records (Opus 0.94 vs 0.39) and a support bot's path to production (Opus 0.83–0.94 vs 0.44–0.50).

**Code review and diagnosis.** Five cases from three real projects ([401k-rag](https://github.com/tanayvenkata/401k-rag), [campaign-intel](https://github.com/tanayvenkata/campaign-intel), [fda-guidance-diff](https://github.com/tanayvenkata/fda-guidance-diff)) with bugs confirmed in the code, including a hybrid-search score-scale mismatch that drops every result and a section truncation that hides 70% of the text from a diff tool.

- Opus finds most of these bugs without the skill, so the skill adds little there.
- On Haiku, `review` scored within noise of the baseline (0.93 vs 0.87, one criterion differing by one run). `diagnose`, when named, added the regression check that unaided runs usually skipped (3/3 vs 1/3 runs; 1.00 vs 0.75).
- One bug, a parent-to-child key that the reindex script reads under a different name than the data uses, was found in 1 of 18 review runs across both models and arms.

What this shows: Stemma's value is in open-ended planning and in smaller models, not in teaching strong models individual facts.

## What's inside

```text
plugins/stemma/skills/stemma/
  SKILL.md              commands, mistakes seen in practice, decision-to-notes table
  Indexing Pipeline/    parsing, cleaning, chunking, metadata, embeddings, HNSW/IVF/BM25/SPLADE, index lifecycle
  Retrieval Pipeline/   query understanding and rewriting, dense/sparse/hybrid retrieval, fusion, reranking,
                        calibration, abstention, authorization
  Generation Pipeline/  context assembly, prompting, citations, verification, structured output, model execution
  RAG Architectures/    baseline and modular RAG, evidence sufficiency, adaptive, agentic, graph RAG
  Evaluation/           experimental design, labeling, component and end-to-end evaluation, LLM judges,
                        statistics for gates, failure diagnosis
  RAG Production/       requirements, data lifecycle, release gates, observability, reliability, security,
                        caching, cost, governance
  scripts/gate_stats.py Wilson intervals, zero-event bounds, paired bootstrap
```

The notes are plain Markdown with `[[wiki links]]`; open the folder as an Obsidian vault to browse them as a graph.

## Install

| Route | Command |
|---|---|
| Claude Code plugin | `claude plugin marketplace add tanayvenkata/stemma` then `claude plugin install stemma@tanayv` |
| [skills CLI](https://github.com/vercel-labs/skills) (Claude Code and other Agent Skills clients) | `npx skills add tanayvenkata/stemma -s stemma` |
| git, personal skill with live edits | `git clone https://github.com/tanayvenkata/stemma.git` and link `plugins/stemma/skills/stemma` into `~/.claude/skills/` (or `~/.agents/skills/` for Codex) |

Refresh a marketplace install with `claude plugin marketplace update tanayv`.

The skill follows the open [Agent Skills](https://agentskills.io) standard, so it works outside Claude Code too; it has been tried in Codex, where it loaded on its own and read the right notes. The `/stemma` command and the marketplace install are Claude Code features; in other agents, ask for the stemma skill by name or let it load on its own.

## Commands

| Command | For | Produces |
|---|---|---|
| `plan` | a new RAG system or its path to production | steps from the project's current state, each ending in a check: baseline, evaluation gates, data lifecycle, authorization, release and rollback |
| `eval-plan` (or `gate`) | evaluation gates, before or after a run | estimands, slices, frozen thresholds with margins, what the sample can and cannot show |
| `review` | auditing an existing codebase | findings ranked by harm with file, quoted code, and a way to confirm each; whether the eval measures what ships; what is done well |
| `diagnose` | a reported failure | the first failing stage and mechanism, a fix at that stage, and a regression check |

## How it works

`SKILL.md` stays short. It states one idea (start from the simplest baseline that serves the decision, and add a mechanism only when a measurement on the real pipeline shows it earns its place), lists mistakes seen in working-looking systems, and maps each decision to the notes that own it. The agent reads only those notes. The notes avoid universal thresholds: where a number would be a guess, they give a cheap starting point as an assumption and name the measurement that confirms it.

The plugin has no hooks, MCP servers, or network access. Its only executable is `scripts/gate_stats.py` (Python standard library), which the agent runs locally to compute gate statistics.

Changes to `SKILL.md` are kept only when the eval cases show no harm. One example of why: adding a list of example triggers to the description once dropped Haiku's triggering from 12 of 12 to 0 of 12.

## Limits

- The notes are a synthesis, not an authority. Model names, library APIs, prices, and benchmarks change; check time-sensitive claims against the primary source and its "verified" date.
- The evaluation is small: few cases, 3 runs per arm, an LLM judge. Differences of one run in three are noise. All measured runs used Claude models.
- Smaller models may not load the skill on their own for planning or debugging requests; name the command.
- Stemma targets document and data corpora. Agentic code search (grep-style tools over a repository) is not covered yet.

## Repository layout

Only `plugins/stemma/` is installed. The rest is development material:

- [`evals/`](evals): cases, graders, fixtures, and recorded results ([case list](evals/README.md));
- [`docs/`](docs): [design](docs/design.md), [usage log](docs/usage-log.md), and the [hygiene ledger](docs/hygiene-ledger.md) for the last content pass;
- [`scripts/`](scripts): `check_notes.py` (links and references), `check_release.py` (version and changelog), `run_evals.sh` (evals), `trigger_test.sh` (whether the skill loads when it should), and tests.

## Contributing

Fixes go straight to a pull request; new notes and changes of opinion start as an issue. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The notes are [CC BY 4.0](plugins/stemma/LICENSE): use, adapt, and share them, including commercially, with a credit such as "Adapted from Stemma by Tanay Venkata". Scripts and the eval harness are MIT. See [LICENSE](LICENSE).

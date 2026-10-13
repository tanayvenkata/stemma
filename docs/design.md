# Design

Why Stemma is built the way it is, and what the evaluations taught. For what is inside and how to install it, see the [README](../README.md).

## Goal

Make agents plan, review, and debug RAG systems the way production demands, and show that it works with a measured comparison against the same agent without the skill.

## Principles

- **Add only what the model lacks.** Strong models already know what BM25, HNSW, and reranking are. Stemma's value is the production work they skip unless asked: authorization inside retrieval, evaluation gates written before the components they judge, safe reindexing, abstention, version-stamped traces.
- **One skill, thin commands, notes as the reasoning layer.** `SKILL.md` is a short table of contents: a core idea, mistakes seen in practice, four commands, and a table that routes each decision to the one to four notes that own it. Each command says what to produce, what to assume when inputs are missing, and which notes to read. The reasoning lives in the notes, one hop from `SKILL.md`.
- **No universal thresholds.** Where a number would be a guess, the notes give a cheap starting point as an assumption and name the measurement that confirms it. Checks are options, not a mandatory procedure; a skill that turns optional steps into required work makes agents slower and worse.
- **Deterministic work goes in scripts.** Confidence intervals and paired comparisons are computed by `scripts/gate_stats.py`, not estimated in prose.
- **Portable.** Only `name`, `description`, and `license` are needed for the skill to work in any Agent Skills client. `argument-hint` is a Claude Code extension that others ignore. Paths in `SKILL.md` are relative to its own folder, so the same file works as a plugin, a skills-CLI install, or a linked personal skill.

These follow Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (add only context the model lacks, keep `SKILL.md` under 500 lines with references one level deep, use scripts for fragile operations, build evaluations before extensive documentation) and the [Agent Skills specification](https://agentskills.io/specification).

## Layout

```text
.claude-plugin/marketplace.json     the marketplace that lists the plugin
plugins/stemma/                     the only folder that gets installed
  .claude-plugin/plugin.json
  skills/stemma/
    SKILL.md                        commands, mistakes, decision-to-notes table
    <six note folders>/             123 notes, plain Markdown with [[wiki links]]
    scripts/gate_stats.py
evals/                              cases, graders, fixtures, recorded results
docs/                               this file, the usage log, the hygiene ledger
scripts/                            note checker, release check, eval and trigger runners, tests
```

## How the skill is evaluated

Each case runs an agent twice under `claude plugin eval`: with the plugin and without it. Runs use 3 repetitions per arm, and an LLM judge scores one criterion per production practice. Graders are written from the notes and kept out of the prompt, because a prompt that leaks the rubric erases the measured difference. See [`evals/README.md`](../evals/README.md) for the cases.

What the evaluations showed, in the order they were learned (details in the [usage log](usage-log.md)):

1. **Pointed questions show no lift on strong models.** Asked directly about score fusion or a similarity cutoff, Opus answers correctly with or without the skill.
2. **Open-ended planning shows a large lift.** Asked to plan a system or its path to production, the agent with the skill covers production practices the unaided agent skips. The evaluation therefore centers on planning, review, and diagnosis tasks built from real projects.
3. **The description decides triggering, and it is fragile.** Adding a list of example triggers dropped Haiku from 12 of 12 to 0 of 12. The description is changed only with a trigger test (unprompted RAG questions plus unrelated tasks, on Haiku, Sonnet, and Opus).
4. **Strong models review code well unaided.** `review` adds little on Opus; `diagnose`, when named, adds the regression check that unaided runs skip.
5. **Tuned cases overstate.** Cases that earlier `SKILL.md` changes were tuned against are reported as in-sample. Headline numbers come from a held-out case whose graders were committed before any run.

## Changing the skill

- A change to `SKILL.md` is kept only if no grader drops by more than one run in three on Opus or Haiku.
- Notes change for two reasons: a factual or hygiene correction, or an evaluation that shows a gap. Every content pass is recorded in a ledger with a status per item (Preserved, Improved, Relocated, Removed deliberately, Missing); see the [hygiene ledger](hygiene-ledger.md).
- `scripts/check_notes.py` runs before every commit and in CI: every `[[link]]` resolves, note names are unique, and every note `SKILL.md` names exists.

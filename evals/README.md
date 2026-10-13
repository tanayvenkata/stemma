# Evaluation cases

Each folder is one case for [`claude plugin eval`](https://code.claude.com/docs/en/plugins): a `prompt.md` (the task, with run settings in its frontmatter), `graders/` (one LLM-judged criterion per file), and, for cases built from real projects, a `fixture/` copied into the agent's workspace by `scaffold.sh`. Every case runs with and without the plugin, 3 runs per arm by default.

Graders are written from the notes and never appear in the prompt. `graders/skill-fired.md` only records whether the skill loaded and is not part of the score.

## Cases

| Tag | Case | What it asks | What it tests |
|---|---|---|---|
| `heldout` | `heldout-plan-sec-risk` | Plan a 10-K risk-search tool's path to 40 analysts and the S&P 500 (fixture from [sec-risk-analysis](https://github.com/tanayvenkata/sec-risk-analysis)) | Out-of-sample planning. Graders committed before any run; `SKILL.md` is never tuned on it |
| `heldout-invoked` | `heldout-plan-sec-risk-invoked` | The same, naming the `plan` command | Planning when the skill is invoked, for models that do not load it on their own |
| `process` | `plan-hr-assistant` | Build plan for an assistant over HR policies and per-employee records | Planning (in-sample: earlier `SKILL.md` changes were tuned on it) |
| `process` | `prototype-to-production` | What a support-docs prototype needs before launch | Planning (in-sample) |
| `review` | `review-401k-rag` | Review a 401(k) plan assistant before shipping ([401k-rag](https://github.com/tanayvenkata/401k-rag)) | Finding confirmed bugs in real code |
| `review` | `review-campaign-intel` | Review the retrieval path before turning on hybrid search ([campaign-intel](https://github.com/tanayvenkata/campaign-intel)) | Same |
| `review` | `review-fda-guidance-diff` | Review a guidance-document diff tool and whether its validation backs its claims ([fda-guidance-diff](https://github.com/tanayvenkata/fda-guidance-diff)) | Same |
| `diagnose`, `diagnose-invoked` | `diagnose-401k-routing` | Fee questions answered as "not in the documents" | Localizing a routing failure, with and without naming `diagnose` |
| `diagnose`, `diagnose-invoked` | `diagnose-campaign-hybrid-empty` | Hybrid search returns no quotes | Localizing a score-scale mismatch, with and without naming `diagnose` |
| `niche` | `chunker-gold-labels`, `permission-filter-leak`, `synthetic-question-citations`, `relevant-but-insufficient`, `claim-level-confidence` | Short questions on points specific to the notes | Whether the notes add knowledge to a pointed question |
| `generic` | `score-fusion`, `similarity-cutoff`, `small-eval-improvement` | Short questions on common RAG pitfalls | Same, for well-known pitfalls |

The `niche` and `generic` cases showed no lift on Opus, which already answers them correctly. They remain as regression checks: the skill should never lower their scores.

## Running

```bash
scripts/run_evals.sh --tag heldout --scaffold --model opus --judge-model sonnet
scripts/run_evals.sh --tag process --model haiku --judge-model sonnet
scripts/run_evals.sh --case review-401k-rag --scaffold --model opus --judge-model sonnet
```

`run_evals.sh` copies the plugin and these cases into a temporary plugin root, because the eval sandbox cannot read the notes through a linked folder. `--scaffold` runs each case's `scaffold.sh`, which only copies its fixture into the workspace; read it before passing the flag. Each run starts Claude Code sessions with your own login and uses your plan's usage.

## Results

`results/<timestamp>-<label>/aggregate-result.json` holds per-run scores and grader verdicts for every sweep the README cites. `docs/usage-log.md` records what each sweep showed and what changed because of it. Compare with and without within one sweep, not across sweeps: graders were revised twice when they rejected valid answers.

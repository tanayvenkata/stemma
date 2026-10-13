# Contributing

Stemma is judged by whether it makes agents and people build, measure, and operate RAG systems better. Most of this page is about keeping it trustworthy.

## What to send where

- **Fixes** (a wrong claim, a stale number, a broken link, unclear wording): open a pull request. Cite a primary source for any factual change.
- **New notes and changes of opinion** (a recommendation should be different): open an issue first with the proposal template. Notes are opinionated on purpose, so a change of view needs evidence and a short discussion before text.
- **Skill behavior** (it did not trigger, read the wrong notes, or made an answer worse): open an issue with the skill-behavior template. These reports drive changes to `SKILL.md`.

## How notes are written

- One owner note per concept. Link to the owner rather than repeating it.
- No universal thresholds or defaults. Give a cheap starting point as an assumption, and name the measurement that confirms or overturns it.
- Classify claims: durable mechanism, measured result under stated conditions, hypothesis, or time-sensitive. Time-sensitive claims (models, vendors, APIs, prices, benchmarks) need a primary source and a "verified YYYY-MM" date, or should be stated generally.
- Prefer the simplest baseline, and say what evidence would justify adding a mechanism.
- Notes are plain Markdown with `[[Note Name]]` links, which open as a vault in Obsidian. Note names are unique.

## Checks before a pull request

```bash
python3 scripts/check_notes.py       # every [[link]] and SKILL.md reference resolves
python3 scripts/test_gate_stats.py   # tests for the skill's statistics script
python3 scripts/check_release.py     # plugin version, marketplace entry, and changelog agree
```

CI runs these and validates the plugin and marketplace manifests.

## Changing SKILL.md

`SKILL.md` decides when the skill triggers and which notes an agent reads, so small wording changes can have large effects. In one test, adding a list of example triggers to the description dropped triggering on Haiku from 12 of 12 to 0 of 12.

- Treat the `description` as frozen unless a trigger test shows a problem. After any change to it, rerun `scripts/trigger_test.sh haiku` and `scripts/trigger_test.sh opus 1`: RAG questions should load the skill and unrelated tasks should not.
- Rerun the eval cases that cover a changed command:

  ```bash
  scripts/run_evals.sh --tag process --model sonnet
  scripts/run_evals.sh --tag review diagnose --scaffold --model sonnet
  ```

  Each run starts Claude Code sessions with your own login, so it uses your plan's usage. `--scaffold` runs each case's `scaffold.sh`, which copies its fixture into the workspace; read those scripts first.
- Never tune `SKILL.md` against the `heldout` case. It exists to give out-of-sample numbers.

## Releasing

Changes land on `main` without changing the version. A release is a separate step: `plugins/stemma/.claude-plugin/plugin.json` holds the only version number, installed copies update only when it changes, and the Claude directory follows the `release` branch, so nothing on `main` reaches users until it is promoted.

1. **Stage.** On the commit to release, check the plugin exactly as it will ship: `scripts/trigger_test.sh haiku 1` (it loads the plugin from this repository with `--plugin-dir`), then try `/stemma plan <something>` in `claude --plugin-dir plugins/stemma`.
2. **Bump.** Raise `version` in `plugin.json` (patch for fixes, minor for new notes or commands, major for changes that break how the skill is invoked), add a matching `## X.Y.Z (YYYY-MM-DD)` entry at the top of `CHANGELOG.md`, run the checks above, and commit to `main`.
3. **Tag.** `claude plugin tag plugins/stemma --push` creates and pushes `stemma--vX.Y.Z`.
4. **Promote.** `git push origin stemma--vX.Y.Z^{commit}:release`. The directory scans the new commit on `release`, and an Anthropic reviewer publishes it.

## Code of conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

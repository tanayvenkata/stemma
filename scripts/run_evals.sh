#!/usr/bin/env bash
# Run `claude plugin eval` against the plugin with the repo's evals/ directory.
# The eval runner only reads cases inside the plugin root, and evals/ stays out of
# the installed plugin, so this builds a throwaway plugin root holding copies of
# the plugin and the cases. Copies, not links: the runner rejects a linked evals/,
# and the run's sandbox blocks reads through a linked skills/ folder, so the agent
# would see SKILL.md but not the notes. Results go under evals/results/.
# Usage: scripts/run_evals.sh [claude plugin eval options...]
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
plugin="$repo/plugins/stemma"
root="$(mktemp -d)"
trap 'rm -rf "$root"' EXIT

rsync -a "$plugin/.claude-plugin" "$plugin/skills" "$root/"
rsync -a --exclude results "$repo/evals/" "$root/evals/"

out="$repo/evals/results/$(date -u +%Y-%m-%dT%H-%M-%SZ)"
claude plugin eval "$root" --trust-plugin --no-publish --output-dir "$out" "$@"

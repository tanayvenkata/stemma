#!/usr/bin/env bash
# Trigger test: does the skill load for RAG questions and stay out of unrelated tasks?
# Runs each prompt headless with the plugin loaded and records whether the Skill tool
# was called for stemma. Rerun after any change to the SKILL.md description or name.
# Usage: scripts/trigger_test.sh [model] [runs per prompt]   (default: haiku 3)
set -uo pipefail
model="${1:-haiku}"; runs="${2:-3}"
plugin="$(cd "$(dirname "$0")/.." && pwd)/plugins/stemma"
work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT; cd "$work"
prompts=(
  "rag|Our RAG chatbot over internal wikis returns irrelevant chunks for about a third of questions. Should we add a reranker or change chunking first?"
  "rag|I want to switch our embedding model to a newer one. How do I know whether the new one is actually better on our documents?"
  "rag|We're building search over 2 million support tickets where each customer may only see their own. How should retrieval be set up?"
  "rag|How should I chunk long PDF contracts that contain tables for a question-answering system?"
  "other|Write a Python function that checks whether a string is a palindrome."
  "other|Explain the difference between TCP and UDP in two sentences."
  "other|Help me write a short birthday message for my sister."
)
rag_fired=0; rag_total=0; other_fired=0; other_total=0
for p in "${prompts[@]}"; do
  kind="${p%%|*}"; text="${p#*|}"
  for _ in $(seq 1 "$runs"); do
    out="$(claude -p --plugin-dir "$plugin" --model "$model" --max-turns 3 \
      --output-format stream-json --verbose "$text" 2>/dev/null)"
    hit=0; grep -q '"name":"Skill"[^}]*stemma' <<<"$out" && hit=1
    if [ "$kind" = rag ]; then rag_total=$((rag_total + 1)); rag_fired=$((rag_fired + hit))
    else other_total=$((other_total + 1)); other_fired=$((other_fired + hit)); fi
  done
done
echo "$model: RAG questions loaded the skill $rag_fired/$rag_total; unrelated tasks $other_fired/$other_total (should be 0)"
